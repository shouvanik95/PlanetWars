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
		if dist < mindist:
			if source.NumShips() > 2*np.NumShips():
				mindist=dist
				mindest=np.PlanetID()
	return mindest
		

def DoTurn(pw):
  my_planets = pw.MyPlanets()
  for p in my_planets:
	destID=closestConquer(pw,p);
	if(destID!=-1):
		pw.IssueOrder(p.PlanetID(), destID,(int) (p.NumShips()/2))



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
