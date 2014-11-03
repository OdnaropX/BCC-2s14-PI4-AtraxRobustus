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
from datetime import date, datetime

import re
import urlparse
import collections
import sys
import calendar

class MangaUpdatesSpider(CrawlSpider):
		name = "mangaupdates_part2"
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/series.html?page=1&"
		#"https://www.mangaupdates.com/releases.html?search=4757&stype=series"#line for test only.
		]
		dbase = None
		login_page = 'http://www.mangaupdates.com/login.html'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('series\.html\?page=[0-9]{1,}?'), deny=('letter', 'orderby', 'filter', 'categories', 'act'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(allow=(#'id=',
		#Parse release from request on demand items
		'releases\.html\?(page=[0-9]{1,}&)?search=[0-9]{1,}&stype=series',
		), deny=('members', 'orderby','asc=asc')), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'series\.html\?id=[0-9]{1,}')
		pattern_series_releases = re.compile(ur'releases\.html\?(page=[0-9]{1,}&)?search=[0-9]{1,}&stype=series')
		pattern_last_newline = re.compile(ur'\n$')
		pattern_last_bracket = re.compile(ur'\[$')
		pattern_doujin = re.compile(ur'\bdj\b')
		pattern_novel = re.compile(ur'\b[Nn]ovel\b')
		pattern_remove_doujin = re.compile(ur'\bdj\b.*')
		pattern_replace_name = re.compile(ur'(:.*|\bdj\b.*|\(.*\)|\[.*\]|- .*)')
		
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
					self.dbase = None
					raise SystemExit
		
		"""
			Method called to parse link from extractor.
		"""
		def parse_items(self, response):
			print "response url: ", response.url
			
			self.instancialize_database()
			print "Initialized database and parse"
			if(re.search(self.pattern_series, response.url) != None):
				#Parse Series.
				self.parse_series(response)
		
			elif(re.search(self.pattern_series_releases, response.url) != None):
				#Parse Groups.
				self.parse_series_releases(response)
					

		"""
			Method used 
			TODO: Change anime relation and series status on database so the information is relational. 
		"""
		def parse_series(self, response):
			#print response.url			
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'entity')
			except ValueError as e:
				print "Error on getting dummy id on Series", e.message
			except:
				print "Error on getting dummy on Series", sys.exc_info()[0]
				util.PrintException()
				
			#Get romanized title
			romanized_title = response.css('span.releasestitle.tabletitle::text').extract()

			#Get description
			description = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(2)::text').extract()
			
			#Get webnovel link
			webnovel_link = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(2) a::attr(href)').extract()
			
			
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
			
			english_publisher_url = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(35) a::attr(href)').extract()
			english_publisher_alias = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(35) a u::text').extract()
			english_publisher_text = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(35)::text').extract()
			
			#Get year
			year = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(23)::text').extract()
			
			#Get related items.
			related = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(8) a::attr(href)').extract()
			related_text = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(8) a::text').extract()
			related_type = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(8)::text').extract()
			
			#Get status 
			status = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(20)::text').extract()
			
			#Get animé comparative			
			anime_start_end = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(26)::text').extract()

			#Get releases
			releases = response.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(17) [rel=nofollow]::attr(href)').extract()

			#Get image
			images = response.css('div.sContainer:nth-child(4) > div:nth-child(1) > div center img::attr(src)').extract()
	
			#Get partial categories
			categories = response.css('li.tag_normal a::text').extract()
			
			try:		
				#format romanized title
				romanized_title = util.sanitize_title(romanized_title[0])
				
				#format description (synopsis)
				description = util.sanitize_content(description)
				
				descriptions = []
				if(description):
					new_description = {}
					new_description['language_id'] = self.dbase.language_en
					new_description['content'] = description
					descriptions.append(new_description)
				
				#format titles
				titles = []
				language_titles = []
				for name in associated_name:
					new_name = util.sanitize_title(name)
					if(new_name):
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
				type = util.sanitize_content(type)
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
					language_id = self.dbase.language_zh
				elif(type == 'Novel'):
					new_status = " ".join(status)
						
					#if is there is Web Volumes or Web Chapters in status
					if "Web Novel" in categories or re.search("Web",new_status) != None:
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
				
				author_alias_text = [x for x in author_alias_text if x != ']']
				relation_type_id = self.dbase.people_relation_type_writer
				
				for index, url in enumerate(author_url):
					add_dummy = False
					if 'add_author' in url:
						#Add dummy author
						people_name = util.get_formatted_name(util.sanitize_content(author_alias_text[index]))
						add_dummy = True
					else:
						where_values = []
						where_values.append(url)
						where_values.append('people')
						#Get author id from link.
						people_id = self.dbase.get_var('spider_item', ['id'], "url = %s and table_name = %s", where_values)
						people_name = util.get_formatted_name(util.sanitize_content(author_alias[index]))
						if(people_id == None):
							add_dummy = True
						else:
							where_values = []
							where_values.append(people_name['name'])
							where_values.append(people_name['lastname'])
							where_values.append(people_id)
							alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = %s and people_id = %s", where_values)
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
						#print "Added dummy people"
						
					new_people = {}
					new_people['id'] = people_id
					new_people['alias_used_id'] = alias_used_id
					new_people['relation_type_id'] = relation_type_id
					peoples.append(new_people)
					
				artist_alias_text = [x for x in artist_alias_text if x != ']']
				relation_type_id = self.dbase.people_relation_type_illustrator
					
				for index, url in enumerate(artist_url):
					add_dummy = False
					if 'add_author' in url:
						#Add dummy author
						people_name = util.get_formatted_name(util.sanitize_content(artist_alias_text[index]))
						add_dummy = True
					else:
						#Get author id from link.
						people_id = self.dbase.get_spider_item_id(url, 'people')
						people_name = util.get_formatted_name(util.sanitize_content(artist_alias[index]))
						if(people_id == None):
							add_dummy = True
						else:
							where_values = []
							where_values.append(people_name['name'])
							where_values.append(people_name['lastname'])
							where_values.append(people_id)
							alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = %s and people_id = %s", where_values)
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
				
				#print original_publisher_url, original_publisher_alias, original_publisher_text
				if not "N/A" in original_publisher_url:
					for index, url in enumerate(original_publisher_url):
						add_dummy = False
						if 'add_publisher' in url:
							#Add dummy company
							company_name = util.sanitize_content(original_publisher_text[index])
							add_dummy = True
						else:
							#Get author id from link.
							company_id = self.dbase.get_spider_item_id(url, 'company')
							company_name = util.sanitize_content(original_publisher_alias[index])
							
							if(company_id == None):
								add_dummy = True
							else:
								where_values = []
								where_values.append(company_name)
								where_values.append(company_id)
								alias_used_id = self.dbase.get_var('company_alias', ['id'], "name = %s and company_id = %s", where_values)
								#print "Alias used id", alias_used_id
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
									#print "Name :", company_name
									alias_used_id = self.dbase.add_alias(company_name, company_id, language_id, 'company', self.dbase.alias_type_alias)
									
						#print "Company name: ", company_name
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
					
				magazines = []
				#Get serialized maganize:
				for index, magazine in enumerate(serialized_publisher_alias):
					maganizes.append(magazine + " " + serialized_publisher_text[index])
				
				maganizes = util.sanitize_content(maganizes)
				
				company_function_type_id = self.dbase.company_function_type_translator
				
				#Get english company:
				if not "N/A" in english_publisher_text:
					country_origin_id = self.dbase.country_us
					language_release = self.dbase.language_en
					
					for index, url in enumerate(english_publisher_url):
						add_dummy = False
						if 'add_publisher' in url:
							#Add dummy company
							company_name = util.sanitize_content(english_publisher_text[index])
							add_dummy = True
						else:
							#Get author id from link.
							company_id = self.dbase.get_spider_item_id(url, 'company')
							company_name = util.sanitize_content(english_publisher_alias[index])
							
							if(company_id == None):
								add_dummy = True
							else:
								where_values = []
								where_values.append(company_name)
								where_values.append(company_id)
								alias_used_id = self.dbase.get_var('company_alias', ['id'], "name = %s and company_id = %s", where_values)
								
								if(alias_used_id == None):
									#Insert alias.
									#print "Name :", company_name
									alias_used_id = self.dbase.add_alias(company_name, company_id, language_release, 'company', self.dbase.alias_type_alias)
									
						#print "Company name: ", company_name
						if(add_dummy):
								
							company_id = self.dbase.create_company(company_name, language_release, country_origin_id, None, None, None, None, None,
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

						
				
				
				create_webnovel_also = False
					
				if(webnovel and company_publisher):
					create_webnovel_also = True
					entity_type_id = self.dbase.entity_type_lightnovel
						
				#format year
				year = util.sanitize_content(year[0])
				
				language = None
				
				#format country. Get country from associated name, if not found country_id will be Japan.
				if not country_id:
					language_country = {'ja': self.dbase.country_jp, 'ko': self.dbase.country_kr, 'zn': self.dbase.country_cn}
					
					language_test = {'ja': 0, 'ko': 0, 'zn' : 0}
					for title in titles:
						if title['language_id'] == self.dbase.language_ja:
							language_test['ja'] += 1
						elif title['language_id'] == self.dbase.language_ko:
							language_test['ko'] += 1
						elif title['language_id'] == self.dbase.language_zh:
							language_test['zn'] += 1
					
					if(language_test['ja'] == language_test['ko'] and language_test['ko'] == language_test['zn']):
						language = language_country['ja']
					else:
						language, value = max(language_test.iteritems(), key=lambda x: x[1])
					
					country_id = language_country[language]
				
				if not language_id:
					if language:
						languages = {'ja': self.dbase.language_ja, 'ko': self.dbase.language_ko, 'zn': self.dbase.language_zh}
						language_id = languages[language]
					else:
						language_id = self.dbase.language_ja
					
				#format related
				relateds = []
				
				if(related):
					lenght_related_text = len(related_text)
					for index, item in enumerate(related):
						#Save dummy if not on database, if in database get id.
						dummy_series_id = self.dbase.get_spider_item_id(url, 'entity')
						collection_series_id = None
						
						if dummy_series_id == None:
							if index < lenght_related_text:
								dummy_name = util.sanitize_title(related_text[index])
							else:
								dummy_name = None
							#Create dummy
							dummy_series_id = self.dbase.create_entity(dummy_name, self.dbase.entity_type_manga, self.dbase.classification_type_12, language_id, country_id)
							self.dbase.add_spider_item('entity', dummy_series_id, item)
						else:
							#Get collection from database:
							where_values = []
							where_values.append(collection_series_id)
							collection_series_id = self.dbase.get_var('entity', ['collection_id'], "id = %s", where_values)
							
						#print "Dummy" , dummy_series_id
						new_related_type = util.sanitize_content(related_type[index])
						
						if new_related_type:
							related_type_id = self.dbase.add_type(new_related_type, 'based')
						else:
							related_type_id = self.dbase.based_type_sequel_spinoff
						
						new_related = {}
						new_related['id'] = dummy_series_id
						new_related['type_id'] = related_type_id
						new_related['type_name'] = new_related_type
						new_related['collection_id'] = collection_series_id
						relateds.append(new_related)
				
				#Format images. The correct would be the edition have image and not entity. But mangaupdate don't save any related editions. 
				#image = image[0]
				formatted_image = []
				for image in images:
					image_array = image.split('.')
					new_image = {}
					new_image['url'] = image
					new_image['extension'] = image_array.pop()
					new_image['name'] = image_array.pop()
					formatted_image.append(new_image)
				
				#Format related Doujinshi
				category_adult = False	
				related_doujin = False
				
				#check if is doujinshi on title
				if(re.search(self.pattern_doujin, romanized_title) != None):
					#if is doujinshi, create a relation of doujinshi type.
					related_doujin = True
					category_adult = True
					#Get original from first part of " dj - "
					original_name = re.sub(self.pattern_remove_doujin, '', romanized_title, flags=re.IGNORECASE)
					original_name = util.sanitize_title(original_name)
					if(original_name):
						where_values = []
						where_values.append(original_name)
						original_id = self.dbase.get_var('entity_alias', ['entity_id'], "name = %s", where_values)
					else:
						original_name = 'Unkown name (Cralwer)'
						original_id = None
						
					if not original_id:
						#create dummy:
						original_id = self.dbase.create_entity(original_name, self.dbase.entity_type_manga, self.dbase.classification_type_12, language_id, country_id)
						self.dbase.add_spider_item('entity', original_id, 'Unknown')
						
				#format collection
				collection_id = None
				collection_started = 'False'
						
				#Get a collection from a related item only if type is prequel, sequel or spin-off. 
				if related_doujin:
					#Get collection from original_name. if don't exists create collection.
					collection_id = self.dbase.create_collection(original_name)
				else:
					#if there is related items
					if relateds:
						'''
						TODO:
						#Get collection from related items (Get from database because some other spider could make other item related with this).
						#Check if related is sequel, doujinshi or based on. If is there is a collection with the name of this entity. Collection will be the first part of the name.
						#Check if related is prequel, if is the collection is the name of prequel if there inst a collection on the prequel.
						#Update name of collection if there is more than one prequel. check recursive prequel.
						#Check which item started the collection.
						#if none found create collection from most used name.
						#Get name to make a new collection name.
						#self.dbase.get_related_item(self, table, first_field, second_field, relation_type, type_id, entity_id, limit = None)
						'''
						for item in relateds:
							if item['collection_id']:
								collection_id = item['collection_id']
								break
				
				if not collection_id:
					#Check if name is similar to another collection already registered. Only check if name is larger then 3 characters.
					#This method can have mismatch collection names and collections will need to be check after all items was crawled using get_related_item.
					if(len(romanized_title) > 3):
						collection_id = self.dbase.get_col('collection', 'id', "%s LIKE '%%' || name || '%%'", series_name)
					
						if not collection_id:
							#create new collection with the first name type, get firstname part using regex.
							original_name = re.sub(self.pattern_replace_name,'',romanized_title)
							collection_id = self.dbase.create_collection(original_name)
				
				'''
					Change this to use a relation on database.
				'''
				#format status
				status = util.sanitize_content(status)
			
				#format animé comparative
				anime_start_end = util.sanitize_content(anime_start_end)

				#format classification_type_id
				if(categories):
					if "Adult" in categories or "Hentai" in categories or "Doujin" in categories or "Seinen" in categories:
						category_adult = True
								
				if(not category_adult):
					classification_type_id = self.dbase.classification_type_12
				else:
					classification_type_id = self.dbase.classification_type_18
				
			except ValueError as e:
				print "Error on formatting and getting IDs to save Series", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Series", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return

			try:
				self.dbase.set_auto_transaction(False)
				entity_id = self.dbase.create_entity(romanized_title, entity_type_id, classification_type_id, language_id, country_id, year, collection_id, collection_started, titles, [], [], [], descriptions, [], [], [], [], companies, peoples, relateds, None, formatted_image, update_id)
				
				if(status):
					self.dbase.add_comment('Crawler status', status, 1, entity_id, 'entity')
				
				if(anime_start_end):
					self.dbase.add_comment('Crawler anime_start_end', anime_start_end, 1, entity_id, 'entity')
					
				if maganizes:
					self.dbase.add_comment('Crawler serialized on', maganizes, 1, entity_id, 'entity')
					
				#Create doujinshi relation.
				if related_doujin:
					self.dbase.add_relation_with_type('entity', 'entity', original_id, entity_id, 'based', self.dbase.based_type_doujin)
			
				
				#Create webnovel for lightnovel
				if create_webnovel_also:
					entity_type_id = self.dbase.entity_type_webnovel
					romanized_title = romanized_title.replace('Novel','Web Novel')
					#create					
					webnovel_id = self.dbase.create_entity(romanized_title, entity_type_id, classification_type_id, language_id, country_id, year, collection_id, collection_started, titles, [], [], [], descriptions, [], [], [], [], [], peoples, relateds, None, formatted_image)
					#make relation Adapted From
					self.dbase.add_relation_with_type('entity', 'entity', webnovel_id, entity_id, 'based', self.dbase.based_type_adapted_from)
					#Add original link if has one on a comment
					if webnovel_link:
						self.dbase.add_comment('Crawler Original Link', webnovel_link, 1, webnovel_id, 'entity')
						
				self.dbase.add_spider_item('entity', entity_id, response.url, True)
				self.dbase.commit()
				print "Success"
				
				#Request release
				if(releases):
					meta = {}
					meta['series_id'] = entity_id
					meta['name'] = romanized_title
					meta['url'] = response.url
					Request(url=releases[0],callback=self.parse_series_releases,meta=meta)
			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Series", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Series", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
		
		"""
			Method used to save releases on database.
			This method save one release per file. In mangaupdates there isn't file information, 
			so for each chapter is create a release. 
			TODO: Save on database.
			
		"""
		def parse_series_releases(self, response):
			print "Releases"
		
			#Get release rows.
			release_row = response.css('#main_content table table tr:nth-child(1) > td table:nth-child(1) tr')
			releases = []
			
			for row in release_row[2:]:
				release = {}
				
				#Get release date from row
				release_date = row.css('td:nth-child(1)::text').extract()
				if release_date:
					release_date = release_date[0]
				release['date'] = release_date
				
				#Get release series from row
				url = row.css('td:nth-child(2) a::attr(href)').extract()
				if url:
					url = url[0]
				release['serie_url'] = url
				url_text = row.css('td:nth-child(2) a::text').extract()
				if url_text:
					url_text = url_text[0]
				release['serie_url_text'] = url_text
				text =  row.css('td:nth-child(2)::text').extract()
				if text:
					text = text[0]
				release['serie_text'] = text
				
				#Get release number from row
				volume = row.css('td:nth-child(3)::text').extract()
				volume = util.sanitize_title(volume)
				release['volume_number'] = volume
				
				chapter = row.css('td:nth-child(4)::text').extract()
				chapter = util.sanitize_title(chapter)
				release['chapter_number'] = chapter
				
				#Get release group from row
				release['group_url'] = row.css('td:nth-child(5) a::attr(href)').extract()
				release['group_text'] = row.css('td:nth-child(5) a::text').extract()
				
				releases.append(release)
				
			#Get next url for the crawler
			next_url = response.css("td.specialtext[align='right'] a::attr(href)").extract()
			
			
			try:
				#Format and save releases
				self.dbase.set_auto_transaction(False)
			
				for index, release in enumerate(releases):
					
					#Format entity_id
					dummy_id = None
					
					if release['serie_url']:
						#get id from spider_item
						dummy_id = self.dbase.get_spider_item_id(release['serie_url'], 'entity')
						
					if not dummy_id:
						dummy_name = util.sanitize_title(release['serie_url_text'])
						if not dummy_name:
							dummy_name = util.sanitize_title(release['serie_text'])
							
						if not dummy_name:
							util.Log(response.url, "Cannot get name of release line %s" % (index + 1))
							return
						else:
							#get id from name
							where_values = []
							where_values.append(dummy_name)
							dummy_id = self.dbase.get_var('entity_alias', ['entity_id'], "name = %s", where_values)
						
						if not dummy_id:
							if(re.search(self.pattern_doujin,dummy_name) != None):
								classification_type = self.dbase.classification_type_18
							else:
								classification_type = self.dbase.classification_type_12
							
							if(re.search(self.pattern_novel, dummy_name) != None):
								type = self.dbase.entity_type_lightnovel
							else:
								type = self.dbase.entity_type_manga
							
							#create dummy
							dummy_id = self.dbase.create_entity(dummy_name, type, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
					
					entity_id = dummy_id
					
					#Format release type. Can be chapter or volume, if chapter is None.
					if release['chapter_number']:
						release_type_id = self.dbase.release_type_chapter
					else:
						release_type_id = self.dbase.release_type_volume
					
					#Format country
					country_id = self.dbase.country_us
					
					#Format language
					language_id = self.dbase.language_en
					languages = []
					languages.append(language_id)
					
					#Format collaborator
					collaborators = []
					for index, url in enumerate(release['group_url']):
						#Check if group exists.
						group_id = self.dbase.get_spider_item_id(url, 'collaborator')
						
						if not group_id:
							#Create dummy
							group_name = None
							if release['group_text'][index]:
								group_name = util.sanitize_title(release['group_text'][index])
							
							if not group_name:
								group_name = 'Unkown'
								
							group_id = self.dbase.create_collaborator(group_name, country_id)
							
						collaborator = {}
						collaborator['id'] = group_id
						collaborator['function_type_id'] = self.dbase.collaborator_function_type_scanlator
						collaborators.append(collaborator)
						
					#Format release date
					new_date = []
					if release['date']:
						ndate = release['date'].split("/")
						if len(ndate) == 3:
							new_date.append(2000 + util.convert_to_number(ndate[2]))
							new_date.append(util.convert_to_number(ndate[0]))
							new_date.append(util.convert_to_number(ndate[1]))
						
					if not new_date:
						new_date.append(1999)
						new_date.append(1)
						new_date.append(1)
					
					date_object = date(new_date[0],new_date[1], new_date[2])
					timestamp = calendar.timegm(date_object.timetuple())
					
					saved = False
					#Format release number. Probability is higher that the chapter and volume is not null. 
					numbers = []
					
					if release['chapter_number']:
						number = {}
						number['parent'] = release['volume_number']
						number['parent_type'] = self.dbase.release_type_volume #1
						number['child'] = util.get_formatted_number(release['chapter_number']) #list of itens
						number['child_type'] = self.dbase.release_type_chapter						
						numbers.append(number)
					elif release['volume_number']:
						volumes = util.get_formatted_number(release['volume_number'])
						for vol in volumes:
							child = []
							child.append(vol)
							
							number = {}
							number['parent'] = None
							number['child'] = child #list of itens
							number['child_type'] = self.dbase.release_type_volume
							
							numbers = []
							numbers.append(number)
							
							#Save release of volume.
							self.dbase.create_release(entity_id, release_type_id, country_id, timestamp, None, None, numbers, languages, collaborators)
							saved = True
					#else: #Release has not number, usually doujinshi has no number, so this will be in blank so numbers is equal to empty [].				

					if not saved:
						#Save releases
						self.dbase.create_release(entity_id, release_type_id, country_id, timestamp, None, None, numbers, languages, collaborators)
				
				self.dbase.commit()
				print "Success"
			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Release", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Release", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
				
			if(next_url):
				Request(url=next_url[0],callback=self.parse_series_releases)