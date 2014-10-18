######################### Entity Methods #########################

#set commit to false.
		self.set_auto_transaction(False)
		
	except ValueError as e:
			print "ValueError({0}): {1}".format(e.errno, e.strerror)
			self.rollback()
			return False
		finally:
			self.set_auto_transaction(True)
			
	"""
		Method used to add a image and associated it with an entity edition.
		This method implements try except and return boolean, so there is no need to implement try except on method above.
	"""
	def add_image_to_edition(self, url, extension, name, edition_id, image_type_id):
		try:
			image_id = add_image(url, extension, name)
			return add_relation_image('entity_edition', image_id, edition_id, image_type_id)
		except ValueError as e:
			print "ValueError({0}): {1}".format(e.errno, e.strerror)
			return False
			
			
			
	
	raise ValueError("Table cannot be empty on add_name_to_table method.")
	raise ValueError("Description cannot be empty on add_name_to_table method.")
	raise ValueError("Name cannot be empty on add_name_to_table method.")
	id = self.get_last_insert_id(table)
	raise ValueError("There is no last insert id to return on add_image(%s, %s, %s)." % (url, extension,name))
	raise ValueError("There is no last insert id to return on add_image(%s, %s, %s, %s)." % (url, extension,name))
	raise ValueError("There is no last insert id to return on add_image(%s, %s, %s, %s, %s)." % (url, extension,name))
	
	"An error occurred when trying to insert on add_software_edition(%s, %s, %s, %s)."
	
	if(self.insert(table, value, columns) == False):
				raise ValueError("An error occurred when trying to insert on add_multi_relation(%s, %s, %s, %s, %s)." % (first_id, second_id, first_table, second_table, relation_type))
		return True
		
	add_multi_relation(self, first_id, second_id, first_table, second_table, relation_type = 'has')
	entity_has_category, entity_has_tag,
	
	
	GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO teste; 
	
	return_method = False
	
	if(return_method):
				return edition_id
				
	probabilidade acumulada
	
	
		"""
		Method used to insert a entity. This method don't insert any related item to entity like name or categories.
		This method can be use to insert on entity table.
		
	"""
			
subheading

on insert parse:

	#need to made a unique field to identify person with same name.
		
		#check if there is already a people, check know alias from alias table. If there inst create.
		
		#register social network url from author.
		
		#if there is work associated register the author work.
		
		#return author id.	
		
		
caption
	"""
		Method used to register all items related with entity.
		This method must be used instead other specified methos related with entity.
		
		To use this method the types must be already registered on database.
		The parameters titles must have elements that are dict. 
	"""
	
	
		def create_entity(self, romanize_title, romanize_subtitle = None, entity_type_id, classification_type_id, genre_id, collection_id, language_id, country_id, launch_year, collection_started = 0, 
	titles = [], subtitles = [], synopsis = [], wiki = [], descriptions = [], categories = [], tags = [], personas = [], companies = []):
		if(romanize_title == ""):
			raise ValueError("Name cannot be empty on create_entity method.")
		
		#set commit to false.
		self.set_auto_transaction(False)
		
		try:
			entity_id = add_entity(entity_type_id, classification_type_id, gender_id, collection_id, language_id, country_id, launch_year, collection_started)
		
			#register main name (Romanize title and Romanized Subtitle)
			add_entity_alias(entity_id, language_id, romanize_title,  self.alias_type_romanized)
			
			if(romanize_subtitle != None):
				add_entity_alias(entity_id, language_id, romanize_subtitle,  self.alias_type_subromanized)
			
			for title in titles:
				add_entity_alias(entity_id, title['language_id'], title['title'],  self.alias_type_title)
			
			for subtitle in subtitles:	
				add_entity_alias(entity_id, subtitle['language_id'], subtitle['title'],  self.alias_type_subtitle)
				
			#register synopsis
			for synops in synopsis:	
				add_entity_synopsis(entity_id, synops['language_id'], synops['content'])
			
			for description in descriptions:
				add_entity_description(entity_id, description['language_id'], description['content'])
			
			for category in categories:
				add_multi_relation(entity_id, category['id'], 'entity', 'category')

			for tag in tags:
				add_multi_relation(entity_id, tag['id'], 'entity', 'tag')
	
			for wiki in wikis:
				add_entity_wiki(entity_id, wiki['name'], wiki['url'], wiki['language_id']):
			
			for persona in personas:
				#persona first_appear is 0 or 1.
				add_persona_to_entity(entity_id, persona['id'], persona['alias_id'], persona['first_appear'])
			
			for company in companies:
				add_relation_company(company['id'], entity_id, company['function_type_id'], 'entity')
			
			#commit changes
			self.commit()
			return True
		except ValueError as e:
			print "ValueError({0}): {1}".format(e.errno, e.strerror)
			self.rollback()
			return False
		finally:
			self.set_auto_transaction(True)
	
	

	
	
	
		entity_release
			
		#check if there is a series where this release is from, check table entity and alias to find the series name. If not exists create the series.

		
		#normalize release number to be insert on database, release number can be e.g. 'c.53', 'v2.9', 'v1 c.1-4','v1-2', 'v.1 c.14', 'Oneshot', 'v.1 c.Interlude 2-3', 'c.Parts 1-2'
		
		#don't put version on same method as release. 