#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""
import sys
import logging
with open('example.log', 'w'):
    pass
logging.basicConfig(filename='example.log',level=logging.DEBUG)

from PlanetWars import PlanetWars
import math
def closestConquer(pw,source):
	not_my_planets = pw.NotMyPlanets()
	mindist = 100000.0
	mindest = -1
	for np in not_my_planets:
		dist=math.sqrt((np.X()-source.X())**2+(np.Y()-source.Y())**2)
		timetoreach=int(dist)+1
		if dist < mindist:
			if source.NumShips() > 2*np.NumShips():
				mindist=dist
				mindest=np.PlanetID()
	return mindest
	
class SuperPlanet:
  def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
    self._planet_id = planet_id
    self._owner = owner
    self._num_ships = num_ships
    self._growth_rate = growth_rate
    self._x = x
    self._y = y
    self._netWorth = num_ships
    self._captureTurn=0
    self._netOwner=owner
    self._timeline = [(0,0)]*101
    self._timeline[0] = (num_ships,owner)
    for i in range(1,101) :
				if(owner!=0):
						st = self._timeline[i-1][0] + growth_rate
						self._timeline[i] = (st,owner)
				else:
						st = self._timeline[i-1][0]
						self._timeline[i] = (st,owner)
	
  def getOwner(self):
    return self._netOwner
   
  def getTimeline(self):
    return self._timeline
    
  def setOwner(self,netOwner):
    self._netOwner=netOwner
    
  def setNet(self,netWorth):
    self._netWorth=netWorth
    
  def setCapture(self,captureTurn):
    self._captureTurn=captureTurn
    
  def getNet(self):
    return self._netWorth
    
  def getCapture(self):
    return self._captureTurn
    
  def PlanetID(self):
    return self._planet_id

  def Owner(self, new_owner=None):
    if new_owner == None:
      return self._owner
    self._owner = new_owner

  def NumShips(self, new_num_ships=None):
    if new_num_ships == None:
      return self._num_ships
    self._num_ships = new_num_ships

  def GrowthRate(self):
    return self._growth_rate

  def X(self):
    return self._x

  def Y(self):
    return self._y

  def updateState(self,pw):
			self._timeline[0] = (self._num_ships,self._owner)
			for i in range(1,101) :
					if(self._owner!=0):
							st = self._timeline[i-1][0] + self._growth_rate
							self._timeline[i] = (st,self._owner)
					else:
							st = self._timeline[i-1][0]
							self._timeline[i] = (st,self._owner)
									
			fleetss = pw.Fleets()
			sorted_fleets = sorted(fleetss, key=lambda tup: tup.TurnsRemaining())
      
      
      
			for f in sorted_fleets:
					if(self._planet_id == f.DestinationPlanet()) :
							if(f.Owner()==self._netOwner):
									self._timeline[f.TurnsRemaining()] = (self._timeline[f.TurnsRemaining()][0]+f.NumShips(),self._netOwner)
									self._netWorth = self._timeline[f.TurnsRemaining()][0]
									self._captureTurn = f.TurnsRemaining()
									for i in range(f.TurnsRemaining()+1,101):
											if(self._netOwner != 0):
													tmp = self._timeline[i-1][0] + self._growth_rate
													self._timeline[i] = (tmp,self._netOwner)
											else:
													tmp = self._timeline[i-1][0]
													self._timeline[i] = (tmp,self._netOwner)
							else:
									if(self._timeline[f.TurnsRemaining()][0]<f.NumShips()):
											self._timeline[f.TurnsRemaining()] = (f.NumShips()-self._timeline[f.TurnsRemaining()][0],f.Owner())
											self._netOwner = f.Owner()
											for i in range(f.TurnsRemaining()+1,101):
													if(self._netOwner != 0):
															tmp = self._timeline[i-1][0] + self._growth_rate
															self._timeline[i] = (tmp,self._netOwner)
													else:
															tmp = self._timeline[i-1][0]
															self._timeline[i] = (tmp,self._netOwner)
									else:
											self._timeline[f.TurnsRemaining()] = (self._timeline[f.TurnsRemaining()][0]-f.NumShips(),self._netOwner)
											for i in range(f.TurnsRemaining()+1,101):
													if(self._netOwner != 0):
															tmp = self._timeline[i-1][0] + self._growth_rate
															self._timeline[i] = (tmp,self._netOwner)
													else:
															tmp = self._timeline[i-1][0]
															self._timeline[i] = (tmp,self._netOwner)
									self._netWorth = self._timeline[f.TurnsRemaining()][0]
									self._captureTurn = f.TurnsRemaining()
	
  def simulateState(self,num,time):
			
			simtime = self._timeline[:]
			growth = self._growth_rate
			currentval = simtime[time][0]
			ownernow = self._owner
			if(ownernow == 1):
					simtime[time]=(currentval+num,ownernow)
					for i in range(time+1,101):
							if(ownernow != 0):
									tmp = simtime[i-1][0]+growth
									simtime[i] = (tmp,ownernow)
							else:
									tmp = simtime[i-1][0]
									simtime[i] = (tmp,ownernow)
			else:
					if(num > currentval):
							simtime[time]=(num-currentval,1)
							ownernow=1
							for i in range(time+1,101):
									if(ownernow != 0):
											tmp = simtime[i-1][0]+growth
											simtime[i] = (tmp,ownernow)
									else:
											tmp = simtime[i-1][0]
											simtime[i] = (tmp,ownernow)
					else:
							simtime[time]=(currentval-num,ownernow)
							for i in range(time+1,101):
									if(ownernow != 0):
											tmp = simtime[i-1][0]+growth
											simtime[i] = (tmp,ownernow)
									else:
											tmp = simtime[i-1][0]
											simtime[i] = (tmp,ownernow)
			return simtime
	
	
  def getValue(self,time):
		if(self._timeline[time][1] == 1):
			return self._timeline[time][0]
		elif(self._timeline[time][1] == 0):
			return 0
		else:
			return -1*self._timeline[time][0]	
			
  def getState(self,time):
		return self._timeline[time]
		
		  
	
 
