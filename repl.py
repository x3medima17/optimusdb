import os 
import sys
import dbms
import models
import util

from models import Result

# ses = models.Session()

dbms = models.DBMS()
print dbms.purge()
print dbms.init()
print dbms.create_db("test")
print dbms.create_db("test")
print dbms.create_db("dima")
dbms.print_databases()

# print dbms.create_db("test")
while(0):
	try:
		print "optimusdb>",
		cmd = raw_input()
		if not cmd:
			continue

		result = ses.execute(cmd)
		if result:
			result = Result(0,result)
		else:
			result = Result(1,"Unrecognized command")
		print result

		
	except KeyboardInterrupt:
		print "Bye"
		sys.exit(0)