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
                  if(self._timeline[f.TurnsRemaining()]<f.NumShips()):
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
	  
  def getState(self,time):
		return self._timeline[time]			  

	
def supercurrentState(pw):
	planets = pw.Planets()
	Superplanets=list()
	for p in planets:
		Superplanets.append(SuperPlanet(p.PlanetID(),p.Owner(),p.NumShips(),p.GrowthRate(),p.X(),p.Y()))
	return Superplanets
	

def superConquerWhat(pw,source,superplanets):
	conquerList=list()
	for p in superplanets:
		if(p.PlanetID()!=source.PlanetID()):
			dist=math.sqrt((p.X()-source.X())**2+(p.Y()-source.Y())**2)
			timetoreach=int(dist)+1
			netWp=0
			if(p.getOwner()!=source.Owner()):
				if(p.getOwner()!=0):
					netWp=2*p.getState(timetoreach)[0]
				else:
					netWp=6*p.getState(timetoreach)[0]
				conquerList.append((p.PlanetID(),netWp,timetoreach,p.GrowthRate()))
	return conquerList

 

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
		shipsSent+=p[0].NumShips()
		if(shipsSent>=(planetToRape.getState(p[1]))[0]):
			canCapture=True
			captureTime=p[1]
			shipsSent+=(planetToRape.getState(p[1]))[0]
			shipsSent-=p[0].NumShips()
			break
	if(canCapture==False):
		return list()
	else:
		#For now the best 4 planets will send 10 each
		actionList=list()
		i=0
		for p in finalList:
				if(i<4):
					i+=1
					actionList.append((p[0],min(p[0].NumShips(),10)))
					
		return (actionList,captureTime,shipsSent)

import sys
def DoTurn(pw):
		#~ f.open("L",'a')
		#~ f.write("A")
		superplanets=supercurrentState(pw)
		my_planets = pw.MyPlanets()
		for p in superplanets:
			p.updateState(pw)
		rapelist=list()
		for p in superplanets:
			if(p.Owner()!=1):
				
				ll=computeRapeStats(pw,p,superplanets)
				if len(ll)!=0:
					rapelist.append((p,ll))
		sortedRapeList = sorted(rapelist, key=lambda tup: (tup[1][2]+2*tup[1][1])/(tup[0].GrowthRate()+0.01))
		i=0
		for rapes in sortedRapeList:
			if (i<4):
				i+=1
				fleetOrders=rapes[1][0]
				for fleets in fleetOrders:
					pw.IssueOrder(fleets[0].PlanetID(),rapes[0].PlanetID(),fleets[1])
		



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

