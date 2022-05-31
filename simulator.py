customer_structure=[{"customer":1,"interarrival":0,"arrival":0,"serviceTime":3},
{"customer":2,"interarrival":2,"arrival":2,"serviceTime":2},
{"customer":3,"interarrival":4,"arrival":6,"serviceTime":3},
{"customer":4,"interarrival":1,"arrival":7,"serviceTime":4},
{"customer":5,"interarrival":1,"arrival":8,"serviceTime":2}]


calendar=[{"customer":1,"simTime":0,"event":"arrive"},
{"customer":2,"simTime":2,"event":"arrive"},
{"customer":1,"simTime":3,"event":"departure"},
{"customer":2,"simTime":5,"event":"departure"}, 
{"customer":3,"simTime":6,"event":"arrive"},
{"customer":4,"simTime":7,"event":"arrive"},
{"customer":5,"simTime":8,"event":"arrive"},
{"customer":3,"simTime":9,"event":"departure"},
{"customer":4,"simTime":13,"event":"departure"},
{"customer":5,"simTime":15,"event":"departure"}] 
#sortedi=sorted(a, key=lambda d: d["time"])



class Simulator:

    def __init__(self,calendar):
        self.serverState=None
        self.queue=[]
        self.time=0
        self.N=0
        self.i=0
        self.T={}
        self.theta={}
        self.futureEvent=calendar.copy()


    def get_T(self):
        return self.T
    
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

        tStart=0
        current=None
        customerLocal=customer.copy()
        
        while(len(self.futureEvent)!=0):

            current=self.futureEvent[0]
            if current["simTime"]==self.i:

                if current["event"]=="arrive":
                    print(current)
                    if len(self.queue) in self.T.keys():
                        self.T[len(self.queue)]+=self.i-tStart
                    else:self.T[len(self.queue)]=self.i-tStart
    
                    self.queue.append(customerLocal[0])
                    customerLocal.pop(0)

                    self.serverState=1
                    self.futureEvent.pop(0)
                    tStart=self.i
                
                elif current["event"]=="departure":
                    
                    if len(self.queue) in self.T.keys():
                        self.T[len(self.queue)]+=self.i-tStart
                    else:
                        self.T[len(self.queue)]=self.i-tStart

                    print(str(self.queue)+'\n')
                    self.N+=1
                    print(current)
                    self.theta[current["customer"]]=self.i-self.queue[0]["arrival"]
                    self.queue.pop(0)
                    self.futureEvent.pop(0)
                    tStart=self.i


               
                else:
                    self.T[len(self.queue)]=self.i-tStart

            else:

                if len(self.queue)==0:
                    self.serverState=0
                    print("\nFree\n")

                self.i+=1
                    
                    
Obsim=Simulator(calendar)
Obsim.begin(customer_structure)

print("\n","T:",Obsim.get_T(),"\n","theta:",Obsim.get_theta(),"\n","ThetaKi:",Obsim.get_thetaKi(),"\n","X:",Obsim.get_X(),"\n","V:",Obsim.get_V(),"\n")

