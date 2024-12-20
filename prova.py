from hashlib import new
from math import sqrt
from hamcrest import none
import numpy


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        data=numpy.random.exponential(2,size=None)
        return data

    ################################################################################################################################################################################################
    
    def generate_Time(self):#this is used for the service time but is limited in a range between 10 and 1
        data=numpy.random.exponential(0.3,size=None)
        return data

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
        #print(self.i)
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

bcolors=bcolors()             
thetaki_array=[]
v_array=[]
x_array=[]                
Obsim=Simulator()
print("Number of simulations: ")
simulations=int(input())
print("Number of customers: ")
customerNum=int(input())
print("Show info ? (y/n): ")
info=input()

for index in range(simulations):
    Obsim.begin(customerNum)
    print("\n",bcolors.OKCYAN+"T:"+bcolors.ENDC,Obsim.get_T(),"\n",
        bcolors.OKCYAN+"theta:"+bcolors.ENDC,Obsim.get_theta(),"\n",#SI
        bcolors.OKCYAN+"ThetaKi:"+bcolors.ENDC,Obsim.get_thetaKi(),"\n",
        bcolors.OKCYAN+"X:"+bcolors.ENDC,Obsim.get_X(),#SI
        "\n",bcolors.OKCYAN+"V:"+bcolors.ENDC,Obsim.get_V(),"\n")#SI
    print(bcolors.OKGREEN+"END SIMULATION: "+bcolors.ENDC,index+1,'\n')
    v_array.append(Obsim.get_V())
    thetaki_array.append(Obsim.get_thetaKi())
    x_array.append(Obsim.get_X())

####Confidence Intervall############
alpha=((100-95)/100)/2
t=1.98
expected_v=0
expected_x=0
expected_thetaki=0
s2_thetaki=0
s2_x=0
s2_v=0

for key in range(len(thetaki_array)):
    expected_thetaki+=thetaki_array[key]
    expected_x+=x_array[key]
    expected_v+=v_array[key]

expected_thetaki=expected_thetaki/index
expected_v=expected_v/index
expected_x=expected_x/index

for key in range(len(thetaki_array)):
    s2_thetaki=pow(thetaki_array[key]- expected_thetaki,2)
    s2_x=pow((x_array[key]- expected_x),2)
    s2_v=pow((v_array[key]- expected_v),2)


s2_thetaki=s2_thetaki/(index-1)
s2_x=s2_x/(index-1)
s2_v=s2_v/(index-1)

H_thetaki=1.98*(sqrt(s2_thetaki)/sqrt(index))
H_v=1.98*(sqrt(s2_v)/sqrt(index))
H_x=1.98*(sqrt(s2_x)/sqrt(index))

#####Final values###########

print(bcolors.OKGREEN+'RISULTATI:'+bcolors.ENDC,(expected_thetaki-H_thetaki),bcolors.OKCYAN+'< thetaki <'+bcolors.ENDC,(expected_thetaki+H_thetaki))
print(bcolors.OKGREEN+'RISULTATI:'+bcolors.ENDC,(expected_v-H_v),bcolors.OKCYAN+'< v <'+bcolors.ENDC,(expected_v+H_v))
print(bcolors.OKGREEN+'RISULTATI:'+bcolors.ENDC,(expected_x-H_x),bcolors.OKCYAN+'< x <'+bcolors.ENDC,(expected_x+H_x))