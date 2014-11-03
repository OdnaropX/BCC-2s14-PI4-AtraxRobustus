import psycopg2
import warnings
import types
import collections
import urlparse
import re
import sys
import util

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
	connected = False
		
	"""
		Set the transaction option. Set False to not commit and roll-back automatic when query is call.   
	"""
	auto_transaction = True
	"""
		Set the amount of times that the auto_transaction was called.
	"""
	auto_transaction_call = 0
	
	
	#variable to table loaded from database
	type_alias = None
	#Default types registered
	alias_type_main = 1 #Alias Main
	alias_type_alias = 2 #Alias Alias
	alias_type_nickname = 3 #Alias Nickname
	alias_type_nativename = 4
	alias_type_title = 5
	alias_type_subtitle = 6
	alias_type_romanized = 7 #Alias Romanized Title
	alias_type_subromanized = 8 #Alias Romanized Subtitle
	
	entity_type_manga = 3
	entity_type_lightnovel = 9
	
	based_type_doujin = 1
	based_type_sequel_spinoff = 2
	based_type_adapted_from = 5
	
	#Default image types registered
	image_user_type_profile = 1
	
	classification_type_12 = 11
	classification_type_18 = 17
	
	country_us = 236
	country_jp = 112
	country_kr = 211
	country_cn = 47
	
	language_ja = 74
	language_en = 42
	language_ko = 87
	language_zh = 31
	
	entity_type_manga = 3
	entity_type_manhaw = 4
	entity_type_manhua = 5
	entity_type_webtoon = 6
	entity_type_lightnovel = 9
	entity_type_webnovel = 10
	
	company_function_type_publisher = 1
	company_function_type_translator = 1
	
	collaborator_function_type_scanlator = 1
	collaborator_function_type_fansub = 2
	
	people_relation_type_writer = 2 #author 
	people_relation_type_illustrator = 1 #artist
 
	release_type_chapter = 3
	release_type_volume = 4
	
	pattern_remove_function = re.compile(ur'[a-zA-Z ]{1,}\(.*\)')
	
	def __init__(self, dbname, dbuser, dbpass,dbhost,dbport, load_types = True):
		self.dbname = dbname
		self.dbuser = dbuser
		self.dbpass = dbpass
		self.dbhost = dbhost
		self.dbport = dbport	
		
		#Load used type from database 
		#if(load_types):
		#	self.type_alias = self.get_results('alias_type')

	"""
		Method to set the auto transaction option status
	"""
	def set_auto_transaction(self, auto):
		if(self.auto_transaction_call == 0):
			if(auto == True):
				self.auto_transaction = True
			else:
				self.auto_transaction = False
			
		if(auto == False):
			self.auto_transaction_call += 1 
		else:
			self.auto_transaction_call -= 1

		if(self.auto_transaction_call < 0 ):
			warnings.warn("Warning: auto_transaction_call is less than 0. You must have called set_auto_transaction(True) more than set_auto_transaction(False) and on your code. You must call the same amount to both.")
			
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
		Method used to commit a transaction.
		The transaction will only be committed when was called on first runtime stack.
	"""
	def commit(self):
		if(self.auto_transaction_call < 2):
			self.conn.commit()
		
	"""
		Method used to roll-back a transaction
		The transaction will only be roll-back when was called on first runtime stack.
	"""
	def rollback(self):
		if(self.auto_transaction_call < 2):
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
		if(not sql):
			#error returning
			self.set_error("No SQL query to execute")
			self.last_query = ""
			return False

		#print sql, parameters
			
		try:
			if(parameters == None):
				self.cursor.execute(sql)
			else:
				self.cursor.execute(sql, parameters)
			return True
		except psycopg2 as e:
			print "Error on query: ", self.cursor.query
			util.PrintException()
			return False
		except psycopg2.InternalError as e:
			print "Error Internal on query: ", self.cursor.query
			print e.message
			util.PrintException()
			return False
		except:
			
			print "Error on query", sys.exc_info()[0], self.cursor.query, sql, parameters
			util.PrintException()
			return False
		finally:
			self.last_query = self.cursor.query
			self.status_message = self.cursor.statusmessage

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
		if(self.query(sql, parameters) == False or self.has_error() == True):
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
		if(not table):
			raise ValueError("Table name cannot be empty on _fetch_last_inserted_id method.")
			
		if(not column):
			raise ValueError("Column name cannot be empty on _fetch_last_inserted_id method.")
			
		columns = []
		columns.append("currval('{table}_{column}_seq')".format(table=table, column=column))

		row = self.select("", columns, None, None, [], [], ["INNER"], None, False)
		
		if(row):
			#gimmick to return only the number.
			while not isinstance(row, (int, long)) or not row:
				row = row[0]
			#print "row: ", row
		return row
	
	"""
		Method used to set insert_id variable and return last_insert_id
	"""
	def get_last_insert_id(self, table):
		try:
			self.insert_id = self._fetch_last_inserted_id(table, 'id')
		except ValueError as e:
			self.insert_id = 0
			print "ValueError:{0}".format(e.message)	
		finally:
			#print self.insert_id
			return self.insert_id
	
	"""
		Method used to insert data on any table on the database.
	"""
	def insert(self, table, values, columns = []):
		if columns is None:
			columns = []
			length_columns = 0
		else:
			length_columns = len(columns)
		
		if(not table):
			self.set_error("Table name cannot be empty")
			return False
		elif(length_columns > 0 and length_columns != len(values)):
			self.set_error("Column length is not equal to values length.")
			return False
		elif(len(values) == 0):
			self.set_error("Values can be empty")
			return False;

		value = []
		for index, element in enumerate(values):
			if(isinstance(element, collections.Iterable) and not isinstance(element, types.StringTypes)):
				value.append(element[0])
				values[index] = element[1]
			else:
				value.append("%s")
		
		if(length_columns > 0):
			sql = "INSERT INTO {table} ({columns}) VALUES ({values});".format(table=table, columns = ",".join(columns), values=",".join(value))
		else:
			sql = "INSERT INTO {table} VALUES ({values});".format(table=table, values=",".join(value))
		
		self.insert_id = 0;
		
		return self.change(sql, values)
		
	"""
		Method used to update the columns data on table.
		TODO: Change call of this method.
	"""
	def update(self, table, values, columns, where = None, where_values = None):
		if(not table):
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
			if(isinstance(element, collections.Iterable) and not isinstance(element, types.StringTypes)):
				value.append(element[0])
				values[index] = element[1]
			else:
				value.append("%s")
			
		sql = "UPDATE {table} SET ({columns}) = ({values})".format(table=table, columns = ",".join(columns), values=",".join(value))
		
		if where:
			sql = sql + " WHERE " + where
			for element in where_values:
				values.append(element)
		
		sql = sql + ";"
		return self.change(sql, values)
		
	"""
		Method used to delete data from database. 
		Case Where is not provide all row of the table will be delete, be aware of that.
		Condition on where must have %s on instead of values and parameter values must contain the values used on where in the correct order.
	"""
	def delete(self, table, where = None, where_values = None):
		if(not table):
			self.set_error("Table cannot be empty")
			return False
		
		if(where == None):
			sql = "DELETE FROM {table};".format(table=table)
		else:
			sql = "DELETE FROM {table} WHERE {condition};".format(table=table, condition=where)
		return self.change(sql, where_values)
	
	"""
		Method use to select the data from database.
		If there is no data None is returned.
	"""
	def select(self, table, columns = ['*'], where = None, where_values = None, joins = None, join_columns = None, join_type = None, limit = None, from_table = True):
		if(not table and from_table == True):
			raise ValueError("Table name cannot be empty on select method.")
		
		#Set parameter default.
		if not columns:
			columns = ['*']
		
		if joins is None:
			joins = []
		
		if join_columns is None:
			join_columns = []
		
		if join_type is None:
			join_type = ["INNER"]

		if(from_table == False):
			sql = "SELECT {column};".format(column= ",".join(columns))
		elif(where == None):
			sql = "SELECT {column} FROM {table};".format(table=table, column= ",".join(columns))
		else:
			if(len(joins) != 0 and len(joins) != len(join_columns)):
				raise ValueError("Join and column join on can have a length different.")
			elif(len(joins) != 0):
				join = ""
				default = len(join_type) == 1
					
				for index in range(len(joins)):
					if(default):
						e = join_type[0]
					else:
						e = join_type[index]
					join = join + " {join_type} JOIN {element} ON ({condition}) ".format(join_type=e, element=joins[index], condition=join_columns[index])
				#print columns
				column = ",".join(columns)
				sql = "SELECT {column} FROM {table} {join} WHERE {condition}".format(column = column, table=table, condition=where, join=join)	
			else:
				sql = "SELECT {column} FROM {table} WHERE {condition}".format(column = ",".join(columns), table=table, condition=where)
			if(isinstance( limit, ( int, long ))):
				sql + " LIMIT {0}".format(limit);
			sql = sql + ";"
			
		if(self.change(sql, where_values)):
			if(limit == 1):
				return self.cursor.fetchone();
			else:
				return self.cursor.fetchall();
		return None;
	
	"""
		Method used to get all elements associated with others elements on same 
		table using temporary table and WITH RECURSIVE.
	"""
	def select_with_recursive(self, table, recursive_columns, columns, recursive_where = None, where = None, where_values = None, joins = None, join_columns = None, join_type = None,recursive_alias = None, limit = None):
		if(not table):
			raise ValueError("Table name cannot be empty on get_with_recursive method.")

		if not columns:
			raise ValueError("columns cannot be empty on get_with_recursive method.")

		if(isinstance(columns, types.StringTypes)):
			raise ValueError("columns must be a list on get_with_recursive method.")
			
		if(len(columns) < 2):
			raise ValueError("columns cannot have less than 2 items on get_with_recursive method.")
			
		if(isinstance(recursive_columns, types.StringTypes)):
			raise ValueError("recursive_columns must be a list on get_with_recursive method.")
			
		if(len(recursive_columns) < 2):
			raise ValueError("recursive_columns cannot have less than 2 items on get_with_recursive method.")
			
		
		if joins is None:
			joins = []
		
		if join_columns is None:
			join_columns = []
		
		if join_type is None:
			join_type = ["INNER"]
			cls
		#where = "based_type_id = 3 and entity_id = 1"
		columns_filtered = [i for i in columns if not self.pattern_remove_function.search(i)]
		
		sql = "WITH RECURSIVE recursive_table({columns}) AS (SELECT {columns} FROM {table}".format(columns=", ".join(recursive_columns),table=table)
		
		if(recursive_where):
			sql += " WHERE {condition}".format(condition = recursive_where)
		
		sql += " UNION ALL SELECT p.{second_field}, p.{first_field} FROM recursive_table pr, {table} p WHERE p.{first_field} = pr.{second_field})".format(first_field = recursive_columns[0], second_field = recursive_columns[1],table=table)

		outside_where = ""
		
		if where:
			outside_where = "WHERE " + where
		
		if recursive_alias:
			recursive_alias = "as " + recursive_alias
			
		if(len(joins) != 0 and len(joins) != len(join_columns)):
			raise ValueError("Join and column join on cannot have a length different.")		
		elif(len(joins) != 0):
			join = ""
			default = len(join_type) == 1
					
			for index, element in enumerate(joins):
				if(default):
					e = join_type[0]
				else:
					e = join_type[index]
				join = join + " {join_type} JOIN {element} ON ({condition}) ".format(join_type=e, element=element, condition=join_columns[index])
			#print columns
			column = ",".join(columns)
			sql += "SELECT {columns} FROM recursive_table {recursive_alias} {join} {where} GROUP BY {columns_filtered}".format(columns=", ".join(columns), recursive_alias=recursive_alias,join=join, where=outside_where, columns_filtered = ", ".join(columns_filtered))	
		else:
			sql += " SELECT {columns} FROM recursive_table {recursive_alias} {where} GROUP BY {columns_filtered}".format(columns=", ".join(columns), recursive_alias=recursive_alias, where=outside_where, columns_filtered = ", ".join(columns_filtered))
		
		if(isinstance( limit, ( int, long ))):
			limited = True
			sql + " LIMIT {0}".format(limit);
		sql = sql + ";"
		
		if(self.change(sql, where_values)):
			if(limit == 1):
				return self.cursor.fetchone();
			else:
				return self.cursor.fetchall();
		return None;
	
	"""
		Method used to get only one row and one column from database.
		This method is projection and selection with limit 1.
	"""
	def get_var(self, table, columns = ['*'], where = None, where_values = None, joins = None, join_columns = None, join_type = None):
		result = self.select(table, columns, where, where_values, joins, join_columns, join_type, 1)
		if not result:
			return None
		else:
			return result[0]
		
	"""
		Method used to get only one row from database.
	"""
	def get_row(self, table, where = None, where_values = None, joins = None, join_columns = None, join_type = None):
		result = self.select(table, ['*'], where, where_values, joins, join_columns, join_type, 1)
		if result == None:
			return None
		else:
			return result[0]
				
	"""
		Method used to get only one column from database.
		All rows within the column will be returned.
	"""
	def get_col(self, table, column, where = None, where_values = None, joins = None, join_columns = None, join_type = None):
		columns = []
		columns.append(column)
		column = self.select(table, columns, where, where_values, joins, join_columns, join_type)
		if column:
			return column[0]
		return None
	
	"""
		Method used to get all the data from a database query.
	"""
	def get_results(self, table, where = None, where_values = None, joins = None, join_columns = None, join_type = None, limit = None):
		return self.select(table, ['*'], where, where_values, joins, join_columns, join_type, limit)
		
	############################### Begin of specified methods for the crawler ################################### 
	##############################################################################################################
	
	################### Internal Methods Used by Other Methods #################### 
	
	"""
		Method used to get id from a table given a name.
	
	"""
	def get_id_from_name(self, table, name):
		return self.get_id_from_field(table, 'name', name)
	
	"""
		Method used to return the value from column ID from database
		given a field and value for where condition.
	"""
	def get_id_from_field(self, table, field, value):
		numeric_value = isinstance(value, types.StringTypes) or isinstance(value, (int, long))
		
		if(isinstance(field, types.StringTypes) and numeric_value):
			where = "{field} = %s".format(field=field)
			sanitize_value = []
			sanitize_value.append(value)
		elif(not isinstance(field, types.StringTypes) and isinstance(field, collections.Iterable) and isinstance(value, collections.Iterable)):
			where = []
			for element in field:
				where.append("{element}=%s".format(element=element))
			where = " and ".join(where)
			sanitize_value = value
		else:
			raise ValueError("Invalid field name input on get_id_from_field(%s, %s, %s)" % (table, field, value))
		return self.get_var(table, ['id'], where, sanitize_value)
		
	
	"""
		Method used to insert a item name on a table type.
		This method can be use to insert name on the follow tables:
		hash_type, release_read_status_type, release_type, software_type, edition_type, image_edition_type, image_goods_type,
		produces_type, create_type, product_condition_type, figure_version, plataform_type, print_type, genre_type, related_type, 
		release_ownership_type, entity_type, filter_type, edition_read_status_type, function_type,condition_type, classification_type,
		collaborator_type, media_type, number_type, alias_type, mod_type, blood_type, blood_rh_type, box_condition_type, based_type, stage_developer_type,
		company_function_type, soundtrack_type, compose_type, image_soundtrack_type, lyric_type, user_filter_type
		
		If the item name already exists on database a new one will not be created and the id from the existent one will be returned instead.
		
	"""
	def add_type(self, name, type_name):
		if(not name):
			raise ValueError("Name cannot be empty on add_type method.")
		
		table = type_name + '_type'
		
		#create name on table if there isn't none. 
		id = self.get_id_from_name(table, name)
		
		if(id == None):
			value = []
			value.append(name)
			self.insert(table, value, ['name'])
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_type(%s, %s)" % (name, type_name))
		return id
	
	"""
		Method use to insert a item name on a table that only have id and name as columns.
		This method can be use to insert name on the follow tables:
		shop_location, scale, material, ownership_status, tag, category, genre, archive_container
	"""
	def add_name_to_table(self, name, table):
		if(not name):
			raise ValueError("Name cannot be empty on add_name_to_table method.")
			
		if(not table):
			raise ValueError("Table cannot be empty on add_name_to_table method.")
			
		#create name on table if there isnt none. 
		id = self.get_id_from_name(table, name)
		
		if(id == None):
			value = []
			value.append(name)
			self.insert(table, value, ['name'])
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_name_to_table(%s, %s)" % (name, table))
		return id
		
	"""
		Method use to insert a codec on the codecs table.
		This method can be use to insert name on the follow tables:
		audio_codec, video_codec
	"""
	def add_codec(self, name, type ='audio', lossless = False):
		if(not name):
			raise ValueError("Name cannot be empty on add_name_to_table method.")
		
		table = type + '_codec'
		
		id = self.get_id_from_name(table, name)
		if(id == None):
			columns = ['name', 'lossless']
			
			value = []
			value.append(name)
			
			if(lossless):
				value.append(1)
			else:
				value.append(0)
		
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_name_to_table(%s, %s)" % (name, table))
		return id
			
	
	"""
		Method used to insert a image to the image table.
		To insert and make a relationship between a image and an entity use the methods add_image_to_ 
	"""
	def add_image(self, url, extension, name):
		if(not name):
			raise ValueError("Name cannot be empty on add_image method.")
		
		if(not url):
			raise ValueError("Url cannot be empty on add_image method.")
			
		table = 'image'
		id = self.get_id_from_field(table, 'url', url)
		if(id == None):
			columns = ['url', 'extension', 'name']
			value = []
			value.append(url)
			value.append(extension)
			value.append(name)
			
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_image(%s, %s, %s)." % (url, extension,name))
		return id
	
	"""
		Method used to insert a relationship for images that have a certain type.
		This method can be use to insert name on the follow tables:
		entity_edition_has_image, goods_has_image, soundtrack_has_image, audio_has_image, collaborator_has_image
		
		For people_has_image table use the add_multi_relation method.
		The methods add_image_to_ already uses the appropriate relation method 
	"""
	def add_relation_image(self, relation_table, image_id, second_id, type_id):
		if(not relation_table):
			raise ValueError("relation_table cannot be empty on add_relation_image method.")
		if(not image_id or not second_id):
			raise ValueError("image_id and second_id cannot be empty on add_relation_image method.")
		
		table = relation_table + "_has_image"
		
		where_values = []
		where_values.append(image_id)
		where_values.append(second_id)
		where_values.append(image_id)
		id = self.get_var(table, ['image_id'], "image_id = %s and {relation_table}_id = %s".format(relation_table=relation_table), where_values)
		
		if(id == None):
			columns = ['image_id', relation_table + '_id', 'image_' + relation_table + '_type_id']
			value = []
			value.append(image_id)
			value.append(second_id)
			value.append(type_id)
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_relation_image(%s, %s, %s, %s)." % (relation_table, image_id, second_id, type_id))
		return True
		
	"""
		Method used to insert on tables with cardinality N:M that have only the foreign keys.
		This method can be use to insert on the follow tables:
		country_has_language, soundtrack_integrate_collection, category_has_filter_type, tag_has_filter_type,audio_has_language, company_sponsors_event,
		company_owner_collection, company_has_country, people_has_image, genre_type_has_audio, entity_has_category, entity_has_tag, entity_has_gender,
		soundtrack_for_entity_edition, entity_edition_has_language, entity_edition_has_currency, goods_from_persona, goods_has_category,
		entity_release_has_version, entity_release_has_language, goods_has_material, goods_has_shop_location, goods_has_tag, mod_release_has_image,
		shops_operate_on_country, people_nacionalization_on_country, entity_has_tag, entity_edition_has_subtitle, software_edition_has_version,
		genre_has_filter_type, persona_has_image, requirements_has_driver, entity_has_image
		
		The table name to be used will be assembly by first_table + relation_type + second_table. 
		By default relation_type is equal to has, but can be overwrite.
	"""
	def add_multi_relation(self, first_id, second_id, first_table, second_table, relation_type = 'has'):
		if not first_table or not second_table:
			raise ValueError("Table names cannot be empty on add_multi_relation method.")
	
		#check if there is already a compost key with the given ids.
		if(first_table != second_table):
			another = ''
		else:
			another = 'another_'
		
		table = first_table + '_' + relation_type + '_' + second_table
		
		where_values = []
		where_values.append(first_id)
		where_values.append(second_id)
		id = self.get_var(table, [first_table + '_id'], "{first_table}_id = %s and {another}{second_table}_id = %s".format(first_table=first_table, another=another, second_table=second_table), where_values)
		
		if(id == None):
			if(first_table != second_table):
				columns = [first_table + '_id', second_table + '_id']
			else:
				columns = [first_table + '_id', 'another_' + second_table + '_id']
			value = []
			value.append(first_id)
			value.append(second_id)

			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_multi_relation(%s, %s, %s, %s, %s)." % (first_id, second_id, first_table, second_table, relation_type))
		return True
		
	
	"""
		Method used to insert a N:M relationship with attribute type.
		This method can be use to insert on the follow tables:
		entity_based_entity, persona_related_persona, video_release_has_audio_codec
		
		The only table available on database N:M with type are auto-relationship, but this methods can be used with
		another table with the same structure, I just didn't create any besides the already mentioned. 
		The database N:M auto-related table must have another_ as prefix on the second id. 
		
		If used for the video_release_has_audio_codec table set use_type_id to false because there isn't a language_type_id only language_id.
		
		relation_type parameter is the middle name for the table, current can be 'has', 'related' or 'based'
	"""
	def add_relation_with_type(self, first_table, second_table, first_id, second_id, relation_type, relation_type_id, use_type_id = True):
		if not first_table or not second_table:
			raise ValueError("Table names cannot be empty on add_relation_with_type method")
		
		if not relation_type:
			raise ValueError("Relation type cannot be empty on add_relation_with_type method")
		
		#check if there is already a compost key with the given ids.
		if(first_table != second_table):
			another = ''
		else:
			another = 'another_'
			
		if(use_type_id):
			type = '_type'
		else:
			type = ''
			
		table = first_table + "_" + relation_type + "_" + second_table
		
		where_values = []
		where_values.append(first_id)
		where_values.append(second_id)
		where_values.append(relation_type_id)
		id = self.get_var(table, [first_table + '_id'], "{first_table}_id = %s and {another}{second_table}_id = %s and {relation_type}{type}_id = %s".format(first_table=first_table, another=another, second_table=second_table, relation_type=relation_type, type=type),where_values)
		if(id == None):
			columns = [first_table + '_id', another + second_table + '_id', relation_type + type + '_id']
			value = []
			value.append(first_id)
			value.append(second_id)
			value.append(relation_type_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_relation_with_type(%s, %s, %s, %s, %s, %s, %s)." % (first_table, second_table, first_id, second_id, relation_type, relation_type_id, use_type_id))
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
	def add_number(self, entity_id, number_type_id, number, type = 'release', number_release_id = None):
		if(not number):
			raise ValueError("Number cannot be empty on add_number method.")
		
		if(not number_type_id):
			raise ValueError("Number type id cannot be empty on add_number method.")

		where_values = []
		#check if already there is this number registered on database
		if(type == 'release'):
			#check if entity_id really exists
			self.check_id_exists('entity_release', entity_id)
			if number_release_id:
				where = "number = %s and number_release_id = %s and entity_release_id = %s and number_type_id = %s"
				where_values.append(number)
				where_values.append(number_release_id)
				where_values.append(entity_id)
				where_values.append(number_type_id)
			else:
				where = "number = %s and number_release_id IS NULL and entity_release_id = %s and number_type_id = %s"
				where_values.append(number)
				where_values.append(entity_id)
				where_values.append(number_type_id)
		else:
			#check if entity_id really exists
			self.check_id_exists('entity_edition', entity_id)
			
			where = "number = %s and entity_edition_id = %s and number_type_id = %s"
			where_values.append(number)
			where_values.append(entity_id)
			where_values.append(number_type_id)
			
		table = 'number_' + type
		
		id = self.get_var(table, ['id'], where, where_values)
		
		if(id == None):
			#register
			columns = ['entity_'+ type +'_id', 'number_type_id', 'number']
			value = []
			value.append(entity_id)
			value.append(number_type_id)
			value.append(number)
			
			if number_release_id:
				columns.append('number_release_id')
				value.append(number_release_id)
				
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_number(%s, %s, %s, %s, %s)." % (entity_id, number_type_id, number, type, number_release_id))
		return id
	
	"""
		Method used to check if id exists on determined table.
		This method can be call on another method without try except, but method above must have a try except.  
	"""
	def check_id_exists(self, table, id):
		#check if id really exists on table
		id = self.get_id_from_field(table, 'id', id)
		if(id == None):
			raise ValueError("Error on getting id. Id don't exists for check_id_exists(%s, %s)." % (table, id))
		return True
		
	"""
		Method used to check if all input fields are not empty.
	"""
	def check_field(self, fields = [], message = None):
		if not message:
			message = "The field %s cannot be empty."
		for field in fields:
			if not field:
				raise ValueError(message % (field))
	
	
	"""
		Method used to insert a alias or title to an item.
		This method can be use to insert on the follow tables:
		entity_alias, goods_alias, company_alias.
		
	"""
	def add_alias(self, name, entity_id, language_id, alias_for, alias_type_id):
		if not name:
			raise ValueError("Name cannot be empty on add_alias method.")
			
		#check if entity_id really exists on correct table
		self.check_id_exists(alias_for, entity_id)
		
		table = alias_for + '_alias'
		
		where_values = []
		where_values.append(language_id)
		where_values.append(name)
		where_values.append(entity_id)
		id = self.get_id_from_field(table, ['language_id','name',alias_for + '_id'], where_values)
		
		if(id == None):
			columns = ['alias_type_id', alias_for + '_id', 'language_id', 'name']
			value = []
			value.append(alias_type_id)
			value.append(entity_id)
			value.append(language_id)
			value.append(name)
			self.insert(table, value, columns)

			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_alias(%s, %s, %s, %s, %s)." % ( name, entity_id, language_id, alias_for, alias_type_id))
		return id
		
	"""
		Method used to register the launch country to an entity edition.
		This method can be use to insert on the follow tables:
		entity_edition_launch_country, goods_launch_country.
		
	"""
	def add_to_launch_country(self, entity_id, country_id, launch_date, launch_price, launch_currency_id, launch_for = 'entity_edition'):
		if(not entity_id):
			raise ValueError("Entity id cannot be empty on add_to_launch_country method.")
		
		if(not country_id):
			raise ValueError("Country id cannot be empty on add_to_launch_country method.")
		
		#check if entity_edition_id really exists
		self.check_id_exists(launch_for, entity_id)
		
		table = launch_for + '_launch_country'
		where_values = []
		where_values.append(entity_id)
		where_values.append(country_id)
		where_values.append(launch_currency_id)
		id = self.get_var(table, [launch_for + '_id'], "{launch_for}_id = %s and country_id = %s and currency_id = %s".format(launch_for=launch_for), where_values)
		if(id == None):
			columns = [launch_for + '_id', 'country_id' , 'launch_date', 'launch_price', 'currency_id']
			value = []
			value.append(entity_id)
			value.append(country_id)
			value.append(launch_date)
			value.append(launch_price)
			value.append(launch_currency_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_to_launch_country(%s, %s, %s, %s, %s, %s)." % (entity_id, country_id, launch_date, launch_price, launch_currency_id, launch_for))
		return True
		
		
		
	############################## Entity Methods #################################
	
	"""
		Method used to insert a entity. This method don't insert any related item to entity like name or categories.
		This method can be use to insert on entity table.
		
	"""
	def add_entity(self, entity_type_id, classification_type_id, language_id, country_id, launch_year = None, collection_id = None, collection_started = 'False', update_id = None):
		table = 'entity'
		#cannot warranty uniqueness
		columns = ['entity_type_id', 'classification_type_id', 'language_id','country_id', 'collection_started']
		value = []
		value.append(entity_type_id)
		value.append(classification_type_id)
		value.append(language_id)
		value.append(country_id)
		value.append(collection_started)
		
		if launch_year:
			columns.append('launch_year')
			value.append(launch_year)
			
		if collection_id:
			columns.append('collection_id')
			value.append(collection_id)
		
		if update_id:
			where_values = []
			where_values.append(update_id)
			if not self.update(table, value, columns, "id = %s", where_values):
				raise ValueError("An error occurred while trying to update on add_entity(%s, %s, %s, %s, %s, %s, %s, %s)." % (entity_type_id, classification_type_id, collection_id, language_id, country_id, launch_year, collection_started, update_id))
			id = update_id	
		else:
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_entity(%s, %s, %s, %s, %s, %s, %s, %s)." % (entity_type_id, classification_type_id, collection_id, language_id, country_id, launch_year, collection_started, update_id))
		return id
	
	
	"""
		Method used to insert a description to an entity.
		This method can be use to insert on entity_description.
		
		TODO: Change method and table entity_description to register user who send the description. Allow multiples descriptions.
	"""
	def add_entity_description(self, entity_id, language_id, description):
		if(not description):
			raise ValueError("Description cannot be empty on add_entity_description method.")
			
		table = 'entity_description'
		
		columns = ['entity_id', 'language_id', 'description']
		value = []
		value.append(entity_id)
		value.append(language_id)
		value.append(description)
		
		self.insert(table, value, columns)
		id = self.get_last_insert_id(table)
		if(id == 0):
			raise ValueError("An error occurred when trying to insert on add_entity_description(%s, %s, %s)." % (entity_id, language_id, description))
		return id
		
	"""
		Method used to insert a wiki to an entity.
		This method can be use to insert on entity_wiki.
		
	"""
	def add_entity_wiki(self, entity_id, name, url, language_id):
		if(not url):
			raise ValueError("Url cannot be empty on add_entity_wiki method.")

		if(not name):
			raise ValueError("Name cannot be empty on add_entity_wiki method.")
		
		table =	'entity_wiki'

		id = self.get_id_from_field(table, 'url', url)
		if(id == None):
			columns = ['entity_id', 'name', 'url', 'language_id']
			value = []
			value.append(entity_id)
			value.append(name)
			value.append(url)
			value.append(language_id)
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_entity_wiki(%s, %s, %s, %s)." % (entity_id, name, url, language_id))
		return id
	
	"""
		Method used to insert a synopsis to an entity.
		This method can be use to insert on entity_synopse.
		
	"""
	def add_entity_synopsis(self, entity_id, language_id, description):
		if(not description):
			raise ValueError("Description cannot be empty on add_entity_synopse method.")
		
		#print "Entity_synopsis"
		#check if entity_id really exists
		self.check_id_exists('entity', entity_id)
		
		table = 'entity_synopsis'
		where_values = []
		where_values.append(entity_id)
		where_values.append(language_id)
		id = self.get_var(table, ['entity_id'], "entity_id = %s and language_id = %s",where_values)
		if(id == None):
			columns = ['entity_id', 'language_id', 'content']
			value = []
			value.append(entity_id)
			value.append(language_id)
			value.append(description)
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_entity_synopsis(%s, %s, %s)." % (entity_id, language_id, description))
		return True
	
	"""
		Method used to add a image and associated it with an entity.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
		This method only will be used when is not possible to have a edition and is necessary to save a entity image.
	"""	
	def add_image_to_entity(self, url, extension, name, entity_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_multi_relation(entity_id, image_id, 'entity', 'image')
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	"""
		Method used to register all items related with entity.
		This method must be used instead other specified methos related with entity.
		
		To use this method the types must be already registered on database.
		The parameters titles must have elements that are dict. 
	"""
	def create_entity(self, romanized_title, entity_type_id, classification_type_id, language_id, country_id, launch_year = None, collection_id = None, collection_started = 'False', 
	titles = [], subtitles = [], synopsis = [], wikis = [], descriptions = [], categories = [], tags = [], genres = [], personas = [], companies = [], peoples = [], relateds = [], romanize_subtitle = None, images = [], update_id = None):
		#if(not romanized_title):
		#	raise ValueError("Romanized title cannot be empty on create_entity method.")
		
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			entity_id = self.add_entity(entity_type_id, classification_type_id, language_id, country_id, launch_year, collection_id, collection_started, update_id)
			
			if romanized_title:
				#register main name (Romanize title and Romanized Subtitle)
				self.add_alias(romanized_title, entity_id, language_id, 'entity', self.alias_type_romanized)
			
			if romanize_subtitle:
				self.add_alias(romanize_subtitle, entity_id, language_id, 'entity', self.alias_type_subromanized)
			
			for title in titles:
				self.add_alias(title['title'], entity_id, title['language_id'], 'entity', self.alias_type_title)
			
			for subtitle in subtitles:	
				self.add_alias(subtitle['title'], entity_id, subtitle['language_id'], 'entity', self.alias_type_subtitle)
			
			#register synopsis
			for synops in synopsis:	
				self.add_entity_synopsis(entity_id, synops['language_id'], synops['content'])
			
			for description in descriptions:
				self.add_entity_description(entity_id, description['language_id'], description['content'])
			
			for category in categories:
				self.add_multi_relation(entity_id, category['id'], 'entity', 'category')

			for tag in tags:
				self.add_multi_relation(entity_id, tag['id'], 'entity', 'tag')
	
			for wiki in wikis:
				self.add_entity_wiki(entity_id, wiki['name'], wiki['url'], wiki['language_id'])
			
			for persona in personas:
				#persona first_appear is 0 or 1.
				self.add_persona_to_entity(entity_id, persona['id'], persona['alias_id'], persona['first_appear'])
			
			for company in companies:
				#print company
				self.add_relation_company(company['id'], entity_id, company['function_type_id'], 'entity')
			
			for people in peoples:
				self.add_relation_people(people['id'], people['alias_used_id'], entity_id, 'entity', people['relation_type_id'])
			
			for related in relateds:
				self.add_relation_with_type('entity', 'entity', entity_id, related['id'], 'based', related['type_id'])
			
			for genre in genres:
				self.add_multi_relation(entity_id, genre['id'], 'entity', 'genre')
			
			for image in images:
				self.add_image_to_entity(image['url'], image['extension'], image['name'], entity_id)
			
			#commit changes
			self.commit()
			
			return entity_id
		except ValueError as e:
			print "ValueError: ", e.message
			self.rollback()
			raise ValueError("Return id is equal to 0 on create_entity method. Some error must have occurred on create_entity(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)." % (romanized_title, entity_type_id, classification_type_id, language_id, country_id, launch_year, collection_id, collection_started, titles, subtitles, synopsis, wikis, descriptions, categories, tags, genres, personas, companies, peoples, relateds, romanize_subtitle, images, update_id))
		finally:
			self.set_auto_transaction(True)
	
	############################### Edition Methods ###############################
	
	"""
		Method used to insert a entity edition. This method don't insert any related item to entity like subtitles or audio languages.
		This method can be use to insert on entity_edition table.
		
		The parameter subtitle refers to subheading and not a caption.
	"""
	def add_edition(self, edition_type_id, entity_id, title, free = 0, censored = 0, subtitle = None, code = None, complement_code = None, release_description = None, height = None, width = None, depth = None, weight = None, event_id = None, update_id = None):
		if(not title):
			raise ValueError("Name cannot be empty on add_edition method.")
		
		if(not entity_id):
			raise ValueError("Entity id cannot be empty on add_edition method.")
		
		#print "Edition"
		#check if entity_id really exists
		self.check_id_exists('entity', entity_id)
		
		where = ['entity_id','title']
		where_values = []
		where_values.append(entity_id)
		where_values.append(title)
		if code:
			where.append('code')
			where_values.append(code)
			
		table = 'entity_edition'
		
		id = self.get_id_from_field(table, where, where_values)
		if(id == None or update_id):
			columns = ['edition_type_id', 'entity_id', 'title', 'free', 'censored']
			value = []
			value.append(edition_type_id)
			value.append(entity_id)
			value.append(title)
			value.append(free)
			value.append(censored)
			
			if code:
				columns.append('code')
				value.append(code)			
			if complement_code:
				columns.append('complement_code')
				value.append(complement_code)			
			if release_description:
				columns.append('release_description')
				value.append(release_description)			
			if height:
				columns.append('height')
				value.append(height)			
			if width:
				columns.append('width')
				value.append(width)	
			if depth:
				columns.append('depth')
				value.append(depth)			
			if weight:
				columns.append('weight')
				value.append(weight)		
			if event_id:
				columns.append('event_id')
				value.append(event_id)
			if subtitle:
				columns.append('subtitle')
				value.append(subtitle)
			
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_edition(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)." % (edition_type_id, entity_id, title, free, censored, subtitle, code, complement_code, release_description, height, width, depth, weight, event_id, update_id))
				id = update_id	
			else:
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_edition(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)." % (edition_type_id, entity_id, title, free, censored, subtitle, code, complement_code, release_description, height, width, depth, weight, event_id, update_id))
		return id
	
	"""
		Method used to insert a number related with edition.
		This method can be use to insert on number_edition table. 
		The method only call the add_number method, not being at all special, you can use add_number is you like for insert number on edition,
		but a strongly recommend against it.
		
	"""
	#Method above that use this method need to call try except. add_number() raise exception that need to be catch.
	def add_edition_number(self, edition_id, number, number_type_id):
		if(not edition_id):
			raise ValueError("Edition id cannot be empty on add_edition_number method.")
			
		return add_number(edition_id, number_type_id, number, 'edition')

	
	"""
		Method used to insert a software edition to the specialization of entity_edition table.
		This method can be used to insert on software_edition table. 
		This method require a entity_edition_id to register, if you would like to add a entity_edition and a software edition with
		the same method use create_software_edition method instead.
	"""
	def add_software_edition(self, entity_edition_id, plataform_type_id, software_type_id, media_type_id, visual_type_id):
		if(not entity_edition_id):
			raise ValueError("entity_edition_id cannot be empty on add_software_edition method.")
			
		if(not plataform_type_id):
			raise ValueError("plataform_type_id cannot be empty on add_software_edition method.")
			
		if(not software_type_id):
			raise ValueError("software_type_id cannot be empty on add_software_edition method.")
		
		if(not media_type_id):
			raise ValueError("media_type_id cannot be empty on add_software_edition method.")
			
		if(not visual_type_id):
			raise ValueError("visual_type_id cannot be empty on add_software_edition method.")
	
		#check if entity_edition_id really exists
		self.check_id_exists('entity_edition', entity_edition_id)
		
		table = 'software_edition'
		
		where_values = []
		where_values.append(entity_edition_id)
		where_values.append(plataform_type_id)
		where_values.append(software_type_id)
		where_values.append(media_type_id)
		
		id = self.get_var(table, ['entity_edition_id'], "entity_edition_id = %s and plataform_type_id = %s and software_type_id = %s and media_type_id = %s",where_values)
		if(id == None):
			columns = ['entity_edition_id', 'plataform_type_id', 'software_type_id', 'media_type_id']
			value = []
			value.append(entity_edition_id)
			value.append(media_type_id)
			value.append(software_type_id)
			value.append(media_type_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_software_edition(%s, %s, %s, %s)." % (entity_edition_id, plataform_type_id, software_type_id, media_type_id))
		return True
		
	"""
		Method used to insert a read edition to the specialization of entity_edition table.
		This method can be used to insert on read_edition table. 
		This method require a entity_edition_id to register, if you would like to add a entity_edition and a read edition with
		the same method use create_read_edition method instead.
	"""
	def add_read_edition(self, entity_edition_id, print_type_id, pages_number, chapters_number = None, update_id = None):
		if(not entity_edition_id):
			raise ValueError("entity_edition_id cannot be empty on add_software_edition method.")
			
		if(not pages_number):
			raise ValueError("pages_number cannot be empty on add_read_edition method.")
		
		table = 'read_edition'
		
		where_values = []
		where_values.append(entity_edition_id)
		id = self.get_var(table, ['entity_edition_id'], 'entity_edition_id = %s', where_values)
		if(id == None or update_id):
			columns = ['entity_edition_id', 'print_type_id', 'pages_number']
			value = []
			value.append(entity_edition_id)
			value.append(print_type_id)
			value.append(pages_number)
			
			if chapters_number:
				columns.append('chapters_number')
				value.append(chapters_number)

			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_read_edition(%s, %s, %s, %s, %s)." % (entity_edition_id, print_type_id, pages_number, chapters_number, update_id))
				id = update_id	
			else:
				if(self.insert(table, value, columns) == False):
					raise ValueError("An error occurred when trying to insert on add_read_edition(%s, %s, %s, %s, %s)." % (entity_edition_id, print_type_id, pages_number, chapters_number, update_id))
		return id
	
	"""
		Method used to add a image and associated it with an entity edition.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""
	def add_image_to_edition(self, url, extension, name, edition_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('entity_edition', image_id, edition_id, image_type_id)
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	"""
		Method used to register all items related with entity.
		This method must be used instead other specified methos related with entity.
		
		To use this method the types must be already registered on database.
		The parameters titles must have elements that are dict. 
	"""
	def create_edition(self, edition_type_id, entity_id, title, number, number_type_id, free = 0, censored = 0, subtitle = None, code = None, complement_code = None, release_description = None, height = None, width = None, depth = None, weight = None, event_id = None,
	languages_id = [], subtitles_id = [], launch_countries = [], companies = [], images = [], update_id = None):

		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			table = 'entity_edition'
			
			edition_id = self.add_edition(edition_type_id, entity_id, title, free, censored, subtitle, code , complement_code, release_description,height,width, depth, weight, event_id, update_id)
		
			#Add number
			self.add_edition_number(edition_id, number, number_type_id)
		
			for language in languages:
				self.add_multi_relation(edition_id, language, table, 'language')
			
			for caption in subtitles:
				self.add_multi_relation(edition_id, caption, table, 'subtitle')
		
			#Add launch countries
			for launch in launch_countries:
				self.add_to_launch_country(edition_id, launch['country_id'], launch['date'], launch['price'], launch['currency_id'], 'entity_edition')
			
			for company in companies:
				self.add_relation_company(company['id'], edition_id, company['function_type_id'], table)
			
			for image in images:
				self.add_image_to_edition(image['url'], image['extension'], image['name'], edition_id, image['type_id'])

			#commit changes
			self.commit()
			
			
			return edition_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_edition method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
		
	"""
		Method used to create a entity edition that is a read_edition specialization.
		The method differ from create_edition on that it not request subtitles because subtitles, or captions, are for videos; game is a video based content.
		This method as well all other create method will only commit the transaction after all be run successful. 
	"""
	def create_read_edition(self, print_type_id, pages_number, edition_type_id, entity_id, title, number, number_type_id, free = 0, censored = 0, chapters_number = None, subtitle = None, code = None, complement_code = None, release_description = None, height = None, width = None, depth = None, weight = None, launch_event_id = None,
	languages_id = [], launch_countries = [], companies = [], images = [], update_id = None):
		
		#set commit to false.
		self.set_auto_transaction(False)
			
		try:
			edition_id = self.create_edition(edition_type_id, entity_id, title, number, number_type_id, free, censored, subtitle, code, complement_code, release_description, height, width, depth, weight, launch_event_id, languages_id, [], launch_countries, companies, images)
			self.add_read_edition(self, edition_id, print_type_id, pages_number, chapters_number, update_id)
			
			#commit changes
			self.commit()
			
			return edition_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("Return id is equal to 0 on create_read_edition method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
	
	"""
		Method used to create a entity edition that is a software_edition specialization.
		This method as well all other create method will only commit the transaction after all be run successful. 
	"""
	def create_software_edition(self, plataform_type_id, software_type_id, media_type_id, visual_type_id,
	edition_type_id, entity_id, title, number, number_type_id, free = 0, censored = 0, subtitle = None, code = None, complement_code = None, release_description = None, height = None, width = None, depth = None, weight = None, launch_event_id = None,
	languages_id = [], subtitles = [], launch_countries = [], companies = [], images = []):
	
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			edition_id = self.create_edition(edition_type_id, entity_id, title, number, number_type_id, free, censored, subtitle, code, complement_code, release_description, height, width, depth, weight, launch_event_id, languages_id, subtitles, launch_countries, companies, images)
			self.add_software_edition(edition_id, plataform_type_id, software_type_id, media_type_id, visual_type_id)
			#commit changes
			self.commit()
			
			return edition_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("Return id is equal to 0 on create_software_edition method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
	
	

	################################ Release Methods ##############################
	
	"""
		Method used to insert a entity release. This method don't insert any related item to entity like number or languages.
		This method can be use to insert on entity_release table.
		Only one release per file.
	"""
	def add_release(self, entity_id, release_type_id, country_id, release_date = None, entity_edition_id = None, description = None):
		if(not entity_id):
			raise ValueError("entity_id cannot be empty on add_release method.")	
		
		if(not release_type_id):
			raise ValueError("release_type_id cannot be empty on add_release method.")	
		
		if(not country_id):
			raise ValueError("country_id cannot be empty on add_release method.")	
			
		#check if entity really exists
		self.check_id_exists('entity', entity_id)
		
		table = 'entity_release'
		
		'''
		where_values = []
		where_values.append(entity_id)
		where_values.append(release_type_id)
		where_values.append(entity_edition_id)
		where_values.append(country_id)
		
		#id = self.get_id_from_field(table, ['entity_id','release_type_id','entity_edition_id','country_id'], where_values)
		#if(id == None):
		'''
		
		columns = ['entity_id','release_type_id','country_id']
		value = []
		value.append(entity_id)
		value.append(release_type_id)
		value.append(country_id)
			
		if entity_edition_id:
			columns.append('entity_edition_id')
			value.append(entity_edition_id)
			
		if description:
			columns.append('description')
			value.append(description)
		
		if release_date:
			columns.append('release_date')
			release = []
			release.append('to_timestamp(%s)')
			release.append(release_date)
			value.append(release) 
		
		#print value, columns
		
		print self.insert(table, value, columns)
				
		id = self.get_last_insert_id(table)
		if(id == 0):
			raise ValueError("There is no last insert id to return on add_release(%s, %s, %s, %s, %s, %s, %s)." % (entity_id, release_type_id, country_id, entity_edition_id, release_date, description, update_id))
		return id
		
	"""
		Method used to insert a game release to the specialization of entity_release table.
		This method can be used to insert on game_release table. 
		This method require a entity_release_id to register, if you would like to add a entity_release and a read edition with
		the same method use create_game_release method instead.
	"""
	def add_game_release(self, entity_release_id, installation_instructions = None, emulate = 0):
		if(not entity_release_id):
			raise ValueError("entity_release_id cannot be empty on add_game_release method.")
			
		table = 'game_release'
		
		where_values = []
		where_values.append(entity_release_id)
		id = get_var(table, ['entity_release_id'], "entity_release_id = %s", where_values)
		
		if(id == None):
			columns = ['entity_release_id']
			value = []
			value.append(entity_release_id)
			if(emulate != 0):
				columns.append('emulate')
				value.append(emulate)
			if installation_instructions:
				columns.append('installation_instructions')
				value.append(installation_instructions)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_game_release(%s, %s, %s)." % (entity_release_id, installation_instructions, emulate ))
		return True
	
	"""
		Method used to insert a game mod release to the specialization of entity_release table.
		This method can be used to insert on mod_release table. 
		This method require a entity_release_id to register, if you would like to add a entity_release and a mod release with
		the same method use create_mod_release method instead.
	"""
	def add_mod_release(self, name, type_id, entity_release_id, author_name, launch_date = None, description = None, installation_instruction = None, update_id = None):
		if(not entity_release_id):
			raise ValueError("entity_release_id cannot be empty on add_mod_release method.")
			
		#check if entity_release really exists
		self.check_id_exists('entity_release', entity_release_id)
			
		table = 'mod_release'
		#check if already is a mod fro this entity
		id = self.get_id_from_field(table, 'entity_release_id', entity_release_id)
		if(id == None or update_id):
			columns = ['entity_release_id', 'mod_type_id', 'name', 'author']
			value = []
			value.append(entity_release_id)
			value.append(type_id)
			value.append(name)
			value.append(author_name)
			
			if launch_date:
				columns.append('launch_date')
				value.append(launch_date)
			if description:
				columns.append('description')
				value.append(description)
			if installation_instruction:
				columns.append('installation_instruction')
				value.append(installation_instruction)
			
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_mod_release(%s, %s, %s, %s, %s, %s, %s, %s)." % (name, type_id, entity_release_id, author_name, launch_date, description, installation_instruction, update_id ))
				id = update_id	
			else:
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_mod_release(%s, %s, %s, %s, %s, %s, %s, %s)." % (name, type_id, entity_release_id, author_name, launch_date, description, installation_instruction, update_id ))
		return id
	
	"""
		Method used to insert a video release to the specialization of entity_release table.
		This method can be used to insert on video_release table. 
		This method require a entity_release_id to register, if you would like to add a entity_release and a video edition with
		the same method use create_video_release method instead.
	"""
	def add_video_release(self, entity_release_id, duration, video_codec_id, container_id, softsub, resolution, update_id = None):
		if(not entity_release_id):
			raise ValueError("entity_release_id cannot be empty on add_mod_release method.")
			
		#check if entity_release really exists
		self.check_id_exists('entity_release', entity_release_id)
		
		table = 'video_release'
		#check if already is a video release for this entity
		id = self.get_id_from_field(table, 'entity_release_id', entity_release_id)
		if(id == None or update_id):
			columns = ['entity_release_id', 'video_codec_id', 'archive_container_id', 'duration', 'resolution','softsub']
			value = []
			value.append(entity_release_id)
			value.append(video_codec_id)
			value.append(container_id)
			value.append(duration)
			value.append(resolution)
			if(softsub):
				value.append(1)
			else:
				value.append(0)
			
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_video_release(%s, %s, %s, %s, %s, %s, %s)." % ( entity_release_id, duration, video_codec_id, container_id, softsub, resolution, update_id ))
				id = update_id	
			else:			
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_video_release(%s, %s, %s, %s, %s, %s, %s)." % ( entity_release_id, duration, video_codec_id, container_id, softsub, resolution, update_id ))
		return id
		
	"""
		Method used to add a number to a release.
		This method can be used to insert multiples numbers and hierarchies number, 
		e.g. Volume 1 Chapter 1-4 or Season 4 Episode 89-102. 
	"""
	def add_release_number(self, release_id, numbers):
		if not release_id:
			raise ValueError("Release id cannot be empty on add_release_number method.")
			
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			for number in numbers:
				#register volume first.
				volume_id = None
				if number['parent']:
					volume_id = self.add_number(release_id, number['parent_type'], number['parent'])
				#print volume_id
				for chapter in number['child']:
					self.add_number(release_id, number['child_type'], chapter, 'release', volume_id)
				
			return True
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("An error occurred when trying to run add_release_number(%s, %s)." % (release_id, numbers ))
		finally:
			self.set_auto_transaction(True)
			
		
	"""
		Method used to add a image and associated it with an entity release.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""
	def add_image_to_release(self, url, extension, name, release_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('entity_release', image_id, release_id, image_type_id)
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
	

	"""
		Method used to register all items related with entity release.
		This method must be used instead other specified methods related with entity release.
		
		To use this method the types must be already registered on database.
		The parameters numbers,collaborators and collaborator_members must have elements that are dict.
		Please use only a release per file. If your file contains more than a chapter you can add multiples with this method.
			
		One release for each file.
		
		Release number must be the same amount on release file, e.g, release chapter 1 and 2 on file release 1, so number must be 1-2 to release 1, case release chapter 1 and 2 on each separated file the release must be one for each file.  
	"""
	def create_release(self, entity_id, release_type_id, country_id, release_date = None, entity_edition_id = None, description = None,
	numbers = [], languages_id = [], collaborators = [], collaborator_members = [], images = []):
		
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			release_id = self.add_release(entity_id, release_type_id, country_id, release_date, entity_edition_id, description)
			#register numbers
			self.add_release_number(release_id, numbers)
			
			#register languages
			for language in languages_id:
				self.add_multi_relation(release_id, language, 'entity_release', 'language')
			
			#register collaborator
			for collaborator in collaborators:
				self.add_relation_collaborator_release(collaborator['id'], release_id, collaborator['function_type_id'], 'collaborator')
				
			#register collaborator members
			for member in collaborator_members:
				self.add_relation_collaborator_release(member['id'], release_id, member['function_type_id'], 'collaborator_member', 'produces')
			
			for image in images:
				self.add_image_to_release(image['url'], image['extension'], image['name'], release_id)
			
			#commit changes
			self.commit()
			
			return release_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_release method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to create a game release that is a specialization of entity_release.
		This method as well all other create method will only commit the transaction after all be run successful. 
	"""
	def create_game_release(self, entity_id, release_type_id, country_id, entity_edition_id, 
	installation_instructions = None, emulate = 0, release_date = None, description = None, 
	numbers = [], languages_id = [], collaborators = [], collaborator_members = [], images = []):
		#set commit to false.
		self.set_auto_transaction(False)
			
		try:
			entity_release_id = self.create_release(entity_id, release_type_id, country_id, entity_edition_id, release_date, description,
			numbers, languages_id, collaborators, collaborator_members, images)
			self.add_game_release(entity_release_id, installation_instructions, emulate)
			
			#commit changes
			self.commit()
			return entity_release_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("Some error must have occurred on create_game_release method.")
		finally:
			self.set_auto_transaction(True)
	
	"""
		Method used to create a mod release that is a specialization of entity_release.
		This method as well all other create method will only commit the transaction after all be run successful. 
	"""
	def create_mod_release(self, name, mod_type_id, author_name, entity_id, release_type_id, country_id, entity_edition_id,
	launch_date = None, description = None, installation_instruction = None, images = [], update_id = None):
		
		if(not name):
			raise ValueError("Name cannot be empty on create_mod_release method.")
			
		#set commit to false.
		self.set_auto_transaction(False)
			
		try:
			entity_release_id = self.create_release(self, entity_id, release_type_id, country_id, entity_edition_id, release_date, description,
			numbers, languages_id, collaborators, collaborator_members, images)
			
			self.add_mod_release(name, mod_type_id, entity_release_id, author_name, launch_date, description, installation_instruction, update_id)
			
			
			#commit changes
			self.commit()
			return entity_release_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("Some error must have occurred on create_mod_release method.")
		finally:
			self.set_auto_transaction(True)
	
	"""
		Method used to create a video release that is a specialization of entity_release.
		This method as well all other create method will only commit the transaction after all be run successful. 
	"""
	def create_video_release(self, entity_release_id, duration, video_codec_id, container_id, softsub, resolution, 
	entity_id, release_type_id, country_id, entity_edition_id, audio_codecs = [], release_date = None, description = None,
	numbers = [], languages_id = [], collaborators = [], collaborator_members = [], images = [], update_id = None):
		
		#set commit to false.
		self.set_auto_transaction(False)
			
		try:
			entity_release_id = self.create_release(entity_id, release_type_id, country_id, entity_edition_id, release_date, description,
			numbers, languages_id, collaborators, collaborator_members, images)
			self.add_video_release(entity_release_id, duration, video_codec_id, container_id, softsub, resolution, update_id)
			
			for audio_codec in audio_codecs:
				self.add_relation_with_type('video_release', 'audio_codec', video_release_id, audio_codec['id'], 'has', audio_codec['language_id'], False)

			#commit changes
			self.commit()
			return entity_release_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_video_release method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
	
	################################ Persona methods ##############################
	
	"""
		Method used to insert a persona on database.
		This method don't insert any related item to persona like voice actors or names.
		This method can be use to insert on entity_release table.
	"""
	def add_persona(self, gender, birthday = None, blood_type_id = None, blood_rh_type_id = None, height = None, weight = None, eyes_color = None, hair_color = None, update_id = None):
		if(not gender):
			raise ValueError("Gender cannot be empty on add_persona method.")	
		
		table = 'persona'
		
		#Cannot verify uniqueness.
		
		columns = ['gender']
		value = []
		value.append(gender)
			
		if blood_type_id:
			columns.append('blood_type_id')
			value.append(blood_type_id)	
		if blood_rh_type_id:
			columns.append('blood_rh_type_id')
			value.append(blood_rh_type_id)
		if birthday:
			columns.append('birthday')
			value.append(birthday)
		if height:
			columns.append('height')
			value.append(height)
		if weight:
			columns.append('weight')
			value.append(weight)
		if eyes_color:
			columns.append('eyes_color')
			value.append(eyes_color)
		if hair_color:
			columns.append('hair_color')
			value.append(hair_color)
		
		if update_id:
			where_values = []
			where_values.append(update_id)
			if not self.update(table, value, columns, "id = %s", where_values):
				raise ValueError("An error occurred while trying to update on add_persona(%s, %s, %s, %s, %s, %s, %s, %s)." % (gender, birthday, blood_type_id, height, weight, eyes_color, hair_color, update_id))
			id = update_id	
		else:
			self.insert(table, value,columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_persona(%s, %s, %s, %s, %s, %s, %s, %s)." % (gender, birthday, blood_type_id, height, weight, eyes_color, hair_color, update_id))
		return id
	
	"""
		Method used to insert data related with persona.
		This method can be use to insert on the follow tables:
		persona_occupation, persona_unusual_features, persona_affiliation, persona_race
	"""
	def add_persona_items(self, name, persona_id, item_table):
		if(not name):
			raise ValueError("Name cannot be empty on add_persona_items method.")
		
		if(not item_table):
			raise ValueError("Item table cannot be empty on add_persona_items method.")
			
		if(not persona_id):
			raise ValueError("Persona id cannot be empty on add_persona_items method.")
			
		self.check_id_exists('persona', persona_id)
		
		table = 'persona_' + item_table
		
		where_values = []
		where_values.append(name)
		where_values.append(persona_id)
		id = self.get_id_from_field(table, ['name','persona_id'], where_values)
		
		if(id == None):
			columns = ['persona_id', 'name']
			value = []
			value.append(persona_id)
			value.append(name)

			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_persona_items(%s, %s, %s)." % (name, persona_id, item_table))
		return id
	
	"""
		Method used to insert a alias for a persona.
		This method can be use to insert data on persona_alias table.
	"""
	def add_persona_alias(self, name, persona_id, alias_type_id):
		if(not name):
			raise ValueError("Name cannot be empty on add_persona_items method.")
		
		if(not alias_type_id):
			raise ValueError("Alias type cannot be empty on add_persona_items method.")
			
		self.check_id_exists('persona', persona_id)
		
		table = 'persona_alias'
		
		where_values = []
		where_values.append(name)
		where_values.append(persona_id)
		id = self.get_id_from_field(table, ['name', 'persona_id'], where_values)
		
		if(id == None):
			columns = ['persona_id', 'name', 'alias_type_id']
			value = []
			value.append(persona_id)
			value.append(name)
			value.append(alias_type_id)

			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_persona_alias(%s, %s, %s)." % (name, persona_id, alias_type_id))
		return id
	
	
	"""
		Method used to add a image and associated it with a persona.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""
	def add_image_to_persona(self, url, extension, name, persona_id):
		try:
			image_id = self.add_image(url, extension, name)
			return add_multi_relation(persona_id, image_id, 'persona', 'image')
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)

	"""
		Method used to associate a persona with a entity.
		This method is used to insert on persona_appear_on_entity table.
		
	"""
	def add_persona_to_entity(self, entity_id, persona_id, alias_used_id, first_appear = 0):
		if(not persona_id):
			raise ValueError("Persona id cannot be empty on add_persona_items method.")
			
		if(not entity_id):
			raise ValueError("Entity id cannot be empty on add_persona_items method.")
			
		#print "persona to entity"
		self.check_id_exists('entity', entity_id)
		
		table = 'persona_appear_on_entity'
		
		where_values = []
		where_values.append(entity_id)
		where_values.append(persona_id)
		id = self.get_var(table, ['persona_id'], "entity_id = %s and persona_id = %s",where_values)
		
		if(id == None):
			columns = ['persona_id', 'entity_id', 'first_appear', 'alias_used_id']
			value = []
			value.append(persona_id)
			value.append(entity_id)
			value.append(first_appear)
			value.append(alias_used_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_persona_to_entity(%s, %s, %s, %s)." % (entity_id, persona_id, alias_used_id, first_appear))
		return True
		
	"""
		Method used to register all items related with persona.
		This method must be used instead other specified methods related with persona.
		
		To use this method the types must be already registered on database.
		Alias is to alternative names where nickname is for nickname. 
		Think like Tatsuya alias is Ooguro where his nickname is Mahesvara on Mahou Kokkou no Retousei.
		The parameters entities_appear_on,     must have elements that are dict.
		
		To add a relationship the other persona id on relationship must be already registered on database.
	"""
	def create_persona(self, name, gender, birthday = None, blood_type_id = None, blood_rh_type_id = None, height = None, weight = None, eyes_color = None, hair_color = None,
	unusual_features = [], aliases = [], nicknames = [], occupations = [], affiliations = [], races = [], goods = [], voices_actor = [], entities_appear_on = [],
	relationship = [], images = [], update_id = None):
		if(not name):
			raise ValueError("Name cannot be empty on create_persona method.")
	
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			persona_id = self.add_persona(self, gender, birthday, blood_type_id, blood_rh_type_id, height, weight, eyes_color, hair_color, update_id)
			
			#register main name
			self.add_persona_alias(name, persona_id, self.alias_type_main)
			#register alias
			for alias in aliases:
				self.add_persona_alias(alias, persona_id, self.alias_type_alias)
			
			#register nicknames
			for nick in nicknames:
				self.add_persona_alias(nick, persona_id, self.alias_type_nickname)
			
			#add voices
			for people in voices_actor:
				self.add_relation_people_voice_persona(people['id'], persona_id, people['language_id'], people['entity_id'], people['entity_edition_id'], people['observation'], people['numbers_edition_id'])
			
			#add entity
			for entity in entities_appear_on:
				self.add_persona_to_entity(self, entity['id'], persona_id, entity['alias_used_id'], entity['first_appear'])
				
			#add relationship with another persona
			for unusual_feature in unusual_features:
				self.add_persona_items(unsual_feature, persona_id, 'unusual_features')
				
			for occupation in occupations:
				self.add_persona_items(occupation, persona_id, 'occupation')
					
			for race in races:
				self.add_persona_items(race, persona_id, 'race')
					
			for affiliation in affiliations:
				self.add_persona_items(affiliation, persona_id, 'affiliation')
				
			for good in goods:
				self.add_multi_relation(good['id'], persona_id, 'goods', 'persona', 'from')
				
			for image in images:
				self.add_image_to_persona(image['url'], image['extension'], image['name'], persona_id)
				
			self.commit()
			return persona_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_persona method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
	
		
	############################### Company Methods ###############################
	
	"""
		Method used to insert a company. This method don't insert any related item to company like websites or filial countries.
		This method can be use to insert on entity_edition table.
		
		Countries must be already save on database prior to the usage of this method.
		TODO: Use similarity instead equal on name.
	"""
	def add_company(self, name, country_origin_id, description = None, social_name = None, start_year = None, website = None, foundation_date = None, update_id = None):
		#print name, country_origin_id, description, social_name, start_year, website, foundation_date, update_id
		if(not name):
			raise ValueError("Name cannot be empty on add_company method.")
		
		if(not country_origin_id):
			raise ValueError("country_origin_id cannot be empty on add_company method.")
	
		self.check_id_exists('country', country_origin_id)
		
		table = 'company'
		where_values = []
		where_values.append(name)
		where_values.append(country_origin_id)
		id = self.get_id_from_field(table, ['name','country_id'], where_values)
		if(id == None or update_id):
			columns = ['name']
			value = []
			value.append(name)
			
			if country_origin_id:
				columns.append('country_id')
				value.append(country_origin_id)
			if description:
				columns.append('description')
				value.append(description)
			if social_name:
				columns.append('social_name')
				value.append(social_name)
			if start_year:
				columns.append('start_year')
				value.append(start_year)
			if website:
				columns.append('website')
				value.append(website)
			if foundation_date:
				columns.append('foundation_date')
				value.append(foundation_date)
				
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_company(%s, %s, %s, %s, %s, %s, %s, %s)." % (name, country_origin_id, description, social_name, start_year, website, foundation_date, update_id))
				id = update_id	
			else:
				self.insert(table, value, columns)
			
				id = self.get_last_insert_id(table)
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_company(%s, %s, %s, %s, %s, %s, %s, %s)." % (name, country_origin_id, description, social_name, start_year, website, foundation_date, update_id))
		return id
	
	
	"""
		Method used to insert a relation with company on database.
		This method can be use to insert a relation on the follow tables:
		entity_edition_has_company, entity_has_company, goods_has_company
		
		The parameter relation_table is used as the first part of table name that have _has_company
	"""
	def add_relation_company(self, company_id, second_id, company_function_type_id, relation_table):
		if not company_id:
			raise ValueError("company_id cannot be empty on add_relation_company method.")
		
		if not second_id:
			raise ValueError("second_id cannot be empty on add_relation_company method.")
		
		if not company_function_type_id:
			raise ValueError("company_function_type_id cannot be empty on add_relation_company method.")
			
		if not relation_table:
			raise ValueError("relation_table cannot be empty on add_relation_company method.")
			
		self.check_id_exists('company', company_id)
		
		table = relation_table + '_has_company'
		
		where_values = []
		where_values.append(company_id)
		where_values.append(second_id)
		where_values.append(company_function_type_id)
		id = self.get_var(table, ['company_id'], "company_id = %s and {relation_table}_id = %s and company_function_type_id = %s".format(relation_table=relation_table),where_values)
		if(id == None):
			columns = ['company_id', relation_table + '_id', 'company_function_type_id']
			value = []
			value.append(company_id)
			value.append(second_id)
			value.append(company_function_type_id)

			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_relation_company(%s, %s, %s, %s)." % (company_id, second_id, company_function_type_id, relation_table))
		return True
		
	"""
		Method used to add a image and associated it with an company.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""		
	def add_image_to_company(self, url, extension, name, company_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('entity_edition', image_id, company_id, image_type_id)
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)

	"""
		Method used to register all items related with company.
		This method must be used instead other specified methos related with company.
		
		To use this method the types must be already registered on database.
		The parameters images, editions, entities must have elements that are dict. 
	"""		
	def create_company(self, name, language_id, country_origin_id, description = None, social_name = None, start_year = None, website = None, foundation_date = None, events_sponsored = [], owned_collections = [], countries = [], socials = [], editions = [], entities = [], images = [], alternate_names = [], update_id = None):	
		if not language_id:
			raise ValueError("Language id cannot be empty on create_company method.")
		
		self.set_auto_transaction(False)
		
		try:
			company_id = self.add_company(name, country_origin_id, description, social_name, start_year, website, foundation_date, update_id)
			
			if name:
				self.add_alias(name, company_id, language_id, 'company', self.alias_type_romanized)
			
			#add events sponsored
			for event_sponsored in events_sponsored:
				self.add_multi_relation(company_id, event_sponsored, 'company', 'event', 'sponsors')
			
			for owned_collection in owned_collections:
				self.add_multi_relation(company_id, owned_collection, 'company', 'collection', 'owner')
				
			for country in countries:
				self.add_multi_relation(company_id, country, 'company', 'country')
				
			for edition in editions:
				self.add_relation_company(company_id, edition['id'], edition['company_function_type_id'], 'entity_edition')
				
			for entity in entities:
				self.add_relation_company(company_id, entity['id'], entity['company_function_type_id'], 'entity')
				
			for social in socials:
				self.create_social(social['type_id'], social['url'], 'company', company_id, social['last_checked'])
				
			for image in images:
				self.add_image_to_company(image['url'], image['extension'], image['name'], company_id, image['type_id'])
			
			for alias in alternate_names:
				self.add_alias(alias['name'], company_id, alias['language_id'], 'company', self.alias_type_alias)
			
			self.commit()
			return company_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_company method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			

	
	################################ People Methods ###############################
	
	"""
		Method used to insert a person on database. This method don't insert any related item to a persona like socials or websites.
		This method can be used to insert on people table.
		
		Countries must be already save on database prior to the usage of this method.
	"""
	def add_people(self, country_id, gender = None, birth_place = None, birth_date = None, blood_type_id = None, blood_rh_type_id = None, website = None, description = None, update_id = None):
		if(not country_id):
			raise ValueError("Country id cannot be empty on add_people method.")
		
		
		self.check_id_exists('country', country_id)
		
		table = 'people'
		#cannot check uniqueness
		columns = ['country_id']
		value = []
		value.append(country_id)
		
		if blood_type_id:
			columns.append('blood_type_id')
			value.append(blood_type_id)
			
		if blood_rh_type_id:
			columns.append('blood_rh_type_id')
			value.append(blood_rh_type_id)
			
		if website:
			columns.append('website')
			value.append(website)
			
		if description:
			columns.append('description')
			value.append(description)
			
		if gender:
			if(gender == 'Male' or gender == 'Female'):
				columns.append('gender')
				value.append(gender)
			elif(gender == 'N/A'):
				print "Null gender"
			else:
				columns.append('gender')
				value.append('Undefined')
				
		if birth_place:
			columns.append('birth_place')
			value.append(birth_place)	
			
		if birth_date:
			columns.append('birth_date')
			value.append(birth_date)
			
		if update_id:
			where_values = []
			where_values.append(update_id)
			print where_values
			if not self.update(table, value, columns, "id = %s", where_values):
				raise ValueError("An error occurred while trying to update on add_people(%s, %s, %s, %s, %s, %s, %s, %s)." % (country_id, blood_type_id, gender, birth_place, birth_date, website, description, update_id))
			id = update_id	
		else:
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_people(%s, %s, %s, %s, %s, %s, %s, %s)." % (country_id, blood_type_id, gender, birth_place, birth_date, website, description, update_id))
		return id
	
	
	"""
		Method used to insert a relation with people on database.
		This method can be use to insert a relation on the follow tables:
		people_create_goods, people_produces_entity, people_compose_audio
	
	"""
	def add_relation_people(self, people_id, people_alias_used_id, second_id, relation_table, relation_type_id, relation_type = 'produces'):
		if(not people_id):
			raise ValueError("People id cannot be empty on add_relation_people method.")
		
		if(not relation_table):
			raise ValueError("relation_table cannot be empty on add_relation_people method.")
			
		if(not second_id):
			raise ValueError("Second id cannot be empty on add_relation_people method.")	
			
		if(not relation_type_id):
			raise ValueError("relation_type id cannot be empty on relation_type_id method.")	
			
		self.check_id_exists('people', people_id)
		
		table = 'people_' + relation_type + '_' + relation_table
		#check if already is a relation with the people_id, second_id and relation_type_id.
		where_values = []
		where_values.append(people_id)
		where_values.append(second_id)
		where_values.append(relation_type_id)
		id = self.get_var(table, ['people_id'], "people_id = %s and {relation_table}_id = %s and {relation_type}_type_id = %s".format(relation_table=relation_table, relation_type=relation_type),where_values)
		if(id == None):
			columns = ['people_id', relation_table + '_id', 'people_alias_id', relation_type + '_type_id']
			value = []
			value.append(people_id)
			value.append(second_id)
			value.append(people_alias_used_id)
			value.append(relation_type_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_relation_people(%s, %s, %s, %s, %s, %s)." % (people_id, people_alias_used_id, second_id, relation_table, relation_type_id, relation_type))
		return True
		
	"""
		Method used to insert a name to an people.
		This method can be use to insert on people_alias.
	"""
	def add_people_alias(self, name, lastname, people_id, alias_type_id):
		if(not name):
			raise ValueError("Name cannot be empty on add_people_alias method.")
		
		if(not lastname):
			raise ValueError("Last name id cannot be empty on add_people_alias method.")
			
		if(not people_id):
			raise ValueError("People id cannot be empty on add_people_alias method.")
			
		if(not alias_type_id):
			raise ValueError("alias_type_id id cannot be empty on add_people_alias method.")
			
			
		#check if people_id really exists
		self.check_id_exists('people', people_id)
		
		table = 'people_alias'
		
		where_values = []
		where_values.append(name)
		where_values.append(lastname)
		where_values.append(people_id)
		id = self.get_id_from_field(table, ['name','lastname','people_id'], where_values)
		if(id == None):
			columns = ['name', 'alias_type_id', 'people_id', 'lastname']
			value = []
			value.append(name)
			value.append(alias_type_id)
			value.append(people_id)
			value.append(lastname)
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_people_alias(%s, %s, %s, %s)." % (name, lastname, people_id, alias_type_id))
		return id

	
	"""
		Method used to insert a N:M relationship between People and Persona
		This method can be use to insert on the follow tables:
		people_voice_persona
		
		Language must be already registered on database.

	"""		
	def add_relation_people_persona(self, people_id, persona_id, language_id, entity_id, entity_edition_id, observation = None):
		if(not people_id):
			raise ValueError("People id cannot be empty on add_people_alias method.")
			
		if(not persona_id):
			raise ValueError("People id cannot be empty on add_people_alias method.")
			
		if(not language_id):
			raise ValueError("People id cannot be empty on add_people_alias method.")
			
		if(not entity_id):
			raise ValueError("People id cannot be empty on add_people_alias method.")
			
		if(not entity_edition_id):
			raise ValueError("People id cannot be empty on add_people_alias method.")
			
		#print "relation people persona"
		
		self.check_id_exists('people', people_id)
		self.check_id_exists('persona', persona_id)
		self.check_id_exists('entity', entity_id)
		self.check_id_exists('language', language_id)
		self.check_id_exists('entity_edition', entity_edition_id)
	
		table = 'people_voice_persona'
		
		where_values = []
		where_values.append(persona_id)
		where_values.append(people_id)
		where_values.append(language_id)
		id = self.get_var(table, ['persona_id'], " persona_id = %s and people_id = %s and language_id = %s", where_values) 
		if(id == None):
			columns = ['persona_id','people_id','language_id','entity_id','entity_edition_id']
			value = []
			value.append(persona_id)
			value.append(people_id)
			value.append(language_id)
			value.append(entity_id)
			value.append(entity_edition_id)

			if observation:
				columns.append('observation')
				value.append(observation)
				
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_software_edition(%s, %s, %s, %s, %s, %s)." % (people_id, persona_id, language_id, entity_id, entity_edition_id, observation))
		return True
		
	"""
		Method used to insert on the associated table people_voice_persona_on_number_edition.
		This method must be used only if there is information about the number of episode that a persona was voiced by a people.
		
	"""
	def add_relation_people_persona_on_entity_edition_number(self, people_id, persona_id, language_id, number_id):
		if(not people_id):
			raise ValueError("People id cannot be empty on add_relation_people_persona_on_entity_edition_number method.")
			
		if(not persona_id):
			raise ValueError("People id cannot be empty on add_relation_people_persona_on_entity_edition_number method.")
			
		if(not language_id):
			raise ValueError("People id cannot be empty on add_relation_people_persona_on_entity_edition_number method.")
			
		if(not number_id):
			raise ValueError("Number id cannot be empty on add_relation_people_persona_on_entity_edition_number method.")
		
		self.check_id_exists('people', people_id)
		self.check_id_exists('persona', persona_id)
		self.check_id_exists('number_edition', number_id)
		self.check_id_exists('language', language_id)
		
		table = 'people_voice_persona_on_number_edition'
		
		where_values = []
		where_values.append(persona_id)
		where_values.append(people_id)
		where_values.append(language_id)
		where_values.append(number_id)
		id = self.get_var(table, ['persona_id'], " people_voice_persona_persona_id = %s and people_voice_persona_people_id = %s and people_voice_persona_language_id = %s and number_edition_id = %s", where_values) 
		if(id == None):
			columns = ['people_voice_persona_persona_id', 'people_voice_persona_people_id', 'people_voice_persona_language_id', 'number_edition_id']
			value = []
			value.append(persona_id)
			value.append(people_id)
			value.append(language_id)
			value.append(number_id)
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_software_edition(%s, %s, %s, %s)." % (people_id, persona_id, language_id, number_id))
		return True
		
	"""
		Method used to make a relationship between a person and a persona.
		This method differ from add_relation_people_persona in it receive a number and make a association with  
		the table people_voice_persona_on_number_edition
	"""
	def add_relation_people_voice_persona(self, people_id, persona_id, language_id, entity_id, entity_edition_id, observation = None,
	numbers = []):
		self.set_auto_transaction(False)
		try:
			self.add_relation_people_persona(people_id, persona_id, language_id, entity_id, entity_edition_id, observation)
			for number_id in numbers:
				self.add_relation_people_persona_on_entity_edition_number(people_id, persona_id, language_id, number_id)
			#commit changes
			self.commit()
			return True
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError(e.strerror)
		finally:
			self.set_auto_transaction(True)
	"""
		Method used to add a image and associated it with an people.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""			
	def add_image_to_people(self, url, extension, name, people_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_multi_relation(people_id, image_id, 'people', 'image')
			
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	
	"""
		Method used to register all items related with people.
		This method must be used instead other specified methods related with entity.
		
		To use this method the types must be already registered on database.
		The parameters alias, nicknames, goods,entities_produced and audios_composed must have elements that are dictionary. 
	"""
	def create_people(self, name, lastname, country_id, gender = None, birth_place = None, birth_date = None, blood_type_id = None,blood_rh_type_id = None, website = None, description = None,
	aliases = [], nicknames = [], native_names = [], goods = [], entities_produced = [], audios_composed = [], personas_voiced = [], images = [], socials = [], update_id = None):
		if(not name):
			raise ValueError("Name cannot be empty on create_people method.")
			
		if(not lastname):
			raise ValueError("Last name cannot be empty on create_people method.")
		
		self.set_auto_transaction(False)
		try:
			#print "Here people1"
			#add_people
			people_id = self.add_people(country_id, gender, birth_place, birth_date, blood_type_id, blood_rh_type_id, website, description, update_id)
			
			#print "Here people2"
			#add_people_alias
			self.add_people_alias(name, lastname, people_id, self.alias_type_main)
			
			#print "People alias Main"
			
			for alias in aliases:
				self.add_people_alias(alias['name'], alias['lastname'], people_id, self.alias_type_alias)
			
			#print "People alias"
			for nick in nicknames:
				self.add_people_alias(nick['name'], nick['lastname'], people_id, self.alias_type_nickname)
			
			for native in native_names:
				self.add_people_alias(native['name'], native['lastname'], people_id, self.alias_type_nativename)
			
			for good in goods:
				self.add_relation_people(people_id, good['people_alias_used_id'], good['id'], 'goods', good['people_relation_type_id'], 'create')

			for entity in entities_produced:
				self.add_relation_people(people_id, entity['people_alias_used_id'], entity['id'], 'entity', entity['people_relation_type_id'])

			for audio in audios_composed:
				self.add_relation_people(people_id, audio['people_alias_used_id'], audio['id'], 'audio', audio['people_relation_type_id'], 'compose')

			for persona in personas_voiced:
				self.add_relation_people_voice_persona(people_id, persona['id'], persona['language_id'], persona['entity_id'], persona['entity_edition_id'], persona['observation'], persona['numbers'])

			for image in images:
				self.add_image_to_people(image['url'], image['extension'], image['name'], people_id)
			
			for social in socials:
				self.create_social(social['type_id'], social['url'], 'people', people_id, social['last_checked'])
			
			#commit changes
			self.commit()
			return people_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_people method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
		
			
	################################ Archive Methods ##############################
	
	"""
		Method used to insert a requirement related with a version.
		This method check if version_id really exists prior to insert on table.
	"""
	def add_requirements(self, version_id, video_board, processor, memory, hd_storage):
		if(not version_id):
			raise ValueError("version_id cannot be empty on add_requirements method.")
		
		self.check_id_exists('version', version_id)
		
		table = 'requirements'

		id = self.get_id_from_field(table, 'version_id', version_id)
		
		if(id == None):
			columns = ['version_id', 'video_board', 'processor', 'memory', 'hd_storage']
			value = []
			value.append(version_id)
			value.append(video_board)
			value.append(processor)
			value.append(memory)
			value.append(hd_storage)
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_requirements(%s, %s, %s, %s, %s)." % (version_id, video_board, processor, memory, hd_storage))
		return id
	
	"""
		Method used to insert a driver to a requirement.
		This method check if requirements_id really exists prior to insert on table.
	"""
	def add_driver(self, name, url_download):
		if(not name):
			raise ValueError("Name cannot be empty on add_requirements method.")
		
		self.check_id_exists('requirements', requirements_id)
		
		where_values = []
		where_values.append(name, url_download)
		id = self.get_var('driver', ['id'], "name = %s and url_download = %s",where_values)
		if(id == None):
			columns = ['name', 'url_download']
			value = []
			value.append(name)
			value.append(url_download)
			self.insert('driver', value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_driver(%s, %s)." % (name, url_download))
		return id
	
	"""
		Method used to insert a archive associated with a version
		This method check if version_id really exists prior to insert on table.
	"""
	def add_archive(self, name, version_id, size, extension):
		if(not version_id):
			raise ValueError("version_id cannot be empty on add_archive method.")
			
		if(not name):
			raise ValueError("Name cannot be empty on add_archive method.")
			
		if(not size):
			raise ValueError("size cannot be empty on add_archive method.")
			
		if(not extension):
			raise ValueError("extension cannot be empty on add_archive method.")
			
		self.check_id_exists('version', version_id)
		
		table = 'archive'
		
		where_values = []
		where_values.append(name)
		where_values.append(extension)
		where_values.append(version_id)
		id = self.get_id_from_field(table, ['name', 'extension','version_id'], where_values)
		if(id == None):
			columns = ['name', 'version_id', 'size', 'extension']
			value = []
			value.append(name)
			value.append(version_id)
			value.append(size)
			value.append(extension)
			
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_archive(%s, %s, %s, %s, %s)." % (name, version_id, url, size, extension))
		return id
	
	"""
		Method used to insert a url associated with a archive
		This method check if archive_id really exists prior to insert on table.
	"""
	def add_url_archive(self, archive_id, url, url_type_id):
		if(not archive_id):
			raise ValueError("archive_id cannot be empty on add_archive method.")
			
		if(not url):
			raise ValueError("URL cannot be empty on add_archive method.")
			
		if(not url_type_id):
			raise ValueError("url_type_id cannot be empty on add_archive method.")
			
		self.check_id_exists('archive', archive_id)
		
		table = 'archive_url'
		
		id = self.get_id_from_field(table, 'url', url)
		if(id == None):
			columns = ['url_type_id', 'archive_id', 'url']
			value = []
			value.append(url_type_id)
			value.append(archive_id)
			value.append(url)
			
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_url_archive(%s, %s, %s)." % (archive_id, url, url_type_id))
		return id
		
		
	"""
		Method used to insert a hash associated with a archive
		This method check if archive_id really exists prior to insert on table.
	"""
	def add_hash(self, hash_type_id, archive_id, code):
		if(not hash_type_id):
			raise ValueError("hash_type_id cannot be empty on add_hash method.")
			
		if(not archive_id):
			raise ValueError("archive_id cannot be empty on add_hash method.")
			
		if(not code):
			raise ValueError("code cannot be empty on add_hash method.")

		self.check_id_exists('archive', archive_id)
		
		table = 'hash'
		
		where_values = []
		where_values.append(archive_id,hash_type_id)
		id = self.get_id_from_field(table, ['archive_id','hash_type_id'], where_values)
		if(id == None):
			columns = ['hash_type_id', 'archive_id', 'code']
			value = []
			value.append(hash_type_id)
			value.append(archive_id)
			value.append(code)
			
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_hash(%s, %s, %s)." % (hash_type_id, archive_id, code))
		return id
	

	"""
		Method used to add a version to the version table on database.
		This method don't insert any relationship to version like release version or software edition version.
	"""
	def add_version(self, stage_developer_type_id, number, changelog = None):
		if(not stage_developer_type_id):
			raise ValueError("stage_developer_type_id cannot be empty on add_version method.")
			
		if(not number):
			raise ValueError("Number cannot be empty on add_version method.")
			
		table = 'version'

		columns = ['stage_developer_type_id', 'number']
		value = []
		value.append(stage_developer_type_id)
		value.append(number)
			
		if changelog:
			columns.append('changelog')
			value.append(changelog)
			
		self.insert(table, value, columns)
		
		id = self.get_last_insert_id(table)
		if(id == 0):
			raise ValueError("There is no last insert id to return on add_version(%s, %s, %s)." % (stage_developer_type_id, number, changelog))
		return id
		
	"""
		Method used to insert a archive and the related hash.
		The parameter hashes and urls must have elements that are dictionary. 
	"""		
	def create_archive(self, name, version_id, size, extension, hashes = [], urls = []):
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			archive_id = self.add_archive(name, version_id, url, size, extension)
			
			for hash in hashes:
				self.add_hash(self, hash['type_id'], archive_id, hash['code'])
	
			for url in urls:
				self.add_url_archive(archive_id, url['url'], url['type_id'])
				
			#commit changes
			self.commit()
			return archive_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_archive method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to insert a requirement and the related driver.
		The parameter drivers must have elements that are dictionary. 
	"""		
	def create_requirements(self, version_id, video_board, processor, memory, hd_storage,
	drivers = []):
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			requirement_id = self.add_requirements(self, version_id, video_board, processor, memory, hd_storage)
			
			for driver in drivers:
				driver_id = self.add_driver(driver['name'], driver['url_download'])
				self.add_multi_relation(requirement_id, driver_id, 'requirements', 'driver')
			
			#commit changes
			self.commit()
			return requirement_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_requirements method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
		 
	"""
		Method used to register all items related with version.
		This method must be used instead other specified methods related with version.
		
		To use this method the types must be already registered on database.
		The parameter version_for will be used to know in which relationship to make, if is version for entity_release or for software_edition. 
		The parameter archive and requirements must be a dictionary
	"""
	def create_version(self, version_for_table, version_for_entity_id, stage_developer_type_id, number, changelog, archive = None, requirements = None):
		#set commit to false.
		self.set_auto_transaction(False)
		try:
			version_id = add_version(self, stage_developer_type_id, number, changelog)
			if archive:
				self.create_archive(archive['name'], version_id, archive['url'], archive['size'], archive['extension'], archive['hashes'])
			if requirements:
				self.create_requirements(version_id, requirements['video_board'], requirements['processor'], requirements['memory'], requirements['hd_storage'], requirements['drivers'])
			
			#associate version with entity specified on version_for_table
			self.add_multi_relation(self, version_for_entity_id, version_id, version_for_table, 'version')
			
			#commit changes
			self.commit()
			return version_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_version method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			

			
	############################## Collection Methods #############################
	
	"""
		Method used to insert a collection on database. This method don't insert any related item to a collection like soundtracks.
		This method can be used to insert on collection table.
		
		TODO: check with full text search a collection that have the a entity with similar name
	"""
	def add_collection(self, name, description = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_collection method.")
		
		table = 'collection'
		#register the collection if the collection is mentioned, if not is registered.	
		id = self.get_id_from_name(table, name)
		if(id == None):
			columns = ['name']
			value = []
			value.append(name)
			
			if description:
				columns.append('description')
				value.append(description)
				
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("An error occurred when trying to insert on add_collection(%s, %s)." % (name, description))
		return id
	
	"""
		Method used to register all items related with collection.
		This method must be used instead other specified methods related with collection.
		
		There is no entities to register with collection because a collection is already registered with entity. 
		Because that a collection must be create previous the insertion of entity.
	"""
	def create_collection(self, name, description = None, soundtracks = [], owners = []):
		#set commit to false.
		self.set_auto_transaction(False)
		try:
			collection_id = self.add_collection( name, description)
			
			for soundtrack_id in soundtracks:
				self.add_multi_relation(id, soundtrack_id, 'soundtrack', 'collection', 'integrate')
			
			for owner in owners:
				self.add_multi_relation(owner_id, id, 'company', 'collection', 'owner')
			
			#commit changes
			self.commit()
			return collection_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_collection method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
	

		
	################################# Audio Methods ###############################
	
	"""
		Method used to insert a audio on database. This method don't insert any related item to a audio like soundtracks.
		This method can be used to insert on audio table.
		
	"""
	def add_audio(self, country_id, audio_codec_id, name, duration, bitrate, update_id = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_audio method.")
		
		if(not country_id):
			raise ValueError("country_id cannot be empty on add_audio method.")
		
		self.check_id_exists('country', country_id)
		
		table = 'audio'
		where_values = []
		where_values.append(name)
		where_values.append(country_id)
		where_values.append(duration)
		id = self.get_id_from_field(table, ['name','country_id','duration'], where_values)
		if(id == None or update_id):
			columns = ['country_id', 'audio_codec_id', 'name','duration','bitrate']
			value = []
			value.append(country_id)
			value.append(audio_codec_id)
			value.append(name)
			value.append(duration)
			value.append(bitrate)
			
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_audio(%s, %s, %s, %s, %s, %s)." % (country_id, audio_codec_id, name, duration, bitrate, update_id))
				id = update_id	
			else:			
				self.insert(table, value, columns)
				
				id = self.get_last_insert_id(table)
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_audio(%s, %s, %s, %s, %s, %s)." % (country_id, audio_codec_id, name, duration, bitrate, update_id))
		return id
	
	"""
		Method used to insert a relationship between audio and soundtrack on database.
		This method can be used to insert on the follow tables:
		soundtrack_has_audio
		
	"""
	def add_relation_soundtrack_audio(self, audio_id, soundtrack_id, exclusive):
		if(not soundtrack_id):
			raise ValueError("Name cannot be empty on add_relation_soundtrack_audio method.")
		
		if(not audio_id):
			raise ValueError("country_id cannot be empty on add_relation_soundtrack_audio method.")

		if(not exclusive):
			raise ValueError("exclusive cannot be empty on add_relation_soundtrack_audio method.")
	
		self.check_id_exists('audio', audio_id)
		self.check_id_exists('soundtrack', soundtrack_id)
		
		table = 'soundtrack_has_audio'
		where_values = []
		where_values.append(audio_id)
		where_values.append(soundtrack_id)
		id = get_var(table, ['audio_id'], "audio_id = %s and soundtrack_id = %s", where_values)
		if(id == None):
			columns = ['soundtrack_id','audio_id','exclusive']
			value = []
			value.append(soundtrack_id)
			value.append(audio_id)
			value.append(exclusive)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_relation_soundtrack_audio(%s, %s, %s)." % (audio_id, soundtrack_id, exclusive))
		return True
	
	"""
		Method used to insert a lyric on database. 
		This method can be used to insert on lyric table.
		
		The lyric_type_id must be previously registered on database.
	"""
	def add_lyric(self, lyric_type_id, audio_id, language_id, title, content, user_id = None, update_id = None):
		if(not soundtrack_id):
			raise ValueError("soundtrack_id cannot be empty on add_lyric method.")
		
		if(not audio_id):
			raise ValueError("audio_id cannot be empty on add_lyric method.")

		if(not language_id):
			raise ValueError("Language id cannot be empty on add_lyric method.")
			
		if(not title):
			raise ValueError("Title cannot be empty on add_lyric method.")
			
		if(not content):
			raise ValueError("Content cannot be empty on add_lyric method.")
	
		self.check_id_exists('audio', audio_id)
		self.check_id_exists('language', language_id)
		
		where_values = []
		if user_id:
			where = ['audio_id','language_id','user_id','title','lyric_type_id']
			where_values.append(audio_id)
			where_values.append(language_id)
			where_values.append(user_id)
			where_values.append(title)
			where_values.append(lyric_type_id)
		else:
			where = ['audio_id','language_id','title','lyric_type_id']
			where_values.append(audio_id)
			where_values.append(language_id)
			where_values.append(title)
			where_values.append(lyric_type_id)
			
		table = 'lyric'
		id = self.get_id_from_field(table, where, where_values)
		
		if(id == None or update_id):
			columns = ['lyric_type_id', 'audio_id' ,'language_id', 'title', 'lyric']
			value = []
			value.append(lyric_type_id)
			value.append(audio_id)
			value.append(language_id)
			value.append(title)
			value.append(lyric)
			
			if user_id:
				columns.append('user_id')
				value.append(user_id)
			
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_lyric(%s, %s, %s, %s, %s, %s, %s)." % (lyric_type_id, audio_id, language_id, title, content, user_id, update_id))
				id = update_id	
			else:
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_lyric(%s, %s, %s, %s, %s, %s, %s)." % (lyric_type_id, audio_id, language_id, title, content, user_id, update_id))
		return id
	
	
	"""
		Method used to insert a soundtrack on database. This method don't regiter anything related with soundtrack, like tracks (also know as audio) 
		This method can be used to insert on lyric table.
		
		The lyric_type_id must be previously registered on database.
		
	"""
	def add_soundtrack(self, name, type_id, launch_year, launch_country_id, code = None, update_id = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_soundtrack method.")
			
		if(not type_id):
			raise ValueError("type_id cannot be empty on add_soundtrack method.")
			
		if(not launch_year):
			raise ValueError("launch_year cannot be empty on add_soundtrack method.")
		
		if(not launch_country_id):
			raise ValueError("launch_country_id cannot be empty on add_soundtrack method.")
		
		self.check_id_exists('country', launch_country_id)
		
		table = 'soundtrack'
		
		where_values = []
		if code:
			where = ['soundtrack_type_id','name','launch_year','country_id','code']
			where_values.append(type_id)
			where_values.append(name)
			where_values.append(launch_year)
			where_values.append(launch_country_id)
			where_values.append(code)
		else:
			where = ['soundtrack_type_id','name','launch_year','country_id']
			where_values.append(type_id)
			where_values.append(name)
			where_values.append(launch_year)
			where_values.append(launch_country_id)
		
		id = self.get_id_from_field(table, where, where_values)
		if(id == None or update_id):
			columns = ['soundtrack_type_id', 'name' ,'launch_year', 'country_id', 'code']
			value = []
			value.append(type_id)
			value.append(name)
			value.append(launch_year)
			value.append(launch_country_id)
			value.append(code)

			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_soundtrack(%s, %s, %s, %s, %s, %s)." % (url, name, type_id, launch_year, launch_country_id, code, update_id))
				id = update_id	
			else:
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_soundtrack(%s, %s, %s, %s, %s, %s)." % (url, name, type_id, launch_year, launch_country_id, code, update_id))
		return id
	
	"""
		Method used to add a image and associated it with an audio.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""	
	def add_image_to_audio(self, url, extension, name, audio_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('audio', image_id, audio_id, image_type_id)
			
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	"""
		Method used to add a image and associated it with an soundtrack.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""	
	def add_image_to_soundtrack(self, url, extension, name, soundtrack_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('soundtrack', image_id, soundtrack_id, image_type_id)
			
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	"""
		Method used to register all items related with audio.
		This method must be used instead other specified methods related with entity.
		
		To use this method the types must be already registered on database.
		The parameters titles must have elements that are dict. 
	"""		
	def create_audio(self, country_id, audio_codec_id, name, duration, bitrate,	soundtracks = [], lyrics = [], images = [], user_id = None, update_id = None):
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			audio_id = self.add_audio(country_id, audio_codec_id, name, duration, bitrate, update_id)
			
			for soundtrack in soundtracks:
				self.add_relation_soundtrack_audio(audio_id, soundtrack['id'], soundtrack['exclusive'])
			
			for lyric in lyrics:
				self.add_lyric(lyric['type_id'], audio_id, lyric['language_id'], lyric['title'], lyric['content'], lyric['user_id'])
			
			for image in images:
				self.add_image_to_audio(image['url'], image['extension'], image['name'], audio_id, image['type_id'])
				
			#commit changes
			self.commit()
			return audio_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_audio method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
	
	"""
		Method used to register all items related with soundtrack.
		This method must be used instead other specified methods related with entity.
		
		To use this method the types must be already registered on database.
		The parameters titles must have elements that are dict. 
	"""	
	def create_soundtrack(self, name, type_id, launch_year, launch_country_id, code = None,	collections = [], audios = [], images = [], update_id = None):
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			soundtrack_id = self.add_soundtrack(name, type_id, launch_year, launch_country_id, code, update_id)
			
			for collection in collections:
				self.add_multi_relation(soundtrack_id, collection, 'soundtrack', 'collection', 'integrate')
				
			for image in images:
				self.add_image_to_soundtrack(image['url'], image['extension'], image['name'], audio_id, image['type_id'])
				
			#commit changes
			self.commit()
			return soundtrack_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_soundtrack method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)	
				
	
	
	################################# Figure Methods ##############################
	
		
	"""
		Method used to insert a goods on database. This method don't insert any related item to a good like title.
		This method can be used to insert on goods table. Figure is specialization from Goods.
		
	"""
	def add_goods(self, goods_type_id, height, collection_id = None, width = None, weight = None, observation = None, has_counterfeit = 0, collection_started = 0, update_id = None):
		if(not goods_type_id):
			raise ValueError("goods_type_id cannot be empty on add_goods method.")
			
		if(not height):
			raise ValueError("Height cannot be empty on add_goods method.")
		
		table = 'goods'
		
		columns = [ 'goods_type_id', 'height', 'has_counterfeit', 'collection_started']
		value = []
		value.append(goods_type_id)
		value.append(height)
		value.append(has_counterfeit)
		value.append(collection_started)
			
		if collection_id:
			columns.append('collection_id')
			value.append(collection_id)
		if width:
			columns.append('width')
			value.append(width)
		if weight:
			columns.append('weight')
			value.append(weight)
		if observation:
			columns.append('observation')
			value.append(observation)
		
		if update_id:
			where_values = []
			where_values.append(update_id)
			if not self.update(table, value, columns, "id = %s", where_values):
				raise ValueError("An error occurred while trying to update on add_goods(%s, %s, %s, %s, %s, %s, %s, %s, %s)." % (goods_type_id, height, collection_id, width, weight, observation, has_counterfeit, collection_started, update_id))
			id = update_id	
		else:
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_goods(%s, %s, %s, %s, %s, %s, %s, %s, %s)." % (goods_type_id, height, collection_id, width, weight, observation, has_counterfeit, collection_started, update_id))
		return id
	
	"""
		Method used to insert a description to a goods.
		This method can be use to insert on goods_description.
		
		TODO: Change method and table goods_description to register user who send the description. Allow multiples descriptions.
	"""
	def add_goods_description(self, goods_id, language_id, description):
		if(not description):
			raise ValueError("Description cannot be empty on add_goods_description method.")
			
		table = 'goods_description'
		
		columns = ['goods_id', 'language_id', 'description']
		value = []
		value.append(goods_id)
		value.append(language_id)
		value.append(description)
		
		if(self.insert(table, value, columns) == False):
			raise ValueError("An error occurred when trying to insert on add_goods_description(%s, %s, %s)." % (goods_id, language_id, description))
		return True
				
	"""
		Method used to add a relationship between goods and shops table.
		This method will insert data on the follow tables:
		goods_has_shops

	"""
	def add_goods_relation_shops(self, goods_id, shop_id, product_url):
		if(not goods_id):
			raise ValueError("goods_id cannot be empty on add_goods method.")
		
		if(not shop_id):
			raise ValueError("shop_id cannot be empty on add_goods method.")
		
		self.check_id_exists('goods', goods_id)
		
		table = 'goods_has_shops'
		#if already is registered on database update the checked_last
		where_values = []
		where_values.append(goods_id)
		where_values.append(shop_id)
		where_values.append(product_url)
		id = self.get_var(table, ['social_id'], "goods_id = %s and shops_id = %s and product_url = %s", where_values)
		if(id == None):
			columns = ['goods_id', 'shops_id', 'product_url']
			value = []
			value.append(goods_id)
			value.append(shop_id)
			value.append(product_url)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("There is no last insert id to return on add_goods_relation_shops(%s, %s, %s)." % (goods_id, shop_id, product_url))
			return True
		#else update last checked.
		else:
			where_value = []
			where_value.append(goods_id)
			where_value.append(shop_id)
			where_value.append(product_url)
			if(self.update(table, ['now()'], ['checked_last'], "goods_id = %s and shops_id = %s and product_url = %s", where_value) == False):
				raise ValueError("An error occurred while trying to update last_checked on add_goods_relation_shops(%s, %s, %s)." % (goods_id, shop_id, product_url))
			return True
	
	"""
		Method used to insert a shop on the database. 
		This method not insert anything related with the shop like goodss associated.
	"""
	def add_shops(self, name, url = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_name_to_table method.")
	
		where_values = []
		if url:
			where = ['name','url']
			where_values.append(name)
			where_values.append(url)
		else:
			where = ['name']
			where_values.append(name)
			
		table = 'shops'
		id = self.get_id_from_field(table, where, where_values)
		if(id == None):
			columns = ['name']
			value = []
			value.append(name)
			if url:
				columns.append('url')
				value.append(url)
			
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_shops(%s, %s)." % (name,url))
		return id
	
	
	"""
		Method used to add a image and associated it with an goods.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""	
	def add_image_to_goods(self, url, extension, name, goods_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('goods', image_id, goods_id, image_type_id)
			
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	"""
		Method used to insert a figure to the specialization of goods table.
		This method can be used to insert on figure table. 
		This method require a goods_id to register, if you would like to add a goods and a figure with 
		the same method use create_figure method instead.
	"""
	def add_figure(self, goods_id, figure_version_id, scale_id):
		if(not goods_id):
			raise ValueError("goods id cannot be empty on add_figure method.")
		
		if(not figure_version_id):
			raise ValueError("figure_version_id cannot be empty on add_figure method.")
		
		if(not scale_id):
			raise ValueError("scale_id cannot be empty on add_figure method.")
			
		#check if entity_release really exists
		self.check_id_exists('goods', goods_id)
		
		table = 'figure'
		
		where_values = []
		where_values.append(goods_id)
		id = self.get_var(table, ['goods_id'], "goods_id = %s",where_values)
		if(id == None):
			columns = ['goods_id', 'figure_version_id', 'scale_id']
			value = []
			value.append(goods_id)
			value.append(scale_id)
			value.append(figure_version_id)
				
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_figure(%s, %s, %s)." % ( goods_id, figure_version_id, scale_id))
		return id

	
	"""
		Method used to register all items related with shops.
		This method must be used instead other specified methods related with shops.
		
		To use this method the types must be already registered on database.
		The parameters goodss must have elements that are dictionary. 
	"""
	def create_shops(self, name, url = None, goods = []):
	
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			shop_id = self.add_shops(self, name, url)
			for good in goods:
				self.add_goods_relation_shops(good['id'], shop_id, good['product_url'])
			
			#commit changes
			self.commit()
			return shop_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_shops method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to register all items related with shops.
		This method must be used instead other specified methods related with shops.
		
		To use this method the types must be already registered on database.
		The parameters goods must have elements that are dictionary. 
	"""
	def create_goods(self, romanize_title, language_id, goods_type_id, height, collection_id = None, width = None, weight = None, observation = None, has_counterfeit = 0, collection_started = 0,
	aliases = [], descriptions = [], categories = [], tags = [], materials = [], personas = [], companies = [], countries = [], shops_location =[], peoples = [], images = [], update_id = None):
		if(not romanize_title):
			raise ValueError("romanize_title cannot be empty on create_goods method.")
		
		if(not language_id):
			raise ValueError("Language id cannot be empty on create_goods method.")
		
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			goods_id = self.add_goods(goods_type_id, height, collection_id, width, weight, observation, has_counterfeit, collection_started, update_id)
			
			#romanized name
			self.add_alias(romanize_title, goods_id, language_id, 'goods', self.alias_type_romanized)
			
			#alias
			for alias in aliases:
				self.add_alias(alias['name'], goods_id, alias['language_id'], 'goods', alias['alias_type_id'])
				
			#descriptions
			for description in descriptions:
				self.add_goods_description(goods_id, description['language_id'], description['description'])
			
			#category
			for category in categories:
				self.add_multi_relation(goods_id, category, 'goods', 'category')
			
			#tags
			for tag in tags:
				self.add_multi_relation(goods_id, tag, 'goods', 'tag')
			
			#material
			for material in materials:
				self.add_multi_relation(goods_id, material, 'goods', 'material')
			
			#goods persona
			for persona in personas:
				self.add_multi_relation(goods_id, persona, 'goods', 'persona', 'from')
	
			#company
			for company in companies:
				self.add_relation_company(company['id'], goods_id, company['function_type_id'], 'goods')
			
			#Add launch countries
			for launch in countries:
				self.add_to_launch_country(goods_id, launch['country_id'], launch['date'], launch['price'], launch['currency_id'], 'goods')
				
			
			#shop location (local de compra)
			for shop in shops_location:
				self.add_multi_relation(goods_id, shop, 'goods', 'shop_location')
			
			#people
			for people in peoples:
				self.add_relation_people(people['id'], people['alias_id'], goods_id, 'goods', people['function_type_id'], 'create')
				
			#images
			for image in images:
				self.add_image_to_goods(image['url'], image['extension'], image['name'], goods_id, image['image_type_id'])
		
			#commit changes
			self.commit()
			
			return goods_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_goods method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to create a figure that is a specialization of goods.
		This method as well all other create method will only commit the transaction after all be run successful. 
	"""
	def create_figure(self, figure_version_id, scale_id, romanize_title, language_id, goods_type_id, height, 
	collection_id = None, width = None, weight = None, observation = None, has_counterfeit = 0, collection_started = 0,
	aliases = [], descriptions = [], categories = [], tags = [], materials = [], personas = [], companies = [], countries = [], shops_location =[], peoples = [], images = []):
		
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			goods_id = self.create_goods(romanize_title, language_id, goods_type_id, height, collection_id, width, weight, observation, has_counterfeit, collection_started, aliases, descriptions, categories, tags, materials, personas, companies, countries, shops_location, peoples, images)
			self.add_figure(goods_id, figure_version_id, scale_id)
			
			#commit changes
			self.commit()
			return goods_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_figure method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			
	################################# Event methods ###############################
		
	"""
		Method used to insert a event on database.
		This method don't insert anything related with the event like edition launches or goods launch.
	"""
	def add_event(self, name, edition, date, country_id, location = None, website = None, duration = None, free = 0, update_id = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_event methsod.")	
		
		if(not edition):
			raise ValueError("Edition cannot be empty on add_event method.")	
		
		if(not date):
			raise ValueError("Date cannot be empty on add_event method.")	
			
		table = 'event'
		where_values = []
		where_values.append(name)
		where_values.append(edition)
		id = self.get_id_from_field(table, ['name', 'edition'], where_values)
		if(id == None or update_id):
			columns = ['name', 'edition', 'date', 'country_id', 'free']
			value = []
			value.append(name)
			value.append(edition)
			value.append(date)
			value.append(country_id)
			value.append(free)
			
			if location:
				columns.append('location')
				value.append(location)
			
			if website:
				columns.append('website')
				value.append(website)
			
			if duration:
				columns.append('duration')
				value.append(duration)
				
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_event(%s, %s, %s, %s, %s, %s, %s, %s, $s)." % (name, edition, date, country_id, location, website, duration, free, update_id))
				id = update_id	
			else:
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_event(%s, %s, %s, %s, %s, %s, %s, %s, $s)." % (name, edition, date, country_id, location, website, duration, free, update_id))
		return id
	
	"""
		Method used to register all items related with entity.
		This method must be used instead other specified methods related with event.
		
		Event has sponsor, country and entity_edition, but entity_edition and host_country is already related on create_edition and add_event 
	"""
	def create_event(self, name, edition, date, country_id, location = None, website = None, duration = None, free = 0, sponsors = [], update_id = None):
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			event_id = self.add_event(name, edition, date, location, website, duration, free, update_id)
			
			for sponsor_id in sponsors:
				self.add_multi_relation(self, sponsor_id, event_id, 'company', 'event', 'sponsors')
			
			#commit changes
			self.commit()
			return event_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_event method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
			

	
	############################## Collaborator methods ###########################
	
	"""
		Method used to insert a collaborator on database. This method don't insert any related item to a collaborator.
		This method can be used to insert on collaborator table.
		
		Country must be already registered before use this method.
	"""
	def add_collaborator(self, name, country_id, description = None, irc = None, foundation_date = None, update_id = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_collaborator method.")
		
		if(not country_id):
			raise ValueError("Country id cannot be empty on add_collaborator method.")
		
		#check_id not working correct in this method.
		self.check_id_exists('country', country_id)
	
		table = 'collaborator'

		where_values = []
		where_values.append(name)
		where_values.append(country_id)
		
		id = self.get_id_from_field(table, ['name', 'country_id'], where_values)
		
		if(id == None or update_id):
			columns = ['name', 'country_id']
			value = []
			value.append(name)
			value.append(country_id)
			
			if irc:
				columns.append('irc')
				value.append(irc)
			
			if description:
				columns.append('description')
				value.append(description)
			
			if foundation_date:
				columns.append('foundation_date')
				value.append(foundation_date)
			
			if update_id:
				where_values = []
				where_values.append(update_id)
				if not self.update(table, value, columns, "id = %s", where_values):
					raise ValueError("An error occurred while trying to update on add_collaborator(%s, %s, %s, %s, %s, %s)." % (name, country_id, description, irc, foundation_date, update_id))
				id = update_id
			else:
				self.insert(table, value, columns)
				id = self.get_last_insert_id(table)
				if(id == 0):
					raise ValueError("There is no last insert id to return on add_collaborator(%s, %s, %s, %s, %s, %s)." % (name, country_id, description, irc, foundation_date, update_id))
		return id
	
	"""
		Method used to insert a member on database. This method don't insert any related item to a member and do not related a member with a collaborator.
		This method can be used to insert on member table.
		This method only add a new member, to add and associate a member to a collaborator use add_collaborator_member.
	"""
	def add_member(self, name, active = 1):
		if(not name):
			raise ValueError("Name cannot be empty on add_collaborator method.")
		
		table = 'collaborator_member'
		
		id = self.get_id_from_name(table, name)
		if(id == None):
			columns = ['name', 'active']
			value = []
			value.append(name)
			value.append(active)
			
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_member(%s, %s)." % (name, active))
		return id
	
	
	"""
		Method used to associate a member to a collaborator.
		This method add member to a existent collaborator.
	
	"""
	def add_collaborator_member(self, collaborator_id, name, active = 1, founder = 0):
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			member_id = add_member(name, active)
			self.add_relation_collaborator_member(collaborator_id, id, founder)
			
			#commit changes
			self.commit()
			return True
		except ValueError as e:
			print e.message
			self.rollback()
			return False
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to related the member with a collaborator.
		This method can be used to insert on the follow tables:
		collaborator_has_collaborator_member
	"""
	def add_relation_collaborator_member(self, collaborator_id, member_id, founder = 0):
		if(not collaborator_id):
			raise ValueError("Collaborator id cannot be empty on add_relation_collaborator_member method.")
			
		if(not member_id):
			raise ValueError("Member id cannot be empty on add_relation_collaborator_member method.")
			
		table = 'collaborator_has_collaborator_member'
		
		where_values = []
		where_values.append(collaborator_id)
		where_values.append(member_id)
		id = self.get_var(table, ['collaborator_id'], "collaborator_id = %s and collaborator_member_id = %s",where_values)
		if(id == None):
			columns = ['collaborator_id', 'collaborator_member_id', 'founder']
			value = []
			value.append(collaborator_id)
			value.append(member_id)
			value.append(founder)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred on inserting on add_relation_collaborator_member(%s, %s, %s)." % (collaborator_id, member_id, founder))
		return True
	
	"""
		Method used to related the collaborator with a entity_release.
		This method can be used to insert on the follow tables:
		collaborator_provides_entity_release, collaborator_member_produces_entity_release
	"""
	def add_relation_collaborator_release(self, collaborator_id, release_id, function_type_id, first_table, relation = 'provides'):
		if(not collaborator_id):
			raise ValueError("collaborator_id cannot be empty on add_name_to_table method.")
	
		if(not release_id):
			raise ValueError("release_id cannot be empty on add_name_to_table method.")
			
		if(not function_type_id):
			raise ValueError("function_type_id cannot be empty on add_name_to_table method.")
	
		if(not first_table):
			raise ValueError("first_table cannot be empty on add_name_to_table method.")
	
		
		table = first_table + '_' + relation + '_entity_release'
		
		where_values = []
		where_values.append(collaborator_id)
		where_values.append(release_id)
		id = self.get_var(table, ['collaborator_id'], "{first_table}_id = %s and entity_release_id = %s".format(first_table=first_table), where_values)
		
		if(id != None):
			columns = [first_table + '_id', 'entity_release_id', first_table + '_type_id']
			value = []
			value.append(collaborator_id)
			value.append(release_id)
			value.append(function_type_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to add on add_relation_collaborator_release(%s, %s, %s, %s, %s)." % (collaborator_id, release_id, function_type_id, first_table, relation))
		return True
	
	"""
		Method used to add a website to a collaborator.
	
	"""
	def add_collaborator_website(self, collaborator_id, website):
		if(not collaborator_id):
			raise ValueError("collaborator_id cannot be empty on add_collaborator_website method.")
	
		if(not website):
			raise ValueError("website cannot be empty on add_collaborator_website method.")
	
		table = 'collaborator_website'
		
		where_values = []
		where_values.append(collaborator_id)
		where_values.append(website)
		id = self.get_var(table, ['collaborator_id'], "collaborator_id = %s and website = %s",where_values)
		
		if(id == None):
			columns = ['collaborator_id', 'website']
			value = []
			value.append(collaborator_id)
			value.append(website)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to insert on add_collaborator_website(%s, %s)." % (collaborator_id, website))
		return True
		
	"""
		Method used to add a image and associated it with a collaborator.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""
	def add_image_to_collaborator(self, url, extension, name, collaborator_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('collaborator', image_id, collaborator_id, image_type_id)
			
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
			
	"""
		Method used to register all items related with collaborator.
		This method must be used instead other specified methods related with collaborator.
		
		To use this method the types must be already registered on database.
		The parameters members, releases, images, socials must have elements that are dictionary. 
	"""
	def create_collaborator(self, name, country_id, description = None, irc = None, foundation_date = None,
	members = [], releases = [], images = [], socials = [], websites = [], update_id = None
	):
		self.set_auto_transaction(False)
		try:
			collaborator_id = self.add_collaborator(name, country_id, description, irc, foundation_date, update_id)
			
			for member in members:
				self.add_collaborator_member(collaborator_id, member['name'], member['active'], member['founder'])
				
			for release in releases:
				self.add_relation_collaborator_release(collaborator_id, release['id'], release['collaborator_function_type_id'], 'collaborator')
				
				for member in release['members']:
					self.add_relation_collaborator_release(member['id'], release['id'], member['function_type_id'], 'collaborator_member', 'produces')
			
			for image in images:
				self.add_image_to_collaborator(image['url'], image['extension'], image['name'], collaborator_id, image['type_id'])
				
			for social in socials:
				self.create_social(social['type_id'], social['url'], 'collaborator', collaborator_id, social['last_checked'])
				
			for website in websites:
				self.add_collaborator_website(collaborator_id, website)
			
			#commit changes
			self.commit()
			return collaborator_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("An error occurred while trying to save a collaborator on create_collaborator.")
		finally:
			self.set_auto_transaction(True)


	################################# Social Methods ##############################
	
	"""
		Method used to insert a social type.
		This method can be use to insert on social_type table.
		
	"""
	def add_social_type(self, name, website, website_secure = None):
		if(not name):
			raise ValueError("Name cannot be empty on add_social_type method.")
	
		if(not website):
			raise ValueError("Website cannot be empty on add_social_type method.")
	
		table = 'social_type'
		
		#insert on table if there isnt the name on table . 
		id = self.get_id_from_name(table, name)
		if(id == None):
			columns = ['name', 'website']
			value = []
			value.append(name)
			value.append(website)
			
			if website_secure:
				columns.append('website_secure')
				value.append(website_secure)
			
			#insert = self.insert(table, value, columns)
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			#print insert
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_social_type(%s, %s, %s)." % (name, website, website_secure))
		return id	
	
	
	"""
		Method used to create a social type from a given url.
	"""
	def create_social_type_from_url(self, website):
		url = urlparse.urlparse(website)
		new_url = []
		#print url
		#Get name from domain
		domain = re.sub(r'^ww[w0-9]{1,}.', '', url.netloc) 
		domain = domain.split('.')
		name = domain[0].capitalize()
		#Get url from social link
		new_url.append(url[0])
		new_url.append(url[1])
		new_url.append("")
		new_url.append("")
		new_url.append("")
		new_url.append("")

		link = urlparse.urlunparse(new_url)
		#Get url secure
		new_url[0] = 'https'
		link_secure = urlparse.urlunparse(new_url)
		try:
			return self.add_social_type(name, link, link_secure)
		except ValueError as e:
			print e.message
			raise ValueError(e.message)
			
				
	"""
		Method used to insert a social.
		This method don't insert any related data like relation between a people and a social. To insert a social and a relation use create_social.
		Social type must be already registered on the database.
		
	"""
	def add_social(self, social_type_id, url):
		if(not url):
			raise ValueError("URL cannot be empty on add_social method.")
	
		table = 'social'
		
		id = self.get_id_from_field(table, 'url', url)
		if(id == None):
			columns = ['social_type_id', 'url']
			value = []
			value.append(social_type_id)
			value.append(url)
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_image(%s, %s)." % (social_type_id, url))
		return id
		
	"""
		Method used to insert a relationship between social and other table.
		This method can be used to insert on the follow tables:
		users_has_social, people_has_social, collaborator_has_social, company_has_social	
		
	"""
	def add_relation_social(self, relation_table, social_id, second_id, last_checked = None):
		if(not relation_table):
			raise ValueError("relation_table cannot be empty on add_relation_social method.")
		
		if(not social_id):
			raise ValueError("social_id cannot be empty on add_relation_social method.")
		
		if(not second_id):
			raise ValueError("second_id cannot be empty on add_relation_social method.")
		
		self.check_id_exists('social', social_id)
		
		table = relation_table + "_has_social"
		
		where_values = []
		where_values.append(social_id)
		where_values.append(second_id)
		id = self.get_var(table, ['social_id'], "social_id = %s and {relation_table}_id = %s".format(relation_table=relation_table),where_values)
		if(id == None):
			columns = ['social_id', relation_table + '_id']
			value = []
			value.append(social_id)
			value.append(second_id)
			
			if last_checked:
				columns.append('last_checked')
				value.append(last_checked)

			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to insert on add_relation_social(%s, %s, %s, %s)." % (relation_table, social_id, second_id, last_checked))
			return True
		#else update last checked.
		else:
			where_value = []
			where_value.append(social_id)
			where_value.append(second_id)
			if(self.update(table, ['now()'], ['last_checked'], "social_id = %s and {relation_table}_id = %s".format(relation_table=relation_table), where_value) == False):
				raise ValueError("An error occurred while trying to update last_checked on add_relation_social(%s, %s, %s, %s)." % (relation_table, social_id, second_id, last_checked))
			return True
	
	"""
		Method used to register all items related with social.
		This method must be used instead other specified methods related with social.
		
		To use this method the types must be already registered on database. 
	"""
	def create_social(self, social_type_id, url, relation_table, second_id, last_checked = None):	
		
		#set commit to false.
		self.set_auto_transaction(False)
			
		try:
			social_id = self.add_social(social_type_id, url)
			
			self.add_relation_social(relation_table, social_id, second_id, last_checked)
			
			#commit changes
			self.commit()
			
			return social_id
	
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("return id is equal to 0 on create_edition method. Some error must have occurred.")
		finally:
			self.set_auto_transaction(True)
		
		
		

	############################## Localization Methods ###########################

	"""
		Method used to insert a country or language to the database.
		This method can be used to insert on the follow tables:
		country, language
		
	"""
	def add_localization(self, name, code, type = 'country'):
		if(not name):
			raise ValueError("Name cannot be empty on add_localization method.")
		
		if(not code):
			raise ValueError("Code cannot be empty on add_localization method.")
		
		if(type != 'country'):
			type = 'language'
			
		id = self.get_id_from_name(type, name)
		if(id == None):
			columns = ['name', 'code']
			value = []
			value.append(name)
			value.append(code)
			
			self.insert(type, value, columns)
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_localization(%s, %s, %s)." % (name, code, type))
		return id
		
	"""
		Method used to insert a relation between country and currency.
	"""
	def add_relation_country_currency(self, country_id, currency_id, main_currency = 1):
		if(not country_id):
			raise ValueError("country_id cannot be empty on add_name_to_table method.")
	
		if(not currency_id):
			raise ValueError("currency_id cannot be empty on add_name_to_table method.")
	
		self.check_id_exists('country', country_id)
		self.check_id_exists('currency', currency_id)
		
		table = 'country_has_currency'
		
		where_values = []
		where_values.append(currency_id)
		where_values.append(country_id)
		id = self.get_var(table, ['currency_id'], "currency_id = %s and country_id = %s",where_values)
		
		if(id == None):
			columns = ['currency_id','country_id','main']
			value = []
			value.append(currency_id)
			value.append(country_id)
			value.append(main_currency)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to insert on add_relation_country_currency(%s, %s, %s)." % (country_id, currency_id, main_currency))
		return True
	
	
	"""
		Method used to insert a currency on the database.
	
	"""
	def add_currency(self, name, symbol, code):
		if(not name):
			raise ValueError("Name cannot be empty on add_currency method.")
			
		if(not code):
			raise ValueError("code cannot be empty on add_currency method.")
			
		if(not symbol):
			raise ValueError("symbol cannot be empty on add_currency method.")
		
		table = 'currency'
		id = self.get_id_from_field(table, 'code', code)
		if(id == None):
			columns = ['name', 'symbol', 'code']
			value = []
			value.append(name)
			value.append(symbol)
			value.append(code)
			
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_currency(%s, %s, %s)." % (name, symbol, code))
		return id
		
		
	################################## Lists Methods ##############################
	
	"""
		Method used to insert data on lists from users.
		This method can be used for the follow tables:
		lists_edition, lists_release, lists_goods
	
	"""
	def add_list(self, name, user_id, type = 'edition', entity_type_id = 0):
		if(not name):
			raise ValueError("Name cannot be empty on add_list method.")
		
		if(not user_id):
			raise ValueError("user_id cannot be empty on add_list method.")
		
		self.check_id_exists('users', user_id)
		
		
		where_values = []
		#check if already is a lists with this name
		if(type == 'goods'):
			field = ['user_id','name']
			where_values.append(user_id)
			where_values.append(name)
		else:
			where =  "user_id = {user_id} and name = '{name}' and entity_type_id = {entity_type_id}".format(user_id=user_id, name=name, entity_type_id=entity_type_id)
			field = ['user_id','name','entity_type_id']
			where_values.append(user_id)
			where_values.append(name)
			where_values.append(entity_type_id)
			
		table = 'lists_' + type
		
		id = self.get_id_from_field(table, field, where_values)
		if(id == None):
			columns = ['user_id', 'name']
			value = []
			value.append(user_id)
			value.append(name)
			
			if(type != 'goods'):
				columns.append('entity_type_id')
				value.append(entity_type_id)
			self.insert(table, value, columns)

			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_list(%s, %s, %s, %s)." % (name, user_id, type, entity_type_id))
		return id
	
	"""
		Method used to add a release to a list by the user.
		This method can be used to insert on lists_release_list_entity_release table.
	"""
	def add_release_to_list(self, list_id, entity_id, read_status_type_id, ownership_type_id, local_storage = None):
		if(not entity_id):
			raise ValueError("entity_id cannot be empty on add_release_to_list method.")
		
		if(not list_id):
			raise ValueError("list_id cannot be empty on add_release_to_list method.")
		
		if(not read_status_type_id):
			raise ValueError("read_status_type_id cannot be empty on add_release_to_list method.")
		
		if(not ownership_type_id):
			raise ValueError("ownership_type_id cannot be empty on add_release_to_list method.")
		
		self.check_id_exists('lists_release', list_id)
		
		where_values = []
		where_values.append(list_id)
		where_values.append(entity_id)
		table = 'lists_release_list_entity_release'
		id = self.get_var(table, ['lists_release_id'], "lists_release_id = %s and entity_release_id = %s",where_values)
		if(id == None):
			columns = ['lists_release_id', 'entity_release_id', 'release_edition_read_status_type_id', 'release_ownership_type_id', 'local_storage']
			value = []
			value.append(list_id)
			value.append(entity_id)
			value.append(read_status_type_id)
			value.append(ownership_type_id)
			
			if local_storage:
				columns.append('local_storage')
				value.append(local_storage)
				
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to insert on  add_release_to_list(%s, %s, %s, %s, %s)." % (list_id, entity_id, read_status_type_id, ownership_type_id, local_storage))
		return True

	"""
		Method used to add a goods to a list by the user.
		This method can be used to insert on lists_goods_list_goods table.
	"""
	def add_goods_to_list(self, list_id, goods_id, ownership_status_id, box_condition_type_id, product_condition_type_id, observation = None):
		if(not goods_id):
			raise ValueError("goods_id cannot be empty on add_release_to_list method.")
		
		if(not list_id):
			raise ValueError("list_id cannot be empty on add_release_to_list method.")
		
		if(not ownership_status_id):
			raise ValueError("ownership_status_id cannot be empty on add_release_to_list method.")
		
		if(not box_condition_type_id):
			raise ValueError("box_condition_type_id cannot be empty on add_release_to_list method.")
			
		if(not product_condition_type_id):
			raise ValueError("product_condition_type_id cannot be empty on add_release_to_list method.")
		
		self.check_id_exists('lists_release', list_id)
		
		table = 'lists_goods_list_goods'
		
		where_values = []
		where_values.append(list_id)
		where_values.append(entity_id)
		id = self.get_var(table, ['lists_release_id'], "lists_release_id = %s and entity_release_id = %s",where_values)
		if(id == None):
			columns = ['lists_goods_id', 'goods_id', 'ownership_status_id', 'box_condition_type_id', 'product_condition_type_id']
			value = []
			value.append(list_id)
			value.append(entity_id)
			value.append(ownership_status_id)
			value.append(box_condition_type_id)
			value.append(product_condition_type_id)
		
			if observation:
				columns.append('observation')
				value.append(observation)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to insert on add_goods_to_list(%s, %s, %s, %s, %s, %s)." % (list_id, goods_id, ownership_status_id, box_condition_type_id, product_condition_type_id, observation))
		return True
  
	"""
		Method used to add a edition to a list by the user.
		This method can be used to insert on lists_edition_list_entity_edition table.
	"""
	def add_edition_to_list(self, list_id, entity_id, read_status_type_id, ownership_status_id, condition_type_id, edition_read_status_type_id, observation = None):
		if(not entity_id):
			raise ValueError("entity_id cannot be empty on add_release_to_list method.")
		
		if(not list_id):
			raise ValueError("list_id cannot be empty on add_release_to_list method.")
		
		if(not read_status_type_id):
			raise ValueError("read_status_type_id cannot be empty on add_release_to_list method.")
			
		if(not ownership_status_id):
			raise ValueError("ownership_status_id cannot be empty on add_release_to_list method.")
		
		if(not condition_type_id):
			raise ValueError("condition_type_id cannot be empty on add_release_to_list method.")
			
		if(not edition_read_status_type_id):
			raise ValueError("edition_read_status_type_id cannot be empty on add_release_to_list method.")
			
		if(not observation):
			raise ValueError("observation cannot be empty on add_release_to_list method.")
		
		self.check_id_exists('lists_release', list_id)
		
		table = 'lists_edition_list_entity_edition'
		
		where_values = []
		where_values.append(list_id)
		where_values.append(entity_id)
		id = self.get_var(table, ['lists_release_id'], "lists_release_id = %s and entity_release_id = %s",where_values)
		if(id == None):
			columns = ['lists_edition_id', 'entity_edition_id', 'ownership_status_id', 'condition_type_id', 'edition_read_status_type_id']
			value = []
			value.append(list_id)
			value.append(entity_id)
			value.append(ownership_status_id)
			value.append(condition_type_id)
			value.append(edition_read_status_type_id)
				
			if(observation):
				columns.append('observation')
				value.append(observation)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred while trying to insert on add_edition_to_list(%s, %s, %s, %s, %s, %s, %s)." % (list_id, entity_id, read_status_type_id, ownership_status_id, condition_type_id, edition_read_status_type_id, observation))
		return True
		
		
	################################ User Methods #################################

	
	"""
		Method used to insert a user. This method don't insert any related item to user like email.
		This method can be use to insert on users table.
		
	"""
	def add_user(self, username, password, gender, birthday, location = None, signup_date = None, activated = 1):
		if(not username):
			raise ValueError("User name cannot be empty on add_user method.")
		
		if(not password):
			raise ValueError("Password cannot be empty on add_user method.")
		
		if(not gender):
			raise ValueError("Gender cannot be empty on add_user method.")
		
		if(not birthday):
			raise ValueError("Birthday cannot be empty on add_user method.")
			
		table = 'users'
		id = self.get_id_from_field(table, 'username', username)
		if(id == None):
			columns = ['username', 'pass', 'gender', 'birthday']
			value = []
			value.append(username)
			value.append(password)
			value.append(gender)
			value.append(birthday)
			
			if(location):
				columns.append('location')
				value.append(location)
			
			if(signup_date):
				columns.append('signup_date')
				value.append(signup_date)
			
			if(activated != 1):
				columns.append('activated')
				value.append(0)
				
			self.insert(table, value, columns)
			id = self.get_last_insert_id(table)
			
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_user(%s, %s, %s, %s, %s, %s, %s)." % (username, password, gender, birthday, location, signup_date, activated))
		return id
	
	"""
		Method used to add an email to an already registered used.
	
	"""
	def add_user_email(self, user_id, email):
		if(not email):
			raise ValueError("Email cannot be empty on add_user_email method.")
		
		if(not user_id):
			raise ValueError("User id cannot be empty on add_user_email method.")
	
		table = 'user_email'
		
		where_values = []
		where_values.append(email)
		id = self.get_var(table, ['email'], "email = %s", where_values)
		if(id == None):
			columns = ['user_id', 'email']
			value = []
			value.append(user_id)
			value.append(email)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("There is no last insert id to return on add_user_email(%s, %s)." % (user_id, email))
		return True

	
	"""
		Method used to add a filter to filter content for the user.
		This method don't insert any related item to the user filter like elements.
		If you want to create a filter for the user and associated together the elements 
		use create_user_filter instead.
	"""
	def add_user_filter(self, name, user_id, type_id):
		if(not name):
			raise ValueError("Name cannot be empty on add_user_filter method.")
	
		if(not user_id):
			raise ValueError("user_id cannot be empty on add_user_filter method.")
	
		if(not type_id):
			raise ValueError("type_id cannot be empty on add_user_filter method.")
	
		self.check_id_exists('users', user_id)
		
		table = 'user_filter'
		
		where_values = []
		where_values.append(user_id)
		where_values.append(name)
		where_values.append(type_id)
		id = self.get_id_from_field(table, ['user_id', 'name', 'user_filter_type_id'], where_values)
		if(id == None):
			columns = ['name','user_id','user_filter_type_id']
			value = []
			value.append(name)
			value.append(user_id)
			value.append(type_id)
			
			self.insert(table, value, columns)
			
			id = self.get_last_insert_id(table)
			if(id == 0):
				raise ValueError("There is no last insert id to return on add_user_filter(%s, %s, %s)." % (name, user_id, type_id))
		return id
		
	"""
		Method used to add a element to a user filter.
		Elements can be tag, classification and category.
	"""
	def add_element_to_user_filter(self, user_filter_id, attribute_id, attribute = 'tag'):
		if(not user_filter_id):
			raise ValueError("user_filter_id cannot be empty on add_element_to_user_filter method.")
		
		if(not attribute_id):
			raise ValueError("attribute_id cannot be empty on add_element_to_user_filter method.")
		
		table = attribute + '_user_filter'
		
		where_values = []
		where_values.append(user_filter_id)
		where_values.append(attribute_id)
		id = self.get_var(table, ['user_filter_id'], "user_filter_id = %s and {attribute}_id = %s".format(attribute=attribute), where_values)
		if(id == None):
			columns = ['user_filter_id', attribute + '_id']
			value = []
			value.append(filter_id)
			value.append(attribute_id)
			
			if(self.insert(table, value, columns) == False):
				raise ValueError("There is no last insert id to return on add_element_to_user_filter(%s, %s, %s)." % (user_filter_id, attribute_id, attribute))
		return True
	
	"""
		Method used to register all items related with user_filter.
		This method must be used instead other specified methods related with user_filter.
		
		To use this method the types must be already registered on database.
		The parameters elements must have elements that are dictionary. 
	"""
	def create_user_filter(self, name, user_id, type_id, elements = []):

		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			user_filter_id = self.add_user_filter(name, user_id, type_id)
			
			for element in elements:
				self.add_element_to_user_filter(user_filter_id, element['id'], element['attribute'])
			
			#commit changes
			self.commit()
			
			return user_filter_id
				
		except ValueError as e:
			print e.message
			self.rollback()
			
			raise ValueError("return id is equal to 0 on create_user_filter method. Some error must have occurred.")		
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to add a image and associated it with an soundtrack.
		This method implements try except and return boolean, there is need to implement try except on method above because
		on error a raise will be flagged.
	"""	
	def add_image_to_user(self, url, extension, name, user_id, image_type_id):
		try:
			image_id = self.add_image(url, extension, name)
			return self.add_relation_image('user', image_id, user_id, image_type_id)
			
		except ValueError as e:
			print e.message
			raise ValueError(e.strerror)
		
	"""
		Method used to register all items related with user.
		This method must be used instead other specified methods related with entity.
		
		To use this method the types must be already registered on database.
		The parameters images, user_filters must have elements that are dictionary.
		The parameter photo_profile must be a dictionary.
	"""
	def create_user(self, username, password, gender, birthday, location = None, signup_date = None, activated = 1,
	emails = [], photo_profile = None, images = [], user_filters = []):
		
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			user_id = add_user(self, username, password, gender, birthday, location, signup_date, activated)
	
			for email in emails:
				self.add_user_email(user_id, email)
				
			for image in images:
				self.add_image_to_user(image['url'], image['extension'], image['name'], user_id, image['type_id'])
			
			for user_filter in user_filters:
				self.create_user_filter(user_filter['name'], user_id, user_filter['type_id'], user_filter['elements'])
			
			if photo_profile:
				self.add_image_to_user(photo_profile['url'], photo_profile['extension'], photo_profile['name'], user_id, self.image_user_type_profile)
			
			#commit changes
			self.commit()
			return user_id
		except ValueError as e:
			print e.message
			self.rollback()
			raise ValueError("An error occurred while trying to save a user on create_user.")
		finally:
			self.set_auto_transaction(True)
	
	
	
	################################# Comments Methods ############################

	"""
		Method used to insert comments from users.
		This method can be used to insert on the follow tables:
		soundtrack_comments, audio_comments, company_comments, people_comments, 
		goods_comments, entity_edition_comments, entity_release_comments, collection_comments
		collaborator_comments
	"""
	def add_comment(self, title, content, user_id, entity_id, type = 'release'):
		if(not title):
			raise ValueError("Title cannot be empty on add_comment method.")
		
		if(not content):
			raise ValueError("Content cannot be empty on add_comment method.")
			
		if(not user_id):
			raise ValueError("user_id cannot be empty on add_comment method.")
	
		self.check_id_exists('users', user_id)
		
		table = type + '_comments'
		
		#don't need to check if already exists.
		columns = [type + '_id', 'user_id', 'content', 'title']
		value = []
		value.append(entity_id)
		value.append(user_id)
		value.append(content)
		value.append(title)
		self.insert(table, value, columns)
		
		id = self.get_last_insert_id(table)
		if(id == 0):
			raise ValueError("There is no last insert id to return on add_comment(%s, %s, %s, %s, %s)." % (title, content, user_id, entity_id, type))
		return id
	
	
	######################### External Get Methods ###############################
	#where = "based_type_id = 3 and entity_id = 1"
	"""
		Method used to get the related ID from a hierarchic relationship. 
		This method can be used with the follow table:
		entity_based_entity, persona_related_persona
	"""
	def get_related_item_id(self, table, first_field, second_field, relation_type, type_id, entity_id, limit = None):
		if not first_field:
			raise ValueError("first_field cannot be empty on get_related_item method.")
			
		if not second_field:
			raise ValueError("second_field cannot be empty on get_related_item method.")

		table = table + "_" + relation_type + "_" + table
		
		recursive_columns = [first_field, second_field]
		
		where = "{relation_type}_type_id = %s and {first_field} = %s".format(relation_type=relation_type,first_field=first_field)
		
		where_values = []
		where_values.append(entity_id)
		where_values.append(type_id)
		
		return self.select_with_recursive(table, recursive_columns, recursive_columns, where, None, where_values, None, None, None, None, limit)
		
		
	"""
		Method used to get the related item from a hierarchic relationship. 
		This Method return the ID and Name.
	"""
	def get_related_item(self, table, first_field, second_field, relation_type, type_id, entity_id, limit = None):
		if not first_field:
			raise ValueError("first_field cannot be empty on get_related_item method.")
			
		if not second_field:
			raise ValueError("second_field cannot be empty on get_related_item method.")

		table = table + "_" + relation_type + "_" + table
		
		recursive_columns = [first_field, second_field]
		
		columns = ['r.' + second_field, 'n.name']
		
		join = [relation_type + '_alias as n']
		join_columns = [' n.entity_id = r.another_entity_id ']
		
		where = "{relation_type}_type_id = %s and {first_field} = %s".format(relation_type=relation_type,first_field=first_field)
		
		where_values = []
		where_values.append(entity_id)
		where_values.append(type_id)
		
		return self.select_with_recursive(table, recursive_columns, columns, where, None, where_values, join, join_columns, None, 'r', limit)
	
	#def get_related_item_collection()
		
	
	"""
		Method used to get a country id from a given language code.
	"""
	def get_country_from_language(self, language_code, default_country = None):
		if(not language_code):
			return default_country
			
		code = []
		code.append(language_code)
		#print "Language code", language_code
		#this method will not return the correct country on cases there is more than one country with the same language. So country_id will set to None.
		countries = self.get_col('country_has_language as c', 'c.country_id', "language.code = %s", code, ['language'], ['c.language_id = language.id'])
		if(countries != None):
			length_country = len(countries)
			if(length_country > 1 or length_country < 1):
				country_id = default_country
			else:
				country_id = countries[0]
			return country_id
		
		return default_country
	
	"""
		Method used to get a language id from a given country id.
		This method return default language if none is found or the first language found on database.
		TODO: Change database to return only the official and main language from country.
	"""
	def get_language_from_country_id(self, country_id, default_language = None):
		if(not country_id):
			return default_language
			
		code = []
		code.append(country_id)
		#this method will not return the correct country on cases there is more than one country with the same language. So country_id will set to None.
		countries = self.get_col('country_has_language', 'language_id', "country_id = %s", code)
		if(countries != None):
			return countries[0]
					
		return default_country

	"""
		Method used to get a language id from a given country id.
		This method return default language if none is found or the first language found on database.
		TODO: Change database to return only the official and main language from country.
	"""
	def get_country_from_language_id(self, language_id, default_country = None):
		if(not language_id):
			return default_country
			
		code = []
		code.append(language_id)
		#this method will not return the correct country on cases there is more than one country with the same language. So country_id will set to None.
		countries = self.get_col('country_has_language', 'country_id', "language_id = %s", code)
		if(countries != None):
			return countries[0]
					
		return default_country
		
	################################## Crawler Methods ############################
	
	"""
		Method used to insert a item on spider item table.
		All crawled URL must have a row on spider_item with the status 
		True or False for complete crawled status.
	"""
	def add_spider_item(self, table, id, url, complete_crawled = False):
		if(not table):
			raise ValueError("Table cannot be empty on add_spider_item method.")
			
		if(not id):
			raise ValueError("id cannot be empty on add_spider_item method.")
			
		if(not url):
			raise ValueError("URL cannot be empty on add_spider_item method.")
		
		table_base = 'spider_item'
		
		where_values = []
		where_values.append(id)
		where_values.append(url)
		where_values.append(table)
		where = "id = %s and url = %s and table_name = %s"
		id_base = self.get_var(table_base, ['complete_crawled'], where, where_values)
		
		if(id_base == None):
			columns = ['id','table_name', 'url','complete_crawled']
			value = []
			value.append(id)
			value.append(table)
			value.append(url)
			value.append(complete_crawled)
			
			#insert
			if not self.insert(table_base, value, columns):
				raise ValueError("An error occurred while trying to insert a URL on add_spider_item(%s, %s, %s, %s)." % ( table, id, url, complete_crawled))
		elif(complete_crawled and id_base == 'False'):
			#Update to full crawled
			if(not self.update(table_base, ['True'],['complete_crawled'], where, where_values)):
				raise ValueError("An error occurred while trying to update complete_crawled on add_spider_item(%s, %s, %s, %s)." % ( table, id, url, complete_crawled))
		return True
		
	"""
		Method used to get a ID from a already crawled URL.
		If there isn't no ID for the given URL on database None is returned.
	"""
	def get_spider_item_id(self, url, table):
		where_values = []
		where_values.append(url)
		where_values.append(table)
		return self.get_var('spider_item', ['id'], "url = %s and table_name = %s", where_values)
		