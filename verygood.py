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
    self.invasions=[list()]*101
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

			fleetss = pw.Fleets()
			sorted_fleets = sorted(fleetss, key=lambda tup: tup.TurnsRemaining())
			for f in sorted_fleets:
					if(self._planet_id == f.DestinationPlanet()) :
							self.invasions[f.TurnsRemaining()].append((f.TurnsRemaining(),f.NumShips(),f.Owner()))
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
	
	#If i remove num fleets from my ship,will I lose in turns
  def quicksimstate(self,num,turns):
		for i in range(1,turns):
			if(self._timeline[i][0]-num<0):
				return i
		return -1

  def quicklossstate(self,turns):
		for i in range(1,turns):
			if(self._timeline[i][1]==2):
				return i
		return -1
	#If i add num fleets in turn x will I retain the planet
  def quickcheckstate(self,num,x,turns):
		for i in range(x,turns):
			if(self._timeline[i][1]==2): #If planet is enemy
				if(self._timeline[i][0]-num<0): #If adding num ships will make it mine at some time
					return i
		return -1
		
  def simulateState(self,myfleets,timeweneed):
		logging.debug(myfleets)
		simtime=self._timeline[:]
		currentowner=self._timeline[0][1]
		#~ if(currentowner==1):
			#~ simtime[time]=(simtime[time][0]+num,1)
		#~ else:
			#~ if(simtime[time][0]>=num):
				#~ simtime[time]=(simtime[time][0]-num,currentowner)
			#~ else:
				#~ simtime[time]=(-1*simtime[time][0]+num,1)
				#~ currentowner=1
		inv=self.invasions[:]
		for m in myfleets:
			inv[m[1]].append((m[1],m[0],1))
		for ii in range(1,timeweneed+1):
				for f in inv[ii]:
					if(f[2]==currentowner):
							simtime[f[0]] = (simtime[f[0]][0]+f[1],currentowner)
							for i in range(f[0]+1,101):
									if(currentowner != 0):
											tmp = simtime[i-1][0] + self._growth_rate
											simtime[i] = (tmp,currentowner)
									else:
											tmp = simtime[i-1][0]
											simtime[i] = (tmp,currentowner)
					else:
							if(simtime[f[0]][0]<f[1]):
									simtime[f[0]] = (f[1]-simtime[f[0]][0],f[2])
									currentowner = f[2]
									for i in range(f[0]+1,101):
											if(currentowner != 0):
													tmp = simtime[i-1][0] + self._growth_rate
													simtime[i] = (tmp,currentowner)
											else:
													tmp = simtime[i-1][0]
													simtime[i] = (tmp,currentowner)
							else:
									simtime[f[0]] = (simtime[f[0]][0]-f[1],currentowner)
									for i in range(f[0]+1,101):
											if(currentowner != 0):
													tmp = simtime[i-1][0] + self._growth_rate
													simtime[i] = (tmp,currentowner)
											else:
													tmp = simtime[i-1][0]
													simtime[i] = (tmp,currentowner)
		
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
	
def friendproximity(pw,superplanets):
			dist=0.0
			count=0.001
			for p in superplanets:
					if(p.Owner()==1):
							count+=1.0
							dist+=math.sqrt((p.X()-pw.X())**2+(p.Y()-pw.Y())**2)
			return dist/count

def allproximity(pw,superplanets):
			dist=0.0
			for p in superplanets:
					dist+=math.sqrt((p.X()-pw.X())**2+(p.Y()-pw.Y())**2)
			return dist

def enemyproximity(pw,superplanets):
			dist=10000.0
			for p in superplanets:
					if(p.Owner()==2):
							d=math.sqrt((p.X()-pw.X())**2+(p.Y()-pw.Y())**2)
							if(d<dist):
								dist=d
			return dist
			

