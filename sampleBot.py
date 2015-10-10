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

def timetoreach(source,dest):
    dist = math.sqrt((source.X()-dest.X())**2 + (source.Y()-dest.Y())**2)
    return int(dist) + 1

class SuperPlanet:
  def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
    self._planet_id = planet_id
    self._owner = owner
    self._num_ships = num_ships
    self._growth_rate = growth_rate
    self._x = x
    self._y = y
    self._netWorth = num_ships
    self._captureTurn = 0
    self._netOwner=owner
    self._timeline = {}
    self._timeline[0] = (0,owner)
    for i in range(1,101) :
        st = self._timeline[i-1] + self._growth_rate
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
              if(f.Owner()==self._owner):
                  self._timeline[f.TurnsRemaining()] = (self._timeline[f.TurnsRemaining()][0]+f.NumShips(),self._owner)
                  self._netWorth = self._timeline[f.TurnsRemaining()][0]
                  self._captureTurn = f.TurnsRemaining()
                  for i in range(f.TurnsRemaining()+1,101):
                      tmp = self._timeline[i-1] + self._growth_rate
                      self._timeline[i] = (tmp,self._owner)
              else:
                  if(self._timeline[f.TurnsRemaining()]<f.NumShips()):
                      self._timeline[f.TurnsRemaining()] = (self._timeline[f.TurnsRemaining()][0]-f.NumShips(),f.Owner())
                      for i in range(f.TurnsRemaining()+1,101):
                          tmp = self._timeline[i-1] + self._growth_rate
                          self._timeline[i] = (tmp,f._owner)
                  else:
                      self._timeline[f.TurnsRemaining()] = (f.NumShips()-self._timeline[f.TurnsRemaining()][0],self._owner))
                      for i in range(f.TurnsRemaining()+1,101):
                          tmp = self._timeline[i-1] + self._growth_rate
                          self._timeline[i] = (tmp,self._owner)
                  self._netWorth = self._timeline[f.TurnsRemaining()][0]
                  self._captureTurn = f.TurnsRemaining()

  def getState(self,time):
      return self._timeline[time]
    
  def simulateState(self,num,time):
      simtime = self._timeline
      currentval = simtime[time][0]
      if(self._owner==1):
          simtime[time] = (currentval+num,self._owner)
          for i in range(time+1,101):
              tmp = simtime[i-1] + self._growth_rate
              simtime[i] = (tmp,self._owner)
      else:
          if(num > currentval):
              simtime[time] = (num-currentval,1)
              for i in range(time+1,101):
                  tmp = simtime[i-1] + self._growth_rate
                  simtime[i] = (tmp,1)
          else:
              simtime[time] = (currentval-num,self._owner)
              for i in range(time+1,101):
                  tmp = simtime[i-1] + self._growth_rate
                  simtime[i] = (tmp,self._owner)
      return simtime
                      

def DoTurn(pw):
  # (1) If we currently have a fleet in flight, just do nothing.
  if len(pw.MyFleets()) >= 1:
    return
  # (2) Find my strongest planet.
  source = -1
  source_score = -999999.0
  source_num_ships = 0
  my_planets = pw.MyPlanets()
  for p in my_planets:
    score = float(p.NumShips())
    if score > source_score:
      source_score = score
      source = p.PlanetID()
      source_num_ships = p.NumShips()

  # (3) Find the weakest enemy or neutral planet.
  dest = -1
  dest_score = -999999.0
  not_my_planets = pw.NotMyPlanets()
  for p in not_my_planets:
    score = 1.0 / (1 + p.NumShips())
    if score > dest_score:
      dest_score = score
      dest = p.PlanetID()

  # (4) Send half the ships from my strongest planet to the weakest
  # planet that I do not own.
  if source >= 0 and dest >= 0:
    num_ships = source_num_ships / 2
    pw.IssueOrder(source, dest, num_ships)


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
