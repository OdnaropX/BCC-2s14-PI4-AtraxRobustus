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
import types

class AnimeCharactersSpider(CrawlSpider):
		name = "animecharacter_media"
		allowed_domains = ["www.animecharactersdatabase.com"]
		start_urls = ["http://www.animecharactersdatabase.com/allseries.php?x=0"
		]
		dbase = None
		login_page = 'http://www.animecharactersdatabase.com/newforum.php'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('allseries\.php\?x=[0-9]{1,}'), deny=('edit','order','kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(allow=('source\.php\?id=[0-9]{1,}'),	deny=('x=','edit','order','members', 'orderby','kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/')), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'source\.php\?id=[0-9]{1,}')
		pattern_replace_name = re.compile(ur'(\(.*\)|- .*)')
		
		pattern_parenthisis_right = re.compile(ur'.*\(')
		pattern_parenthisis_left = re.compile(ur'\).*')
		
		pattern_language = re.compile(ur'lang=[a-zA-Z]{1,}&')
		pattern_companies = re.compile(ur'([Dd]evelop|[Pp]ublish)er')
		pattern_jp = re.compile(ur'\bj[pa]\b')
		pattern_pt = re.compile(ur'\bpt\b')
		pattern_episodes = re.compile(ur'\b[eE]pisodes?\b')
		pattern_origin = re.compile(ur'[Oo]rig[ie][nm]?')
		pattern_people = re.compile(ur'((ADR|ARD)? ?([Dd]irect|[Aa]uth|[Ii][l]{1,2}ustrat)or|[Aa]rtist|[Ss]cenar(io|y)|[Cc]haracter[ _-]?[Dd]esign|([cC]ompos|[Ww]rit)er|[Mm]usic)')
		pattern_twitter = re.compile(ur'[Tt]wi[t]{1,2}er')

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
                    formdata={'username': Settings().get('MUUSERNAME'), 'userpass': Settings().get('MUPASSWORD')},
                    callback=self.after_login,
					#dont forget dont_filter, without it the after_login will not be loaded.
					dont_filter=True)

		"""
			Method callback of login method.
			This method check if the login was successful and call start_requests to start the crawler.
		
		"""
		def after_login(self, response):
			if "Logout" in response.body:
				self.log("Successfully logged in. Let's start crawling!")
				print "Successfully logged in. Let's start crawling!"
				return super(AnimeCharactersSpider, self).start_requests()
			else:
				#self.log("Bad times :(")
				print "Error login. Begin crawler without login."
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
	
			#print "Initialized database and parse"
			if(re.search(self.pattern_series, response.url) != None):
				search_title = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > h3::text').extract()
				search_title = util.sanitize_content(search_title)

				if "Franchise" in search_title:
					#Parse Franchise
					self.parse_series(response, True)
				else:
					#Parse Series.
					self.parse_series(response)
			
		"""
			Method used 
			TODO: Change anime relation and series status on database so the information is relational. 
			TODO: Change episodes number on database to relate the information.
			TODO: Fix insert on database to use less calls on insert company. Currently the company is being called to verify possible repeated owners.

		"""
		def parse_series(self, response, franchise = False):
			#print response.url	
			if franchise:
				print "Franchise"
			else:
				print "Series"
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				if franchise:
					update_id = self.dbase.get_spider_item_id(response.url, 'collection')
				else:
					update_id = self.dbase.get_spider_item_id(response.url, 'entity')
			except ValueError as e:
				if franchise:
					print "Error on getting dummy id on Franchise", e.message
				else:
					print "Error on getting dummy id on Series", e.message
			except:
				if franchise:
					print "Error on getting dummy on Franchise", sys.exc_info()[0]
				else:
					print "Error on getting dummy on Series", sys.exc_info()[0]
				util.PrintException()
				
			#Get search title/collection name
			series_title = response.css('div.middleframe:nth-child(3) > h1:nth-child(1)::text').extract()

			#Get series ID
			
			#Get details table.
			table_details = response.css('#bt tr')

			#Get english title
			english_title = table_details[1].css('td:nth-child(2)::text').extract()
			
			#Get romaji title
			romanji_title = table_details[2].css('td:nth-child(2)::text').extract()
			
			#Get furigana title
			furigana_title = table_details[3].css('td:nth-child(2)::text').extract()
			
			#Get japanese title
			japanese_title = table_details[4].css('td:nth-child(2)::text').extract()
				
			#Get synopse/Description
			synopsis = response.css('div.middleframe:nth-child(3) > div:nth-child(2) #besttable')
			synopsis = synopsis[2].css('::text').extract()
			
			#Get type
			type = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > h3:nth-child(6)::text').extract()
			if not type:
				type = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > h3:nth-child(7)::text').extract()
			if not type:
				util.Log(response.url, "Verificar type dessa entitdade.", False)
				type = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > h3:nth-child(8)::text').extract()
				
			if not franchise:		
				#Get related work
				related_url = response.css('#tile > ul:nth-child(1) li a::attr(href)').extract()
			
				#Collection name
				notice = response.css('.notice_inner::text').extract()
				notice_name = response.css('.notice_inner > a:nth-child(2)::text').extract()
				notice_url = response.css('.notice_inner > a:nth-child(2)::attr(href)').extract()
			
				#Get images
				images = response.css('div.middleframe:nth-child(6) > div:nth-child(2) img::attr(src)').extract()
				images_url = response.css('div.middleframe:nth-child(6) > div:nth-child(2) a::attr(href)').extract()
			
				front_image = response.css('.vector table tr > td:nth-child(4) > a:nth-child(1) > img:nth-child(1)::attr(src)').extract()
			else:
				#Get associated entities
				entities_url = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > ul:nth-child(14) li a::text').extract()
				entities_text = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > ul:nth-child(14) li a::text').extract()
				
			try:
				series_title = util.sanitize_title(series_title)

				series_title =  re.sub(self.pattern_replace_name,'', series_title)
				
				first = True
				aliases = []
				
				new_search = series_title.split('/')				
				for part in new_search:
					if first:
						series_title = util.sanitize_title(part)
						first = False
					else:
						if part:
							new_title = {}
							new_title['title'] = util.sanitize_title(part)
							new_title['language_id'] = self.dbase.language_en
							aliases.append(new_title)
				
				#Format type. get from series_title, types avaliable: Franchise, Light Novel, Manga, Anime, Visual Novel, H-Game, OVA, ONA - Original Net Animation, Video Game, Movie, Drama CD
				type = util.sanitize_title(type)
				type_name = re.sub(self.pattern_parenthisis_right, '', type)
				type_name = re.sub(self.pattern_parenthisis_left, '', type_name)

				if "H-Game" in type_name:
					type_id = self.dbase.entity_type_erogame 
				elif "OVA" in type_name:
					type_id = self.dbase.entity_type_ova
				elif "Movie" in type_name:
					type_id = self.dbase.entity_type_anime_movie
				else:
					type_id = self.dbase.add_type(type_name, 'entity')
					
				if update_id == None:
					#if is manga, light novel, or book check if there is
					if type_id == self.dbase.entity_type_manga or type_id == self.dbase.entity_type_lightnovel or type_id == self.dbase.entity_type_manhaw or type_id == self.dbase.entity_type_manhua:
						new_name = []
						if type_id == self.dbase.entity_type_lightnovel or type_id == self.dbase.entity_type_webnovel:
							new_search_title = series_title + " (Novel)"
						new_name.append(new_search_title)
						update_id = self.dbase.get_var('entity_alias', ['entity_id'], "name = %s", new_name)

				
				#Format alias. Separe alias by /			
				english_title = util.sanitize_title(english_title)
				if english_title:
					new_nme = english_title.split('/')
					for new in new_nme:
						new = util.sanitize_title(new)
						if new:
							new_title = {}
							new_title['title'] = new
							new_title['language_id'] = self.dbase.language_en
							aliases.append(new_title)
					
				romanji_title = util.sanitize_title(romanji_title)
				if romanji_title:
					new_nme = romanji_title.split('/')
					for new in new_nme:
						new = util.sanitize_title(new)
						if new:
							new_title = {}
							new_title['title'] = new
							new_title['language_id'] = self.dbase.language_ja
							aliases.append(new_title)
					
				furigana_title = util.sanitize_title(furigana_title)
				if furigana_title:
					new_nme = furigana_title.split('/')
					for new in new_nme:
						new = util.sanitize_title(new)
						if new:
							new_title = {}
							new_title['title'] = new
							new_title['language_id'] = self.dbase.language_ja
							aliases.append(new_title)
					
				japanese_title = util.sanitize_title(japanese_title)
				if japanese_title:
					new_nme = japanese_title.split('/')
					for new in new_nme:
						new = util.sanitize_title(new)
						if new:
							new_title = {}
							new_title['title'] = new
							new_title['language_id'] = self.dbase.language_ja
							aliases.append(new_title)
				
				comments = []
				
				#Format table details
				#episodes = 0
				#ova_episodes = 0
				release_date, origin_entity_id, origin_type_id, origin_type = None, None, None, None
				genres_id = []
				aliases_company, companies, peoples, wikies = [], [], [], []
				found_origin = False
				classification_type_id = self.dbase.classification_type_12
				
				for item in table_details[5:]:
					new_item = util.sanitize_title(item.css('th::text').extract())
					if not new_item:
						new_item = util.sanitize_title(item.css('th a::text').extract())
					
					new_content_url_text = item.css('td a::text').extract()
					new_content_url = item.css('td a::attr(href)').extract()
					new_content_text = item.css('td::text').extract()
				
					if new_item and (new_content_url_text or new_content_text):
						#print new_item
						
						#Check release date
						if new_item == "Release Date":
							release_date = util.sanitize_title(new_content_url_text)
							if not release_date:
								release_date = util.sanitize_title(new_content_text)
								
						#Check studios
						elif "Studio Name" in new_item:
							if new_item == "English Studio Name" or new_item == "Japanese Studio Name":
								if new_item == "Japanese Studio Name":
									language_company = self.dbase.language_ja
								else:
									language_company = self.dbase.language_en
								
								for index, url in enumerate(new_content_url):
									company_name = util.sanitize_title(new_content_url_text[index])
									if company_name:
										new_alias = {}
										new_alias['url'] = re.sub(self.pattern_language, '', self.get_formatted_link(url))
										new_alias['name'] = company_name
										new_alias['language_id'] = language_company
										aliases_company.append(new_alias)
								
						#Check publisher and developer.
						elif re.search(self.pattern_companies, new_item) != None:
							#Get company id from alias.
							company_name = util.sanitize_title(new_content_url_text)
							if not company_name:
								company_name = util.sanitize_title(new_content_text)
							
							if company_name:
								#Get function type:
								function_type = self.dbase.add_type(new_item.title(), 'company_function')
								
								new_company_name = company_name.split(',')
								for company_name in new_company_name:
									company_id = None
									if company_name:
										
										where_values = []
										where_values.append(company_name)
										company_id = self.dbase.get_var('company_alias', ['company_id'], "name = %s", where_values)
										#Get relation_type
										if not company_id:
											#create dummy.
											company_id = self.dbase.create_company(company_name, self.dbase.language_ja, self.dbase.country_jp)
										
										company = {}
										company['id'] = company_id
										company['function_type_id'] = function_type
										if not franchise:
											companies.append(company)
										else:
											companies.append(company_id)

						#Check ratings
						elif new_item == "Content Rating":
							#Format rating
							ratings = util.sanitize_title(new_content_text)
							if not ratings:
								ratings = util.sanitize_title(new_content_url_text)
								if ratings:
									if "Mature" in ratings:
										classification_type_id = self.dbase.classification_type_17
									elif "Everyone" in ratings:
										classification_type_id = self.dbase.classification_type_free
									elif "Child" in ratings:
										classification_type_id = self.dbase.classification_type_3
									elif "10+" in ratings:
										classification_type_id = self.dbase.classification_type_10
									elif "Teen" in ratings:
										classification_type_id = self.dbase.classification_type_13
									elif "Adult" in ratings:
										classification_type_id = self.dbase.classification_type_18
				
						#Check genre
						elif new_item == "Genre Tags":
							#Format genre
							genres = new_content_url_text
							for genre in genres:
								new_genre = util.sanitize_title(genre)
								if new_genre:
									#Create genre
									genre_id = self.dbase.add_name_to_table(new_genre.title(), 'genre')
									#if genre_id: Dont need to check, if not save will raise a valueerror.
									new_genre = {}
									new_genre['id'] = genre_id
									genres_id.append(new_genre)
							
						#Check links
						elif new_item == "Links":
							#Format wikis
							for index, link in enumerate(new_content_url):
							
								if re.search(self.pattern_jp, link) != None:
									link_language = self.dbase.language_ja
								elif re.search(self.pattern_pt, link) != None:
									link_language = self.dbase.language_pt
								else:
									link_language = self.dbase.language_en
									
								wiki = {}
								wiki['name'] = new_content_url_text[index]
								wiki['url'] = link
								wiki['language_id'] = link_language
								wikies.append(wiki)
						
						#Check episodes number (Epidoses, OVA)
						elif re.search(self.pattern_episodes, new_item) != None:
							#check if OVA
							#if re.search(ur'\b[OovVAa]{3}\b', new_item) != None:	
							#else:
							content = util.sanitize_title(new_content_url_text)
							if not content:
								content = util.sanitize_title(new_content_text)
								
							if content:
								comment = {}
								comment['title'] = 'Cralwer Episodes Number'
								comment['content'] = content
								comments.append(comment)

						#Check origin
						elif re.search(self.pattern_origin, new_item) != None:
							#If Origin in manga
							origin_type = util.sanitize_title(new_content_text)
							if not origin_type:
								origin_type = util.sanitize_title(new_content_url_text)

							if origin_type:
								where_values = []
								where_values.append(origin_type.title())
								origin_type_id = self.dbase.get_var('entity_type', ['id'], "name = %s", where_values)
								if origin_type_id:
									found_origin = True
									where_values = []
									where_values.append(origin_type_id)
									where_values.append(series_title)
									where_values.append(series_title)
									origin_entity_id = self.dbase.get_var('entity', ['entity.id'], "entity.entity_type_id = %s and (%s like '%%' || entity_alias.name || '%%' or entity_alias.name = %s)", where_values, ['entity_alias'], ["entity_alias.entity_id = entity.id"])
									
							if not found_origin:
								util.Log(response.url, "not found origin type", False)
								
						#Check people (Director, Author, Artist, Writer, Composer, ADR Director, Character Design, Illustrator, Scenario
						elif re.search(self.pattern_people, new_item) != None:
							#Get people id from alias.
							people_name = util.sanitize_title(new_content_url_text)
							if not people_name:
								people_name = util.sanitize_title(new_content_text)
							
							if people_name:
								new_people_name = people_name.split(',')
								for people_name in new_people_name:								
									people_id, alias_used_id = None, None
									people_name = util.get_formatted_name(people_name, True)
									if people_name:
										#Get relation type
										relation_type_id = self.dbase.add_type(new_item.title(), 'produces')
										
										where_values = []
										where_values.append(people_name['name'])
										where_values.append(people_name['lastname'])
										alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = %s", where_values)
										#Get relation_type
										if not alias_used_id:
											#create dummy.
											people_id = self.dbase.create_people(people_name['name'], people_name['lastname'], self.dbase.country_jp)
											#Get alias.
											where_values = []
											where_values.append(people_id)
											alias_used_id = self.dbase.get_var('people_alias', ['id'], "people_id = %s", where_values)
										else:
											#get people_id
											where_values = []
											where_values.append(alias_used_id)
											people_id = self.dbase.get_var('people_alias', ['people_id'], "id = %s", where_values)
											
										people = {}
										people['id'] = people_id
										people['alias_used_id'] = alias_used_id
										people['relation_type_id'] = relation_type_id
										peoples.append(people)#There is no plural for multiple individual but, I don`t care.
								
						#Check twitter
						elif re.search(self.pattern_twitter, new_item) != None:
							#Add twitter as comment.
							comment = {}
							comment['title'] = 'Cralwer Twitter new_item'
							comment['content'] = new_content_url
							comments.append(comment)

						else:
							content = util.sanitize_content(new_content_url_text)
							if not content:
								content = util.sanitize_content(new_content_text)
							else:
								second_content = util.sanitize_content(new_content_text)
								if second_content:
									content = content + '\n' + second_content
							if content:
								#save comment
								comment = {}
								comment['title'] = 'Cralwer unknown new_item' + new_item
								comment['content'] = content
								comments.append(comment)		

				#Format companies creator
				#Get company id from spider_item or alias								
				for item in aliases_company:
					company_update_id = self.dbase.get_spider_item_id(self.get_formatted_link(item['url']), 'company')
					if not company_update_id:
						where_values = []
						where_values.append(item['name'])
						company_update_id = self.dbase.get_var('company_alias', ['company_id'], "name = %s", where_values)
					
					alternate_names = []
					if not company_update_id:
						company_current_alias = item['name']
					else:
						company_current_alias = None
						new_alias = {}
						new_alias['name'] = item['name']
						new_alias['language_id'] = item['language_id']
						alternate_names.append(new_alias)
						
					#Create dummy. This method return the company ID and add new aliases if the company already exists. The new alias will be named as romanized type.
					company_id = self.dbase.create_company(company_current_alias, item['language_id'], self.dbase.country_jp, None, None, None, None, None, [], [], [], [], [], [], [], alternate_names, company_update_id)
					#Don't need to check if company_id is True because a error is raise if not True.
					new_company = {}
					new_company['id'] = company_id
					new_company['function_type_id'] = self.dbase.company_function_type_creator
					if not franchise:
						companies.append(new_company)
					else:
						companies.append(company_id)
					self.dbase.add_spider_item('company', company_id, item['url'], False)

				
				if not franchise:
					
					#Format related work
					relateds = []
					for url in related_url:
						#Check if already registered, else create dummy without name.
						new_url = self.get_formatted_link(url)
						related_id = self.dbase.get_spider_item_id(new_url, 'entity')
						if not related_id:
							#create dummy.
							related_id = self.dbase.create_entity(None, type_id, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
						self.dbase.add_spider_item('entity', related_id, new_url)
						new_related = {}
						new_related['id'] = related_id
						new_related['type_id'] = self.dbase.based_type_sequel
						
						relateds.append(new_related)
						
					#Format images
					new_images = []
					
					for image in images:
						image_array = image.split('.')
						new_image = {}
						new_image['url'] = image
						new_image['extension'] = image_array.pop()
						new_image_name = image_array.pop()
						new_image_name = new_image_name.split('/')
						new_image['name'] = new_image_name.pop()
						new_images.append(new_image)
						
					for image in front_image:
						image_array = image.split('.')
						new_image = {}
						new_image['url'] = image
						new_image['extension'] = image_array.pop()
						new_image_name = image_array.pop()
						new_image_name = new_image_name.split('/')
						new_image['name'] = new_image_name.pop()
						new_images.append(new_image)
					
					#Format collection
					collection_id = None
					collection_started = 'False'
					if "extends" in notice:
						#Get collection from spider item
						if notice_url:
							new_url_collection = self.get_formatted_link(notice_url[0])
							collection_id = self.dbase.get_spider_item_id(new_url_collection, 'new_url_collection')
							
						if not collection_id and notice_name:
							notice_name = util.sanitize_title(notice_name)
							notice_name = re.sub(self.pattern_replace_name,'', notice_name)
							where_values = []
							where_values.append(notice_name)
							collection_id =self.dbase.get_col('collection', 'id', "%s LIKE '%%' || name || '%%'", where_values)
							
							if not collection:
								#create collection
								collection_name = util.normalize_collection_name(util.normalize_collection_name(notice_name))
								collection_id = self.dbase.create_collection(collection_name)
								if new_url_collection:
									add_spider_item('collection', collection_id, new_url_collection)
							elif(isinstance(collection_id, collections.Iterable) and not isinstance(collection_id, types.StringTypes)):
								#return the element most appear on list
								collection_id = util.most_common_oneliner(collection_id)
								
					if not collection_id:
						#Check if name is similar to another collection already registered. Only check if name is larger then 3 characters.
						#This method can have mismatch collection names and collections will need to be check after all items was crawled using get_related_item.
						if(len(series_title) > 3):
							series_name = []
							series_name.append(series_title)
							collection_id = self.dbase.get_col('collection', 'id', "%s LIKE '%%' || name || '%%'", series_name)
						
							if not collection_id:
								#create new collection with the first name type, get firstname part using regex.
								original_name = re.sub(self.pattern_replace_name,'',series_title)
								
								if not original_name:
									original_name = series_title
								original_name = util.normalize_collection_name(original_name)
								collection_id = self.dbase.create_collection(original_name)
							elif(isinstance(collection_id, collections.Iterable) and not isinstance(collection_id, types.StringTypes)):
								#return the element most appear on list
								collection_id = util.most_common_oneliner(collection_id)
								
					#Format language and country
					if type_id == self.dbase.entity_type_manhaw:
						language_id = self.dbase.language_ko
						country_id = self.dbase.country_kr
					elif type_id == self.dbase.entity_type_manhua:
						language_id = self.dbase.language_zh
						country_id = self.dbase.country_cn
					else:
						#Format language
						language_id = self.dbase.language_ja
						#Format country
						country_id = self.dbase.country_jp
				
					#Format classification
					if type_id == self.dbase.entity_type_erogame and classification_type_id != self.dbase.classification_type_18:
						classification_type_id = self.dbase.classification_type_18
				
					#Format origin
					if not origin_entity_id and found_origin:
						#Create dummy origin.
						if aliases:
							new_title = aliases[0]['title']
							origin_entity_id = self.dbase.create_entity(new_title, origin_type_id, classification_type_id, language_id, country_id)
							
					#Format synopsis
					synopses = []
					if synopsis:
						synopis_content = util.sanitize_content(synopsis)
						if synopis_content:
							synops = {}
							synops['language_id'] = self.dbase.language_en
							synops['content'] = synopis_content
							synopses.append(synops)
				
				else:
					#Format name
					franchise_name = series_title.replace('(Franchise)', '')
					franchise_name = re.sub(self.pattern_replace_name, '', franchise_name)
					
					#Format description
					description = None
					if synopsis:
						description = util.sanitize_content(synopsis)
						
					entities = []
					#Format associated entities
					for index, entity in enumerate(entities_text):
						entity_name = util.sanitize_title(entities_text)
						if entity_name:
							#Get id from spider_item
							entity_id = self.dbase.get_spider_item_id(self.get_formatted_link(entities_url[index]), 'entity')
							if not entity_id:
								#Get id from alias.
								where_values = []
								where_values.append(entity_name)
								entity_id = self.dbase.get_var('entity_alias', ['entity_id'], "name = %s", where_values)
							if not entity_id:
								#Create dummy.
								entity_id = self.dbase.create_entity(entity_name, type_id, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
								self.dbase.add_spider_item('entity', entity_id, entities_url[index])
							entities.append(entity_id)

			except ValueError as e:
				if not franchise:
					print "Error on formatting and getting IDs to save Series", e.message
				else:
					print "Error on formatting and getting IDs to save Franchise", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				if not franchise:
					print "Error on formatting Series", sys.exc_info()[0]
				else:
					print "Error on formatting Franchise", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)
				
				if franchise:
					collection_id = self.dbase.create_collection(franchise_name, description, [], companies, aliases, self.dbase.language_ja, update_id, entities)
				
					self.dbase.add_spider_item('collection', collection_id, response.url, True)
				else:
					entity_id = self.dbase.create_entity(series_title, type_id, classification_type_id, language_id, country_id, release_date, collection_id, collection_started, aliases, [], synopses, wikies, [], [], [], genres_id, [], companies, [], relateds, None, new_images, update_id)
					
					if origin_entity_id:
						self.dbase.add_relation_with_type('entity', 'entity', origin_entity_id, entity_id, 'based', self.dbase.based_type_adapted_from)
						
					for comment in comments:
						self.dbase.add_comment(comment['title'], comment['content'], 1, entity_id, 'entity')
					
					self.dbase.add_spider_item('entity', entity_id, response.url, True)

				self.dbase.commit()
				print "Success"

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
		
		def get_formatted_link(self, url):
			if "www.animecharactersdatabase.com/" in url:
				return url
			else:
				return "http://www.animecharactersdatabase.com/" + url