#We should include if gainList is calculating the gain if the current planet is ourselves
def gainList(planetlist,planetweights,Target,turns,superplanets):
	gain=0
	shipsSent=0
	captured=False
	captureTime=0
	hitin3=0
	fleetsafter3=0
	#~ logging.debug("XYZ")
	if(Target.Owner()!=1):
		for i in range(0,len(planetlist)):
			shipsSent+=int(planetlist[i].NumShips()*planetweights[i])
			if(captured==True):
				fleetsafter3+=int(planetlist[i].NumShips()*planetweights[i])
			simstate=planetlist[i].quicksimstate(int(planetlist[i].NumShips()*planetweights[i]),turns)
			if(simstate!=-1):
				gain-=planetlist[i].GrowthRate()*(turns-simstate)
			if(shipsSent>Target.getState(timetoreach(planetlist[i],Target))[0] and captured==False):
				#Captured
				captureTime=timetoreach(planetlist[i],Target)
				captured=True
				if(captureTime+3<turns):
					#R-G
					if(Target.getState(captureTime+3)[1]==1 and Target.getState(turns)[1]==2):
						hitin3=Target.getState(turns)[0]-(turns-captureTime-3)*Target.GrowthRate()+Target.getState(captureTime+3)[0]
					#G-G
					if(Target.getState(captureTime+3)[1]==2 and Target.getState(turns)[1]==2):
						hitin3=Target.getState(turns)[0]-(turns-captureTime-3)*Target.GrowthRate()-Target.getState(captureTime+3)[0]
					#N-G
					if(Target.getState(captureTime+3)[1]==0 and Target.getState(turns)[1]==2):
						hitin3=Target.getState(turns)[0]-(turns-captureTime-3)*Target.GrowthRate()+Target.getState(captureTime+3)[0]					
				if(Target.getState(timetoreach(planetlist[i],Target))[1]==0):
					gain-=Target.getState(timetoreach(planetlist[i],Target))[0]
				
		if(fleetsafter3>=hitin3 and captured==True):
			gain+=(Target.GrowthRate()*(turns-captureTime))
			if(Target.getState(captureTime)[1]==2):
				gain+=(Target.GrowthRate()*(turns-captureTime))
	else:
		qstate=Target.quicklossstate(turns)
		ccheck=False
		for i in range(0,len(planetlist)):
			shipsSent+=int(planetlist[i].NumShips()*planetweights[i])
			simstate=planetlist[i].quicksimstate(int(planetlist[i].NumShips()*planetweights[i]),turns)
			if(simstate!=-1):
				gain-=2*planetlist[i].GrowthRate()*(turns-simstate)
			cstate=Target.quickcheckstate(shipsSent,timetoreach(planetlist[i],Target),turns)
			if(qstate!=-1 and ccheck==False):
				if(cstate!=-1):
					ccheck=True
					gain+=2*Target.GrowthRate()*(turns-cstate)
			
	return gain
			
	
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
	planetweights=[0.5]*planetsize
	#The more weight a planet chooses to give,the worse it is.
	#But if a planet gives more weight it is possible to capture early on
	#We need to maximize this tradeoff.
	#We have a gain function gainList
	#We do a coordinate descent and try to optimize
	maxx=-10000.0
	timeoutfactor=100.0
	#~ logging.debug("X")	
	iterationlimit=int(timeoutfactor/(planetsize+1))
	#~ logging.debug(iterationlimit)
	for j in range(0,1):
		for i in range(0,planetsize):
			#Maximize the gain - l1norm(planetweights)
			tempweights=planetweights[:]
			for x in range(0,iterationlimit):
				tempweights[planetsize-i-1]=float(x)/iterationlimit
				Gain=gainList(sortedplanetlist,tempweights,Target,turns,superplanets)
				if(Gain>maxx):
					maxx=Gain
					planetweights=tempweights[:]
	#~ logging.debug(maxx)
	#~ logging.debug((maxx,Target.NumShips()))
	return (sortedplanetlist,planetweights,maxx)
				
	
#In 25 turns I want max gain
#Total Growth rate, number of fleets , proximity of all planets
#Only decision is to attack a planet or no
gainTurns=25
def gainvector(superplanets,closest3):
	mystrategy=list()
	myplanet=superplanets[0]
	maxx=-10000.0
	for getthisplanet in superplanets:
		if(getthisplanet.getState(gainTurns)[1]!=1):
			#If i want to attack this planet in 25 turns get the best strategy
			strategy=bestStrategy(gainTurns,getthisplanet,superplanets)
			mystrategy.append((strategy,getthisplanet,h2proximity(strategy,closest3),h3proximity(strategy,closest3)))
	sortstrategy = sorted(mystrategy, key=lambda tup: (-1*tup[0][2]+tup[2]-1*tup[3]+friendproximity(tup[1],superplanets)*tup[1].GrowthRate()-enemyproximity(tup[1],superplanets)*tup[1].GrowthRate())*allproximity(tup[1],superplanets))
	#~ 
	#~ myplanetlist=list()
	#~ logging.debug("Starting I")
	#~ for i in superplanets:
		#~ if(i.Owner()==1):
			#~ myplanetlist.append(i)
	#~ planetsize=len(myplanetlist)
	#~ planetweights=[0.0]*planetsize
	#~ for getthisplanet in superplanets:
		#~ planetweights=[0.0]*planetsize
		#~ if(getthisplanet.Owner()==1):
			#~ for i in range(0,planetsize):
				#~ pww=planetweights[:]
				#~ if(myplanetlist[i].PlanetID()==getthisplanet.PlanetID() or myplanetlist[i].getState(gainTurns)[1]!=1):
					#~ break
				#~ pww[i]=float(myplanetlist[i].GrowthRate())/(float(myplanetlist[i].NumShips())+0.01)
				#~ if(pww[i]>0.5):
					#~ pww[i]=0.0
				#~ else:
					#~ mystrategy.append(((myplanetlist,pww,100/h1proximity(getthisplanet,closest3)),getthisplanet))
					#~ logging.debug((((myplanetlist,pww,100/h1proximity(getthisplanet,closest3)),getthisplanet)))
	#~ logging.debug("Ending I")
	#~ logging.debug(mystrategy)
	#~ sortstrategy = sorted(mystrategy, key=lambda tup: (-1*tup[0][2]-gain2ndturn(tup[1],superplanets,closest3)+allproximity(tup[1],superplanets)/1000))
	return sortstrategy

