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
	
  def simulateState(self,pw,num,time):
		currentowner=self._owner
		simtime = [(0,0)]*101
		simtime[0] = (self._num_ships,self._owner)
		for i in range(1,101) :
				if(self._owner!=0):
						st = simtime[i-1][0] + self._growth_rate
						simtime[i] = (st,self._owner)
				else:
						st = simtime[i-1][0]
						simtime[i] = (st,self._owner)
		fleetss=pw.Fleets()
		invasions = list()
		for f in fleetss:
			if(self._planet_id == f.DestinationPlanet()) :
				invasions.append((f.TurnsRemaining(),f.NumShips(),f.Owner()))
		invasions.append((time,num,1))
		sorted_fleets = sorted(invasions, key=lambda tup: tup[0])
		for f in sorted_fleets:
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
	
def supercurrentState(pw):
	planets = pw.Planets()
	Superplanets=list()
	for p in planets:
		Superplanets.append(SuperPlanet(p.PlanetID(),p.Owner(),p.NumShips(),p.GrowthRate(),p.X(),p.Y()))
	return Superplanets
	
def distance(planet1,planet2):
	return math.sqrt((planet1.X()-planet2.X())**2+(planet1.Y()-planet2.Y())**2)
	
def timetoreach(planet1,planet2):
	return int(distance(planet1,planet2))+1
	
def val(State):
	if(State[1]==1):
		return State[0]
	elif(State[1]==0):
		return 0
	else:
		return -1*State[0]
	
def gain(pw,planet1,planet2,time1,time2):
	logging.debug(str(planet1.PlanetID())+" "+str(planet2.PlanetID()))
	initial = planet1.getValue(time2)+planet2.getValue(time2)
	logging.debug(planet1.getValue(time2))
	logging.debug(planet2.getValue(time2))
	final = 50
	numships = 2 - planet2.getValue(time1)
	if(numships <= 0):
		return 0
	s1=planet1.simulateState(pw,-1*numships,0)
	logging.debug(s1)
	s2=planet2.simulateState(pw,numships,timetoreach(planet1,planet2))
	logging.debug(s2)
	final = val(s1[time2])+val(s2[time2])
	logging.debug(val(s1[time2]))
	logging.debug(val(s2[time2]))
	logging.debug(final-initial)
	return final-initial
	
def mintimegain(pw,planet1,planet2,time1,LIMIT):
	i=timetoreach(planet1,planet2)
	while i<LIMIT:
		if (gain(pw,planet1,planet2,time1,i) > 0):
			return i
		else:
			i=i+1
	return -1
			
		

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
				conquerList.append((p.PlanetID(),netWp,timetoreach,p.GrowthRate(),p))
	return conquerList
	
def newConquerWhat(pw,source,superplanets,HORIZON):
	conquerList=list()
	logging.debug("loopy")
	for p in superplanets:
		if(p.PlanetID()!=source.PlanetID()):
			g=gain(pw,source,p,timetoreach(source,p),timetoreach(source,p)+HORIZON)
			n=2-p.getState(timetoreach(source,p))[0]
			t=mintimegain(pw,source,p,timetoreach(source,p),timetoreach(source,p)+HORIZON)
			logging.debug("t is "+str(t))
			if(n>0 and t!=-1):
				conquerList.append((p,g,t,n))
	return conquerList
	
import sys
import logging
with open('stupid.log', 'w'):
    pass
logging.basicConfig(filename='stupid.log',level=logging.DEBUG)

def DoTurn(pw):
  superplanets=supercurrentState(pw)
  my_planets = pw.MyPlanets()
  for p in superplanets:
		p.updateState(pw)
  for p in superplanets:
		if(p.Owner()==1):
			CList=newConquerWhat(pw,p,superplanets,10)
			sorted_by_second = sorted(CList, key=lambda tup: (tup[2]-tup[1]))
			c = p.NumShips()
			
			for sd in sorted_by_second:
				if(sd[3]<c and sd[1]<0):
					pw.IssueOrder(p.PlanetID(),sd[0].PlanetID(),sd[3])
					count = count - sd[3]
				else:
					break

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
