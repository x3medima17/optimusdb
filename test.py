import os 
import sys

while(1):
	try:
		print ">",
		cmd = raw_input()
		if cmd:
			print cmd
	except KeyboardInterrupt:
		print "Bye"
		sys.exit(0)