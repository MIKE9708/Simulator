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
        self.futureEvent=[]
        self.current={}

    ################################################################################################################################################################################################
    
    def restart(self):
        self.queue=[]
        self.theta={}
        self.T={}

    ################################################################################################################################################################################################
    
    def get_T(self):
        return self.T

    ################################################################################################################################################################################################
    
    def time_in(self):
        data=numpy.random.exponential(3.0,size=1)
        return data[0]

    ################################################################################################################################################################################################
    
    def generate_Time(self):#this is used for the service time but is limited in a range between 10 and 1
        data=numpy.random.exponential(3.0,size=1)
        return data[0]

    ################################################################################################################################################################################################
    
    def get_theta(self):
        return self.theta

    ################################################################################################################################################################################################
    
    def get_thetaKi(self):
        res=0
        for elem in self.theta:
            res+=self.theta[elem]
        return res/self.N

    ################################################################################################################################################################################################  
    def get_X(self):
        res=0
        for elem in self.T:
            res+=elem*self.T[elem]
        return res/self.i
    ################################################################################################################################################################################################
   
    def get_V(self):
        print(self.i)
        return 1-(self.T[0]/self.i)

    ################################################################################################################################################################################################
    
    def begin(self,customer):
        self.futureEvent=[]
        custNum=[*range(1,customer+1)]#an array of N element corrwsponding to the number of customer that are specified
        tStart=0
        self.i=0
        self.N=0
        data=0
        self.restart()
        self.futureEvent.append({"customer":custNum[0],"simTime":0,"event":"arrive"})
        while(1):

            if(self.futureEvent):
                if info=='y':
                    print(self.i)
                    #print(self.futureEvent)

                if self.futureEvent[0]["simTime"]==self.i:
                    
                    if self.futureEvent[0]["event"]=="arrive":
                        service=self.generate_Time()
                        data=self.time_in()

                        if len(self.queue) in self.T.keys():
                            self.T[len(self.queue)]+=self.i-tStart
                        else:
                            self.T[len(self.queue)]=self.i-tStart

                        if(self.serverState==0):
                            self.current={"customer":self.futureEvent[0]["customer"],
                                "interarrival":self.i-self.futureEvent[0]["simTime"],
                                "arrival":self.futureEvent[0]['simTime'],
                                "serviceTime":service}

                            self.serverState=1

                            self.futureEvent.append({"customer":self.futureEvent[0]["customer"],
                                "simTime":self.i+service,
                                "event":"departure"})

                            self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])

                        else:
                            self.queue.append({"customer":self.futureEvent[0]["customer"],
                                "interarrival":self.i-self.futureEvent[0]["simTime"],
                                "arrival":self.futureEvent[0]['simTime'],
                                "serviceTime":service
                                })
 
                        if(custNum):
                            custNum.pop(0)

                        if(custNum):
                            data=self.time_in()
                            self.futureEvent.append({"customer":custNum[0],
                                "simTime":data+self.futureEvent[len(self.futureEvent)-1]["simTime"],
                                "event":"arrive"})
                            
                        self.futureEvent.pop(0)
                        self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])
                        tStart=self.i
                    
                    elif self.futureEvent[0]["event"]=="departure":
                        self.futureEvent.pop(0)
                        tStart=self.i
                        if(custNum):
                            custNum.pop(0)
                        if(custNum):
                            data=self.time_in()
                            self.futureEvent.append({"customer":custNum[0],
                                "simTime":data+self.futureEvent[len(self.futureEvent)-1]["simTime"],
                                "event":"arrive"})
                            self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])
                        if len(self.queue) in self.T.keys():
                            self.T[len(self.queue)]+=self.i-tStart
                        else:
                            self.T[len(self.queue)]=self.i-tStart

                        self.N+=1
                        self.theta[self.current["customer"]]=self.i-self.current["arrival"]

                        if(self.queue):
                            self.current=self.queue[0]
                            self.futureEvent.append({"customer":self.queue[0]['customer'],
                                "simTime":self.i+self.queue[0]['serviceTime'],
                                "event":"departure"})
                            self.queue.pop(0)
                            
                            self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])

                        else:
                            self.serverState=0

                        self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])

                        if(self.queue):
                            if info=='y':
                                print(str(self.queue)+'\n')
                            
                
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
print("Show info ? (y/n): ")
info=input()

for index in range(simulations):
    Obsim.begin(customerNum)
    print("\n","T:",Obsim.get_T(),"\n",
        "theta:",Obsim.get_theta(),"\n",
        "ThetaKi:",Obsim.get_thetaKi(),"\n",
        "X:",Obsim.get_X(),
        "\n","V:",Obsim.get_V(),"\n")
    print("End simulation: ",index)