def distance(planet1,planet2):
	return math.sqrt((planet1.X()-planet2.X())**2+(planet1.Y()-planet2.Y())**2)
	
def timetoreach(planet1,planet2):
	return int(distance(planet1,planet2))+1
	
def proximity(pw,superplanets):
			dist=0.0
			for p in superplanets:
					if(p.Owner()==1):
							dist+=math.sqrt((p.X()-pw.X())**2+(p.Y()-pw.Y())**2)
			return dist

def val(State):
	if(State[1]==1):
		return State[0]
	elif(State[1]==0):
		return 0
	else:
		return -1*State[0]
	
def gain(planet1,planet2,time1,time2):
	initial = planet1.getValue(time2)+planet2.getValue(time2)
	final = 50
	numships = 2 - planet2.getValue(time1)
	if(numships <= 0):
		return 0
	s1=planet1.simulateState(-1*numships,0)
	s2=planet2.simulateState(numships,timetoreach(planet1,planet2))
	final = val(s1[time2])+val(s2[time2])
	return final-initial



def gainList(planetlist,planetweights,Target,turns):
	shipsSent=0
	i=0
	captured=False
	finalvalue=0
	for i in range(0,len(planetlist)):
		shipsSent+=int(planetlist[i].NumShips()*planetweights[i])
		if(captured==True):
			finalvalue+=int(planetlist[i].NumShips()*planetweights[i])
		if(shipsSent>Target.getState(timetoreach(planetlist[i],Target))[0] and captured==False):
			finalvalue=shipsSent-Target.getState(timetoreach(planetlist[i],Target))[0]+(Target.GrowthRate()*(turns-timetoreach(planetlist[i],Target)))
			captured=True
	if finalvalue ==0:
		return -1000
	else:
		finalvalue+=Target.GrowthRate()*(finalvalue/200)
		if(Target.getState(turns)[1]==1):
			finalvalue+=Target.GrowthRate()*2
		return finalvalue
			
	
