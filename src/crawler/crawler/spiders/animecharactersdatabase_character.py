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
		start_urls = [#"http://www.animecharactersdatabase.com/va.php?x=0",
		"http://www.animecharactersdatabase.com/character.php?id=70124"
		]
		
		dbase = None
		login_page = 'http://www.animecharactersdatabase.com/newforum.php'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('va\.php\?x=[0-9]{1,}'), deny=('kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(
		allow=(#'va\.php\?(x=[0-9]{1,}&)?va_id=[0-9]{1,}(&x=[0-9]{1,})?',
		'character\.php\?id=[0-9]{1,}'
		),
		deny=('char_desc', 'mobile', 'char_asc', 'members', 'orderby', 'kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/')), callback='parse_items', follow=False)
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
			print "loging..."
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
			print "..."
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
			self.instancialize_database()
	
			#print "Initialized database and parse"
			#if(re.search(self.pattern_voice, response.url) != None):
				#return self.parse_voice_actor(response)
			if(re.search(self.pattern_character, response.url) != None):
				return self.parse_persona(response)
				

		def parse_persona(self, response):
			print "Persona"
			print response.url
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'persona')
			except ValueError as e:
				print "Error on getting dummy id on Franchise", e.message
			except:
				print "Error on getting dummy on Franchise", sys.exc_info()[0]
				util.PrintException()
				
			#Get search name
			search_name = response.css('div.middleframe:nth-child(10) > h1::text').extract()
			
			#Get appears table.
			table_appears = response.css('#bt tr')
			#item.css('th::text').extract()
			
			romaji, japanese, role, tags, cv, va, type = None, None, None, None, None, None, None
			
			if table_appears:
				#Get Romaji Name
				romaji = table_appears[1].css('td::text').extract()
				
				#Get Japanese Name
				japanese = table_appears[2].css('td::text').extract()
				
				#Get role
				role = table_appears[3].css('td::text').extract()
				
				#Get tags
				tags = table_appears[4].css('td a::text').extract()
				
				#Get CV
				cv = table_appears[5].css('td a::text').extract()
				
				#Get VA			
				va = table_appears[6].css('td a::text').extract()
				
				#Get type
				type = table_appears[7].css('td::text').extract()
			
			#Get image
			image = response.css('#maincontent img:nth-child(6)::attr(src)').extract()		
			
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
			

			'''
			#Verificado.
			
			print detail_eye_color, detail_eye_color_no_official
			print detail_hair_color, detail_hair_color_no_official
			print detail_hair_highligth_color_official, detail_hair_highligth_color_no_official
			print detail_exact_hair_color, detail_exact_hair_color_no_official
			print detail_hair_length, detail_hair_length_no_official
			print detail_apparent_age, detail_apparent_age_no_official
			print detail_gender, detail_gender_no_official
			print detail_animal_ears, detail_animal_ears_no_official 
			'''
			
			return
			
			try:
				#Format name
				
				#Format alias
				aliases = []
				nicknames = []
				titles = []
				natives = []
				
				#Format table_appears
				occupations = []
				affiliations = []
				favorites = [], tastes = [], weapons = [], powers = [], weaknesses = []
				
				EN Voice Actress (X8),EN Voice Actress, EN Voice Actor, JP Voice Actor, Age, 
				JP Voice Actor (2nd), JP Voice Actor, Birthday, EN Voice Actor (Arise), 2nd EN Voice Actor
				EN Voice Actor (Mini Sengoku Basara), Blood Type, Zodiack Sign,
				Titles, AKA, age, BR Voice Actor, Birthyear, Occupation, Favorite food,  	KO Voice Actor, Fighting Machines 
				A.K.A, FR Voice Actress , DE Voice Actress, DE Voice Actress, DE Voice Actor
				English Voice Actor, IT Voice Actor , CA Voice Actress, EN Voice Actor (Pokemon: Origins) ,Brazilian Voice Actor,
				Waist , Bust,  	Doubles Partner, JP Voice Actor #2 , JP Voice Actor #1,Dislikes , Star Sign
				Pen Name , True Name, Club , Favorite color , Element, Hebrew Voice Actor, Hate, Like,
				measurements, Star Sign, Nickname, Real Name, French Name, PAL Voice Actor
				EN Voice Actress (Fate/Zero), EN Voice Actor (Fate/Zero),  	EN Voice Actor #1 & #3 
				Likes ,Other Names, RUS Voice Actor, PT Voice Actor, ES Voice Actress , IP Voice Actress 
				 	EN Voice Actor (episodes 128-148) 
					EN Voice Actor (episodes 1-10) 
				
				appears_on, age, birthday, weight, height = None, None, None, None, None
				bust_size, waist_size, butt_size = None, None, None
				chinese_sign, zodiac_sign = None, None
				birthyear, birthday = None, None 
				blood_type = None
				height, weight = None, None
				occupation = None, zodiac_type_id = None
				blood_type_id, blood_rh_type_id = None, None 
				
				favorites, tastes, weapons = [], [], []
				comments = []
				
				voice_acting = []
				
				
				for item in table_appears[8:]:
					new_item = util.sanitize_title(item.css('th::text').extract())
					if not new_item:
						new_item = util.sanitize_title(item.css('th a::text').extract())
						
					new_content = item.css('td a::text').extract()
					
					if new_item and new_content:
					
						#Check appears on:
						
						
						#Check birthday
						if(re.search('(\b[tT]ype\b ?)?[bB]lood[ _]?([tT]ype)?', new_item) != None):
						
						#check birthyear
						if(re.search('(\b[tT]ype\b ?)?[bB]lood[ _]?([tT]ype)?', new_item) != None):
						
						
						#Check blood type
						if(re.search('(\b[tT]ype\b ?)?[bB]lood[ _]?([tT]ype)?', new_item) != None):
							new_content = util.sanitize_title(new_content)
							blood_rh = re.sub(pattern_alphabet, '', new_content)
							blood_type = re.sub(pattern_rh, '', new_content)
							
							blood_type = util.sanitize_title(blood_type)
							blood_rh = util.sanitize_title(blood_rh)
							
							if blood_type:
								blood_type_id = self.dbase.add_type(util.sanitize_title(blood_type), 'blood')
							
							if blood_rh:
								blood_rh_type_id = self.dbase.add_type(util.sanitize_title(blood_rh), 'blood_rh')
						
						#Check voices 
						elif(re.search('ur\b[Vv]oice\b', new_item) != None):
							new_voice = {}
							#Check gender
							if(re.seach(ur'\b[Aa]ctress\b', new_item) != None):
								new_voice['gender'] = 'Female'
							else:
								new_voice['gender'] = 'Undefined'
							#Check language
							language = re.sub(ur' ?\b[Vv]oice\b \b[Aa]ct(or|ress)\b ?\(.*\)','', new_item)
							language_id = None
							if language:
								if len(language) > 2:
									language = language.strip().title()
									if language == 'Brazillian':
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
									elif language == 'cn':
										language_id = self.dbase.language_zh
									else:	
										#Check if language code on language table.
										language_id = self.dbase.get_language_id_from_code(language)
										if not language_id:
											#Get language from country table.
											language_id = self.dbase.get_language_from_country_code(language, self.dbase.language_ja)
							if language_id == None:
								language_id = self.dbase.language_ja
							
							new_voice['language_id'] = language_id
							voice_acting.append(new_voice)
						
						
						#Check Age
						elif(re.search('\b[Aa]ge\b', new_item) != None):
							age = uti.sanitize_title(new_content)
						
						#Check alias
						elif(re.search('\b(A\.?K\.?A\.?|[Pp]en ?[Nn]ame|[Aa]lias)\b', new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										aliases.append(a)
								else:
									aliases.append(alias)
						
						#Check nickname
						elif(re.search('\b[nN]ick[ -]?[nN]ame\b', new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										nicknames.append(a)
								else:
									nicknames.append(alias)

						#Check title
						elif(re.search('\b[Tt]itles?\b', new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										titles.append(a)
								else:
									titles.append(alias)

						#Check native name
						elif(re.search('\b([Rr]eal|[Nn]ativ|[Tt]ru)e?[ -]?[nN]ame\b', new_item) != None):
							for aliase in new_content:
								alias = aliase.split(',')
								if(not isinstance(alias, types.StringTypes)):
									for a in alias:
										natives.append(a)
								else:
									natives.append(alias)
						
						#Check Occupation
						elif(re.search('\b[oO]ccupation\b', new_item) != None):
							occupation = util.sanitize_title(new_content)
						
						#Check tastes
						elif(re.search('\b(([Dd]is)?[Ll]ikes?|[Hh]ates?)\b', new_item) != None):
							
							taste_type = re.sub(':$', '', new_item)
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
						elif(re.search('([zZ]odiac|[sS]tar)[ -]?[sS]igns?', new_item) != None):
							zodiac_type_id = self.dbase.add_name_to_table(util.sanitize_title(new_content), 'zodiac_sign')
						
						elif(re.search('([zZ]odiac|[sS]tar)[ -]?[sS]igns?', new_item) != None):
							chinese_type_id = self.dbase.add_name_to_table(util.sanitize_title(new_content), 'chinese_sign')
							
						#Check measurement
						elif(re.search('\b[Mm]easure(ment)?s?\b', new_item) != None):
							new_content = util.sanitize_title(new_content)
							if new_content:
								new_content = new_content.split(' ')
								if len(new_content) == 3:
									bust_size = new_content[0]
									waist_size = new_content[1]
									butt_size = new_content[2]
							
						#Check weapons
						elif(re.search('\b[Ff]ight(ing)?\b \b[Mm]achines?\b', new_item) != None):
							for new_weapon in new_content:
								n_weapon = new_weapon.split(',')
								for n in n_weapon:
									weapon = {}
									weapon['type_id'] = self.dbase.weapon_fighting_machine
									weapon['name'] = util.sanitize_title(n)
									weapons.append(weapon)
						
						#Check favorites
						elif(re.search('\b[Ff]avorites?\b', new_item) != None):
							favorite_type = re.sub('\b[Ff]avorites?\b ?', '')
							favorite_type = favorite_type.strip()
							if favorite_type:
								favorite_type_id = self.dbase.add_type(favorite_type, 'favorite')
								for favorite in new_content:
									new_favorite = {}
									new_favorite['type_id'] = favorite_type_id
									new_favorite['name'] = favorite
									favorites.append(new_favorite)
						else:
							#Save comment
							save_comment = True
							new_comment = {}
							new_comment['title'] = 'Crawler ' + new_item
							new_comment['content'] = util.sanitize_content(new_content)
							comments.append(new_comment)
				
				#Format images
				images = [],
				
				#Format name
				if name:
					name = util.sanitize_title(name)
				
			unusual_features = 
				if not name:
					name = util.sanitize_title(romaji)
				
				franchise_name = name.replace('(Franchise)', '')
				franchise_name = re.sub(self.pattern_replace_name, '', franchise_name)
				
				#Format alias
				aliases = []
				
				#Format role
					
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
			
				persona_id = self.create_persona(name, last_name, gender, age = None, apparent_age = None, exact_hair_color = None, 
				bust_size = None, waist_size = None, butt_size = None, chinese_sign_id = None, zodiac_sign_id = None, birthyear = None, 
				birthday = None, blood_type_id = None, blood_rh_type_id = None, height = None, weight = None, eyes_color = None, hair_lenght = None, hair_color = None,
				unusual_features = [], aliases = [], nicknames = [], occupations = [], affiliations = [], races = [], goods = [], voices_actor = [], entities_appear_on = [],
				relationship = [], images = [], favorites = [], tastes = [], weapons = [], powers = [], weaknesses = [], update_id = None)
	
				self.dbase.add_spider_item('persona', persona_id, response.url, True)
				
				for comment in comments:
					self.dbase.add_comment(comment['title'], comment['content'], 1, persona_id, 'persona')
					
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
		def parse_voice_actor(self, response):
			print "response url: ", response.url
			print "Series"
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
				