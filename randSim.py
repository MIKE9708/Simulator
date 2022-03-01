import numpy
import time

'''
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
'''
#sortedi=sorted(a, key=lambda d: d["time"])



class Simulator:

    def __init__(self):
        self.serverState=None #define the status of entity who's serving {FREE=0|BUSY=1}
        self.queue=[]
        self.time=0
        self.N=0
        self.i=0 #the simulation time
        self.T={} #value for T
        self.theta={} #value for theta
        self.futureEvent=[]#calendar.copy() this will contain the overall event that will happen during the simulation


    def get_T(self):
        return self.T


    ##########
    def time_in(self,value,dep):#generate a random value with an exponential distribution that is then summed with the current max time of the simulation
                                #we also make sure that there is not any value with the same time inside the futureEvent list
        data=int(numpy.random.exponential(3.0,size=1))
        #while(data<=value and not any(d['simTime']<=data for d in self.futureEvent)):
        while(data<=value and not any(d['simTime']<=data for d in self.futureEvent)):
            data=int(numpy.random.exponential(3.0,size=1))+(value+1)
        return data

    def waitTime(self,queue,currentServing,arrivedUser,currentTime):
            if(len(queue)==1):
                res=0
            elif len(queue)==2:
                res= currentServing['serviceTime']-(currentTime-currentServing['arrival'])
            
            elif len(queue)>2:
                res=currentServing['serviceTime']-(currentTime-currentServing['arrival'])
                for item in queue:
                    res+=(item['serviceTime'])
                res=res-currentServing['serviceTime']-arrivedUser['serviceTime']
            
            return (res)

    def generate_Time(self):#this is used for the service time but is limited in a range between 10 and 1

        data=1+(int(numpy.random.exponential(3.0,size=1))%(11-1))
        return data
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
        
        custNum=[*range(1,customer+1)]#an array of N element corrwsponding to the number of customer that are specified
        tStart=0
        current=None #current customer to be served
        customerLocal=[]#customer.copy() array of the customer to be served
        self.futureEvent.append({"customer":custNum[0],"simTime":0,"event":"arrive"})
        #while(len(self.futureEvent)!=0):
        ##########
        while(1):
            #time.sleep(1)
            print(self.i)
                #arrive=self.generate_Time() #first customer to arrive
                #service=self.generate_Time()
                
                #self.futureEvent.append({"customer":custNum[0],"simTime":1,"event":"arrive"})# adding to the future event list
                #print(self.futureEvent)
                #customerLocal.append({"customer":custNum[0],"interarrival":custNum[0],"arrival":self.futureEvent[0]["simTime"],"serviceTime":service})
            ##########
            
            if(self.futureEvent):# if not empty
                current=self.futureEvent[0] #the current is the customer in the first place of the future event list
            else: break

            if current["simTime"]==self.i :# we check if the current customer arrive or depart in the current simulation time
                print("Istant: "+str(self.i)+" Current User: "+str(current)+"\n")


                if current["event"]=="arrive":
                    self.futureEvent.pop(0) #the customer is being served
                    #print(self.queue)
                    #######

                    service=self.generate_Time()
                    data=self.time_in(current["simTime"],None)
                    customerLocal.append({"customer":current["customer"],"interarrival":data-current["simTime"],"arrival":current['simTime'],"serviceTime":service})# we put the customer into the local array
                    self.queue.append(customerLocal[0])
                    wait=self.waitTime(self.queue,self.queue[0],customerLocal[0],self.i)
                    print("ATTESA USER:"+str(wait))
                    print("##############"+str(customerLocal)+"#################")
                    self.futureEvent.append({"customer":current["customer"],"simTime":self.i+wait+service,"event":"departure"}) #we prepare the future event departure of the arrived customer 
                    #customerLocal.append({"customer":current["customer"],"interarrival":data-current["simTime"],"arrival":current['simTime'],"serviceTime":service})# we put the customer into the local array

                    if(custNum):# we controll if all the customer have been served
                        custNum.pop(0) # we pop to say that a customer has been served
                    if(custNum):# we check if now the list is empty
                        data=self.time_in(current["simTime"],data)
                        self.futureEvent.append({"customer":custNum[0],"simTime":data,"event":"arrive"})# we prepare the next customer in the future event 
                        #customerLocal.append({"customer":custNum[0],"interarrival":data-current["simTime"],"arrival":data,"serviceTime":service})
                        self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])# we sort by time the future event
                        #i+=1
                    # in case we do not have any other customers to be served
                    self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])# we sort by time the future event
                    customerLocal=sorted(customerLocal, key=lambda d: d["arrival"])# we do the same for customer local
                    #print(str(customerLocal)+'\n')
                    #print(str(self.futureEvent)+"\n\n")
                    
                   

                    #######
                    
                    if len(self.queue) in self.T.keys():
                        self.T[len(self.queue)]+=self.i-tStart
                    else:
                        self.T[len(self.queue)]=self.i-tStart
                    
                    #self.queue.append(customerLocal[0])
                    #self.queue=sorted(self.queue, key=lambda d: d["arrival"])
                    print("Serving: "+str(self.queue[0])+'\n')
                    customerLocal.pop(0)

                    self.serverState=1
                    tStart=self.i
                    
                
                elif current["event"]=="departure":


                    ######
                    print(self.queue)
                    self.futureEvent.pop(0)
                    data=self.time_in(data,None)
                    #tStart=self.i
                    print("Istant  "+str(self.i)+ " user: "+str(current['customer'])+" is departuring\n")
                    if(custNum):
                        custNum.pop(0)
                    if(custNum):# if we have still other customer to be served
                        
                        self.futureEvent.append({"customer":custNum[0],"simTime":data,"event":"arrive"})# we prepare the next customer arrival
                        #customerLocal.append({"customer":custNum[0],"interarrival":data-current["simTime"],"arrival":data,"serviceTime":service})# we put new customer into the local array
                        self.futureEvent=sorted(self.futureEvent, key=lambda d: d["simTime"])# we sort by time the future event
                        customerLocal=sorted(customerLocal, key=lambda d: d["arrival"])
                       # print(str(self.futureEvent)+"\n\n")
                    #######
                    
                    if len(self.queue) in self.T.keys():
                        self.T[len(self.queue)]+=self.i-tStart

                    else:self.T[len(self.queue)]=self.i-tStart
                    
                    
                    self.N+=1
                    #print(str(current)+'ciao'+str(self.queue[0]))
                    self.theta[current["customer"]]=self.i-self.queue[0]["arrival"]
                    self.queue.pop(0)
                    if(self.queue):
                        print("Istant "+str(self.i)+" Now serving costumer : "+str(self.queue[0])+'\n')
                    tStart=self.i


               
                else:
                    self.T[len(self.queue)]=self.i-tStart
            else:

                if len(self.queue)==0:# if in the we do not have anyone the state is set to FREE
                    self.serverState=0
                   # print("\nFree\n")
                    if(len(self.futureEvent)==0):
                        break

                self.i+=1 # increment simulation time
                    
                    
Obsim=Simulator()
print("Number of customers: ")
customerNum=int(input())

Obsim.begin(customerNum)

print("\n","T:",Obsim.get_T(),"\n","theta:",Obsim.get_theta(),"\n","ThetaKi:",Obsim.get_thetaKi(),"\n","X:",Obsim.get_X(),"\n","V:","\n")