def h1proximity(p,closest3):
	gains=0.0
	for planet in closest3[p.PlanetID()]:
		if(planet.Owner()==2):
			gains+=planet.NumShips()+planet.GrowthRate()*10
	if(gains<0.001):
		gains=10000.0
	return gains

def sendloss1(shipssent,p,closest3):
	#~ logging.debug("X3")
	losses=0.0
	enemygrowth=0
	enemyships=0
	for planet in closest3[p.PlanetID()]:
		if(planet.Owner()==2):
			#~ logging.debug((planet.PlanetID(),planet.NumShips()))
			enemygrowth+=planet.GrowthRate()
			enemyships+=planet.NumShips()
	initialtake=gainTurns
	#~ logging.debug("X4")
	for i in range(0,gainTurns):
		if(enemyships+enemygrowth*i>p.NumShips()+p.GrowthRate()*i):
			initialtake=i
			break
	finaltake=gainTurns
	#~ logging.debug(initialtake)
	for i in range(0,gainTurns):
		if(enemyships+enemygrowth*i>p.NumShips()+p.GrowthRate()*i-shipssent):
			finaltake=i
			break
	#~ logging.debug(finaltake)
	return p.GrowthRate()*(initialtake-finaltake)
	
def attackgain(shipssent,p,closest3):
	gain=0.0
	initialgains=0
	finalgains=0
	for planet in closest3[p.PlanetID()]:
		if(planet.Owner()==2):
			timetobemore=(planet.NumShips()-p.NumShips())/(p.GrowthRate()-planet.GrowthRate()+0.01)
			if(timetobemore<0):
				if(p.GrowthRate()<planet.GrowthRate()):
					timetobemore=10000
				else:
					timetobemore=0
			g=2*(gainTurns-(timetobemore+timetoreach(planet,p)))*planet.GrowthRate()
			if(g>initialgains):
				initialgains=g
		if(planet.Owner()==0):
			timetobemore=(planet.NumShips()-p.NumShips())/(p.GrowthRate()+0.01)
			if(timetobemore<0):
				timetobemore=0
			g=(gainTurns-(timetobemore+timetoreach(planet,p)))*planet.GrowthRate() - planet.NumShips()
			if(g>initialgains):
				initialgains=g
	
	for planet in closest3[p.PlanetID()]:
		if(planet.Owner()==2):
			timetobemore=(planet.NumShips()-p.NumShips()-shipssent)/(p.GrowthRate()-planet.GrowthRate()+0.01)
			if(timetobemore<0):
				if(p.GrowthRate()<planet.GrowthRate()):
					timetobemore=10000
				else:
					timetobemore=0
			g=2*(gainTurns-(timetobemore+timetoreach(planet,p)))*planet.GrowthRate()
			if(g>finalgains):
				finalgains=g
		if(planet.Owner()==0):
			timetobemore=(planet.NumShips()-p.NumShips()-shipssent)/(p.GrowthRate()+0.01)
			if(timetobemore<0):
				timetobemore=0
			g=(gainTurns-(timetobemore+timetoreach(planet,p)))*planet.GrowthRate() - planet.NumShips()
			if(g>finalgains):
				finalgains=g
	
	
	return finalgains-initialgains #Gains by sending fleets
		

def h3proximity(strategy,closest3):
	#~ logging.debug("X1")
	gains=0.0
	for i in range(0,len(strategy[0])):
		#~ logging.debug("X2")
		gains+=attackgain(float(strategy[0][i].NumShips())*strategy[1][i],strategy[0][i],closest3)
	return gains
	
def h2proximity(strategy,closest3):
	#~ logging.debug("X1")
	losses=0.0
	for i in range(0,len(strategy[0])):
		#~ logging.debug("X2")
		losses+=sendloss1(float(strategy[0][i].NumShips())*strategy[1][i],strategy[0][i],closest3)
	return losses

def gain2ndturn(p,superplanets,closest3):
	gains=0.0
	pcount=1
	for planet in closest3[p.PlanetID()]:
		gains-=danger(planet)[0]*5+danger(planet)[1]/pcount
		if(p.GrowthRate()>planet.GrowthRate()):
			g=planet.GrowthRate()*(20-(planet.NumShips()-p.NumShips())/(p.GrowthRate()-planet.GrowthRate()))
			gains+=max(0,g)
		pcount+=1
	return gains
	
