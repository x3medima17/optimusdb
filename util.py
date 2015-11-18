import settings
import struct 
	
def read_meta(file,field):
	type   = settings.meta[field][0]
	offset = settings.meta[field][1]
	nbytes = settings.meta[field][2]

	if type == "s":
		type += str(len(field))

	file.seek(offset)
	bval = file.read(nbytes)
	val = struct.unpack("="+type,bval)[0]
	return val

def write_meta(file,field,value):
	type   = settings.meta[field][0]
	offset = settings.meta[field][1]

	if type == "s":
		type = str(len(value)) + type

	bvalue = struct.pack("="+type,value)
	file.seek(offset)
	file.write(bvalue)


def trim(str):
	return str.strip().replace("\x00","")