# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database
from .. import langid
from .. import util

import re
import urlparse
import collections
import sys

class MangaUpdatesSpider(CrawlSpider):
		name = "mangaupdates_part2"
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/series.html?page=1&"]
		dbase = None
		login_page = 'http://www.mangaupdates.com/login.html'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('series\.html\?page=[0-9]{1,}?'), deny=('letter', 'orderby', 'filter', 'categories', 'act'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(allow=('id=',
		#Parse release from request on demand items
		'releases\.html\?(page=[0-9]{1,}&)?search=[0-9]{1,}&stype=series',
		), deny=('members')), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'series\.html\?id=[0-9]{1,}')
		pattern_series_releases = re.compile(ur'releases\.html\?(page=[0-9]{1,}&)?search=[0-9]{1,}&stype=series')
		pattern_last_newline = re.compile(ur'\n$')
		pattern_last_bracket = re.compile(ur'\[$')
		
		language_probabilistic_pass = 0.7
		
		"""
			Method to overwrite the CrawlSpider homonym method.
			This method is used to request a login page.
		"""
		def start_requests(self):
			yield Request(
				url=self.login_page,
				callback=self.login,
				dont_filter=True
			)

		"""
			Method to make login on mangaupdates.
			This method gets the user name and password from settings.
		"""
		def login(self, response):
			print "login"
			return FormRequest.from_response(response,
                    formdata={'username': Settings().get('MUUSERNAME'), 'password': Settings().get('MUPASSWORD')},
                    callback=self.after_login,
					#dont forget dont_filter, without it the after_login will not be loaded.
					dont_filter=True)

		"""
			Method callback of login method.
			This method check if the login was successful and call start_requests to start the crawler.
		
		"""
		def after_login(self, response):
			print "here3"
			if "You are currently logged in as" in response.body:
				self.log("Successfully logged in. Let's start crawling!")
				print "Successfully logged in. Let's start crawling!"
				return super(MangaUpdatesSpider, self).start_requests()
			else:
				self.log("Bad times :(")
				print "Error login"
				# Something went wrong, we couldn't log in, so nothing happens.
		
		"""
			Method to instancialize the database.
			This method will not replace an already instancialized dbase variable.
		"""
		def instancialize_database(self):
			if(self.dbase == None):
				dbname = Settings().get('DBNAME')
				dbuser = Settings().get('DBUSERNAME')
				dbpass = Settings().get('DBPASSWORD')
				dbhost = Settings().get('DBHOST')
				dbport = Settings().get('DBPORT')
				
				self.dbase = database.Database(dbname, dbuser,dbpass, dbhost,dbport)
				if(self.dbase.connect() == False):
					print vars(self.dbase)
					self.dbase = None
					raise SystemExit
		
		"""
			Method called to parse link from extractor.
		"""
		def parse_items(self, response):
			self.instancialize_database()
			print "Initialized database and parse"
			if(re.search(self.pattern_series, response.url) != None):
				#Parse Series.
				self.parse_series(response)
		
			elif(re.search(self.pattern_series_releases, response.url) != None):
				#Parse Groups.
				self.parse_series_releases(response)
					
			
		def sanitize_title(self, title):
			#remove type from title.
			
			#remove last newline with sub
			title = re.sub(self.pattern_last_newline, '', title)
			title = title.strip()
			if(title == 'N/A'):
				return None
			return title
			
		def sanitize_content(self, description):
			#if description is list join.
			if(isinstance(description, collections.Iterable)):
				description = "\n".join(description)
			#remove extra space. 
			description = description.strip()
			#remove last \n with sub.
			description = re.sub(self.pattern_last_newline, '', description)
			description = re.sub(self.pattern_last_bracket, '', description)
			
			if(description == 'N/A'):
				return None
				
			return description
			
		def parse_series(self, response):
			print response.url			
			#Get romanized title
			romanized_title = response.css('span.releasestitle.tabletitle::text').extract()

			#Get description
			description = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(2)::text').extract()
			
			#Get type
			type = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(5)::text').extract()
			
			#Get titles
			associated_name = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(11)::text').extract()
			
			#Get people
			author_url = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(17) a::attr(href)').extract()
			author_alias = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(17) a u::text').extract()
			author_alias_text = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(17)::text').extract()
			
			artist_url = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(20) a::attr(href)').extract()
			artist_alias = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(20) a u::text').extract()
			artist_alias_text = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(20)::text').extract()
			
			#Get company
			original_publisher_url = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(26) a::attr(href)').extract()
			original_publisher_alias = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(26) a u::text').extract()
			original_publisher_text = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(26)::text').extract()
			
			serialized_publisher = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(29) a::attr(href)').extract()
			serialized_publisher_alias = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(29) a u::text').extract()
			serialized_publisher_text = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(29)::text').extract()
			
			english_publisher = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(35) a::attr(href)').extract()
			english_publisher_alias = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(35) a u::text').extract()
			english_publisher_text = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(35)::text').extract()
			
			#Get year
			year = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(23)::text').extract()
			
			#Get related items.
			related = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(8) a::attr(href)').extract()
			related_type = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(8)::text').extract()
			
			#Get status 
			status = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(20)::text').extract()
			
			#Get animé comparative			
			anime_start_end = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(26)::text').extract()

			#Get releases
			releases = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(17) [rel=nofollow]::attr(href)').extract()

			#Get image
			image = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div center img::attr(src)').extract()
	
			#Get partial categories
			categories = response.css('li.tag_normal a::text').extract()
			
			try:
				#format romanized title
				romanized_title = self.sanitize_title(romanized_title[0])
				
				#format description (synopsis)
				description = self.sanitize_content(description)
				synopsis = []
				new_description = {}
				new_description['language_id'] = self.dbase.language_en
				new_description['content'] = description
				synopsis.append(new_description)
				
				#format titles
				titles = []
				language_titles = []
				for name in associated_name:
					new_name = self.sanitize_title(name)
					language = langid.classify(new_name)
					language_titles.append(language[0])
					code = []
					code.append(language[0])
					
					language_id = self.dbase.get_var('language', ['id'], "code = %s", code)
					
					new_title = {}
					new_title['title'] = new_name
					new_title['language_id'] = language_id
					
					titles.append(new_title)
				
				
				webnovel = False
				country_id = None
				language_id = None
				
				#format partial categories
				if(categories):
					categories = " ".join(categories)
						
				#format type
				type = self.sanitize_content(type)
				if(type == None):
					entity_type_id = self.dbase.entity_type_manga
				elif(type == 'Manga'):
					entity_type_id = self.dbase.entity_type_manga
					country_id = self.dbase.country_jp
					language_id = self.dbase.language_ja
				elif(type == 'Manhaw'):
					entity_type_id = self.dbase.entity_type_manhaw
					country_id = self.dbase.country_kr
					language_id = self.dbase.language_ko
				elif(type == 'Manhua'):
					entity_type_id = self.dbase.entity_type_manhua
					country_id = self.dbase.country_cn
					language_id = self.dbase.language_zn
				elif(type == 'Novel'):
					new_status = " ".join(status)
						
					#if is there is Web Volumes or Web Chapters in status
					if "Web Novel" in categories or "Web" in new_status:
						entity_type_id = self.dbase.entity_type_webnovel
						webnovel = True
					else:
						entity_type_id = self.dbase.entity_type_lightnovel
				else:
					#Add new type:
					entity_type_id = self.dbase.add_type(type, 'entity')
					if(entity_type_id == None):
						entity_type_id = self.dbase.entity_type_manga
				
				
					
				#format people
				#remove [ from name
				#get author. If author don't exists create dummy author   
				peoples = []
				
				print "Author before"
				author_alias_text = [x for x in author_alias_text if x != ']']
				relation_type_id = self.dbase.people_relation_type_writer
				
				for index, url in enumerate(author_url):
					add_dummy = False
					if 'add_author' in url:
						#Add dummy author
						people_name = util.get_formatted_name(self.sanitize_content(author_alias_text[index]))
						add_dummy = True
					else:
						where_values = []
						where_values.append(url)
						where_values.append('people')
						#Get author id from link.
						people_id = self.dbase.get_var('spider_item', ['id'], "url = %s and table_name = %s", where_values)
						people_name = util.get_formatted_name(self.sanitize_content(author_alias[index]))
						if(people_id == None):
							add_dummy = True
						else:
							where_values = []
							where_values.append(people_name['name'])
							where_values.append(people_name['lastname'])
							where_values.append(people_id)
							alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = % and people_id = %s", where_values)
							if(alias_used_id == None):
								#Insert alias.
								alias_used_id = self.dbase.add_people_alias(people_name['name'], people_name['lastname'], people_id, self.dbase.alias_type_alias)
								
					if(add_dummy):
						people_country = self.dbase.country_jp
						people_id = self.dbase.create_people(people_name['name'], people_name['lastname'], people_country)
						
						where_values = []
						where_values.append(people_name['name'])
						where_values.append(people_name['lastname'])
						where_values.append(people_id)
						alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = %s and people_id = %s", where_values)
						self.dbase.add_spider_item('people', people_id, url)
						print "Added dummy people"
						
					new_people = {}
					new_people['id'] = people_id
					new_people['alias_used_id'] = alias_used_id
					new_people['relation_type_id'] = relation_type_id
					peoples.append(new_people)
					
				print "Artist before"
				artist_alias_text = [x for x in artist_alias_text if x != ']']
				relation_type_id = self.dbase.people_relation_type_illustrator
					
				for index, url in enumerate(author_url):
					add_dummy = False
					if 'add_author' in url:
						#Add dummy author
						people_name = util.get_formatted_name(self.sanitize_content(artist_alias_text[index]))
						add_dummy = True
					else:
						#Get author id from link.
						people_id = self.dbase.self.dbase.get_spider_item_id(url, 'people')
						people_name = util.get_formatted_name(self.sanitize_content(artist_alias[index]))
						if(people_id == None):
							add_dummy = True
						else:
							where_values = []
							where_values.append(people_name['name'])
							where_values.append(people_name['lastname'])
							where_values.append(people_id)
							alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = % and people_id = %s", where_values)
							if(alias_used_id == None):
								#Insert alias.
								alias_used_id = self.dbase.add_people_alias(people_name['name'], people_name['lastname'], people_id, self.dbase.alias_type_alias)
								
					if(add_dummy):
						if(country_id != None):
							people_country = country_id
						else:
							people_country = self.dbase.country_jp
							
						people_id = self.dbase.create_people(people_name['name'], people_name['lastname'], people_country)
						
						where_values = []
						where_values.append(people_name['name'])
						where_values.append(people_name['lastname'])
						where_values.append(people_id)
						alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = %s and people_id = %s", where_values)
						self.dbase.add_spider_item('people', people_id, url)
						print "Added dummy people"
						
					new_people = {}
					new_people['id'] = people_id
					new_people['alias_used_id'] = alias_used_id
					new_people['relation_type_id'] = relation_type_id
					peoples.append(new_people)
					
				
				#format company
				companies = []
				company_publisher = False
				original_publisher_text = [x for x in original_publisher_text if x != ']']
				
				company_function_type_id = self.dbase.company_function_type_publisher
				
				for index, url in enumerate(original_publisher_url):
					add_dummy = False
					if 'add_publisher' in url:
						#Add dummy company
						company_name = self.sanitize_content(original_publisher_text[index])
						add_dummy = True
					else:
						#Get author id from link.
						company_id = self.dbase.get_spider_item_id(url, 'company')
						company_name = self.sanitize_content(original_publisher_alias[index])
						if(company_id == None):
							add_dummy = True
						else:
							where_values = []
							where_values.append(company_name)
							where_values.append(company_id)
							alias_used_id = self.dbase.get_var('company_alias', ['id'], "name = %s and company_id = %s", where_values)
							#Get country_id from original publisher
							if(country_id == None):
								where_values = []
								where_values.append(company_id)
								country_id = self.dbase.get_var('company', ['country_id'], "id = %s", where_values)
								if(country_id == None):
									country_id = self.dbase.country_jp
									
							#Get language_id from original publisher
							if(language_id == None):
								language_id = self.dbase.get_language_from_country_id(country_id, self.dbase.language_ja)
							
							if(alias_used_id == None):
								#Insert alias.
								language = langid.classify(company_name)
								code = []
								code.append(language[0])
								language_id = self.dbase.get_var('language', ['id'], "code = %s", code)
								alias_used_id = self.dbase.add_alias(company_name, company_id, language_id, 'company', self.dbase.alias_type_alias)
								
					if(add_dummy):
						if(country_id != None):
							country_origin_id = country_id
						else:
							country_origin_id = self.dbase.country_jp
							
						company_id = self.dbase.create_company(company_name, language_id, country_origin_id, None, None, None, None, None,
						[], [], [], [], [], [], [], [])	
		
						where_values = []
						where_values.append(company_name)
						where_values.append(company_id)
						alias_used_id = self.dbase.get_var('company_alias', ['id'], "name = %s and company_id = %s", where_values)
						self.dbase.add_spider_item('company', company_id, url)
						print "Added dummy company"

					new_company = {}
					new_company['id'] = company_id
					new_company['function_type_id'] = company_function_type_id
					companies.append(new_company)
					
					company_publisher = True
					
				create_lightnovel = False
					
				if(webnovel and company_publisher):
					create_lightnovel = True
						
				#format year
				year = self.sanitize_content(year[0])
				
				
				
				#format related
				if(related):
					print related
			
				if not 'N/A' in related_type[0]:
					print related_type
				
					
				
				
				#format status
					#if complete register status
					#elif ongoing register status
					#if more than on type register
					#remove last \n from elements
			
				#format animé comparative
				#check if element [0] is equal to N/A
				if(anime_start_end):
					if not 'N/A' in anime_start_end[0]:
						print anime_start_end
					
			
				#Format images
				#image = image[0]
				
				#format genre
				genre_id = 0
				
				#format collection
				#create new collection with the first name type, get firstname part using regex.
				collection_id = 0
				
				#format country. Get country from associated name, if not found country_id will be Japan.
				if(not country_id):
					language_country = {'ja': self.dbase.country_jp, 'ko': self.dbase.country_kr, 'zn': self.dbase.country_cn}
					language_test = {'ja': 0, 'ko': 0, 'zn' : 0}
					for title in titles:
						if title['language_id'] == self.dbase.language_ja:
							language_test['ja'] += 1
						elif title['language_id'] == self.dbase.language_ko:
							language_test['ko'] += 1
						elif title['language_id'] == self.dbase.language_zn:
							language_test['zn'] += 1
					
					if(language_test['ja'] == language_test['ko'] and language_test['ko'] == language_test['zn']):
						language = language_country['ja']
					else:
						language, value = max(language_test.iteritems(), key=lambda x: x[1])
					
					country_id = language_country[language]				

				category_adult = False	
				#format classification_type_id
				if(categories):
					if "Adult" in categories or "Hentai" in categories or "Doujin" in categories or "Seinen" in categories:
						classification_type_id = self.dbase.classification_type_18
						category_adult = True
				
				if(not category_adult):
					#check if is doujinshi on title
					
					
					classification_type_id = self.dbase.classification_type_12
				
			except ValueError as e:
				print "Error on formatting and getting IDs to save Series", e.message
				util.PrintException()
				return
			except:
				print "Error on formatting Series", sys.exc_info()[0]
				util.PrintException()
				return
			
			try:
				#entity_id = dbase.create_entity(romanized_title, entity_type_id, classification_type_id, genre_id, collection_id, language_id, country_id, year, collection_started = 0, 
				#titles, [], synopsis, [], [], [], [], [], companies, peoples)
				
				#if(create_lightnovel):
				#	entity_id = dbase.create_entity(romanized_title, self.dbase.entity_type_lightnovel, classification_type_id, genre_id, collection_id, language_id, country_id, year, collection_started = 0, 
				#	titles, [], synopsis, [], [], [], [], [], companies, peoples)
				
				#Request release
				if(releases):
					meta = {}
					meta['series_id'] = entity_id
					meta['name'] = 1
					Request(url=releases[0],callback=self.parse_series_releases,meta=meta)
					
			except ValueError as e:
				print e.message
			except:
				print "Error on save Series", sys.exc_info()[0]
		
		"""
			Method used to save all genres on database and pass initial genre link to be crawled.
			The genre link will be parsed by parse_genres_series after been requested.
			TODO: Save on database.
		"""
		def parse_series_releases(self, response):
			print "Genres"
			genres = response.css('.releasestitle b::text').extract()
			genres_links = response.css('#main_content td.text td.text a::attr(href)').extract()
			
			try:
				for genre in genres:
					print genre
					self.dbase.add_name_to_table(genre, 'genre')
				for	link in genres_links:
					if 'series' in link:
						Request(url=link,callback=self.parse_genres_series)
			except ValueError as e:
				print self.dbase.last_error
				print self.dbase.status_message
				print self.dbase.last_query
			
		#def check_series_type(self, response):
			#from response check what is the type, if is dounjinshi check has tag dounjinshi, if novel check name, if other check Type.
		
		#def check_derivate_from(self, response):
			#check if series is derivate from another work.

			#if it is add derivate type if is a new one and create original work if it was not save on database yet using website url to identify the item. 
		
		#def check_adult_content(self, response):
			#if have tag adult or (+18) on content.
		
		#def get_collection(self,):
			"""
				Pega coleção. Se não for prequel, sequel, spin-off, spinoff, derivate, doujinshi or fanart retorna o nome do trabalho atual.
					como detectar quando a coleção é Gundam, exemplo:
					Kidou Senshi Gundam
		"""	
			
		#def log_error(self, error):
			
		