def supercurrentState(pw):
	planets = pw.Planets()
	Superplanets=list()
	for p in planets:
		Superplanets.append(SuperPlanet(p.PlanetID(),p.Owner(),p.NumShips(),p.GrowthRate(),p.X(),p.Y()))
	return Superplanets

def closest3List(superplanets):
	closeList=[list()]*len(superplanets)
	for planet1 in superplanets:
		sortedList=sorted(superplanets,key=lambda tup: distance(planet1,tup))
		closeList[planet1.PlanetID()]=sortedList[1:4]
	return closeList
	
def danger(planet1):
	if(planet1.Owner()==1):
		return (-1*planet1.GrowthRate(),-1*planet1.NumShips())
	if(planet1.Owner()==2):
		return (planet1.GrowthRate(),planet1.NumShips())
	else:
		return (0,0)
		

def enemymindistance(p,superplanets):
	l22=1000000.0
	for pl in superplanets:
		if(pl.Owner()==2):
			l2=math.sqrt((p.X()-pl.X())**2+(p.Y()-pl.Y())**2)
			if(l2<l22):
				l22=l2
	return l22
	
def planettosupport(p,myplanets,superplanets):
	supportplanets=list()
	for planet in myplanets:
		if(enemymindistance(p,superplanets)>enemymindistance(planet,superplanets) and p.PlanetID()!=planet.PlanetID()):
			supportplanets.append(planet)
	
	sortedclose=sorted(supportplanets,key=lambda tup: timetoreach(tup,p))
	if(len(sortedclose)!=0):
		return sortedclose[0]
	return p
	
def DoTurn(pw):
		superplanets=supercurrentState(pw)
		my_planets = list()
		my_growthrate=0.0
		enemy_growthrate=0.0
		for i in superplanets:
			if(i.Owner()==1):
				my_planets.append(i)
				my_growthrate+=i.GrowthRate()
		enemy_planets = list()
		for i in superplanets:
			if(i.Owner()==2):
				enemy_planets.append(i)
				enemy_growthrate+=i.GrowthRate()
		closest3=closest3List(superplanets)
		for p in superplanets:
			p.updateState(pw)
		logging.debug("OLDTURN")
		gvv=gainvector(superplanets,closest3)
		xxx=[0.0]*len(superplanets)
		quitthis=False
		logging.debug("NEWTURN")
		strategylim=3
		if(enemy_growthrate>my_growthrate or len(my_planets)<4):
			strategylim=3
		else:
			strategylim=2
		for gv in gvv:
			logging.debug((gv,gv[1].PlanetID(),gv[1].NumShips()))
			if(strategylim>0):
				quitthis=False
				strategylim-=1
				if(len(gv[0])!=0 and gv[0][2]-gv[2]>0.0):
					for i in range(0,len(gv[0][0])):
						if(xxx[gv[0][0][i].PlanetID()]>0.3):
							quitthis=True
						xxx[gv[0][0][i].PlanetID()]+=gv[0][1][i]
					if(gv[0][2]-gv[2]>0.0 and quitthis==False):
						planetsize=len(gv[0][0])
						for i in range(0,planetsize):
							a=gv[0][0][i].PlanetID()
							b=gv[1].PlanetID()
							c=int(gv[0][0][i].NumShips()*gv[0][1][i])
							if(c!=0 and c<=gv[0][0][i].NumShips() and xxx[gv[0][0][i].PlanetID()]<=1.0):
								logging.debug((a,b,c))
								pw.IssueOrder(a,b,c)
		logging.debug("XXXX!~EQFWFWF")
		if(len(my_planets)>4):#~ 
			for ii in my_planets:
				dontsend=False
				for enemy in enemy_planets:
					for p in closest3[enemy.PlanetID()]:
						if(p.PlanetID()==ii.PlanetID()):
							dontsend=True
				if(int(xxx[ii.PlanetID()]*ii.NumShips())<0.01 and dontsend==False):
					bestw=0
					bestj=planettosupport(ii,my_planets,superplanets)
					exist=False
					if(bestj.PlanetID()!=ii.PlanetID()):
						exist=True
					if(exist):
						for w in range(1,11):
							weight=float(w)/10.0
							simstate=ii.quicksimstate(int(ii.NumShips()*weight),gainTurns)
							if(simstate==-1):
								bestw=ii.NumShips()*weight
						if(bestw>0):
							logging.debug((ii.PlanetID(),bestj.PlanetID(),bestw))
							pw.IssueOrder(ii.PlanetID(),bestj.PlanetID(),int(bestw))



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

