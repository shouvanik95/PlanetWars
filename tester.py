import os
import sys

os.system("echo " + ">b.txt")
for i in range(1,101):
	#os.system("java -jar tools/PlayGame.jar maps/map"+str(i)+".txt 1000 1000 log.txt \"python harsha.py\" \"python alex.py\" 2> a.txt")
	os.system("java -jar tools/PlayGame.jar maps/map"+str(i)+".txt 1000 1000 log.txt \"python harsha.py\" \"java -jar ./example_bots/RageBot.jar \" 2> a.txt")
	os.system("echo "+str(i) + " >>b.txt") 
	os.system("wc -l a.txt >> b.txt")
	os.system("grep \"Player \" a.txt >> b.txt")
	
	

