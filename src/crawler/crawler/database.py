import psycopg2

"""
	Class for connection and manipulation of database.
	Have methods for delete, update and insert on any table. 
	Have also methods for insert on specified table following it own logic.
"""
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
	programing_message = None
	connected = False
	
	def __init__(self, dbname, dbuser, dbpass,dbhost,dbport):
		self.dbname = dbname
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbhost = dbhost
		self.dbport = dbport	
	
	"""
		Method to set the default data on internal variables.
		Basically destroy the date on the items. 
	"""
	def flush(self):
		self.last_error = None
		self.error = False
		self.insert_id = 0
		self.rows_affected = 0
		self.last_query = None
		self.result = None
		self.last_query = None
		self.programing_message = None
		self.status_message = None
	
	"""
		Set current message error and status
	"""
	def set_error(self,msg):
		self.last_error = msg
		self.error = True 
		self.rows_affected = 0
		self.insert_id = 0
		self.status_message = "Programing error. No DB error."

	"""
		Method responsible for connect with the database.
		The connection will remain open. To close the connection use the method disconnect()
	"""
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
		
	"""
		Method to verify if the current connection is open
	"""
	def is_connected(self):
		return self.connected
		
	"""
		Method to disconnect the current connection.
		The method close the current cursor and connection
	"""
	def disconnect(self):
		self.cursor.close()
		self.conn.close()
		
	"""
		Method used to execute all queries on database.
		Please don't use this method, use the others available method instead.
	"""
	def query(self,sql, parameters = None):
		#reset programing message when a new query is run
		self.programing_message = None
		
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

	"""
		This method verify if an error occurred when the query was run.
	"""
	def has_error(self):
		if(self.cursor.rowcount > 0):
			self.error = False
			return False
		else:
			self.error = True
			self.last_error = "No rows affected."
			return True

	"""
		Method used internally to run a query.
		This method check if the query was run with success and commit the transaction.
		If was found a error the message make a roll back.
	"""
	def change(self, sql, parameters = None):
		if(self.query(sql, parameters) == False or self.has_error()):
			self.conn.rollback()
			return False
		self.conn.commit()
		return True
	
	"""
		Method used internally to fetch the last inserted id from sequence. 
		This method only work with table that have a sequence on schema.
	"""
	def _fetch_last_inserted_id(self, table, column):
		sql = "SELECT currval('{table}_{column}_seq')".format(table=table, column=column)
		if(self.query(sql) != False):
			return self.cursor.fetchone()[0]
		return 0
	
	"""
		Method used to insert data on any table on the database.
	"""
	def insert(self, table, values, columns = []):
		length_columns = len(columns)
		
		if(table == ""):
			self.set_error("Table cannot be empty")
			return False
		elif(length_columns > 0 and length_columns != len(values)):
			self.set_error("Column length is not equal to values length.")
			return False
		elif(len(values) == 0):
			self.set_error("Values can be empty")
			return False;

		value = []
		for element in values:
			value.append("%s")
		
		if(length_columns > 0):
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
		
	"""
		Method used to update the columns data on table.
	"""
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
		
	"""
		Method used to delete data from database. 
		Case Where is not provide all row of the table will be delete, be aware of that.
	"""
	def delete(self, table, where = None):
		if(table == ""):
			self.set_error("Table cannot be empty")
			return False
		
		if(where == None):
			sql = "DELETE FROM {table};".format(table=table)
		else:
			sql = "DELETE FROM {table} WHERE {condition};".format(table=table, condition=where)
		return self.change(sql)
	
	"""
		Method use to select the data from database.
		If there is no data None is returned.
	"""
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
	
	"""
		Method used to get only one row and one column from database.
		This method is projection and selection with limit 1.
	"""
	def get_var(self, table, columns = ['*'], where = None, joins = [], join_columns = [], join_type = ["INNER"]):
		return self.select(table, columns, where, joins, join_columns, join_type, 1)
		
	"""
		Method used to get only one row from database.
	"""
	def get_row(self, table, where = None, joins = [], join_columns = [], join_type = ["INNER"]):
		return self.select(table, ['*'], where, joins, join_columns, join_type, 1)
				
	"""
		Method used to get only one column from database.
		All rows within the column will be returned.
	"""
	def get_col(self, table, column, where = None, joins = [], join_columns = [], join_type = ["INNER"]):
		columns = []
		columns.append(column)
		return self.select(table, columns, where, joins, join_columns, join_type)
	
	"""
		Method used to get all the data from a database query.
	"""
	def get_results(self, table, where = None, joins = [], join_columns = [], join_type = ["INNER"], limit = None):
		return self.select(table, ['*'], where, joins, join_columns, join_type, limit)
	
	
	############################### Begin of specified methods for the crawler ################################### 
	##############################################################################################################
	
	################### Internal Methods Used by Other Methods #################### 
	
	"""
		Method used to insert a item name on a table type.
		This method can be use to insert name on the follow tables:
		hash_type, release_read_status_type, release_type, software_type, edition_type, image_edition_type, image_figure_type,
		produces_type, create_type, product_condition_type, figure_version, plataform_type, print_type, genre_type, related_type, 
		release_ownership_type, entity_type, filter_type, edition_read_status_type, function_type,condition_type, classification_type,
		collaborator_type, media_type, number_type, alias_type, mod_type, blood_type, box_condition_type, based_type, stage_developer_type,
		company_function_type, soundtrack_type, compose_type, image_soundtrack_type, lyric_type, user_filter_type
		
		If the item name already exists on database a new one will not be created and the id from the existent one will be returned instead.
		
	"""
	def add_type(self, name, type_name):
		if(name == ""):
			self.set_error("Name cannot be empty")
			return False
			
		#create name on table if there isn't none. 
		id = self.get_var(type_name + '_type', ['id'], "name = '{name}'".format(name))
		if(id == None):
			value = []
			value.append(name)
			self.insert(type_name + '_type', value, ['name'])
			id = self.insert_id
			if(id == 0):
				return False
		return id	
	
	"""
		Method use to insert a item name on a table that only have id and name as columns.
		This method can be use to insert name on the follow tables:
		shop_location, scale, material, audio_codec, ownership_status, tag, category, genre
	"""
	def add_name_to_table(self, name, table):
		if(name == ""):
			self.set_error("Name cannot be empty")
			return False
			
		#create name on table if there isnt none. 
		id = self.get_var(table, ['id'], "name = '{name}'".format(name))
		if(id == None):
			value = []
			value.append(name)
			self.insert(table, value, ['name'])
			id = self.insert_id
			if(id == 0):
				return False
		return id	
	
	"""
		Method used to insert a image to the image table.
		To insert and make a relationship between a image and an entity use the methods add_image_to_ 
	"""
	def add_image(self, url, extension, name):
		if(name == ""):
			self.set_error("Name cannot be empty")
			return False
		
		if(url == ""):
			self.set_error("Url cannot be empty")
			return False
			
		id = self.get_var('image', ['id'], "url = '{url}'".format(url))
		if(id == None):
			columns = ['url', 'extension', 'name']
			value = []
			value.append(url)
			value.append(extension)
			value.append(name)
			
			self.insert('image', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
	
	"""
		Method used to insert a relationship for images that have a certain type.
		This method can be use to insert name on the follow tables:
		entity_edition_has_image, figure_has_image, soundtrack_has_image
		
		For people_has_image table use the add_multi_relation method.
		The methods add_image_to_ already uses the appropriate relation method 
	"""
	def add_relation_image(self, relation_table, image_id, second_id, type_id):
		id = self.get_var(relation_table + "_has_image", ['image_id'], "image_id = {image_id} and {relation_table}_id = {second_id}".format(image_id, relation_table, second_id))
		if(id == None):
			columns = ['image_id', relation_table + '_id', 'image_' + relation_table + '_type_id']
			value = []
			value.append(image_id)
			value.append(second_id)
			value.append(type_id)
			
			if(self.insert(relation_table + "_has_image", value, columns) == False):
				return False
		return id
		
	"""
		Method used to insert on tables with cardinality N:M that have only the foreign keys.
		This method can be use to insert on the follow tables:
		country_has_language, soundtrack_integrate_collection, category_has_filter_type, tag_has_filter_type,audio_has_language, company_sponsors_event,
		company_owner_collection, company_has_country, people_has_image, genre_type_has_audio, entity_has_category, entity_has_tag, 
		soundtrack_for_entity_edition, entity_edition_has_language, entity_edition_has_currency, figure_from_persona, figure_has_category,
		entity_release_has_version, entity_release_has_language, figure_has_material, figure_has_shop_location, figure_has_tag, mod_has_image,
		shops_operate_on_country, people_nacionalization_on_country, entity_has_tag, entity_edition_has_subtitle, software_edition_has_version,
		software_edition_has_subtitle, genre_has_filter_type
		
		The table name to be used will be assembly by first_table + relation_type + second_table. 
		By default relation_type is equal to has, but can be overwrite.
	"""
	def add_multi_relation(self, first_id, second_id, first_table, second_table, relation_type = 'has'):
		if(first_table == "" or sencod_table == ""):
			self.set_error("Table names cannot be empty")
			return False
	
		#check if there is already a compost key with the given ids.
		if(first_table != second_table):
			another = ''
		else:
			another = 'another_'
		id = self.get_var(first_table + '_' + relation_type + '_' + second_table, [first_table + '_id'], "{first_table}_id = {first_id} and {another}{second_table}_id = {second_id}".format(first_table, first_id, another, second_table, second_id))
		if(id == None):
			if(first_table != second_table):
				columns = [first_table + '_id', second_table + '_id']
			else:
				columns = [first_table + '_id', 'another_' + second_table + '_id']
			value = []
			value.append(first_id)
			value.append(second_id)
			if(self.insert(first_table + relation_type + second_table, value, columns) == False):
				return False
		return True
		
	
	"""
		Method used to insert a N:M relationship with attribute type.
		This method can be use to insert on the follow tables:
		entity_based_entity, persona_related_persona
		
		The only table avaliable on database N:M with type are auto-relationship, but this methods can be used with
		another table with the same structure, I just didn't create any besides the already mentioned. 
		
		relation_type parameter is the middle name for the table, currenty can be 'related' or 'based'
	"""
	def add_relation_with_type(self, first_table, second_table, first_id, second_id, relation_type, relation_type_id):
		if(first_table == "" or sencod_table == ""):
			self.set_error("Table names cannot be empty")
			return False
		
		if(relation_type == ""):
			self.set_error("Relation type cannot be empty")
			return False
			
		id = self.get_var(first_table + "_" + relation_type + "_" + second_table, [first_table + '_id'], "{first_table}_id = {first_id} and another_{second_table}_id = {second_id}".format(first_table, first_id, second_table, second_id))
		if(id == None):
			columns = [first_table + '_id', 'another_' + second_table + '_id', relation_table + '_type_id']
			value = []
			value.append(first_id)
			value.append(second_id)
			value.append(relation_type_id)
			
			if(self.insert(first_table + "_" + relation_type + "_" + second_table, value, columns) == False):
				return False
		return True
			
			
	"""
		Method used to insert a number with type on the database.
		This method can be use to insert a number on the follow tables:
		number_release, number_edition 
		
		To insert multiples number to the same item use add_number_to_ methods instead this one. Volume number type must come first
		than chapter number type, add_number_to_ already handle that, also Oneshot chapter will be equals to 1 and Oneshot volume will be equal
		to 1 and have many chapters.  
		To insert a number associated with another on number_release use the method add_number_to_release instead.
		add_number_to_release also make the relationship after the insertion of number data. 
	"""
	def add_number(self, type = 'release', entity_id, entity_type_id, number_type_id, number, number_release_id = 0):
		#check if already there is this number registered on database
		if(type = 'release'):
			where = "number = {number} and number_release_id = {number_release_id} and entity_release_id = {entity_id} and number_type_id = {number_type_id} and entity_type_id = {entity_type_id}".format(number,number_release_id, entity_id, number_type_id, entity_type_id)
		else:
			where = "number = {number} and entity_edition_id = {entity_id} and number_type_id = {number_type_id} and entity_type_id = {entity_type_id}".format(number, entity_id, number_type_id, entity_type_id)
		id = self.get_var('number_' + type, ['id'], where)
		if(id == None):
			#register
			columns = ['entity_'+ type +'_id', 'number_type_id', 'entity_type_id', 'number']
			value = []
			value.append(entity_id)
			value.append(number_type_id)
			value.append(entity_type_id)
			value.append(number)
			if(launch_date != None):
				columns.append('number_release_id')
				value.append(number_release_id)
			self.insert('number_' + type, value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
	

	################### Internal Methods Used by Other Methods #################### 
	
	
	
	
	
	
	
	
	
		
		
	

	
		
	#on Mangaupdates category = tag and genre = category.
	def add_category(self, type = 'Manga', works = []):
		#check if there is already a category for type. If there inst create.

		#if there is work associated with category register.
		#if(len(work) > 0):
		
		#return category id.
		
		
	def add_tag(self, type = 'Manga'):
		#check if there is already a tag for type. If there inst create.

		#if there is work associated with tag register.
		#if(len(work) > 0):
		
		#return tag id.
	
	def add_genre(self, work = []):
		#check if there is already genre.	
		#if there is work associated with genre register.
		#if(len(work) > 0):
		#return genre id.
		
	def add_publisher():
	
	
	
	def add_derivate_work(self, work_id, another_id, type):
		#insert the derivate work on database.
		
	#def add_category():
	#def add_category():
	#def add_category():