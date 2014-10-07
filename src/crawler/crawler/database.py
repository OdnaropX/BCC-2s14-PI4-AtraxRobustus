import psycopg2

class Database:
	conn = None
	cursor = None
	dbname = None
	dbuser = None
	dbpass = None
	dbhost = None
	dbport = None
	last_error = None
	error = False
	insert_id = 0
	rows_affected = 0
	last_query = None
	result = None
	last_query = None
	status_message = None
	connected = False
	
	def __init__(self, dbname, dbuser, dbpass,dbhost,dbport):
		self.dbname = dbname
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbhost = dbhost
		self.dbport = dbport	
	
	#Destroy cached items.
	def flush(self):
		self.last_error = None
		self.error = False
		self.insert_id = 0
		self.rows_affected = 0
		self.last_query = None
		self.result = None
		self.last_query = None
		self.status_message = None
	
	def set_error(self,msg):
		self.last_error = msg
		self.error = True 
		self.rows_affected = 0
		self.insert_id = 0
		self.status_message = "Programing error. No DB error."
		
	def connect(self):
		try:
			self.conn = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpass, host = self.dbhost, port = self.dbport);
			self.error = False
			self.cursor = self.conn.cursor()
			self.connected = True
		except:
			self.set_error("Database connect error")
			self.connected = False
			return False
		return True
		
	def is_connected(self):
		return self.connected
		
	def disconnect(self):
		self.cursor.close()
		self.conn.close()
		
	def query(self,sql, parameters = None):
		if(sql == "" or sql == None):
			#retorna erro
			self.set_error("No SQL query to execute")
			self.last_query = ""
			return False
			
		try:
			if(parameters == None):
				self.cursor.execute(sql)
			else:
				self.cursor.execute(sql, parameters)
		except psycopg2 as e:
			print e.pgerror
			return False

		#print self.cursor.query
		self.last_query = self.cursor.query
		self.status_message = self.cursor.statusmessage
		return True

	def has_error(self):
		if(self.cursor.rowcount > 0):
			self.error = False
			return False
		else:
			self.error = True
			self.last_error = "No rows affected."
			return True
			
	def change(self, sql, parameters = None):
		if(self.query(sql, parameters) == False or self.has_error()):
			self.conn.rollback()
			return False
		self.conn.commit()
		return True
	
	def _fetch_last_inserted_id(self, table, column):
		sql = "SELECT currval('{table}_{column}_seq')".format(table=table, column=column)
		if(self.query(sql) != False):
			return self.cursor.fetchone()[0]
		return 0
	
	def insert(self, table, values, columns = None):
		if(table == ""):
			self.set_error("Table cannot be empty")
			return False
		elif(columns != None and len(columns) != len(values)):
			self.set_error("Column length is not equal to values length.")
			return False
		elif(len(values) == 0):
			self.set_error("Values can be empty")
			return False;

		value = []
		for element in values:
			value.append("%s")
		
		if(columns != None):
			sql = "INSERT INTO {table} ({columns}) VALUES ({values}) returning id;".format(table=table, columns = ",".join(columns), values=",".join(value))
		else:
			sql = "INSERT INTO {table} VALUES ({values}) returning id;".format(table, values=value.join(","))
		
		if(self.change(sql, values)):
			self.insert_id = self._fetch_last_inserted_id(table, 'id')
			print self.insert_id
			return True
		else:
			self.insert_id = 0;
			return False
		
	def update(self, table, values, columns, where = None):
		if(table == ""):
			self.set_error("Table cannot be empty")
			return False
		elif(len(columns) == 0 or len(values) == 0):
			self.set_error("Values and columns can be empty")
			return False;
		elif(len(columns) != len(values)):
			self.set_error("Column length is not equal to values length.")
			return False;
		
		value = []
		for element in values:
			value.append("%s")
			
		sql = "UPDATE {table} SET ({columns}) = ({values})".format(table=table, columns = ",".join(columns), values=",".join(value))
		
		if(where != None):
			sql = sql + " WHERE " + where
		
		sql = sql + ";"
		return self.change(sql, values)
		
	def delete(self, table, where = None):
		if(table == ""):
			self.set_error("Table cannot be empty")
			return False
		
		if(where == None):
			sql = "DELETE FROM {table};".format(table=table)
		else:
			sql = "DELETE FROM {table} WHERE {condition};".format(table=table, condition=where)
		return self.change(sql)
	
	def select(self, table, columns = ['*'], where = None, joins = [], join_columns = [], join_type = ["INNER"], limit = None):
		if(table == ""):
			self.set_error("Table cannot be empty")
			return False
		
		limited = False
		
		if(where == None):
			sql = "SELECT {column} FROM {table};".format(table=table, column= ",".join(columns))
		else:
			if(len(joins) != 0 and len(joins) != len(join_columns)):
				self.set_error("Join and column join on can have a length different.")
				return False
			elif(len(joins) != 0):
				join = ""
				default = len(join_type) == 1
					
				for index in range(len(joins)):
					if(default):
						e = join_type[0]
					else:
						e = join_type[index]
					join = join + " {join_type} JOIN {element} ON ({condition}) ".format(join_type=e, element=joins[index], condition=join_columns[index])
				sql = "SELECT {column} FROM {table} {join} WHERE {condition}".format(column = ",".join(columns), table=table, condition=where, join=join)	
			else:
				sql = "SELECT {column} FROM {table} WHERE {condition}".format(column = ",".join(columns), table=table, condition=where)
			if(isinstance( limit, ( int, long ))):
				limited = True
				sql + " LIMIT {0}".format(limit);
			sql = sql + ";"
			
		if(self.change(sql)):
			if(limit):
				return self.cursor.fetchone();
			else:
				return self.cursor.fetchall();
		return None;
	
	
	def get_var(self, table, columns = ['*'], where = None, joins = [], join_columns = [], join_type = ["INNER"]):
		return self.select(table, columns, where, joins, join_columns, join_type, 1)
			
	def get_row(self, table, where = None, joins = [], join_columns = [], join_type = ["INNER"]):
		return self.select(table, ['*'], where, joins, join_columns, join_type, 1)
				
	def get_col(self, table, column, where = None, joins = [], join_columns = [], join_type = ["INNER"]):
		columns = []
		columns.append(column)
		return self.select(table, columns, where, joins, join_columns, join_type)
	
	def get_results(self, table, where = None, joins = [], join_columns = [], join_type = ["INNER"], limit = None):
		return self.select(table, ['*'], where, joins, join_columns, join_type, limit)
		
		
	#def add_author():
	
	#def add_genre():
	
	#def add_collaborator():
	
	#def add_category():
	
	#def add_tag():
	
	#def add_category():
	#def add_category():
	#def add_category():
	#def add_category():