import os
import struct
import fx
import settings
import models
import util

from models import Result
"""
Type, Offset, Length,Format
"""




def create_db(db_name):
	db_name = db_name.strip()
	if " " in db_name:
		return Result(5,"Syntax error")

	db = models.Database(db_name)
	if db.exists():
		return Result(4,"Database exists")
	else:
		db.create()
		return Result(0,"Database has been created")
	

def init():
	"""
		Initialization
		1. Create file
		2. Write all meta with zero
		3. Write credentials
	"""
	if os.path.isfile("data.db"):
		return Result(3,"Initialization is already done")

	f = open("data.db","wb")

	name = settings.credentials["name"]
	fx.set_name(f,name)


	version_a = settings.credeantials["version_a"]
	version_b = settings.credeantials["version_b"]
	fx.set_version(f,version_a,version_b)

	util.write_meta(f,"hDatabases",0)
	util.write_meta(f,"hTables",0)
	util.write_meta(f,"hColumns",0)
	util.write_meta(f,"hKeys",0)
	util.write_meta(f,"hSerials",0)

	util.write_meta(f,"cDatabases",0)
	util.write_meta(f,"cTables",0)
	util.write_meta(f,"cKeys",0)
	util.write_meta(f,"cSerials",0)


	f.close()
	return Result(0,"Initialized")

def purge():
	try:
		os.remove("data.db")
		return Result(0,"Purged successfully")
	except:
		return Result(2,"Something went wrong")

def run_command(cmd):
	cmd = cmd.lower().strip()

	if cmd == "init":
		result = init()
		return result

	if cmd == "purge":
		result = purge()
		return result

	if "create database" in cmd:
		db_name = cmd.replace("create database","")
		result = create_db(db_name)
		return result