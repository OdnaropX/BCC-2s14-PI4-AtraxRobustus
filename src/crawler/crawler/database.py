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
	
	#Used for query and database errors. Input errors is handle by exception.
	last_error = None
	error = False
	
	insert_id = 0
	rows_affected = 0
	
	last_query = None
	result = None
	status_message = None
	programing_message = None
	connected = False
		
	"""
		Set the transaction option. Set False to not commit and roll-back automatic when query is call.   
	"""
	auto_transaction = True
	
	#variable to table loaded from database
	type_alias = None
	#Default types registered
	alias_type_main = 1 #Alias Main
	alias_type_romanized = 5 #Alias Romanized Title
	alias_type_subromanized = 6 #Alias Romanized Subtitle
	
	def __init__(self, dbname, dbuser, dbpass,dbhost,dbport, load_types = True):
		self.dbname = dbname
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbhost = dbhost
		self.dbport = dbport	
		
		#Load used type from database 
		if(load_types):
			self.type_alias = self.get_results('alias_type')

	"""
		Method to set the auto transaction option status]
	"""
	def set_auto_transaction(self, auto = False):
		if(auto != False and auto != True):
			raise ValueError("Variable auto must have a boolean value. The value give was: %s" % (auto))
			
		self.auto_transaction = auto
		
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
		Method used to commit a transaction
	"""
	def commit(self):
		self.conn.commit()
		
	"""
		Method used to roll-back a transaction
	"""
	def rollback(self):
		self.conn.rollback()
	
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
			return True
		except:
			self.set_error("Database connect error")
			self.connected = False
			return False
		
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
			#error returning
			self.set_error("No SQL query to execute")
			self.last_query = ""
			return False
			
		try:
			if(parameters == None):
				self.cursor.execute(sql)
			else:
				self.cursor.execute(sql, parameters)
			
			self.last_query = self.cursor.query
			self.status_message = self.cursor.statusmessage
			return True
		except psycopg2 as e:
			print e.pgerror
			return False

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
			if(self.auto_transaction):
				self.rollback()
			return False
		if(self.auto_transaction):
			self.commit()
		return True
	
	"""
		Method used internally to fetch the last inserted id from sequence. 
		This method only work with table that have a sequence on schema.
	"""
	def _fetch_last_inserted_id(self, table, column):
		if(table == ""):
			raise ValueError("Table name cannot be empty on _fetch_last_inserted_id method.")
			
		if(column == ""):
			raise ValueError("Column name cannot be empty on _fetch_last_inserted_id method.")
			
		column = []
		column.append("currval('{table}_{column}_seq')".format(table=table, column=column))
		row = select("", column, None, [], [], ["INNER"], None, False)
		
		if(row != None):
			return row[0]
		return 0
	
	"""
		Method used to insert data on any table on the database.
	"""
	def insert(self, table, values, columns = []):
		length_columns = len(columns)
		
		if(table == ""):
			self.set_error("Table name cannot be empty")
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
		
		self.insert_id = 0;
		
		if(self.change(sql, values)):
			try:
				self.insert_id = self._fetch_last_inserted_id(table, 'id')
				print self.insert_id
			except ValueError as e:
				print "ValueError({0}): {1}".format(e.errno, e.strerror)	
			finally:
				return True
		else:
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
	def select(self, table, columns = ['*'], where = None, joins = [], join_columns = [], join_type = ["INNER"], limit = None, from_table = True):
		if(table == "" and from_table == True):
			self.set_error("Table cannot be empty")
			return False
		
		limited = False
		
		if(from_table == False):
			sql = "SELECT {column};".format(column= ",".join(columns))
		elif(where == None):
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
	

	############################## Entity Methods #################################
	
	"""
		Method used to insert a entity. This method don't insert any related item to entity like name or categories.
		This method can be use to insert on entity table.
		
	"""
	def add_entity(self, entity_type_id, classification_type_id, collection_id, language_id, country_id, launch_year, collection_started = 0):
		
		#cannot warranty uniqueness
		columns = ['entity_type_id', 'classification_type_id', 'collection_id','language_id','country_id', 'launch_year', 'collection_started']
		value = []
		value.append(entity_type_id)
		value.append(classification_type_id)
		value.append(collection_id)
		value.append(language_id)
		value.append(country_id)
		value.append(launch_year)
		value.append(collection_started)
		self.insert('entity', value, columns)
		id = self.insert_id
		if(id == 0):
			return False
		return id
	
	
	"""
		Method used to insert a description to an entity.
		This method can be use to insert on entity_description.
		
	"""
	def add_entity_description(self, entity_id, language_id, description):
		if(description == ""):
			self.set_error("Description cannot be empty")
			return False
			
		#check if already exist a description for this entity and language
		if(id == None):
			columns = ['entity_id', 'language_id', 'description']
			value = []
			value.append(entity_id)
			value.append(language_id)
			value.append(description)
			return self.insert('entity_description', value, columns)
		return id
	
	"""
		Method used to insert a wiki to an entity.
		This method can be use to insert on entity_wiki.
		
	"""
	def add_entity_wiki(self, entity_id, name, url, language_id):
		if(url == ""):
			self.set_error("Description cannot be empty")
			return False
		
		if(name == ""):
			self.set_error("Name cannot be empty")
			return False
			
		id = self.get_var('entity_wiki', ['id'], "url = '{url}'".format(url))
		
		if(id == None):
			columns = ['entity_id', 'name', 'url', 'language_id']
			value = []
			value.append(entity_id)
			value.append(name)
			value.append(url)
			value.append(language_id)
			self.insert('entity_wiki', value, columns)
			if(id == 0):
				return False
		return id
	
	"""
		Method used to insert a synopsis to an entity.
		This method can be use to insert on entity_synopse.
		
	"""
	def add_entity_synopse(self, entity_id, language_id, description):
		if(description == ""):
			self.set_error("Description cannot be empty")
			return False
		
		id = self.get_var('entity_synopse', ['entity_id'], "entity_id = {entity_id} and language_id = {language_id}".format(entity_id, language_id))
		if(id == None):
			columns = ['entity_id', 'language_id', 'content']
			value = []
			value.append(entity_id)
			value.append(language_id)
			value.append(description)
			return self.insert('entity_synopse', value, columns)
		return True

	"""
		Method used to insert a title to an entity.
		This method can be use to insert on entity_alias.
	"""
	def add_entity_alias(self, name, entity_id, language_id, title, alias_type_id):
		if(name == ""):
			self.set_error("Name cannot be empty")
			return False
			
		id = self.get_var('entity_alias', ['id'], "language_id = {language_id} and name = {name} and entity_id = {entity_id}".format(language_id, name, entity_id))
		if(id == None):
			columns = ['people_alias_type_id', 'entity_id', 'language_id', 'name']
			value = []
			value.append(alias_type_id)
			value.append(entity_id)
			value.append(language_id)
			value.append(name)
			self.insert('entity_alias', value, columns)

			id = self.insert_id
			if(id == 0):
				return False
		return id
	
	"""
		Method used to register all items related with entity.
		This method must be used instead other specified methos related with entity.
		
		To use this method the types must be already registered on database.
	"""
	def create_entity(self, romanize_title, romanize_subtitle, entity_type_id, classification_type_id, collection_id, language_id, country_id, launch_year, collection_started = 0, 
	titles	 = [], synopse = [], wiki = [], description = []):
		if(romanize_title == ""):
			self.set_error("Name cannot be empty")
			return False
		
		#set commit to false.
		
		entity_id = add_entity(entity_type_id, classification_type_id, collection_id, language_id, country_id, launch_year, collection_started)
		if(entity_id == False):
			self.set_error("A error occurred when trying to create the entity")
			return False
			
		add_entity_alias(entity_id, language_id, romanize_title,  self.alias_type_romanized)
		add_entity_alias(self, entity_id, language_id, name, self.alias_type_main)
		
		#register main name (Romanize title and Romanized Subtitle)
		
		
		
		#
		
		description = [], alias = [], synopse = [], wiki = [], categories = [], tags = [], persona = []):
		
		#add_entity()
		
		table = 'entity'
		#create entity if there is none with the given name on specified type.
		where = "entity.name = '{name}' and entity_type.name = '{entity_type}'".format(name, entity_type)
		id = self.get_var(table, ['name'], where, ['entity_type'], 'entity.entity_type_id = entity_type.id')
		
		if(id == None):
			#register the entity
			self.insert(table, [name], [name]))
			
			#register name
			
			#classification type
			
			#register the country
			
			#register the collection if the collection is mentioned, if not is registered.
			#check with full text search a collection that have the a entity with similar name
			
			#register the language
			
			#register the description
			
			
			#maybe not register the follow items with create_entity
			#register alias
			
			#register synopse
			
			#wiki
			
			#categories
			
			#tags
			
			#register persona
			
			#company
			
			add_entity_description
			
		#commit changes
		
		return id
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	########################## Edition Methods #######################
	
	def add_edition(self, edition_type_id, entity_id, title, free = 0, censored = 0, code = None, complement_code = None, release_description = None, height = None, width = None, depth = None, weight = None, event_id == None):
		id = self.get_var('entity_edition', ['id'], "".format())
		if(id == None):
			columns = ['edition_type_id', 'entity_id', 'title', 'free', 'censored']
			value = []
			value.append(edition_type_id)
			value.append(entity_id)
			value.append(title)
			value.append(free)
			value.append(censored)
			
			if(code != None):
				columns.append('code')
				value.append(code)			
			if(complement_code != None):
				columns.append('complement_code')
				value.append(complement_code)			
			if(release_description != None):
				columns.append('release_description')
				value.append(release_description)			
			if(height != None):
				columns.append('height')
				value.append(height)			
			if(width != None):
				columns.append('width')
				value.append(width)			
			if(depth != None):
				columns.append('depth')
				value.append(depth)			
			if(weight != None):
				columns.append('weight')
				value.append(weight)		
			if(event_id != None):
				columns.append('event_id')
				value.append(event_id)
			
			self.insert('entity_edition', value, columns)
			id = self.insert_id
			
			if(id == 0):
				return False
		return id
		
	def create_edition():
		self.add_edition()
		
	def add_edition_number():
		#call add_number()
		
	#insert on entity_edition_launch_country
	def add_entity_edition_launch_country(self, entity_id, country_id, launch_date, launch_price):
		id = self.get_var('entity_edition_launch_country', ['entity_edition_id'], "entity_edition_id = {entity_id} and country_id = {country_id}".format(entity_id, country_id))
		if(id == None):
			columns = ['entity_edition_id', 'country_id' , 'launch_date', 'launch_price']
			value = []
			value.append(entity_id)
			value.append(country_id)
			value.append(launch_date)
			value.append(launch_price)
			
			if(self.insert('entity_edition_launch_country', value, columns) == False):
				return False
		return True
		
	#insert software_edition
	def add_software_edition(self, entity_edition_id, plataform_type_id, software_type_id, media_type_id):
		id = self.get_var('software_edition', ['entity_edition_id'], "entity_edition_id = {entity_edition_id} and plataform_type_id = {plataform_type_id} and software_type_id = {software_type_id} and media_type_id = {media_type_id}".format(language_id, name, entity_id))
		if(id == None):
			columns = ['entity_edition_id', 'plataform_type_id', 'software_type_id', 'media_type_id']
			value = []
			value.append(entity_edition_id)
			value.append(media_type_id)
			value.append(software_type_id)
			value.append(media_type_id)
			self.insert('software_edition', value, columns)

			id = self.insert_id
			if(id == 0):
				return False
		return True
		
	def add_read_edition(self, entity_edition_id, print_type_id, pages_number, chapters_number):
		id = self.get_var('read_edition', ['id'], "entity_edition_id = {entity_edition_id}".format(entity_edition_id))
		if(id == None):
			columns = ['entity_edition_id', 'print_type_id', 'pages_number', 'chapters_number']
			value = []
			value.append(entity_edition_id)
			value.append(print_type_id)
			value.append(pages_number)
			value.append(chapters_number)

			self.insert('read_edition', value, columns)
			if(id == 0):
				return False
		return id
		
	def add_image_to_edition(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			if(add_relation_image(#) != False):
				return True
		return False
		
	
############## Release Methods ##################
	
	def add_game_release(self, entity_release_id, installation_instructions = None, emulate = 0):
		id = get_var('game_release', ['entity_release_id'], "entity_release_id = {entity_release_id}".format(entity_release_id))
		if(id == None):
			columns = ['entity_release_id']
			value = []
			value.append(entity_release_id)
			if(emulate != 0):
				columns.append('emulate')
				value.append(emulate)
			if(installation_instructions != None):
				columns.append('installation_instructions')
				value.append(installation_instructions)
			return self.insert('game_release', value,columns)
		return id
		
	def add_release(self, entity_id, release_type_id, country_id, entity_edition_id, release_date = None, description = None):
		id = self.get_var('entity_release', ['id'], "entity_id = {entity_id} and release_type_id = {release_type_id} and entity_edition_id = {entity_edition_id} and country_id = {country_id}".format(entity_id, release_type_id, entity_edition_id, country_id))
		if(id == None):
			columns = ['entity_id','release_type_id','country_id','entity_edition_id','description','release_date']
			value = []
			value.append(entity_id)
			value.append(release_type_id)
			value.append(country_id)
			value.append(entity_edition_id)
			if(description != None):
				columns.append('description')
				value.append(description)
			if(release_date != None):
				columns.append('release_date')
				value.append(release_date) 
				
			self.insert('entity_release', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
	
	def create_release():
		#check if there is a series where this release is from, check table entity and alias to find the series name. If not exists create the series.
		
		#get the id from series, from series table or alias table.
		
		#normalize release number to be insert on database, release number can be e.g. 'c.53', 'v2.9', 'v1 c.1-4','v1-2', 'v.1 c.14', 'Oneshot', 'v.1 c.Interlude 2-3', 'c.Parts 1-2'
		
		#insert release
		
		#insert release number
		
	#insert mods
	def add_mod(self, name, type_id, entity_release_id, author_name, launch_date = None, description = None, installation_instruction = None):
		#check if entity_release exists
		id = self.get_var('entity_release', ['id'], "id = {entity_release_id}".format(entity_release_id))
		if(id == None)
			self.programing_message = "Error on insert mod, entity_release dont exists."
			return False
		#check if already is a mod with the same name
		id = self.get_var('mod', ['id'], "entity_release_id = {entity_release_id} and name= '{name}' ".format(entity_release_id, name)
		if(id == None):
			columns = ['entity_release_id', 'mod_type_id', 'name', 'author']
			value = []
			value.append(entity_release_id)
			value.append(type_id)
			value.append(name)
			value.append(author_name)
			if(launch_date != None):
				columns.append('launch_date')
				value.append(launch_date)
			if(description != None):
				columns.append('description')
				value.append(description)
			if(installation_instruction != None):
				columns.append('installation_instruction')
				value.append(installation_instruction)
			
			self.insert('mod', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	def add_release_number():
		#call add_number()
		
	def add_image_to_release(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
	
############ Persona methods ##################
	
	#insert persona table related data
	#used on persona_occupation, persona_associated_name, persona_unusual_features, persona_affiliation, persona_race
	def add_persona_items(self, name, persona_id, item_table):
		id = get_var('persona_' + item_table, ['id'], "name = '{name}' and persona_id = {persona_id}".format(name, persona_id))
		if(id == None):
			columns = ['persona_id', 'name']
			value = []
			value.append(persona_id)
			value.append(name)

			self.insert('persona_' + item_table, value, columns)
			if(id == 0):
				return False
		return id
	
	def create_persona(self, unusual_features = [], associated_name = [], occupation = [], affiliation = [], race = [], figure = [], voices_actor = []):
		self.add_persona()
		
		#add voices
		
		#add entity
		
		#add relationship with another persona
		
		#add_relation_people_voice_persona
	
		#add affiliation
		
		#persona alias (associated names)
		
		
	
	def add_persona(self, name, entity_id, gender, first_appear_on = None, birthday = None, blood_type_id == None, height = None, weight = None, eyes_color = None, hair_color = None):
		id = self.get_var('persona', ['id'], "entity_id = {entity_id} and name = {name} and gender = {gender}".format(entity_id, name, gender))
		if(id == None):
			columns = ['name', 'gender', 'entity_id']
			value = []
			value.append(name)
			value.append(gender)
			value.append(entity_id)
			
			if(first_appear_on != None):
				columns.append('first_appear_on')
				value.appendfirst_appear_on
			if(blood_type_id != None):
				columns.append('blood_type_id')
				value.append(blood_type_id)
			if(birthday != None):
				columns.append('birthday')
				value.append(birthday)
			if(height != None):
				columns.append('height')
				value.append(height)
			if(weight != None):
				columns.append('weight')
				value.append(weight)
			if(eyes_color != None):
				columns.append('eyes_color')
				value.append(eyes_color)
			if(hair_color != None):
				columns.append('hair_color')
				value.append(hair_color)
			
			self.insert('persona', value,columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	def add_image_to_persona(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
			
################# Company Methods ########################
	
	def add_company(slef, name, country_origin_id, description = None, social_name = None, start_year = None, website = None, foundation_date = None):
		id = self.get_var('company', ['id'], "name = {name} and country_id = {country_origin_id}".format(name, country_origin_id))
		if(id == None):
			columns = ['country_id','name']
			value = []
			value.append(country_id)
			value.append(name)
			
			if(description != None):
				columns.append('description')
				value.append(description)
			if(social_name != None):
				columns.append('social_name')
				value.append(social_name)
			if(start_year != None):
				columns.append('start_year')
				value.append(start_year)
			if(website != None):
				columns.append('website')
				value.append(website)
			if(foundation_date != None):
				columns.append('foundation_date')
				value.append(foundation_date)
				
			return self.insert('company', value, columns)
		return True
	
	def create_company(self, events_sponsored = [], owned_collections = [], countries = [], social = [], editions = [], entities = [], comments = []):
	
	
	#insert relation of company
	#used for tables: entity_edition_has_company, entity_has_company
	def add_relation_company(self, company_id, second_id, company_function_type_id, relation_table):
		id = self.get_var(relation_table + '_has_company', ['company_id'], "company_id = {company_id} and {relation_table}_id = {second_id} and company_function_type_id = {company_function_type_id}".format(people_id, relation_table, second_id, relation_type, company_function_type_id))
		if(id == None):
			columns = ['company_id', relation_table + '_id', 'company_function_type_id']
			value = []
			value.append(company_id)
			value.append(second_id)
			value.append(company_function_type_id)

			self.insert(relation_table + '_has_company', value, columns)
	
			#there inst id, how to check if worked?
			
			id = self.insert_id
			if():
				return False
		return True
		
	def add_image_to_company(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
			
################ People Methods #########################
	
	#need to commit only after all was successful
	def create_people(self, name, country, blood_type, website, decription, alias = []):
		#add_people
		
		#add_people_alias
	
		#add_relation_people
		
		#add_relation_people_voice_persona
		
		
		
		
		#need to made a unique field to identify person with same name.
		
		#check if there is already a people, check know alias from alias table. If there inst create.
		
		#register social network url from author.
		
		#if there is work associated register the author work.
		
		#return author id.	
		
	def add_people(self, country_id, blood_type_id = None, website = None, description = None):
		#cannot check uniqueness
		columns = ['country_id']
		value = []
		value.append(country_id)
		
		if(blood_type_id != None):
			columns.append('blood_type_id')
			value.append(blood_type_id)
			
		if(website != None):
			columns.append('website')
			value.append('website')
			
		if(description != None):
			columns.append('description')
			value.append(description)
			
		self.insert('people', value, columns)
		id = self.insert_id
		if(id == 0):
			return False
		return id
	
	
	#insert relation of people.
	#used for tables: people_create_figure, people_produces_entity, people_compose_audio
	def add_relation_people(self, people_id, people_alias_used_id, second_id, relation_table, relation_type_id, relation_type = 'produces'):
		#check if already is a relation with the people_id, second_id and relation_type_id.
		id = self.get_var('people_' + relation_type + '_' + relation_table, ['people_id'], "people_id = {people_id} and {relation_table}_id = {second_id} and {relation_type}_type_id = {relation_type_id}".format(people_id, relation_table, second_id, relation_type, relation_type_id))
		if(id == None):
			columns = ['people_id', relation_table + '_id', 'people_alias_id', relation_type + '_type_id']
			value = []
			value.append(people_id)
			value.append(second_id)
			value.append(people_alias_used_id)
			value.append(relation_type_id)
			self.insert('users', value, columns)
			
			#there inst id, how to check if worked?
			
			id = self.insert_id
			if():
				return False
		return True
		
	def add_people_alias(self, alias_type_id, people_id, name, lastname):
		id = self.get_var('people_alias', ['id'], "name = '{name}' and lastname = '{lastname}' and people_id = {people_id}".format(name, lastname, people_id))
		if(id == None):
			columns = ['name', 'alias_type_id', 'people_id', 'lastname']
			value = []
			value.append(name)
			value.append(alias_type_id)
			value.append(people_id)
			value.append(lastname)
			self.insert('people_alias', value, columns)
			id = insert_id
			if(id == 0)
				return False
		return id
	
	def add_relation_people_voice_persona(self, people_id, persona_id, language_id, entity_id, entity_edition_id, observation = None):
		id = self.get_var('people_voice_persona', ['persona_id'], " persona_id = {persona_id} and people_id = {people_id} and language_id = {language_id}".format(persona_id, people_id, language_id)) 
		if(id == None):
			columns = ['persona_id','people_id','language_id','entity_id','entity_edition_id']
			value = []
			value.append(persona_id)
			value.append(people_id)
			value.append(language_id)
			value.append(entity_id)
			value.append(entity_edition_id)
			
			if(observation != None):
				columns.append('observation')
				value.append(observation)
				
			return self.insert('people_voice_persona', value, columns)
		return True
		
	def add_image_to_people(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
			
	############# Archive Methods ###############
	
	def add_requirements(self, version_id, video_board, processor, memory, hd_storage):
		id = self.get_var('requirements', ['id'], "version_id = '{version_id}'".format(version_id))
		if(id == None):
			columns = ['version_id', 'video_board', 'processor', 'memory', 'hd_storage']
			value = []
			value.append(version_id)
			value.append(video_board)
			value.append(processor)
			value.append(memory)
			value.append(hd_storage)
			self.insert('requirements', value, columns)
			id = insert_id
			if(id == 0):
				return False
		return id
	
	#requirements have driver.
	def add_driver(self, requirements_id, name, url_download):
		id = self.get_var('driver', ['id'], "name = '{name}'".format(name))
		if(id == None):
			columns = ['name', 'requirements_id', 'url_download']
			value = []
			value.append(name)
			value.append(requirements_id)
			value.append(url_download)
			self.insert('driver', value, columns)
			id = insert_id
			if(id == 0):
				return False
		return id
	
	def add_archive(self, name, version_id, url, size, extension):
		id = self.get_var('archive', ['id'], "name = '{name}' and url = '{url}'".format(name, url))
		if(id == None):
			columns = ['name', 'version_id', 'url', 'size', 'extension']
			value = []
			value.append(name)
			value.append(version_id)
			value.append(url)
			value.append(size)
			value.append(extension)
			self.insert('archive', value, columns)
			id = insert_id
			if(id == 0):
				return False
		return id
	
	def add_hash(self, hash_type_id, archive_id, code):
		id = self.get_var('hash', ['id'], "archive_id = '{archive_id}' and hash_type_id = {hash_type_id}".format(archive_id, hash_type_id))
		if(id == None):
			columns = ['hash_type_id', 'archive_id', 'code']
			value = []
			value.append(hash_type_id)
			value.append(archive_id)
			value.append(code)
			self.insert('hash', value, columns)
			id = insert_id
			if(id == 0):
				return False
		return id
	
	def add_entity_release_version(self, entity_id, stage_developer_type_id, number, changelog):
		id = self.add_version(self, stage_developer_type_id, number, changelog = None)
		if(id != False):
			if(self.add_multi_relation(self, entity_id, id, 'entity_release', 'version') == False):
				self.delete('version', "id = {id}".format(id))
				return False
			return True
		return False
			
	def add_software_edition_version(self, entity_id, stage_developer_type_id, number, changelog):
		id = self.add_version(self, stage_developer_type_id, number, changelog = None)
		if(id != False):
			if(self.add_multi_relation(self, entity_id, id, 'software_edition', 'version') == False):
				self.delete('version', "id = {id}".format(id))
				return False
			return True
		return False
	
	def add_version(self, stage_developer_type_id, number, changelog = None):
		#check the table of relationship version_entity
		columns = ['stage_developer_type_id', 'number']
		value = []
		value.append(stage_developer_type_id)
		value.append(number)
			
		if(changelog != None):
			columns.append('changelog')
			value.append(changelog)
			
		self.insert('version', value, columns)
		id = insert_id
		if(id == 0):
			return False		
		return id
		
##################### Collection Methods #########################3
	#Add to collection table
	def add_collection(self, name, description = None, owner_id = 0, soundtracks_id = []):
		id = self.get_var('collection', ['id'], "name = '{name}'".format(name))
		if(id == None):
			columns = ['name']
			value = []
			value.append(name)
			if(description != None):
				columns.append('description')
				value.append(description)
				
			self.insert('collection', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
	
		not_fail = True
			
		for soundtrack_id in soundtracks_id:
			#check if already is a soundtrack associated with this collection
			sound_id = self.get_var('soundtrack_integrate_collection', ['soundtrack_id'], "soundtrack_id = {soundtrack_id} and collection_id = {collection_id}".format(soundtrack_id, collection_id = id))
			if(sound_id == None):
				not_fail = not_fail and add_multi_relation(id, soundtrack_id, 'soundtrack', 'collection', 'integrate')
			
		if(not_fail == False):
			failed_message = "Error on save some item to multi_relation."
			
		if(owner_id != 0):
			#add company_owner_collection
			if(add_multi_relation(owner_id, id, 'company', 'collection', 'owner') == False):
				failed_message = failed_message + " Error on company_owner_collection insertion."
					
		self.programing_message = failed_message 
			
		return id
	
	
	################### User Methods ####################3
	#insert on user table
	def add_user(self, username, password, gender, location, birthday, signup_date = None, activated = 1, emails = []):
		id = self.get_var('users', ['id'], "username = '{username}'".format(username))
		if(id == None):
			columns = ['username', 'pass', 'gender','location', 'birthday']
			value = []
			value.append(username)
			value.append(password)
			value.append(gender)
			value.append(location)
			value.append(birthday)
			
			if(signup_date != None):
				columns.append('signup_date')
				value.append(signup_date)
			if(activated != 1):
				columns.append('activated')
				value.append(0)
			self.insert('users', value, columns)
			id = self.insert_id
			if(id == 0):
				self.programing_message = "Error on user insertion"
				return False
		#Register emails
		not_fail = True
		for email in emails:
			not_fail = not_fail and add_user_email(id, email)
		
		if(not_fail == False):
			self.programing_message = "Error on emails insertion"
			
		return id
	
	def add_user_email(self, user_id, email):
		id = self.get_var('user_email', ['email'], "email = '{email}'".format(email))
		if(id == None):
			columns = ['users_id', 'email']
			value = []
			value.append(user_id)
			value.append(email)
			self.insert('users', value, columns)
			#there inst id, how to check if worked?
			
			return self.insert_id('user_email', value, columns)
		return True

	def add_user_filter(self, name, user_id, type_id):
		id = get_var('user_filter', ['id'], "users_id = {user_id} and name = {name} and user_filter_type_id = {type_id}".format(user_id, name, type_id))
		if(id == None):
			columns = ['name','users_id','user_filter_type_id']
			value = []
			value.append(name)
			value.append(user_id)
			value.append(type_id)
			
			self.insert('user_filter', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	def add_element_to_user_filter(self, filter_id, attribute_id, attribute = 'tag'):
		id = self.get_var(attribute + '_user_filter', ['user_filter_id'], "user_filter_id = {user_filter_id} and {attribute}_id = {attribute_id}")
		if(id == None):
			columns = ['user_filter_id',attribute +'_id']
			value = []
			value.append(filter_id)
			value.append(attribute_id)
			
			return self.insert(attribute + '_user_filter', value, columns)
		return True
	
	#only commit after all is run successful.
	def create_user_filter(self, name, user_id, type_id, elements = [], attribute = 'tag'):
		id = add_user_filter(name, user_id, type_id)
		
		not_fail = True
		for element in elements:
			not_fail = not_fail and add_element_to_user_filter(id, element, attribute)
		if(not_fail == False)
			self.programing_message = "Error associating some element to user filter"
		return id
	
	def add_comment(self, title, content, user_id, entity_id, type = 'release'):
		#dont need to check if already exists.
		columns = [type + '_id', 'users_id', 'content', 'title']
		value = []
		value.append(entity_id)
		value.append(user_id)
		value.append(content)
		value.append(title)
		self.insert(type + '_comments', value, columns)
		id = self.insert_id
		if(id == 0):
			return False
		return True
		
	def add_image_to_user(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
		
###################### Audio Methods ##########################
	
	#insert audio 
	def add_audio(self, country_id, audio_codec_id, name, duration, bitrate, soundtracks = [], audio_exclusive = []):
		id = get_var('audio', ['id'], "name = {name} and country_id = {country_id}".format(name, country_id))
		if(id == None):
			columns = ['country_id', 'audio_codec_id', 'name','duration','bitrate']
			value = []
			value.append(country_id)
			value.append(audio_codec_id)
			value.append(name)
			value.append(duration)
			value.append(bitrate)
			self.insert('audio', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		
		length_soundtrack = len(soundtracks)
		if(length_soundtrack == len(audio_exclusive)):
			not_fail = True		
			for index in range(length_soundtrack):
				not_fail = not_fail and add_relation_soundtrack_audio(id, soundtrack_id[index], audio_exclusive[index])
			
			if(not_fail == False)
				self.programing_message = "Error on associating some audio to soundtrack"
		return id
	
	#insert relationship between soundtrack and audio
	def add_relation_soundtrack_audio(self, audio_id, soundtrack_id, exclusive):
		id = get_var('soundtrack_has_audio', ['audio_id'], "audio_id = {audio_id} and soundtrack_id = {soundtrack_id}".format(audio_id, soundtrack_id))
		if(id == None):
			columns = ['soundtrack_id','audio_id','exclusive']
			value = []
			value.append(soundtrack_id)
			value.append(audio_id)
			value.append(exclusive)
			if(self.insert('audio', value, columns) == False):
				return False
		return True
			
	#insert lyrics
	def add_lyric(self, type_id, audio_id, language_id, title, content, user_id = None):
		if(user_id != None):
			where = "audio_id = {audio_id} and language_id = {language_id} and user_id = {user_id} and title = {title} and lyric_type_id = {lyric_type_id}".format(audio_id,language_id,user_id,title,lyric_type_id)
		else
			where = "audio_id = {audio_id} and language_id = {language_id} and title = {title} and lyric_type_id = {lyric_type_id}".format(audio_id,language_id,title,lyric_type_id)
		id = get_var('lyrics', ['id'], where)
		if(id == None):
			columns = ['lyric_type_id', 'audio_id' ,'language_id', 'title', 'lyric']
			value = []
			value.append(lyric_type_id)
			value.append(audio_id)
			value.append(language_id)
			value.append(title)
			value.append(lyric)
			
			if(user_id != None):
				columns.append('user_id')
				value.append(user_id)
			
			self.insert('lyrics', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
	
	#insert soundtrack
	def add_soundtrack(self, name, type_id, launch_year, audios_id = [], audios_exclusive[]):
		id = get_var('soundtrack', ['id'], "soundtrack_type_id = {type_id} and name = {name} and launch_year = {launch_year}".format(type_id,name,launch_year))
		if(id == None):
			columns = ['soundtrack_type_id', 'name' ,'launch_year']
			value = []
			value.append(type_id)
			value.append(name)
			value.append(launch_year)

			self.insert('soundtrack', value, columns)
			if(id == 0):
				return False
				
		#register audios
		lenght_audios = len(audios_id)
		if(lenght_audios == len(audios_exclusive)):
			not_fail = True		
			for index in range(lenght_audios):
				not_fail = not_fail and add_relation_soundtrack_audio(id, audios_id[index], audios_exclusive[index])
			
			if(not_fail == False):
				self.programing_message = "Error on audio insertion on add_soundtrack."
		return id
	
	def add_image_to_audio(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
	
	def add_image_to_soundtrack(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
			
	############# Figure Methods ###############
	
	def create_figure(self, alias = [], ):
		#same items as create_entity
		self.create_entity()
		
		#register figure shop
		
		#register scale
		
		#register country
		
		#register currency
		
		#figure version
		
		#register entity_id
		
		#figure persona
		
		#company
		
		#shop location (local de compra)
		
		#material
		#currency
		#country
		
		#figure images
		#category
		#tags
		
		#relacionar entity is there is none create.
		
		
		
	#this is specialization from entity
	def add_figure(self,entity_id, figure_version_id, currency_id, scale_id, country_id, height, launch_price, release_date, width = None, weight = None, observation = None):
		id = self.get_var('figure', ['id'], "entity_id = {entity_id}".format(entity_id))
		if(id == None):
			columns = ['entity_id', 'figure_version_id', 'currency_id', 'scale_id','country_id','height','launch_price','release_date']
			value = []
			value.append(entity_id)
			value.append(figure_version_id)
			value.append(currency_id)
			value.append(scale_id)
			value.append(country_id)
			value.append(height)
			value.append(launch_price)
			value.append(release_date)
			if(width != None):
				columns.append('width')
				value.append(width)
			if(weight != None):
				columns.append('weight')
				value.append(weight)
			if(observation != None):
				columns.append('observation')
				value.append(observation)
			
			self.insert("figure", value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	
	#used on table: figure_has_shops
	def add_figure_relation_shops(self, figure_id, shops_id, product_url):
		#if already is registered on database update the checked_last
		id = self.get_var("figure_has_shops", ['social_id'], "figure_id = {figure_id} and shops_id = {shops_id}".format(figure_id, shops_id, second_id))
		if(id == None):
			columns = ['figure_id', 'shops_id', 'product_url']
			value = []
			value.append(figure_id)
			value.append(shops_id)
			value.append(product_url)
			
			return self.insert("figure_has_shops", value, columns)
		#else update last checked.
		else:
			checked_last DATETIME NOT NULL DEFAULT now(),
	
		#insert shops
	def add_shops(self, url, name):
		id = self.get_var('shops', ['id'], "url = '{url}'".format(url))
		if(id == None):
			columns = ['url', 'name']
			value = []
			value.append(url)
			value.append(name)
			
			self.insert('shops', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
	
		#insert event
	def add_event(self, name, edition,location, website, date, duration, free = 1):
		id = get_var('event', ['id'], "name = {name} and edition = {edition}".format(name, edition))
		if(id == None):
			columns = ['name', 'edition', 'location', 'website', 'date', 'duration', 'free']
			value = []
			value.append(name)
			value.append(edition)
			value.append(location)
			value.append(website)
			value.append(date)
			value.append(duration)
			value.append(free)
			self.insert('event', value, columns)
			id = self.insert_id
			if(id == 0)
				return False
		return id
		
	def add_image_to_figure(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
			
	####### Collaborator methods ##############
	
	def add_collaborator(self, website = None, works = []):
		
	#insert collaborator
	def add_collaborator(name, description, irc = None, websites = [], members_id = [])
		#check if there is already a collaborator with the same name. Check if country is the same, if not create a new collaborator with same name but different country. 
		#put the country name on collaborator name to maintain unique?
		id = self.get_var('collaborator', ['id'], "name = '{name}'".format(code))
		if(id == None):
			columns = ['name', 'description']
			value = []
			value.append(name)
			value.append(description)
			if(irc != None):
				columns.append('irc')
				value.append(irc)
			
			self.insert('collaborator', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		
		#Add members to collaborator if provided.
		not_fail = true;
		failed_message = ""
		for member_id in members_id:
			not_fail = not_fail and add_multi_relation(id, member_id, 'collaborator', 'collaborator_member')
		
		if(not_fail == False):
			failed_message = "Failed to add some collaborator_member. "
			
		#Add collaborator website if provided.
			
		#check if there is website. If not exists get from social network (if possible). Use status on website.
		#if(website != None):

		#register social network.
		
		#if there is work obtained register the collaborator work.
		#if(len(work) > 0):
		
		self.programing_message = failed_message	
		return id
	
	#insert on collaborator_member, this only add a new member, to add and associate a member to a collaborator use add_collaborator_member.
	def add_member(self, name, active = 1):
		id = self.get_var('collaborator_member', ['id'], "name = '{name}'".format(code))
		if(id == None):
			columns = ['name', 'active']
			value = []
			value.append(name)
			value.append(active)
			
			self.insert('collaborator_member', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
	
	def add_collaborator_member(self, collaborator_id, name, active = 1, founder = 0):
		id = add_member(self, name, active)
		if(id == False):
			return False
		
			if(add_relation_collaborator_member(collaborator_id, id, founder) == False):
			self.programing_message = "Error on save collaborator member on collaborator_has_collaborator_member"
		return id
	
	#used for insert on table: collaborator_has_collaborator_member
	def add_relation_collaborator_member(self, collaborator_id, member_id, founder = 0):
		id = self.get_var('collaborator_has_collaborator_member', ['collaborator_id'], "collaborator_id = {collaborator_id} and collaborator_member_id = {member_id}".format(collaborator_id, member_id))
		if(id == None):
			columns = ['collaborator_id', 'collaborator_member_id', 'founder']
			value = []
			value.append(collaborator_id)
			value.append(member_id)
			value.append(founder)
			return self.insert('collaborator_has_collaborator_member', value, columns)
		return True
	
	#used on table: collaborator_provides_release, collaborator_member_produces_entity_release
	def add_relation_collaborator_release(self, collaborator_id, release_id, function_type_id, first_table, second_table, relation = 'provices'):
		id = self.get_var(first_table + '_' + relation + '_' + second_table, ['collaborator_id'], "collaborator_id = {collaborator_id} and entity_release_id = {release_id}".format(collaborator_id, release_id))
		if(id != None):
			columns = ['collaborator_id', 'entity_release_id', first_table + '_type_id']
			value = []
			value.append(collaborator_id)
			value.append(release_id)
			value.append(function_type_id)
			return self.insert(first_table + '_' + relation + '_' + second_table, value, columns);
		return True
	
	def add_collaborator_website(self, collaborator_id, website):
		id = self.get_var('collaborator_website', ['collaborator_id'], "collaborator_id = {collaborator_id} and website = '{website}'".format(collaborator_id, website))
		if(id == None):
			columns = ['collaborator_id', 'website']
			value = []
			value.append(collaborator_id)
			value.append(website)
			return self.insert('collaborator_has_collaborator_member', value, columns)
		return True
		
	def add_image_to_collaborator(self, url, extension, name, edition_id):
		image_id = add_image(url, extension, name):
		if(image_id != False):
			#add relationship
			
			#not add_relation_image
			
############# Social Methods ##################
	
	#insert on social_type table
	def add_social_type(self, name, website, website_secure = None):
		#insert on table if there isnt the name on table . 
		id = self.get_var('social_type', ['id'], "name = '{name}'".format(name))
		if(id == None):
			columns = ['name', 'website']
			value = []
			value.append(name)
			value.append(website)
			if(website_secure != None):
				columns.append(website_secure)
				value.append(website_secure)
			
			self.insert(table, value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id	
	
	#insert socials relationship.
	#can be used for the follow tables: users_has_social, people_has_social, collaborator_has_social, company_has_social
	def add_relation_social(self, relation_table, social_id, second_id, last_checked):
		id = self.get_var(relation_table + "_has_social", ['social_id'], "social_id = {social_id} and {relation_table}_id = {second_id}".format(social_id, relation_table, second_id))
		if(id == None):
			columns = ['social_id', relation_table + '_id']
			value = []
			value.append(social_id)
			value.append(second_id)
			
			self.insert(relation_table + "_has_social", value, columns)
			id = self.insert_id
		#else update last checked.
		else:
			
			
		return id
	
	#insert social
	def add_social(self, social_type_id, url):
		id = self.get_var('social', ['id'], "url = '{url}'".format(url))
		if(id == None):
			columns = ['social_type_id', 'url']
			value = []
			value.append(social_type_id)
			value.append(url)
			self.insert(relation_table + "_has_social", value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
		
############################### Localization Methods ###############################

#insert new country or new language
	def add_localization(self, name, code, type = 'country'):
		if(type != 'country'):
			type = 'language'
		id = self.get_var(type, ['id'], "name = '{name}'".format(name))
		if(id == None):
			columns = ['name', 'code']
			value = []
			value.append(name)
			value.append(code)
			
			self.insert(type, value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	#table used: country_has_currency
	def add_relation_country_currency(self, country_id, currency_id, main_currency = 1):
		id = self.get_var('country_has_currency', ['currency_id'], "currency_id = {currency_id} and country_id = {country_id}".format(currency_id, country_id))
		
		if(id == None):
			columns = ['currency_id','country_id','main']
			value = []
			value.append(currency_id)
			value.append(country_id)
			value.append(main_currency)
			
			if(self.insert('country_has_currency', value, columns) == False):
				return False
		return True
	
	#insert currency
	def add_currency(self, name, symbol, code):
		id = self.get_var('currency', ['id'], "code = '{code}'".format(code))
		if(id == None):
			columns = ['name', 'symbol', 'code']
			value = []
			value.append(name)
			value.append(symbol)
			value.append(code)
			
			self.insert('currency', value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	####################### Lists Methods ########################
	
	#insert user lists
	#used on tables: lists_edition, lists_release, lists_figure
	def add_list(self, name, user_id, type = 'edition', entity_type_id = 0):
		#check if already is a lists with this name
		if(type == 'figure'):
			where =  "user_id = {user_id} and name = {name}".format(user_id,name)
		else:
			where =  "user_id = {user_id} and name = {name} and entity_type_id = {entity_type_id}".format(user_id,name, entity_type_id)
			
		id = self.get_var('lists_' + type, ['id'], where)
		if(id == None):
			columns = ['user_id', 'name']
			value = []
			value.append(user_id)
			value.append(name)
			if(type != 'figure'):
				columns.append('entity_type_id')
				value.append(entity_type_id)
			self.insert('lists_' + type, value, columns)
			id = self.insert_id
			
			if(id == 0):
				return False
		return id
	
	#lists_release_list_entity_release
	def add_release_to_list(list_id, entity_id, read_status_type_id, ownership_type_id, local_storage = None):
		id = self.get_var('lists_release', ['id'], "id = {list_id}".format(list_id))
		if(id != None):
			id = self.get_var('lists_release_list_entity_release', ['lists_release_id'], "lists_release_id = {id} and entity_release_id = {entity_id}")
			if(id == None):
				columns = ['lists_release_id', 'entity_release_id', 'release_edition_read_status_type_id', 'release_ownership_type_id', 'local_storage']
				value = []
				value.append(list_id)
				value.append(entity_id)
				value.append(read_status_type_id)
				value.append(ownership_type_id)
				if(local_storage != None):
					columns.append('local_storage')
					value.append(local_storage)
				return self.insert('lists_release_list_entity_release', value, columns)
			return True
		return False
  
	#lists_figure_list_figure
	def add_figure_to_list(list_id, figure_id, ownership_status_id, box_condition_type_id, product_condition_type_id, observation = None):
		id = self.get_var('lists_figure', ['id'], "id = {list_id}".format(list_id))
		if(id != None):
			id = self.get_var('lists_figure_list_figure', ['lists_release_id'], "lists_release_id = {id} and entity_release_id = {entity_id}")
			if(id == None):
				columns = ['lists_figure_id', 'figure_id', 'ownership_status_id', 'box_condition_type_id', 'product_condition_type_id']
				value = []
				value.append(list_id)
				value.append(entity_id)
				value.append(ownership_status_id)
				value.append(box_condition_type_id)
				value.append(product_condition_type_id)
				if(observation != None):
					columns.append('observation')
					value.append(observation)
				return self.insert('lists_figure_list_figure', value, columns)
			return True
		return False
  
	#lists_edition_list_entity_edition
	def add_edition_to_list(list_id, entity_id, read_status_type_id, ownership_status_id, condition_type_id, edition_read_status_type_id, observation = None):
		id = self.get_var('lists_edition', ['id'], "id = {list_id}".format(list_id))
		if(id != None):
			id = self.get_var('lists_edition_list_entity_edition', ['lists_release_id'], "lists_release_id = {id} and entity_release_id = {entity_id}")
			if(id == None):
				columns = ['lists_edition_id', 'entity_edition_id', 'ownership_status_id', 'condition_type_id', 'edition_read_status_type_id']
				value = []
				value.append(list_id)
				value.append(entity_id)
				value.append(ownership_status_id)
				value.append(condition_type_id)
				value.append(edition_read_status_type_id)
				if(observation != None):
					columns.append('observation')
					value.append(observation)
				return self.insert('lists_edition_list_entity_edition', value, columns)
			return True
		return False

	
	
		
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