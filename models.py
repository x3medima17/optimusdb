import settings
import struct
import util
import json
import os
import sys

class DBMS(object):
	"""
		The main class of entire system
	"""
	def __init__(self):
		self.file = None
		self.file_name = settings.settings["file_name"]
		self.meta = settings.meta

		#Check for file existence
		if not os.path.isfile(self.file_name):
			print Result(0,"Warning: No database file found. Try to initialize the system",bcolors.OKBLUE)
		else:
			self.file = open(self.file_name,"rb+")
		

	def init(self):
		"""
			Initialization
			1. Create file
			2. Write all meta with defaults
			3. Write credentials
		"""
		if os.path.isfile(self.file_name):
			return Result(3,"Initialization is already done")

		self.file = open(self.file_name,"wb")
		self.file.close()
		self.file = open(self.file_name,"rb+")
		f = self.file

		#Write meta
		for key,value in self.meta.iteritems():
			util.write_meta(f,key,value[3])

		
		#Write default database
		db = Database(f,"_default")
		db.prev = self.meta["hDatabases"][1]
		db.id = 0
		db.next = 0
		bdata = struct.pack("=I32sQQ",db.id, db.name, db.prev, db.next)

		f.seek(0,2)
		db.addr = f.tell()
		f.write(bdata)

		#Write head and tail
		util.write_meta(f,"hDatabases",db.addr)
		util.write_meta(f,"tDatabases",db.addr)
		f.flush()

		return Result(0,"Initialization has beend done")
		

	def purge(self):
		"""
			Delete database file
		"""
		try:
			os.remove(self.file_name)
			return Result(0,"Purged successfully")
		except OSError:
			return Result(7,"Nothing to purge")
		except:
			e = sys.exc_info()[0]
			return Result(2,"Something went wrong %s" % e)
	
	def execute(self,query):
		"""
			Execute query
		"""
		if query == "init":
			return self.init()
		elif query == "purge":
			return self.purge()

	def create_db(self,name):
		"""Create database"""
		db = Database(self.file,name)
		if db.exists():
			return Result(4,"Database exists")

		return db.create()
		
	def print_databases(self):
		"""Show all databases"""
		f = self.file
		head = util.read_meta(f,"hDatabases")

		db = Database(f,"_default")
		f.seek(head)
		db.addr = f.tell()
		bdata = f.read(52)
		db.id, db.name, db.prev, db.next = struct.unpack("=I32sQQ",bdata)
		db.name = util.trim(db.name)
		print db
		while db.next != 0:
			f.seek(db.next)
			db.addr = f.tell()
			bdata = f.read(52)
			db.id, db.name, db.prev, db.next = struct.unpack("=I32sQQ",bdata)
			db.name = util.trim(db.name)
			print db



class Meta(object):
	"""
		The meta data of database management system
	"""
	def __init__(self):
		self.fields = settings.meta
		pass

	def read(self):
		"""
			Read certain field from meta block
		"""
		pass

	def write(self):
		"""
			Write certain field to meta block
		"""
		pass

	def write_all_default(self):
		"""
			Write default values 
		"""
		pass		


class Session(object):
	"""Every query must be done through session"""
	def __init__(self):
		self.db = None
		self.dbms = DBMS()

	def set_active_db(self,name):
		"""Select current working database"""
		db = Database(name)
		if not self.db.exists():
			return Result(6,"Database not found")
		self.db = db
		return Result(0,"Database has been selected")

	def execute(self,query):
		return self.dbms.execute(query)


class Database(object):
	"""Database class"""
	def __init__(self,file,name=None):
		self.name = name
		self.id = None
		self.prev = 0
		self.next = 0
		self.addr = 0

		self.file = file

	def exists(self):
		"""Checks for database existence"""

		f = self.file
		head = util.read_meta(f,"hDatabases")
		

		db = Database(f,"_default")
		f.seek(head)
		db.addr = f.tell()
		bdata = f.read(52)
		db.id, db.name, db.prev, db.next = struct.unpack("=I32sQQ",bdata)
		db.name = util.trim(db.name)

		while db.next != 0:
			f.seek(db.next)
			db.addr = f.tell()
			bdata = f.read(52)
			db.id, db.name, db.prev, db.next = struct.unpack("=I32sQQ",bdata)
			db.name = util.trim(db.name)
			if db.name == self.name:
				return True
		return False
		
	def create(self):
		"""Creates new database"""

		f = self.file
		head = util.read_meta(f,"hDatabases")
		#Generate ID
		ID = util.read_meta(f,"cDatabases")+1
		util.write_meta(f,"cDatabases",ID)

		db = self.find_last()
		bdata = struct.pack("=I32sQQ",ID,self.name,db.addr,0)
		f.seek(0,2)
		self.addr = f.tell()

		#Write data 
		f.write(bdata)

		#Bind tail
		util.write_meta(f,"tDatabases",self.addr)

		#Bind previous node
		db.next = self.addr
		f.seek(db.addr+44)
		bdata = struct.pack("=I",db.next)
		f.write(bdata)

		return Result(0,"Database created")

	def find_last(self):
		"""
			Returns last database
		"""
		f = self.file
		head = util.read_meta(f,"tDatabases")

		db = Database(f)
		f.seek(head)
		db.addr = f.tell()
		bdata = f.read(52)
		db.id, db.name, db.prev, db.next = struct.unpack("=I32sQQ",bdata)
		db.name = util.trim(db.name)
		return db			

	def __str__(self):
		return "Name: %s\nID: %s\nPrev: %s\nAddr: %s\nNext: %s\n" % (self.name, self.id, self.prev, self.addr, self.next)




class TableField(object):
	"""
	Table attributes
	"""
	def __init__(self,name,type,size):
		self.name = name
		self.type = type
		self.size = size


class Table(object):
	def __init__(self,name):
		self.name = name
		self.fields = []

	def add_field(field):
		self.fields.append(field)




class Result(object):
	def __init__(self,status,message,color=None,data=None):
		self.status = status
		self.message = message
		self.data = data
		self.color = color


	def dump(self):
		result = dict(
			status = self.status,
			message = self.message,
			data = self.data
			)
		return json.dumps(result)

	def __str__(self):
		result = bcolors.OKGREEN
		if self.color:
			result = self.color
		if self.status != 0:
			color = bcolors.FAIL
			if self.color:
				color = self.color
			result = "%sError %s: " % (bcolors.FAIL,self.status)
		result += "%s%s" % (self.message, bcolors.ENDC)

		return result


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'