def l1norm(x):
	s=0.0
	for i in x:
		s+=abs(i)
	return s
	
def bestStrategy(turns,Target,superplanets):
	myplanetlist=list()
	for i in superplanets:
		if(i.Owner()==1 and timetoreach(i,Target)<=turns):
			myplanetlist.append(i)
	#Now i have to decide how much each planet will send to capture Target
	#Target could be our own planet
	#Assume each planet contributes equal weights initially
	sortedplanetlist = sorted(myplanetlist, key=lambda tup: timetoreach(tup,Target))
	planetsize=len(myplanetlist)
	planetweights=[1.0]*planetsize
	#The more weight a planet chooses to give,the worse it is.
	#But if a planet gives more weight it is possible to capture early on
	#We need to maximize this tradeoff.
	#We have a gain function gainList
	#We do a coordinate descent and try to optimize
	maxx=-10000.0
	for j in range(0,2):
		for i in range(0,planetsize):
			#Maximize the gain - l1norm(planetweights)
			tempweights=planetweights[:]
			for x in range(0,40):
				tempweights[i]=float(x)/40
				Gain=gainList(sortedplanetlist,tempweights,Target,turns)
				if(Gain-100*l1norm(tempweights)>maxx):
					maxx=Gain-100*l1norm(tempweights)
					planetweights=tempweights[:]
	return (sortedplanetlist,planetweights,maxx)
				
	
#In 25 turns I want max gain
#Total Growth rate, number of fleets , proximity of all planets
#Only decision is to attack a planet or no
gainTurns=40
def gainvector(superplanets):
	mystrategy=list()
	myplanet=superplanets[0]
	maxx=-10000.0
	for getthisplanet in superplanets:
		if(getthisplanet.getState(gainTurns)[1]!=1):
			#If i want to attack this planet in 25 turns get the best strategy
			strategy=bestStrategy(gainTurns,getthisplanet,superplanets)
			mystrategy.append((strategy,getthisplanet))
	sortstrategy = sorted(mystrategy, key=lambda tup: -1*tup[0][2])
	return sortstrategy

def scaredplanets(superplanets):
	plist=list()
	for p in superplanets:
		if(p.Owner()==1):
			for i in range(1,101):
				if(p.getState(i)[1]!=1):
					plist.append(p,i)
					break
	return plist

def computeRapeStats(pw,planetToRape,superplanets):
	planetListDist=list()
	for p in superplanets:
		if(p.Owner()==1):
			dist=math.sqrt((p.X()-planetToRape.X())**2+(p.Y()-planetToRape.Y())**2)
			planetListDist.append((p,dist))
	sortedDistList = sorted(planetListDist, key=lambda tup: tup[1])
	finalList=list()
	for planetanddist in sortedDistList:
		x=planetToRape.getState(int(planetanddist[1])+1)
		finalList.append((planetanddist[0],int(planetanddist[1])+1,x[0]))
	#~ #Given the finalList we have to computer how much each planet will send and which planet will send and report after how much time we will capture a planet
	#~ #We see if we can ever capture that planet using all our ships. If we cant just send nothing
	shipsSent=0
	canCapture=False
	captureTime=0
	for p in finalList:
		shipsSent+=(p[0].NumShips()-1)/2
		if(shipsSent>=(planetToRape.getState(p[1]))[0] or (planetToRape.getState(p[1]))[1]==1):
			canCapture=True
			captureTime=p[1]
			shipsSent+=(planetToRape.getState(p[1]))[0]
			shipsSent-=(p[0].NumShips()-1)/2
			break
	if(canCapture==False):
		return list()
	else:
		if(planetToRape.getState(captureTime)[1])==1:
			return list()
		#For now the best 4 planets will send 10 each
		actionList=list()
		shipsSent=0
		statevector=planetToRape.simulateState(0,0)
		for p in finalList:
				shipsSent+=max(0,(p[0].NumShips()-1)/2)
				if(shipsSent>(planetToRape.getState(p[1]))[0]):
					#Now send only how many needed
					shipsSent-=max(0,(p[0].NumShips()-1)/2) #We sent these many before
					needed=(planetToRape.getState(p[1]))[0]-shipsSent+1 #We need to send these many now
					if(needed>0):
						actionList.append((p[0],needed))
						shipsSent+=needed	
						temp=planetToRape.simulateState(shipsSent,p[1])
						
						for i in range(p[1],101):
							statevector[i]=temp[i]			
					break
				actionList.append((p[0],max(0,(p[0].NumShips()-1)/2)))
				temp=planetToRape.simulateState(shipsSent,p[1])

				for i in range(p[1],101):
					statevector[i]=temp[i]
		
		return (actionList,captureTime,shipsSent,planetToRape.getState(captureTime)[1],statevector)


