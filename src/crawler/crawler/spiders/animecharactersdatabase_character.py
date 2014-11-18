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
		name = "animecharacter_character"
		allowed_domains = ["www.animecharactersdatabase.com"]
		start_urls = ["http://www.animecharactersdatabase.com/va.php?x=0",
		"http://www.animecharactersdatabase.com/allcharacters.php?x=0"
		]
		
		dbase = None
		login_page = 'http://www.animecharactersdatabase.com/newforum.php'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('va\.php\?x=[0-9]{1,}', 'allcharacters\.php\?x=[0-9]{1,}'),
		deny=('kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/', 'mode'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(
		allow=(#'va\.php\?(x=[0-9]{1,}&)?va_id=[0-9]{1,}(&x=[0-9]{1,})?',
		'character\.php\?id=[0-9]{1,}'
		),
		deny=('char_desc', 'mobile', 'char_asc', 'mode', 'members', 'orderby', 'kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/')), callback='parse_items', follow=False)
		)
		pattern_series = re.compile(ur'source\.php\?id=[0-9]{1,}')
		pattern_replace_name = re.compile(ur'(\(.*\)|\[.*\]|- .*)')
		
		pattern_parenthisis_right = re.compile(ur'.*\(')
		pattern_parenthisis_left = re.compile(ur'\).*')
		pattern_va_id = re.compile(ur'.*[&?]v')
		
		pattern_voice = re.compile(ur'va\.php\?(x=[0-9]{1,}&)?va_id=[0-9]{1,}(&x=[0-9]{1,})?')
		pattern_character = re.compile(ur'character\.php\?id=[0-9]{1,}')
		
		pattern_alphabet = re.compile(ur'[a-zA-Z]{1,}')
		pattern_rh = re.compile(ur'[+-]')
		
		pattern_appears = re.compile(ur'[Aa]pp?ears?[ -][OoIi]n')
		pattern_club = re.compile(ur'\b[Cc]lubs?\b')
		pattern_element = re.compile(ur'\b[eE]lements?\b')
		pattern_birthday = re.compile(ur'\b[bB]irth[ -]?[dD]ay\b')
		pattern_birthyear = re.compile(ur'\b[bB]irth[ -]?[Yy]ear\b')
		pattern_blood = re.compile(ur'(\b[tT]ype\b ?)?[bB]lood[ _]?([tT]ype)?')
		pattern_voice = re.compile(ur'\b[Vv]oice\b')
		pattern_actress = re.compile(ur'\b[Aa]ctress\b')
		pattern_voice_all = re.compile(ur' ?\b[Vv]oice\b \b[Aa]ct(or|ress)\b ?\(.*\)?')
		pattern_voice_brack = re.compile(ur'(\(.*\)|#)')
		pattern_age = re.compile(ur'\b[Aa]ge\b')
		pattern_nickname = re.compile(ur'\b[nN]ick[ -]?[nN]ame\b')
		pattern_title = re.compile(ur'\b[Tt]itles?\b')
		pattern_name = re.compile(ur'\b([Rr]eal|[Nn]ativ|[Tt]ru)e?[ -]?[nN]ame\b')
		pattern_alias = re.compile(ur'\b(A\.?K\.?A\.?|[Aa]lias|[a-zA-Z]{1,} ?[Nn]ame)\b')
		pattern_occupation = re.compile(ur'\b[oO]ccupation\b')
		pattern_taste = re.compile(ur'\b(([Dd]is)?[Ll]ikes?|[Hh]ates?)\b')
		pattern_taste_remove = re.compile(ur':$')
		pattern_zodiac = re.compile(ur'([zZ]odiack?|[sS]tar)[ -]?[sS]igns?')
		pattern_chinese = re.compile(ur'[Cc]hinese[ -]?[sS]igns?')
		pattern_mesa = re.compile(ur'\b[Mm]easure(ment)?s?\b')
		pattern_weapons = re.compile(ur'\b[Ff]ight(ing)?\b \b[Mm]achines?\b')
		pattern_favorites = re.compile(ur'\b[Ff]avorites?\b')
		pattern_fav_remove = re.compile(ur'\b[Ff]avorites?\b ?')
		pattern_bust = re.compile(ur'\b[Bb]ustt?\b')
		pattern_waist = re.compile(ur'\b[Ww]aist?\b')
		pattern_butt = re.compile(ur'\b[Bb]utt\b')
		pattern_height = re.compile(ur'\b[Hh]eight\b')
		pattern_weight = re.compile(ur'\b[Ww]eight\b')
		
		"""
			Method to overwrite the CrawlSpider homonym method.
			This method is used to request a login page.
		"""
		def start_requests(self):
			meta = {}
			meta['dont_start'] = False
			yield Request(
				url=self.login_page,
				callback=self.login,
				dont_filter=True,
				meta=meta
			)

		"""
			Method to make login on mangaupdates.
			This method gets the user name and password from settings.
		"""
		def login(self, response):
			print "loging..."
			return FormRequest.from_response(response,
                    formdata={'username': Settings().get('MUUSERNAME'), 'userpass': Settings().get('MUPASSWORD')},
                    callback=self.after_login,
					#dont forget dont_filter, without it the after_login will not be loaded.
					dont_filter=True, meta=response.meta)

		"""
			Method callback of login method.
			This method check if the login was successful and call start_requests to start the crawler.
		
		"""
		def after_login(self, response):
			if self.check_logged(response):
				self.log("Successfully logged in. Let's start crawling!")
				print "Successfully logged in. Let's start crawling!"
				if not response.meta['dont_start']:
					return super(AnimeCharactersSpider, self).start_requests()
				else:
					return Request(url=response.meta['current_url'],callback=self.parse_items,dont_filter=True)
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
			Method used to log with the crawl running.
			This method is using in combination with check_logged to re-log on the website.
		"""
		def log_in(self, response):
				print "Re-logging"
				new_meta = response.meta
				new_meta['current_url'] = response.url
				new_meta['dont_start'] = True
				return Request(url=self.login_page, callback=self.login, dont_filter=True, meta = new_meta)
				
		"""
			Method used to check if the user on settings is currently logged
			on the website.
		"""
		def check_logged(self, response):
			if "Logout" in response.body:
				return True
			return False
			
			
		"""
			Method called to parse link from extractor.
		"""
		def parse_items(self, response):
			print "Response url: ", response.url
			self.instancialize_database()
			if not self.check_logged(response):
				return self.log_in(response)
	
			#print "Initialized database and parse"
			#if(re.search(self.pattern_voice, response.url) != None):
				#return self.parse_voice_actor(response)
			if(re.search(self.pattern_character, response.url) != None):
				return self.parse_persona(response)
				

		def parse_persona(self, response):
			print "Persona"
			self.instancialize_database()
			if not self.check_logged(response):
				return self.log_in(response)
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'persona')
			except ValueError as e:
				print "Error on getting dummy id on Persona", e.message
			except:
				print "Error on getting dummy on Persona", sys.exc_info()[0]
				util.PrintException()
				
			#Get search name
			search_name = response.css('div.middleframe:nth-child(10) > h1::text').extract()
			
			#Get appears table.
			table_appears = response.css('#bt tr')
			
			romaji, japanese, role, tags, cv, va, type = None, None, None, None, None, None, None
			
			if table_appears:
				#Get Romaji Name
				romaji = table_appears[1].css('td::text').extract()
				
				#Get Japanese Name
				japanese = table_appears[2].css('td::text').extract()
				
				#Get role
				role = table_appears[3].css('td::text').extract()
				
				#Get CV
				#cv = table_appears[5].css('td a::text').extract()
				
			
			#Get image
			images = response.css('#maincontent img:nth-child(6)::attr(src)').extract()		
			
			#Get details table.
			table_details = response.css('div.middleframe:nth-child(10) > div:nth-child(2) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1)').extract()
			
			#Get others images
			other_images = response.css('div.middleframe:nth-child(10) > div:nth-child(2) > div:nth-child(2) > table:nth-child(1) img::attr(src)').extract()
			
			#Get eye color from details.
			detail_eye_color = response.css('tr.s0:nth-child(3) > td:nth-child(3)::text').extract()
			detail_eye_color_no_official = response.css('tr.s0:nth-child(3) > td:nth-child(2)::text').extract()
			
			#Get hair color
			detail_hair_color = response.css('tr.s1:nth-child(4) > td:nth-child(3)::text').extract()
			detail_hair_color_no_official = response.css('tr.s1:nth-child(4) > td:nth-child(2)::text').extract()
			
			#Get hair color highlight
			detail_hair_highligth_color_official = response.css('tr.s1:nth-child(5) > td:nth-child(3)::text').extract()
			detail_hair_highligth_color_no_official = response.css('tr.s1:nth-child(5) > td:nth-child(2)::text').extract()
			
			#Get exact hair color
			detail_exact_hair_color = response.css('tr.s1:nth-child(6) > td:nth-child(3)::text').extract()
			detail_exact_hair_color_no_official = response.css('tr.s1:nth-child(6) > td:nth-child(2)::text').extract()
			
			#Get hair length
			detail_hair_length = response.css('tr.s0:nth-child(7) > td:nth-child(3)::text').extract()
			detail_hair_length_no_official = response.css('tr.s0:nth-child(7) > td:nth-child(2)::text').extract()
			
			#Get apparent age
			detail_apparent_age = response.css('tr.s1:nth-child(8) > td:nth-child(3)::text').extract()
			detail_apparent_age_no_official = response.css('tr.s1:nth-child(8) > td:nth-child(2)::text').extract()
			
			#Get gender
			detail_gender = response.css('tr.s0:nth-child(9) > td:nth-child(3)::text').extract()
			detail_gender_no_official = response.css('tr.s0:nth-child(9) > td:nth-child(2)::text').extract()
			
			#Get animal ears
			detail_animal_ears = response.css('tr.s1:nth-child(10) > td:nth-child(3)::text').extract()
			detail_animal_ears_no_official = response.css('tr.s1:nth-child(10) > td:nth-child(2)::text').extract()

			
			try:
				#Format name
				if search_name:
					search_name = util.get_formatted_name(search_name[0], True)
				
				#Format CV
				#don't need to. CV is just an alias to VA.
				
				comments = []
				#Format role
				role
				if role:
					role = util.sanitize_title(role)
					if role:
						new_comment = {}
						new_comment['title'] = 'Crawler : Persona Role'
						new_comment['content'] = util.sanitize_title(role)
						comments.append(new_comment)
				
				
				#Format alias
				aliases, nicknames, titles, natives, romanized  = [], [], [], [], []
				
				if romaji:
					romaji = romaji[0]
					romaji = util.get_formatted_name(romaji, True)
					if romaji:
						romanized.append(romaji)
					
				if japanese:
					japanese = japanese[0]
					japanese = util.get_formatted_name(japanese, True)
					if japanese:
						natives.append(japanese)
				
				
				#Format table_appears
				occupations, affiliations, unusual_features = [], [], []
				favorites, tastes, weapons, powers, weaknesses = [], [], [], [], []
				
				age, apparent_age = None, None
				bust_size, waist_size, butt_size = None, None, None
				chinese_type_id, zodiac_type_id = None, None
				birthyear, birthday = None, None 
				height, weight = None, None
				occupation, zodiac_type_id = None, None
				blood_type, blood_type_id, blood_rh_type_id = None, None, None
				type = None
				favorites, tastes, weapons, elements = [], [], [], []
				voice_acting, entities, new_images = [], [], []
				tags_id = []
				
				#Format details
				eyes_color, hair_color, hair_highligth_color, exact_hair_color, hair_length, apparent_age, gender = None, None, None, None, None, None, None
				
				animal_ears = False
				
				if detail_eye_color:
					eyes_color = util.sanitize_title(detail_eye_color[0])
				elif detail_eye_color_no_official:
					eyes_color = util.sanitize_title(detail_eye_color_no_official[0])
					
				if detail_hair_color:
					hair_color = util.sanitize_title(detail_hair_color[0])
				elif detail_hair_color_no_official:
					hair_color = util.sanitize_title(detail_hair_color_no_official[0])
					
				if detail_hair_highligth_color_official:
					hair_highligth_color = util.sanitize_title(detail_hair_highligth_color_official[0])
				elif detail_hair_highligth_color_no_official:
					hair_highligth_color = util.sanitize_title(detail_hair_highligth_color_no_official[0])

				if detail_exact_hair_color:
					exact_hair_color = util.sanitize_title(detail_exact_hair_color)
				elif detail_exact_hair_color_no_official:
					exact_hair_color = util.sanitize_title(detail_exact_hair_color_no_official)
					
				if detail_hair_length:
					hair_length = util.sanitize_title(detail_hair_length)
				elif detail_hair_length_no_official:
					hair_length = util.sanitize_title(detail_hair_length_no_official)
					
				if detail_apparent_age:
					apparent_age = util.sanitize_title(detail_apparent_age)
				elif detail_apparent_age_no_official:
					apparent_age = util.sanitize_title(detail_apparent_age_no_official)
					
				if detail_gender:
					detail_gender = util.sanitize_title(detail_gender)
					if detail_gender == 'Male' or detail_gender == 'Female':
						gender = detail_gender
	
				elif detail_gender_no_official:
					detail_gender = util.sanitize_title(detail_gender_no_official)
					if detail_gender == 'Male' or detail_gender == 'Female':
						gender = detail_gender
					
				if not gender:
					gender = 'Undefined'
					
				if detail_animal_ears:
					ears = util.sanitize_title(detail_animal_ears)
					if ears == 'Yes':
						animal_ears = True
				elif detail_animal_ears_no_official:
					ears = util.sanitize_title(detail_animal_ears_no_official)
					if ears == 'Yes':
						animal_ears = True
						
				if animal_ears:
					unusual_features.append('Animal Ears')
			
				entity_id_main = None
				
				#Choose dummy name.
				if search_name:
					dummy_name = search_name
				elif romaji:
					dummy_name = romaji
				elif japanese:
					dummy_name = japanese
				else:
					dummy_name = {}
					dummy_name['name'] = 'Unknown'
					dummy_name['lastname'] = 'Unknown'
						
				#Create dummy persona and get alias_used_id if dummy already not registered.
				if not update_id:
					
					update_id = self.dbase.create_persona(dummy_name['name'], dummy_name['lastname'], gender)
					self.dbase.add_spider_item('persona', update_id, response.url, False)
					
				#if there is already a update_id the name is also registered.
				where_values = []
				where_values.append(update_id)
				alias_used_id = self.dbase.get_var('persona_alias', ['id'], "persona_id = %s", where_values)
				i = 0
				
				for item in table_appears[4:]:
					new_item = util.sanitize_title(item.css('th::text').extract())
					if not new_item:
						new_item = util.sanitize_title(item.css('th a::text').extract())
						
					new_content = item.css('td a::text').extract()
					
					url = item.css('td a::attr(href)').extract()
					
					if new_item and new_content:
						
						#Check appears on:
						if(re.search(self.pattern_appears, new_item) != None):
							#Get entity id from spider_item
							
							entity_id = self.dbase.get_spider_item_id(self.get_formatted_link(url[0]), 'entity')
							#if not entity_id:
							#Need to check for uniqueness in various type of entity to get entity_id from name.	
							if not entity_id:
								#Create dummy
								title_entity = util.sanitize_content(new_content)
								if title_entity:
									entity_id = self.dbase.create_entity(title_entity, self.dbase.entity_type_anime, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
									self.dbase.add_spider_item('entity', entity_id, self.get_formatted_link(url[0]), False)
								else:
									util.Log(response.url, "Failed to save entity related.", False)
									
							if entity_id:
								if not entity_id_main:
									entity_id_main = entity_id
								new_entity = {}
								new_entity['id'] = entity_id
								new_entity['alias_used_id'] = alias_used_id
								if i == 0:
									new_entity['first_appear'] = True
								else:
									new_entity['first_appear'] = False
								entities.append(new_entity)
								i += 1
								
						#Check tagged:
						elif(new_item == 'Tagged'):
							#Format tags
							if new_content:
								for tag in new_content:
									new_tag = util.sanitize_title(tag)
									if new_tag:
										tag_id = self.dbase.add_name_to_table(new_tag, 'tag')
										tags_id.append(tag_id)							
						
						#Check VA
						elif(new_item == 'Voice Actors'):
							
							language_id = None
							country_id = None
							
							for index, nova_url in enumerate(url):
								#check language_id
								test_language = langid.classify(util.sanitize_content(new_content[index]))
								if test_language:
									language_id = self.dbase.get_language_id_from_code(test_language[0])
									
								if not language_id:
									language_id = self.dbase.language_ja
									
								country_id = self.dbase.get_country_from_language_id(language_id, self.dbase.country_jp)
									
								#Check if already is registered.
								voice_id = self.dbase.get_spider_item_id(self.get_formatted_link(nova_url), 'people')
								if voice_id:
									#Get used alias.
									where_values = []
									where_values.append(voice_id)
									alias_used = self.dbase.get_var('people_alias', ['id'],"people_id = %s", where_values)	
									#if new_id is None some data must be gone from database.
									
									new_voice = {}
									new_voice['language_id'] = language_id
									new_voice['id'] = voice_id
									new_voice['entity_id'] = entity_id_main
									new_voice['entity_edition_id'] = None
									new_voice['numbers_edition_id'] = []
									new_voice['observation'] = None
									voice_acting.append(new_voice)
								else:
									#Create dummy
									
									va_names = util.sanitize_title(new_content[index])
									if va_names:
										va_names = va_names.split(',')
										first_name = None
										new_id = None
										new_alias = []
										
										for index_2, name in enumerate(va_names):
											#Get id from people name
											formatted_name = util.get_formatted_name(name, True)
											if formatted_name:
												if index_2 == 0:
													first_name = formatted_name
												else:
													new_alias.append(formatted_name)
												new_id = self.dbase.get_people_id_from_alias(formatted_name['name'],formatted_name['lastname'])										
											if new_id:
												break;
													
										if not new_id:
											#Create dummy with the first name from names and add other name as alias.
											new_id = self.dbase.create_people(first_name['name'], first_name['lastname'], country_id, gender, None, None, None, None, None, None, new_alias)
											self.dbase.add_spider_item('people', new_id, self.get_formatted_link(nova_url), False)
												
										new_voice = {}
										#new_voice['gender'] = gender
										new_voice['language_id'] = language_id
										new_voice['id'] = new_id
										new_voice['entity_id'] = entity_id_main
										new_voice['entity_edition_id'] = None
										new_voice['numbers_edition_id'] = []
										new_voice['observation'] = None
										voice_acting.append(new_voice)
				
						#Check type
						elif(new_item == 'Type'):
							type = util.sanitize_title(item.css('td::text').extract())
				
						#Check weight
						elif(re.search(self.pattern_weight, new_item) != None):
							weight = util.sanitize_title(new_content)
							if weight:
								weight = weight.replace('kg','')
							
						#Check height
						elif(re.search(self.pattern_height, new_item) != None):
							height = util.sanitize_title(new_content)
							if height:
								height = height.replace('cm', '')
							
						#Check club:
						elif(re.search(self.pattern_club, new_item) != None):
							clubs = util.sanitize_title(new_content)
							if clubs:
								clubs = clubs.split(',')
								for club in clubs:
									affiliations.append(club)
							
						#Check element
						elif(re.search(self.pattern_element, new_item) != None):
							for element in new_content:
								new_element = util.sanitize_title(element)
								new_element = new_element.split(',')
								for e in new_element:
									elements.append(e)
									
						#Check birthday
						elif(re.search(self.pattern_birthday, new_item) != None):
							birthday = util.sanitize_title(new_content)
							
						#check birthyear
						elif(re.search(self.pattern_birthyear, new_item) != None):
							birthyear = util.sanitize_title(new_content)
						
						#Check blood type
						elif(re.search(self.pattern_blood, new_item) != None):
							new_content = util.sanitize_title(new_content)
							blood_rh = re.sub(self.pattern_alphabet, '', new_content)
							blood_type = re.sub(self.pattern_rh, '', new_content)
							
							blood_type = util.sanitize_title(blood_type)
							blood_rh = util.sanitize_title(blood_rh)
							
							if blood_type:
								blood_type_id = self.dbase.add_type(util.sanitize_title(blood_type), 'blood')
							
							if blood_rh:
								blood_rh_type_id = self.dbase.add_type(util.sanitize_title(blood_rh), 'blood_rh')
						
						#Check voices 
						elif(re.search(self.pattern_voice, new_item) != None):
							#Check gender
							if(re.search(self.pattern_actress, new_item) != None):
								gender = 'Female'
							else:
								gender = 'Undefined'
							#Check language
							language = re.sub(self.pattern_voice_all,'', new_item)
	
							language_id = None
							country_id = None
							
							if language:
								language = language.split(" ")
								if not isinstance(language, types.StringTypes):
									if len(language) > 1:
										language = language[1]
									else:
										language = language[0]
									
								if len(language) > 2:
									language = language.strip().title()
									if language == 'Brazilian':
										language_id = self.dbase.language_pt
									elif language == 'Rus':
										language_id = self.dbase.language_ru
									else:
										#Check if language name on language table. True for Hebrew type.
										language_id = self.dbase.get_language_id_from_name(language, None, True)
									
									if not language_id:
										#Check if language name on country table.
										language_id = self.dbase.get_language_from_country_name(language, self.dbase.language_ja)
									
								else:
									language = language.strip().lower()
									
									if language == 'br':
										language_id = self.dbase.language_pt
										country_id = self.dbasae.country_br
									elif language == 'cn':
										language_id = self.dbase.language_zh
										country_id = self.dbasae.country_cn
									else:	
										#Check if language code on language table.
										language_id = self.dbase.get_language_id_from_code(language)
										if not language_id:
											language = language.upper()
											#Get language from country table.
											language_id = self.dbase.get_language_from_country_code(language, self.dbase.language_ja)
											country_id = self.dbase.get_country_id_from_code(language)
											
							if not language_id:
								language_id = self.dbase.language_ja
								country_id = self.dbase.country_jp
							
							if not country_id:
								#Get country from language
								country_id = self.dbase.get_country_from_language_id(language_id)
								if not country_id:
									country_id = self.dbase.country_us
							
							va_names = new_content

							for index_element, names in enumerate(va_names):
								new_id = None
								#Each , is for one alias.
								names = names.split(',')
								first_name = None
								new_alias = []
								for index, name in enumerate(names):
									#Get id from people name
									formatted_name = util.get_formatted_name(name, True)
									if formatted_name:
										if index == 0:
											first_name = formatted_name
										else:
											new_alias.append(formatted_name)
										new_id = self.dbase.get_people_id_from_alias(formatted_name['name'],formatted_name['lastname'])										
									if new_id:
										break;
										
								if not new_id:
									#Create dummy with the first name from names and add other name as alias.
									new_id = self.dbase.create_people(first_name['name'], first_name['lastname'], country_id, gender, None, None, None, None, None, None, new_alias)
									self.dbase.add_spider_item('people', new_id, self.get_formatted_link(url[index_element]), False)
									
								new_voice = {}
								#new_voice['gender'] = gender
								new_voice['language_id'] = language_id
								new_voice['id'] = new_id
								new_voice['entity_id'] = entity_id_main
								new_voice['entity_edition_id'] = None
								new_voice['numbers_edition_id'] = []
								new_voice['observation'] = None
								voice_acting.append(new_voice)
									
							new_content = util.sanitize_content(new_content)
							if(re.search(self.pattern_voice_brack, new_content) != None):
								#Save comment
								save_comment = True
								new_comment = {}
								new_comment['title'] = 'Crawler ' + new_item
								new_comment['content'] = util.sanitize_content(new_content)
								comments.append(new_comment)
						
						#Check Age
						elif(re.search(self.pattern_age, new_item) != None):
							age = util.sanitize_title(new_content)
						
						#Check nickname
						elif(re.search(self.pattern_nickname, new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										new_a = util.get_formatted_name(a)
										if new_a:
											nicknames.append(new_a)
								else:
									new_a = util.get_formatted_name(alias)
									if new_a:
										nicknames.append(new_a)

						#Check title
						elif(re.search(self.pattern_title, new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										new_a = util.get_formatted_name(a)
										if new_a:
											titles.append(new_a)
								else:
									new_a = util.get_formatted_name(alias)
									if new_a:
										titles.append(new_a)

						#Check native name
						elif(re.search(self.pattern_name, new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										new_a = util.get_formatted_name(a)
										if new_a:
											natives.append(new_a)
								else:
									new_a = util.get_formatted_name(alias)
									if new_a:
										natives.append(new_a)
						
						#Check alias
						elif(re.search(self.pattern_alias, new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										new_a = util.get_formatted_name(a)
										if new_a:
											aliases.append(new_a)
								else:
									new_a = util.get_formatted_name(alias)
									if new_a:
										aliases.append(new_a)
						
						#Check Occupation
						elif(re.search(self.pattern_occupation, new_item) != None):
							occupation = util.sanitize_title(new_content)
							occupations.append(occupation)
							
						#Check tastes
						elif(re.search(self.pattern_taste, new_item) != None):
							
							taste_type = re.sub(self.pattern_taste_remove, '', new_item)
							taste_type_id = self.dbase.add_type(taste_type, 'taste')
							
							for new_tastes in new_content:
								taste = new_tastes.split(',')
								if(not isinstance(taste, types.StringTypes)):
									for a in taste:
										new_taste = {}
										new_taste['type_id'] = taste_type_id
										new_taste['name'] = a
										tastes.append(new_taste)
								else:
									new_taste = {}
									new_taste['type_id'] = taste_type_id
									new_taste['name'] = taste
									tastes.append(new_taste)
							
						#check signs
						elif(re.search(self.pattern_zodiac, new_item) != None):
							zodiac_type_id = self.dbase.add_name_to_table(util.sanitize_title(new_content), 'zodiac_sign')
						
						elif(re.search(self.pattern_chinese, new_item) != None):
							chinese_type_id = self.dbase.add_name_to_table(util.sanitize_title(new_content), 'chinese_sign')
							
						#Check measurement
						elif(re.search(self.pattern_mesa, new_item) != None):
							new_content = util.sanitize_title(new_content)
							if new_content:
								new_content = new_content.split(' ')
								if len(new_content) == 3:
									bust_size = new_content[0]
									waist_size = new_content[1]
									butt_size = new_content[2]
						#Check bust
						elif(re.search(self.pattern_bust, new_item) != None):
							bust_size = util.sanitize_title(new_content)
						#Check waist
						elif(re.search(self.pattern_waist, new_item) != None):
							waist_size = util.sanitize_title(new_content)
						#Check butt
						elif(re.search(self.pattern_butt, new_item) != None):
							butt_size = util.sanitize_title(new_content)
						#Check weapons
						elif(re.search(self.pattern_weapons, new_item) != None):
							for new_weapon in new_content:
								n_weapon = new_weapon.split(',')
								for n in n_weapon:
									weapon = {}
									weapon['type_id'] = self.dbase.weapon_fighting_machine
									weapon['name'] = util.sanitize_title(n)
									weapons.append(weapon)
						
						#Check favorites
						elif(re.search(self.pattern_favorites, new_item) != None):
							favorite_type = re.sub(self.pattern_fav_remove, '', new_item)
							favorite_type = favorite_type.strip()
							if favorite_type:
								favorite_type_id = self.dbase.add_type(favorite_type, 'favorite')
								for favorite in new_content:
									new_favorite = {}
									new_favorite['type_id'] = favorite_type_id
									new_favorite['name'] = favorite
									favorites.append(new_favorite)
						else:
							new_comment = {}
							new_comment['title'] = 'Crawler ' + new_item
							new_comment['content'] = util.sanitize_content(new_content)
							comments.append(new_comment)
				
				#Format type
				
				if type:
					new_comment = {}
					new_comment['title'] = 'Crawler : Persona Type'
					new_comment['content'] = util.sanitize_title(type)
					comments.append(new_comment)
						
				#Format images
				for image in images:
					image_array = image.split('.')
					new_image = {}
					new_image['url'] = image
					new_image['extension'] = image_array.pop()
					new_image_name = image_array.pop()
					new_image_name = new_image_name.split('/')
					new_image['name'] = new_image_name.pop()
					new_images.append(new_image)
					
				for image in other_images:
					image_array = image.split('.')
					new_image = {}
					new_image['url'] = image
					new_image['extension'] = image_array.pop()
					new_image_name = image_array.pop()
					new_image_name = new_image_name.split('/')
					new_image['name'] = new_image_name.pop()
					new_images.append(new_image)
				
				if not entity_id_main:
					entity_id_main = self.dbase.entity_null
					
				#Add entity_id to voice if is not already set.
				for index, voice in enumerate(voice_acting):
					if not voice['entity_id']:
						voice_acting[index]['entity_id'] = entity_id_main
					
			except ValueError as e:
				print "Error on formatting and getting IDs to save Persona", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Persona", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)

				persona_id = self.dbase.create_persona(dummy_name['name'], dummy_name['lastname'], gender, age, apparent_age, exact_hair_color, bust_size, waist_size, butt_size, chinese_type_id, zodiac_type_id, birthyear, birthday, blood_type_id, blood_rh_type_id, 
				height, weight, eyes_color, hair_length, hair_color, unusual_features, aliases, nicknames, romanized, natives, titles, occupations, affiliations, [], [], voice_acting, entities, [], new_images, favorites, tastes, weapons, [], [], tags_id,
				elements, update_id)
	
				self.dbase.add_spider_item('persona', persona_id, response.url, True)
				
				for comment in comments:
					self.dbase.add_comment(comment['title'], comment['content'], 1, persona_id, 'persona')
					
				self.dbase.commit()
				print "Success"
				
			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Persona", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Persona", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
				
		"""
			Method used 
			TODO: Change anime relation and series status on database so the information is relational. 
		"""
		def parse_voice_actor(self, response):
			print "Series"
			self.instancialize_database()
			if not self.check_logged(response):
				return self.log_in(response)
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'people')
				if not update_id:
					#Get va_id from url and get id from people on database.
					va = urlparse.urlparse(response.url)
					va = urlparse.parse_qs(va[4])
					va_id = va['va_id'][0]
					where_values = []
					where_values.append('%%va_id=' + va_id)
					where_values.append('%%va_id=' + va_id + '&%%')
					where_values.append('people')
					update_id = self.dbase.get_var('spider_item', ['id'], "url like %s or url like %s and table_name = %s", where_values)
						
			except ValueError as e:
				print "Error on getting dummy id on Voice Actors", e.message
			except:
				print "Error on getting dummy on Voice Actors", sys.exc_info()[0]
				util.PrintException()

			#Get main name
			name = response.css('#maincontent div:nth-child(1) table:nth-child(1) tr:nth-child(1) td::text').extract()
			
			#Get second name
			second_name = response.css('#maincontent div:nth-child(1) table:nth-child(1) tr:nth-child(2) td::text').extract()
			
			#Get third name
			third_name = response.css('#maincontent div:nth-child(1) table:nth-child(1) tr:nth-child(3) td::text').extract()
			
			#Get Additional names
			additional_name = response.css('#maincontent div:nth-child(1) table:nth-child(1) tr:nth-child(4) td::text').extract()
			
			#Get language
			language = response.css('#maincontent div:nth-child(1) table:nth-child(1) tr:nth-child(5) td::text').extract()

			#Get characters from first page.
			characters_url = response.css('#tile1 > ul:nth-child(1) li > div:nth-child(1) > a::attr(href)').extract()
			characters_name = response.css('#tile1 > ul:nth-child(1) li > div:nth-child(1) > a::text').extract()
			
			#Get characters page
			char_series_url = response.css('#tile1 > ul:nth-child(1) li > div:nth-child(3) > a::attr(href)').extract()
			char_series_name = response.css('#tile1 > ul:nth-child(1) li > div:nth-child(3) > a::text').extract()
			
			#Get next url
			next_url = response.css('#newpager table tr td + td + td a::attr(href)').extract()
			
			try:
				#Format names
				name = util.sanitize_title(name)
				second_name = util.sanitize_title(second_name)
				third_name = util.sanitize_title(third_name)
				additional_name = util.sanitize_title(additional_name)
				
				additionals_name = []
				if additional_name:
					additionals_name = additional_name.split(',')
				
				#Format language
				
				language_id, country_id = None, None
				
				language = util.sanitize_title(language)
				if language:
					if 'English' in language:
						country_id = self.dbase.country_us
						language_id = self.dbase.language_en
					else:						
						lang = []
						lang.append(language)
						language_id = self.dbase.get_var('language', ['id'], "name = %s", lang)
					
					if language_id:
						#Get country from language:
						country_id = self.dbase.get_country_from_language_id(language_id, self.dbase.country_jp)
				
				if not language_id:
					#Get language from names.
					if second_name:
						new_lang = langid.classify(second_name)
						language_id = self.dbase.get_language_id_from_code(new_lang[0])
						country_id = self.dbase.get_country_from_language_id(language_id, self.dbase.country_jp)
					elif third_name:
						new_lang = langid.classify(third_name)
						language_id = self.dbase.get_language_id_from_code(new_lang[0])
						country_id = self.dbase.get_country_from_language_id(language_id, self.dbase.country_jp)
					
				if not language_id:
					language_id = self.dbase.language_ja
					
				if not country_id:
					country_id = self.dbase.country_jp
				
				native_names = []
				
				'''
				if language_id == self.dbase.language_ja or language_id == self.dbase.language_zh or language_id == self.dbase.language_ko:
					name_first = False
				else:
					name_first = True
				'''
				name_first = True
				
				new_name = util.get_formatted_name(name, name_first)
				
				first_name, last_name = None, None
				
				if new_name:
					first_name = new_name['name']
					last_name = new_name['lastname']
				
				if second_name:
					new_name = util.get_formatted_name(second_name, name_first)
					if new_name:
						native_names.append(new_name)
						if not first_name:
							first_name = new_name['name']
							last_name = new_name['lastname']
					
				if third_name:
					new_name = util.get_formatted_name(third_name, name_first)
					if new_name:
						native_names.append(new_name)
						if not first_name:
							first_name = new_name['name']
							last_name = new_name['lastname']
							
				for new_name in additionals_name:
					new_name = util.get_formatted_name(new_name, name_first)
					if new_name:
						native_names.append(new_name)
						if not first_name:
							first_name = new_name['name']
							last_name = new_name['lastname']
				
				if not first_name:
					first_name = 'Unknown'
					util.Log(response.url, "Unknown name for people", False)
				
				if not last_name:
					last_name = 'Unknown'
					util.Log(response.url, "Unknown last name for people", False)
					
				#Add people dummy for get alias used.
				if not update_id:
					update_id = self.dbase.create_people(first_name, last_name, country_id)
					
				where_values = []
				where_values.append(first_name)
				where_values.append(last_name)
				where_values.append(update_id)
				alias_used_id = self.dbase.get_var('people_alias', ['id'], "name = %s and lastname = %s and people_id = %s", where_values)
				
				if not alias_used_id:
					where_values = []
					where_values.append(update_id)
					alias_used_id = self.dbase.get_var('people_alias', ['id'], "people_id = %s", where_values)
					
				#Format produces series
				entities_produced = []
				for index, url in enumerate(char_series_url):
					new_url = self.get_formatted_link(url)
					new_produce = {}
					#Get id from spider_item
					id = self.dbase.get_spider_item_id(new_url, 'entity')
						
					if not id:
						#Get id from alias
						where_values = []
						where_values.append(char_series_name[index])
						id = self.dbase.get_var('entity_alias', ['entity_id'], "name = %s", where_values)
					if not id:
						#Create dummy.
						id = self.dbase.create_entity(char_series_name[index], self.dbase.entity_type_anime, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
						self.dbase.add_spider_item('entity', id, new_url, False)
						
					new_produce['id'] = id
					new_produce['people_alias_used_id'] = alias_used_id
					new_produce['people_relation_type_id'] = self.dbase.people_relation_type_voice_actor

					entities_produced.append(new_produce)
					
				#Format persona
				personas_voiced = []
				for index, url in enumerate(characters_url):
					new_url = self.get_formatted_link(url)
					#Get id from spider_item
					id = self.dbase.get_spider_item_id(new_url, 'persona')
					persona_name = util.get_formatted_name(characters_name[index],name_first)
					
					if not persona_name:
						persona_name = util.get_formatted_name("NO_NAME",name_first)
						
					if not id:
						#Get id from alias
						#Get id from alias
						where_values = []
						where_values.append(persona_name['name'])
						where_values.append(persona_name['lastname'])
						id = self.dbase.get_var('persona_alias', ['persona_id'], "name = %s and last_name = %s", where_values)
					if not id:
						#Create dummy.
						id = self.dbase.create_persona(persona_name['name'], persona_name['lastname'], 'Undefined')
						self.dbase.add_spider_item('persona', id, new_url, False)
					
					where_values = []
					where_values.append(persona_name['name'])
					where_values.append(persona_name['lastname'])
					where_values.append(id)
					persona_alias_id = self.dbase.get_var('persona_alias', ['id'], "name = %s and last_name = %s and persona_id = %s", where_values)			
				
					new_persona = {}
					new_persona['id'] = id
					new_persona['language_id'] = language_id
					new_persona['alias_used_id'] = persona_alias_id
					new_persona['first_appear'] = False
					new_persona['entity_id'] = entities_produced[index]['id']
					new_persona['entity_edition_id'] = None
					new_persona['observation'] = None
					new_persona['numbers'] = []
					
					personas_voiced.append(new_persona)

			except ValueError as e:
				print "Error on formatting and getting IDs to save Voice", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Voice", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)
				
				#A new people will be created. For people that appear on both mangaupdates and character anime no relation will be made.
				people_id = self.dbase.create_people(first_name, last_name, country_id, None, None, None, None, None, None, None, [], [], native_names, [], entities_produced, [], personas_voiced, [], [], update_id)
				self.dbase.add_spider_item('people', people_id, response.url, True)
				
				self.dbase.commit()
				print "Success"

			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Voice", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Voice", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
			
			if(next_url):
				util.Log(response.url, "Has next url {}".format(next_url[0]), False)
				return Request(url=self.get_formatted_link(next_url[0]),callback=self.parse_voice_actor, dont_filter=True)
				
		"""
			Method used to add the url on animecharacter if the given url is a relative path.
		"""
		def get_formatted_link(self, url):
			if "http://" in url or "https://" in url:
				return url
			else:
				return "http://www.animecharactersdatabase.com/" + url
				