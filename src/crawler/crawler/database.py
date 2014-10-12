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
	programing_message = None
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
	
	
	#insert types on database type table.
	#create types if dont exists
	#avaliable types: hash_type, release_read_status_type, release_type, software_type, edition_type, image_edition_type,
	#image_figure_type, produces_type, create_type, product_condition_type, figure_version, plataform_type,
	#print_type, genre_type, related_type, release_ownership_type, entity_type, filter_type, edition_read_status_type, function_type,
	#condition_type, classification_type, collaborator_type, media_type, number_type, alias_type, mod_type, blood_type, box_condition_type,
	#based_type, stage_developer_type, company_function_type, soundtrack_type, compose_type, image_soundtrack_type, lyric_type
	def add_type(self, name, type_name):
		#create name on table if there isnt none. 
		id = self.get_var(type_name + '_type', ['id'], "name = '{name}'".format(name))
		if(id == None):
			value = []
			value.append(name)
			self.insert(type_name + '_type', value, ['name'])
			id = self.insert_id
			if(id == 0):
				return False
		return id	
	
	#insert on table that have only one value
	#avaliable tables with id, name: shop_location, scale, material, audio_codec, ownership_status
	def add_name_to_table(self, name, table):
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
	
	#Insert image
	def add_image(self, url, extension, name):
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
	
	
	
	
	####### Entity methods #############
	
	#insert entity description
	def add_entity_description(self, entity_id, language_id, description):
		#check if already exist a description for this entity and language
		
		if(id == None):
			columns = ['entity_id', 'language_id', 'description']
			value = []
			value.append(entity_id)
			value.append(language_id)
			value.append(description)
			self.insert('entity_description', value, columns)
		
		#check what is returned when the field dont have a sequence.
		
		
		id = self.insert_id
		if(id == 0):
			return False
		return id
	
	#insert entity_wiki
	def add_entity_wiki(self, entity_id, name, url, language_id):
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
		
	#insert entity synopse
	def add_entity_synopse(self, entity_id, language_id, description):
		#check if already exist a synopse for this entity and language
		
		if(id == None):
			columns = ['entity_id', 'language_id', 'content']
			value = []
			value.append(entity_id)
			value.append(language_id)
			value.append(description)
			self.insert('entity_synopse', value, columns)
	
		#check what is returned when the field dont have a sequence.
		
		
			id = self.insert_id
			if(id == 0):
				return False
		return id
	
	#insert alternate titles
	#used on table entity_alias
	def add_entity_alias(self, name, entity_id, language_id, title, alias_type_id):
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
	
	####### Collaborator methods ##############
	
	
	#insert collaborator
	def add_collaborator(name, description, irc = None, websites = [], members_id = [])
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
			self.insert('collaborator_has_collaborator_member', value, columns)
			
			#How to know if is ok if there is a seq.
			id = self.insert_id
			if(id == 0):
				return False
		return True
		
	def add_collaborator_website(self, collaborator_id, website):
	
	
	
	############# People Methods ################
	
	def add_people(name, country, blood_type, website, decription, alias = []):
		#need to made a unique field to identify person with same name.
		
		#check if there is already a people, check know alias from alias table. If there inst create.
		
		#register social network url from author.
		
		#if there is work associated register the author work.
		
		#return author id.	
	
	#insert socials.
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
	############# Figure Methods ###############
	
	
	
	
	
	#insert on simple m n tables the given ids.
	#avaliable simple m n tables: country_has_language, soundtrack_integrate_collection, category_has_filter_type, audio_has_language,
	#company_sponsors_event, company_owner_collection, company_has_country, people_has_image, genre_type_has_audio, entity_has_category,
	#entity_has_tag, soundtrack_for_entity_edition, entity_edition_has_language, entity_edition_has_currency, figure_from_persona, figure_has_category,
	#entity_release_has_version, entity_release_has_language, figure_has_material, figure_has_shop_location, figure_has_tag, mod_has_image,
	#shops_operate_on_country, people_nacionalization_on_country, entity_has_tag, entity_edition_has_subtitle, software_edition_has_version,
	#software_edition_has_subtitle
	def add_multi_relation(self, first_id, second_id, first_table, second_table, relation_type = 'has'):
		#check if there is already a compost key with the given ids.
		if(first_table != second_table):
			another = ''
		else:
			another = 'another_'
		id = self.get_var(first_table + relation_type + second_table, [first_table + '_id'], "{first_table}_id = {first_id} and {another}{second_table}_id = {second_id}".format(first_table, first_id, another, second_table, second_id))
		if(id == None):
			if(first_table != second_table):
				columns = [first_table + '_id', second_table + '_id']
			else:
				columns = [first_table + '_id', 'another_' + second_table + '_id']
			value = []
			value.append(first_id)
			value.append(second_id)
			self.insert(first_table + relation_type + second_table, value, columns)
			
			#need to check if will return only a value
			
			
				return False
		return True
		
		
	#insert relation has image
	#used on the follow tables: entity_edition_has_image, figure_has_image, soundtrack_has_image
	def add_relation_image(self, relation_table, image_id, second_id, type_id):
		id = self.get_var(relation_table + "_has_image", ['image_id'], "image_id = {image_id} and {relation_table}_id = {second_id}".format(image_id, relation_table, second_id))
		if(id == None):
			columns = ['image_id', relation_table + '_id', 'image_' + relation_table + '_type_id']
			value = []
			value.append(image_id)
			value.append(second_id)
			value.append(type_id)
			
			self.insert(relation_table + "_has_image", value, columns)
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	#used on the follow tables: entity_based_entity, persona_related_persona
	#relation type can be related or based, usually the middle part of the table.
	def add_relation_with_type(self, first_table, second_table, first_id, second_id, relation_type, relation_type_id):
		id = self.get_var(first_table + "_" + relation_type + "_" + second_table, [first_table + '_id'], "{first_table}_id = {first_id} and another_{second_table}_id = {second_id}".format(first_table, first_id, second_table, second_id))
		if(id == None):
			columns = [first_table + '_id', 'another_' + second_table + '_id', relation_table + '_type_id']
			value = []
			value.append(first_id)
			value.append(second_id)
			value.append(relation_type_id)
			
			self.insert(first_table + "_" + relation_type + "_" + second_table, value, columns)
			#how to know if was inserted without id.
			
			id = self.insert_id
			if(id == 0):
				return False
		return id
		
	
	
	def add_entity_edition_launch_country(self, entity_id, country_id, launch_date, launch_price):
		
		
	
	 
	def add_game_release()
	
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
			
			id = self.insert_id
			if():
				return False
		return True
	
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
			if(id == 0)
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
			if(id == 0)
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
			if(id == 0)
				return False
		return id
	
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
	
	
	################ People Methods #########################
	
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
	
	#insert number
	#volume type must be insert before each chapter number.
	#if is oneshot number = 1 and type = oneshot chapter, because there is oneshot volume that have more than one chapter.
	#used on table number_release, number_edition 
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
	
	
	def add_persona(self):
	
	
	
	
	
	
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
			self.insert('game_release', value,columns)
			
			#how to check if inserted without id returning.
			if():
				return False
		return id
	
	#the type, classification_type must already be on database.
	def create_entity(self, name, entity_type, launch_year, start_collection, classification_type, language_type,
	description = [], alias = [], synopse = [], wiki = [], categories = [], tags = [], persona = []):
		
		
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
			
		return id
	
	def create_entity_figure(self, name, height, width, country, currency, lauch_price, release_date, observation):
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
		
		
		
	def add_release():
		#check if there is a series where this release is from, check table entity and alias to find the series name. If not exists create the series.
		
		#get the id from series, from series table or alias table.
		
		#normalize release number to be insert on database, release number can be e.g. 'c.53', 'v2.9', 'v1 c.1-4','v1-2', 'v.1 c.14', 'Oneshot', 'v.1 c.Interlude 2-3', 'c.Parts 1-2'
		
		#insert release
		
		#insert release number
	
	
	
	def add_collaborator(self, website = None, works = []):
		#check if there is already a collaborator with the same name. Check if country is the same, if not create a new collaborator with same name but different country. 
		#put the country name on collaborator name to maintain unique?

		#check if there is website. If not exists get from social network (if possible). Use status on website.
		#if(website != None):
		
		#register social network.
		
		#if there is work obtained register the collaborator work.
		#if(len(work) > 0):
	
		
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