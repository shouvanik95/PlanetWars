import os
import sys

os.system("echo " + ">xxx.txt")
for i in range(1,101):
	#os.system("java -jar tools/PlayGame.jar maps/map"+str(i)+".txt 1000 1000 log.txt \"python harsha.py\" \"python alex.py\" 2> a.txt")
	#~ os.system("java -jar tools/PlayGame.jar maps/map"+str(i)+".txt 1000 1000 log.txt \"python WatchYourStep.py\" \"../CK/MyBot\" 2> a.txt")
	os.system("java -jar tools/PlayGame.jar maps/map"+str(i)+".txt 1000 100 log.txt \"python verygood.py\" \"../AD/MyBot\" 2> aa.txt")
	os.system("echo "+str(i) + " >>xxx.txt") 
	os.system("wc -l aa.txt >> xxx.txt")
	os.system("grep \"Player \" aa.txt >> xxx.txt")
	
	

