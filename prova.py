from asyncio import futures
from multiprocessing.connection import wait
import numpy
import time

class Simulator:

    def __init__(self):
        self.serverState=0 #define the status of entity who's serving {FREE=0|BUSY=1}
        self.queue=[]
        self.time=0
        self.N=0
        self.i=0 #the simulation time
        self.T={} #value for T
        self.theta={} #value for theta
        self.futureEvent=[]#calendar.copy() this will contain the overall event that will happen during the simulation
        self.current={}

    def get_T(self):
        return self.T


    ##########
    def time_in(self):
        data=numpy.random.exponential(3.0,size=1)

        return data[0]

    def waitTime(self,currentServing,arrivedUser,currentTime):
        res=currentServing['serviceTime']-(currentTime-currentServing['arrival'])
        for item in self.queue:
            res+=(item['serviceTime'])
            res=res-currentServing['serviceTime']-arrivedUser['serviceTime']
            
        return (res)

    def generate_Time(self):#this is used for the service time but is limited in a range between 10 and 1

        data=numpy.random.exponential(3.0,size=1)
        return data[0]
    ###########AW

    def get_theta(self):
        return self.theta
    
    def get_thetaKi(self):
        res=0
        for elem in self.theta:
            res+=self.theta[elem]
        return res/self.N
        
    def get_X(self):
        res=0
        for elem in self.T:
            res+=elem*self.T[elem]
        return res/self.i

    def get_V(self):

        return 1-(self.T[0]/self.i)

    def begin(self,customer):
        self.futureEvent=[]
        custNum=[*range(1,customer+1)]#an array of N element corrwsponding to the number of customer that are specified
        tStart=0
        self.i=0
        self.N=0
        data=0
        self.queue=[]
        self.theta={}
        self.T={}
        
        self.futureEvent.append({"customer":custNum[0],"simTime":0,"event":"arrive"})
        while(1):
            print(self.i)

            if(self.futureEvent):
                print(self.futureEvent)
                if self.futureEvent[0]["simTime"]==self.i:

                    if self.futureEvent[0]["event"]=="arrive":
                        
                        service=self.generate_Time()
                        data=self.time_in()

                        if(self.serverState==0):
                            self.current={"customer":self.futureEvent[0]["customer"],
                                "interarrival":data-self.futureEvent[0]["simTime"],
                                "arrival":self.futureEvent[0]['simTime'],
                                "serviceTime":service
                                }
                            self.serverState=1

                            self.futureEvent.append({"customer":self.futureEvent[0]["customer"],
                                "simTime":self.i+service,
                                "event":"departure"
                                })
                            self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])
                        else:
                            self.queue.append({"customer":self.futureEvent[0]["customer"],
                                "interarrival":data-self.futureEvent[0]["simTime"],
                                "arrival":self.futureEvent[0]['simTime'],
                                "serviceTime":service
                                })
 
                        
                        if(custNum):
                            custNum.pop(0)
                        if(custNum):
                            data=self.time_in()
                            self.futureEvent.append({"customer":custNum[0],
                                "simTime":data+self.futureEvent[len(self.futureEvent)-1]["simTime"],
                                "event":"arrive"
                                })
                            
                        self.futureEvent.pop(0)
                        self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])

                    
                    elif self.futureEvent[0]["event"]=="departure":
                        self.futureEvent.pop(0)
                        if(custNum):
                            custNum.pop(0)
                        if(custNum):
                            data=self.time_in()
                            self.futureEvent.append({"customer":custNum[0],
                                "simTime":data+self.futureEvent[len(self.futureEvent)-1]["simTime"],
                                "event":"arrive"
                                })
                            self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])
                        if len(self.queue) in self.T.keys():
                            self.T[len(self.queue)]+=self.i-tStart
                        else:self.T[len(self.queue)]=self.i-tStart
                        
                        self.N+=1
                        self.theta[self.current["customer"]]=self.i-self.current["arrival"]
                        if(self.queue):
                            self.current=self.queue[0]
                            self.futureEvent.append({"customer":self.queue[0]['customer'],
                                "simTime":self.i+self.queue[0]['serviceTime'],
                                "event":"departure"
                                })
                            self.queue.pop(0)
                            self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])
                        else:
                            self.serverState=0

                        #self.futureEvent.pop(0)
                        self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])

                        if(self.queue):
                            print("Istant "+str(self.i)+" Now serving costumer : "+str(self.queue[0])+'\n')
                        tStart=self.i
                
                    else:
                        self.T[len(self.queue)]=self.i-tStart
            else:

                if len(self.queue)==0:
                    self.serverState=0
                    if(len(self.futureEvent)==0):
                        break
            if(self.futureEvent):
                self.i=self.futureEvent[0]["simTime"]
                    
                    
Obsim=Simulator()
print("Number of simulations: ")
simulations=int(input())
print("Number of customers: ")
customerNum=int(input())

for index in range(simulations):
    
    Obsim.begin(customerNum)
    
    print("\n","T:",Obsim.get_T(),"\n",
    "theta:",Obsim.get_theta(),"\n",
    "ThetaKi:",Obsim.get_thetaKi(),"\n",
    "X:",Obsim.get_X(),
    "\n","V:","\n"
    )
    print("End simulation: ",index)
#nqObsim=Simulator()
#nqObsim.begin(customerNum)
#print("\n","T:",nqObsim.get_T(),"\n","theta:",nqObsim.get_theta(),"\n","ThetaKi:",nqObsim.get_thetaKi(),"\n","X:",nqObsim.get_X(),"\n","V:","\n")
