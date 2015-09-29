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
    
def currentState(pw):
	planets = pw.Planets()
	Superplanets=list()
	for p in planets:
		Superplanets.append(SuperPlanet(p.PlanetID(),p.Owner(),p.NumShips(),p.GrowthRate(),p.X(),p.Y()))
	fleetss = pw.Fleets()
	for f in fleetss:
		dest=f.DestinationPlanet()
		for p in Superplanets:
			if(p.PlanetID()==dest):
				if(f.Owner()==p.getOwner()):
					p.setNet(p.getNet()+f.NumShips())
				else:
					if(p.getNet()>=f.NumShips()):
						p.setNet(p.getNet()-f.NumShips())
					else:
						p.setNet(-p.getNet()+f.NumShips())
						p.setOwner(f.Owner())
				if(f.TurnsRemaining()>p.getCapture()):
					p.setCapture(f.TurnsRemaining())
	return Superplanets
	
def supercurrentState(pw):
	planets = pw.Planets()
	Superplanets=list()
	for p in planets:
		Superplanets.append(SuperPlanet(p.PlanetID(),p.Owner(),p.NumShips(),p.GrowthRate(),p.X(),p.Y()))
	fleetss = pw.Fleets()
	sorted_fleets = sorted(fleetss, key=lambda tup: tup.TurnsRemaining())
	for f in sorted_fleets:
		dest=f.DestinationPlanet()
		for p in Superplanets:
			if(p.PlanetID()==dest):
				if(f.Owner()==p.getOwner()):
					p.setNet(p.getNet()+f.NumShips()+(f.TurnsRemaining()-p.getCapture())*p.GrowthRate())
					p.setCapture(f.TurnsRemaining())
				else:
					if(f.Owner()==0):
						if(p.getNet()>=f.NumShips()):
							p.setNet(p.getNet()-f.NumShips())
							p.setCapture(f.TurnsRemaining())
						else:
							p.setNet(-p.getNet()+f.NumShips())
							p.setOwner(f.Owner())
							p.setCapture(f.TurnsRemaining())
					else:
						if(p.getNet()+(f.TurnsRemaining()-p.getCapture())*p.GrowthRate()>=f.NumShips()):
							p.setNet(p.getNet()+(f.TurnsRemaining()-p.getCapture())*p.GrowthRate()-f.NumShips())
							p.setCapture(f.TurnsRemaining())
						else:
							p.setNet(-p.getNet()-(f.TurnsRemaining()-p.getCapture())*p.GrowthRate()+f.NumShips())
							p.setOwner(f.Owner())
							p.setCapture(f.TurnsRemaining())
						
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
					if(timetoreach>p.getCapture()):
						netWp=2*((timetoreach-p.getCapture())*p.GrowthRate()+p.getNet())
					else:
						netWp=2*(p.getNet())
				else:
					netWp=6*p.getNet()
				conquerList.append((p.PlanetID(),netWp,timetoreach,p.GrowthRate()))
	return conquerList
	
def ConquerWhat(pw,source,superplanets):
	conquerList=list()
	for p in superplanets:
		if(p.PlanetID()!=source.PlanetID()):
			dist=math.sqrt((p.X()-source.X())**2+(p.Y()-source.Y())**2)
			timetoreach=int(dist)+1
			netWp=0
			#If not expected to be the owner then we will do something. We have to improve currentState code to get a better approximation of things happening.
			if(p.getOwner()!=source.Owner()):
				if(p.Owner()==0): #If current owner is neutral, expected after sometime will be the networth
					netWp=-2*p.getNet()
				elif(p.Owner()==1): #If current is us then expected when we reach will be 
					netWp=-1*p.getNet() + p.GrowthRate()*timetoreach
				elif(p.Owner()==2): #If current is enemy then expected when we reach will be 
					netWp=-1*p.getNet() - 1*p.GrowthRate()*timetoreach
				if(netWp<0):
					conquerList.append((p.PlanetID(),netWp,netWp/(0.1+p.GrowthRate()),timetoreach,p.GrowthRate()))
			
	return conquerList

def DoTurn(pw):
  superplanets=supercurrentState(pw)
  my_planets = pw.MyPlanets()
  for p in superplanets:
	if(p.Owner()==1):
		CList=superConquerWhat(pw,p,superplanets)
		sorted_by_second = sorted(CList, key=lambda tup: (tup[1]+2*tup[2]) / (tup[3]+0.1))
		count = p.getNet()
		allowed = p.NumShips()
		for sd in sorted_by_second:
			if(sd[1]/2+2>0):
				if(count > sd[1]/2+2 and allowed > sd[1]/2+2):
					pw.IssueOrder(p.PlanetID(), sd[0],sd[1]/2+2)
					count = count - sd[1]/2-2
					allowed = allowed - sd[1]/2-2
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
