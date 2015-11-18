meta = dict(
	name = ("s",0,16,"OptimusDB"),
	version = ("s",16,3,"0.0"),
	
	hDatabases = ("Q",19,8,0),
	tDatabases = ("Q",27,8,0),
	cDatabases = ("I",35,4,0),
	
	hTables = ("Q",39,8,0),
	tTables = ("Q",48,8,0),
	cTables = ("I",55,4,0),

	hColumns = ("Q",59,8,0),
	tColumns = ("Q",67,8,0),
	cColumns = ("I",75,4,0),

	hSerials = ("Q",79,8,0),
	tSerials = ("Q",87,8,0),
	cSerials = ("I",95,4,0),
	
	hKeys = ("Q",99,8,0),
	tKeys = ("Q",107,8,0),
	cKeys = ("Q",115,4,0),
	)


credentials = dict(
	name = "OptimusDB",
	version = "0.1"
	)


settings = dict(
	file_name = "data.db"
	)