def supercurrentState(pw):
	planets = pw.Planets()
	Superplanets=list()
	for p in planets:
		Superplanets.append(SuperPlanet(p.PlanetID(),p.Owner(),p.NumShips(),p.GrowthRate(),p.X(),p.Y()))
	return Superplanets

def DoTurn(pw):
		#~ f.open("L",'a')
		#~ f.write("A")
		
		superplanets=supercurrentState(pw)
		my_planets = pw.MyPlanets()
		
		for p in superplanets:
			p.updateState(pw)
		gvv=gainvector(superplanets)
		xxx=[0.0]*len(my_planets)
		quitthis=False
		logging.debug("NEWTURN")
		for gv in gvv:
			if(len(gv[0])!=0):
				for i in range(0,len(my_planets)):
					xxx[i]+=gv[0][1][i]
					if(xxx[i]>1.0):
						quitthis=True
				if(gv[0][2]>0 and quitthis==False):
					logging.debug(gv)
					logging.debug(xxx)
					planetsize=len(gv[0][0])
					for i in range(0,planetsize):
						a=gv[0][0][i].PlanetID()
						b=gv[1].PlanetID()
						c=int(gv[0][0][i].NumShips()*gv[0][1][i])
						if(c!=0):
							pw.IssueOrder(a,b,c)
		#~ rapelist=list()
		#~ for p in superplanets:
			#~ if(True):
				#~ ll=computeRapeStats(pw,p,superplanets)
				#~ if len(ll)!=0 and p.getState(ll[1])[1]!=1:
					#~ rapelist.append((p,ll))
		#~ 
		#~ 
		#~ sortedRapeList = sorted(rapelist, key=lambda tup: (tup[1][2]+2*tup[1][1]+10*proximity(tup[0],superplanets))/((tup[1][3]+1)*(tup[0].GrowthRate()+0.01)))
		#~ sortedRapeList = sorted(superplanets, key=lambda tup: (100*proximity(tup,superplanets))/((tup.Owner()+2)))
		#~ i=0
		#~ j=0
		#~ for rapes in sortedRapeList:
			#~ if (i<1 and j<2):
				#~ for r in rapelist:
					#~ if rapes.PlanetID()==r[0].PlanetID(): 
						#~ rape=r
						#~ logging.debug(rape)
						#~ i+=1
						#~ fleetOrders=rape[1][0]
						#~ for fleets in fleetOrders:
							#~ pw.IssueOrder(fleets[0].PlanetID(),rape[0].PlanetID(),fleets[1])
			#~ if(rapes.Owner()!=1):
				#~ j+=1
		



def main():
  map_data = ''
  while(True):
    current_line = raw_input()
    if len(current_line) >= 2 and current_line.startswith("go"):
      pw = PlanetWars(map_data)
      DoTurn(pw)
      pw.FinishTurn()
      map_data = ''
    else:
      map_data += current_line + '\n'


if __name__ == '__main__':
  try:
    import psyco
    psyco.full()
  except ImportError:
    pass
  try:
    main()
  except KeyboardInterrupt:
    print 'ctrl-c, leaving ...'

