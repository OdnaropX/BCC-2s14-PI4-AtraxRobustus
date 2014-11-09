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
		start_urls = [#"http://www.animecharactersdatabase.com/allseries.php?x=0",
		#"http://www.animecharactersdatabase.com/source.php?id=100797",
		"http://www.animecharactersdatabase.com/source.php?id=102662",
		]
		dbase = None
		login_page = 'http://www.animecharactersdatabase.com/newforum.php'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('allseries\.php\?x=[0-9]{1,}'), deny=('kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(allow=('source\.php\?id=[0-9]{1,}'),	deny=('members', 'orderby','kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/')), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'source\.php\?id=[0-9]{1,}')
		pattern_replace_name = re.compile(ur'(\(.*\)|\[.*\]|- .*)')
		
		pattern_parenthisis_right = re.compile(ur'.*\(')
		pattern_parenthisis_left = re.compile(ur'\).*')
		
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
					self.parse_franchise(response)
				else:
					#Parse Series.
					self.parse_series(response)
				

		def parse_franchise(self, response):
			print "Franchise"
			
			return
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'collection')
			except ValueError as e:
				print "Error on getting dummy id on Franchise", e.message
			except:
				print "Error on getting dummy on Franchise", sys.exc_info()[0]
				util.PrintException()
						
			#Get collection name
			name = response.css('div.middleframe:nth-child(3) > h1:nth-child(1)::text').extract()
				
			#Get details table
			table_details = response.css('')
			
			#Get name english
			english_name = response.css('#bt > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text').extract()
			
			#Get romaji name
			romaji = response.css('#bt > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)::text').extract()
			
			#Get furigana name
			furigana = response.css('#bt > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)::text').extract()
			
			#Get japanese name
			japanese = response.css('#bt > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)::text').extract()
			
			#Get owner japanese name
			owners_ja_url = response.css('#bt > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) a::attr(href)').extract()
			owners_ja_text = response.css('#bt > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) a::text').extract()
			
			#Get owner english name
			owners_en_url = response.css('#bt > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2) a::attr(href)').extract()
			owners_en_text = response.css('#bt > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2) a::text').extract()
			
			#Get wiki
			links = response.css('#bt > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(2) a::attr(href)').extract()
			links_name = response.css('#bt > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(2) a::text').extract()
			
			#Get description
			description = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > div:nth-child(12) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)::text').extract()
			
			#Get associated entities.
			entities = response.css('')
			
			print description, name
			
			return
			
			try:
				#Format name
				if name:
					name = util.sanitize_title(name)
				
				if not name:
					name = util.sanitize_title(romaji)
				
				franchise_name = name.replace('(Franchise)', '')
				franchise_name = re.sub(self.pattern_replace_name, '', franchise_name)
				
				#Format alias
				aliases = []
				first = True
				
				new_search = franchise_name.split('/')				
				for part in new_search:
					if first:
						franchise_name = part
						first = False
					else:
						new_title = {}
						new_title['title'] = part
						new_title['language_id'] = self.dbase.language_en
						aliases.append(new_title)
				
				english_name = util.sanitize_title(english_name)
				if english_name:
					new_nme = english_name.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = new
						new_title['language_id'] = self.dbase.language_en
						aliases.append(new_title)
					
				romaji = util.sanitize_title(romaji)
				if romaji:
					new_nme = romaji.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = new
						new_title['language_id'] = self.dbase.language_ja
						aliases.append(new_title)
					
				furigana = util.sanitize_title(furigana)
				if furigana:
					new_nme = furigana.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = furigana
						new_title['language_id'] = self.dbase.language_ja
						aliases.append(new_title)
					
				japanese = util.sanitize_title(japanese)
				if japanese:
					new_nme = japanese.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = japanese
						new_title['language_id'] = self.dbase.language_ja
						aliases.append(new_title)
					
				#Format table details
				for item in table_details[]:
					
					
					
					
				
				
				#Format owner
				aliases_company = []
				
				for index, url in enumerate(owners_ja_url):
					company_name = util.sanitize_title(owners_ja_text[index])
					new_alias = {}
					new_alias['url'] = url
					new_alias['name'] = company_name
					new_alias['language_id'] = self.dbase.language_ja
					aliases_company.append(new_alias)
					
				for index, url in enumerate(owners_en_url):
					company_name = util.sanitize_title(owners_en_text[index])
					new_alias = {}
					new_alias['url'] = url
					new_alias['name'] = company_name
					new_alias['language_id'] = self.dbase.language_en
					aliases_company.append(new_alias)
					
				companies = []
				for item in aliases_company:
					#Create dummy. This method return the company ID and add new aliases if the company already exists. The new alias will be named as romanized type.
					company_id = self.dbase.create_company(item['name'], item['language_id'], self.dbase.country_jp)
					if company_id:
						companies.append(company_id)
						self.dbase.add_spider_item('company', company_id, item['url'], False)
				
				#Format wikis
				wikies = []
				for index, link in enumerate(links):
					wiki = {}
					wiki['name'] = links_name[index]
					wiki['url'] = link
					wiki['language_id'] = self.dbase.language_en
					wikies.append(wiki)
				
				#Format description
				if description:
					description = util.sanitize_content(description)
				
			except ValueError as e:
				print "Error on formatting and getting IDs to save Franchise", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Franchise", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)
			
				collection_id = self.dbase.create_collection(franchise_name, description, [], companies, aliases, self.dbase.language_ja, update_id)
				
				self.dbase.add_spider_item('collection', collection_id, response.url, True)
				self.dbase.commit()
				print "Success"
				
			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Franchise", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Franchise", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
				
		"""
			Method used 
			TODO: Change anime relation and series status on database so the information is relational. 
		"""
		def parse_series(self, response):
			#print response.url	
			print "Series"
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'entity')
			except ValueError as e:
				print "Error on getting dummy id on Series", e.message
			except:
				print "Error on getting dummy on Series", sys.exc_info()[0]
				util.PrintException()
				
			#Get search title
			search_title = response.css('div.middleframe:nth-child(3) > h1:nth-child(1)::text').extract()
		
			#Get type
			type = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > h3:nth-child(6)::text').extract()
			if not type:
				type = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > h3:nth-child(7)::text').extract()
				
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
						
			#Get related work
			related_url = response.css('#tile > ul:nth-child(1) li a::attr(href)').extract()
			
			#Collection name
			notice = response.css('.notice_inner::text').extract()
			notice_name = response.css('.notice_inner > a:nth-child(2)::text').extract()
			notice_url = response.css('.notice_inner > a:nth-child(2)::attr(href)').extract()

			
			#Get synopse
			synopsis = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > div:nth-child(14) table tbody div::text').extract()
			synopsis = util.sanitize_content(synopsis)
			
			if not synopsis:
				synopsis = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > div:nth-child(13) table tbody td::text').extract()
				synopsis = util.sanitize_content(synopsis)
			if not synopsis:
				synopsis = response.css('div.middleframe:nth-child(3) > div:nth-child(2) > div:nth-child(14) table tbody tr td::text').extract()

			#Get images
			images = response.css('div.middleframe:nth-child(6) > div:nth-child(2) img::attr(src)').extract()
			front_image = response.css('.vector table tr > td:nth-child(4) > a:nth-child(1) > img:nth-child(1)::attr(src)').extract()
						
			print related_url
			
			try:
				search_title = util.sanitize_title(search_title)

				#Format type. get from search_title, types avaliable: Franchise, Light Novel, Manga, Anime, Visual Novel, H-Game, OVA, ONA - Original Net Animation, Video Game, Movie, Drama CD
				type = util.sanitize_title(type)
				type_name = re.sub(self.pattern_parenthisis_right, '', type)
				type_name = re.sub(self.pattern_parenthisis_left, '', type_name)
				
				search_title =  re.sub(self.pattern_replace_name,'', search_title)
				
				first = True
				aliases = []
				
				new_search = search_title.split('/')				
				for part in new_search:
					if first:
						search_title = part
						first = False
					else:
						if part:
							new_title = {}
							new_title['title'] = part
							new_title['language_id'] = self.dbase.language_en
							aliases.append(new_title)
			
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
							search_title = search_title + " (Novel)"
						new_name.append(search_title)
						update_id = self.dbase.get_var('entity_alias', ['entity_id'], "name = %s", new_name)

				
				#Format alias. Separe alias by /
								
				english_title = util.sanitize_title(english_title)
				if english_title:
					new_nme = english_title.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = new_nme
						new_title['language_id'] = self.dbase.language_en
						aliases.append(new_title)
					
				romanji_title = util.sanitize_title(romanji_title)
				if romanji_title:
					new_nme = romanji_title.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = new_nme
						new_title['language_id'] = self.dbase.language_ja
						aliases.append(new_title)
					
				furigana_title = util.sanitize_title(furigana_title)
				if furigana_title:
					new_nme = furigana_title.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = new_nme
						new_title['language_id'] = self.dbase.language_ja
						aliases.append(new_title)
					
				japanese_title = util.sanitize_title(japanese_title)
				if japanese_title:
					new_nme = japanese_title.split('/')
					for new in new_nme:
						new_title = {}
						new_title['title'] = new_nme
						new_title['language_id'] = self.dbase.language_ja
						aliases.append(new_title)
				
				
				print len(aliases), type_id, len(table_details)
				
				
				
				
				#Format table details
				episodes = 0
				ova_episodes = 0
				release_date, origin_entity_id, origin_type_id = None, None, None
				classification_type_id = self.dbase.classification_type_12
				genres_id = []
				wikies = []
				companies_id = []
				aliases_company = []
				
				for item in table_details[5:]:
					new_item = util.sanitize_title(item.css('th::text').extract())
					if not new_item:
						new_item = util.sanitize_title(item.css('th a::text').extract())
					
					new_content_url_text = item.css('td a::text').extract()
					new_content_url = item.css('td a::attr(href)').extract()
					new_content_text = item.css('td::text').extract()
				
					if new_item and (new_content_url_text or new_content_text):
						print new_item
						print "teste"
						
						#Check release date
						if new_item == "Release Date":
							release_date = util.sanitize_title(new_content_url_text)
							if not release_date:
								release_date = util.sanitize_title(new_content_text)
								
						#Check studios
						elif "Studio Name" in new_item:# or re.search():
							if new_item == "English Studio Name" or new_item == "Japanese Studio Name":
								if new_item == "Japanese Studio Name":
									language_company = self.dbase.language_ja
								else:
									language_company = self.dbase.language_en
								
								for index, url in enumerate(new_content_url):
									company_name = util.sanitize_title(new_content_url_text[index])
									if company_name:
										new_alias = {}
										new_alias['url'] = url
										new_alias['name'] = company_name
										new_alias['language_id'] = language_company
										aliases_company.append(new_alias)
							'''elif()
								
								
								
							#Check publisher
							elif re.search() != None:
								company_type = 
						
							#Check Developer
							elif re.search() != None:
								company_type = 
							else:
								company_type = self.dbase.company_function_type_creator
								'''
								
								
							
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
									genres_id.append(genre_id)
							
						#Check links
						elif new_item == "Links":
							#Format wikis
							for index, link in enumerate(new_content_url):
							
								if re.search(ur'\bjp\b', link) != None:
									link_language = self.dbase.language_ja
								elif re.search(ur'\bpt\b', link) != None:
									link_language = self.dbase.language_pt
								else:
									link_language = self.dbase.language_en
									
								wiki = {}
								wiki['name'] = new_content_url_text[index]
								wiki['url'] = link
								wiki['language_id'] = link_language
								wikies.append(wiki)
						
						#Check episodes number (Epidoses, OVA)
						elif re.search(ur'\b[eE]pisodes?\b', new_item) != None:
							#check if OVA
							if re.search(ur'\b[OovVAa]{3}\b', new_item) != None:
								
							else:
					
						#Check origin
						elif re.search(ur'[Oo]rig[ie][nm]?', new_item) != None:
							#If Origin in manga
							origin_type = util.sanitize_title(new_contet_text)
							if not origin_type:
								origin_type = util.sanitize_title(new_contet_url_text)
							
							found_origin = False
							if origin_type:
								where_values = []
								where_values.append(origin_type.title())
								origin_type_id = self.dbase.get_var('entity_type', ['id'], "name = %s", where_values)
								if origin_type_id:
									found_origin = True
									origin_entity_id = self.dbase.get_var('entity', ['entity.id'], "entity.entity_type_id = %s and entity_alias.name = %s", where_values, ['entity_alias'], ["entity_alias.entity_id = entity.id"])
									
							if not found_origin:
								util.Log(response.url, "not found origin type", False)
								
						#Check people (Director, Author, Artist, Writer, Composer, ADR Director, Character Design, Illustrator, Scenario
						elif re.search(ur'((ADR|ARD)? ?([Dd]irect|[Aa]uth|[Ii][l]{1,2}ustrat)or|[Aa]rtist|[Ss]cenar(io|y)|[Cc]haracter[ _-]?[Dd]esign|([cC]ompos|[Ww]rit)er)', new_item) != None:
						
						
						#Check twitter
						elif re.search(ur'[Tt]wi[t]{1,2}er', new_item) != None:
							#Add twitter as comment.
						
						else:
							#save comment
				print len(aliases_company)
				return		

				
				
				
				#Format companies creator
				#Get company id from alias				
				
				for item in aliases_company:
					#Create dummy. This method return the company ID and add new aliases if the company already exists. The new alias will be named as romanized type.
					company_id = self.dbase.create_company(item['name'], item['language_id'], self.dbase.country_jp)
					if company_id:
						new_company = {}
						new_company['id'] = company_id
						new_company['function_type_id'] = self.dbase.company_function_type_creator
						companies_id.append(new_company)
						self.dbase.add_spider_item('company', company_id, item['url'], False)
						

				
				
				 
				 
				
				
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
					if(len(search_title) > 3):
						series_name = []
						series_name.append(search_title)
						collection_id = self.dbase.get_col('collection', 'id', "%s LIKE '%%' || name || '%%'", series_name)
					
						if not collection_id:
							#create new collection with the first name type, get firstname part using regex.
							original_name = re.sub(self.pattern_replace_name,'',search_title)
							
							if not original_name:
								original_name = search_title
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
				
				#Format origin
				if not origin_entity_id and found_origin:
					#Create dummy origin.
					if aliases:
						
					new_title = aliases[0]
					origin_entity_id = self.dbase.create_entity(search_title, origin_type_id, classification_type_id, language_id, country_id)
				
				#Format synopsis
				synopses = []
				if synopsis:
					synops = {}
					synops['language_id'] = self.dbase.language_en
					synops['content'] = util.sanitize_content(synopsis)
					synopses.append(synops)
				
				return 
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
				
				entity_id = self.dbase.create_entity(search_title, type_id, classification_type_id, language_id, country_id, release_date, collection_id, collection_started, aliases, [], synopsis, wikies, [], [], [], genres, [], companies_id, [], relateds, None, new_images, update_id)
				
				if origin_entity_id:
					self.add_relation_with_type('entity', 'entity', origin_entity_id, entity_id, 'based', self.dbase.based_type_adapted_from)
					
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