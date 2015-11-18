import struct
import settings

def set_name(file, value):
	name = list(value)
	bname = struct.pack('c'*len(name),*name)
	offset = settings.meta["name"][1]
	file.seek(offset)
	file.write(bname)


def set_version(file,value_a, value_b):
	bversion = struct.pack("BcB",value_a,".",value_b)
	offset = settings.meta["version"][1]
	file.seek(offset)
	file.write(bversion)

def set_head(file,field,value):
	bhead = struct.pack("Q",value)
	offset = settings.meta[field][1]
	file.seek(offset)
	file.write(bhead)



