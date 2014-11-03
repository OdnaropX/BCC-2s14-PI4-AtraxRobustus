# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database
from .. import langid
from .. import groups_website
from .. import groups
from .. import util
import re
import urlparse
import sys
import urllib2
import json 

class MangaUpdatesSpider(CrawlSpider):
		name = "mangaupdates_part1"
		"""
			Domain list that are allowed to be followed and parsed.
		"""
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/groups.html?page=1&",
		"http://www.mangaupdates.com/authors.html?page=1&",
		"http://www.mangaupdates.com/publishers.html?page=1&",
		]
		dbase = None
		groups = None
		websites = None
		login_page = 'http://www.mangaupdates.com/login.html'
		
		"""
			Rules for the crawler know what parse and what follow. 
		"""
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('publishers\.html\?page=[0-9]{1,}?'))),
		#Follow
		Rule(LinkExtractor(allow=['groups\.html\?page=[0-9]{1,}?'])),
		#Follow
		Rule(LinkExtractor(allow=('authors\.html\?page=[0-9]{1,}?'), deny=('genre'))),
		#Parse id.
		Rule(LinkExtractor(allow=('id=',
		), deny=('members')), callback='parse_items', follow=False)
		)
		
		pattern_publishers = re.compile(ur'publishers\.html\?id=[0-9]{1,}')
		pattern_groups = re.compile(ur'groups\.html\?id=[0-9]{1,}')
		pattern_authors = re.compile(ur'authors\.html\?id=[0-9]{1,}')
		pattern_json = re.compile(r'.*groups = ', re.DOTALL)
		pattern_json2 = re.compile(r'}.*', re.DOTALL)
		
		pattern_blood = re.compile(ur'[-+]')
		pattern_blood_rh = re.compile(ur'[a-zA-Z]{1,}')
	
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
			print "Logging"
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
					print vars(self.dbase)
					self.dbase = None
					raise SystemExit
				

		"""
			Method used to load the groups website
			TODO: Fix Method, is not working re.sub
		"""
		def load_website(self):
			if(self.groups == None):
				try:
					response = urllib2.urlopen('https://raw.githubusercontent.com/loadletter/mangaupdates-urlfix/master/mangaupdates_group.user.js')
					data = response.read()
					m = re.sub(self.pattern_json, data)
					m = re.sub(self.pattern_json2, m)
					print m
					#print data
						#print "hre5"
						#data = m.group(0).replace('groups = ','', 1)
						#print data
					#print "Data", m.groups()
					print "Hghudjshgnl"
					#self.groups = json.loads(data)
					
				except:
					print "Error on load_groups", sys.exc_info()[0]
		
			
		"""
			Method called to parse link from extractor.
		"""
		def parse_items(self, response):
			self.instancialize_database()
			
			if(re.search(self.pattern_groups, response.url) != None):
				#Parse Groups.
				self.parse_groups(response)
				
			elif(re.search(self.pattern_authors, response.url) != None):
				#Parse Authors.
				self.parse_authors(response)
				
			elif(re.search(self.pattern_publishers, response.url) != None):
				#Parse Publisher.
				self.parse_publishers(response)
					
			
					
		"""
			Method used to retrieve the scanlator information 
		"""
		def parse_groups(self, response):
			print response.url
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'collaborator')
			except ValueError as e:
				print "Error on getting dummy id on Groups", e.message
			except:
				print "Error on getting dummy on Groups", sys.exc_info()[0]
				util.PrintException()
			
			#Get name
			name = response.css('span.specialtext::text').extract()
			
			#Get website				
			website = []
			try:
				#self.load_website()
				id = urlparse.urlparse(response.url)
				qs = urlparse.parse_qs(id[4])
				index = qs['id']
				website.append(groups.groups[index[0]])
			except:
				print "Website not found for group %s" % (response.url)
			
			#Get IRC
			irc = response.css('#main_content table table table tr:nth-child(2) > td:nth-child(2)::text').extract()
			
			#Get Socials
			socials_twitter = response.css('#main_content > table table table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) a::attr(href)').extract()
			socials_facebook = response.css('#main_content > table table table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) a::attr(href)').extract()
			
			#Get Comments		
			comments = response.css('#main_content table table table tr:nth-child(11) > td:nth-child(2)::text').extract()
	
			
			try:
				#Format name
				name = util.sanitize_title(name[0])
				print "Parse groups: ", name
			
				#Format country
				country_id = self.dbase.country_us
				
				#Dont need to format website.
				
				#Format IRC
				if irc:
					irc = util.sanitize_title(irc[0])
					if 'No IRC' in irc:
						irc = None
				
				#Format socials
				socials = []
				#Social Twitter
				for url in socials_twitter:
					social_twitter = {}
					social_twitter['type_id'] = self.dbase.create_social_type_from_url(url)
					social_twitter['url'] = url
					social_twitter['last_checked'] = None
					socials.append(social_twitter)
					
				#Social Facebook
				for url in socials_facebook:
					social_facebook = {}
					social_facebook['type_id'] = self.dbase.create_social_type_from_url(url)
					social_facebook['url'] = url
					social_facebook['last_checked'] = None
					socials.append(social_facebook)
				
				#Format comments
				if(comments != None):
					comments = util.sanitize_content(comments)
			except ValueError as e:
				print "Error on formatting and getting IDs to save Group", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Group", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)
				#Add group to database. If group already exists will not be duplicated.
				collaborator_id = self.dbase.create_collaborator(name, country_id, None, irc, None,[], [], [], socials, [], update_id)
				#Add group comment
				if comments:
					self.dbase.add_comment('Crawler note', comments, 1, collaborator_id, 'collaborator')
				
				#Add url to spider_item
				self.dbase.add_spider_item('collaborator', collaborator_id, response.url, True)
				self.dbase.commit()
				print "Success"
			except ValueError as e:
				print e.message
				self.dbase.rollback()
				print "Error on save Group", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Group", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
				
		"""
			Method used to retrieve the author information.
		"""
		def parse_authors(self, response):
			print response.url
			#Parse author content html and extract texts from TR. Why Table?!! Why!!!! 
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'people')
			except ValueError as e:
				print "Error on getting dummy id Authors", e.message
			except:
				print "Error on getting dummy on Authors", sys.exc_info()[0]
				util.PrintException()
				
			#Get romanized name
			romanized_name = response.css('#main_content .tabletitle > b::text').extract()
			
			#Get images
			images = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(2) > td img').xpath('@src').extract()
			
			#Get associated names
			associated_names = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(5) > td::text').extract()
			
			#Get native names
			native_name = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(8) > td::text').extract()
			
			#Get birthplace
			birth_place = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(11) > td::text').extract()
			
			#Get birthdate
			birth_date = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(14) > td::text').extract()
			
			#Get gender
			gender = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(8) > td::text').extract()
			
			#Get description
			description = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(2) > td::text').extract()
			
			#Get blood type
			blood_type = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(5) > td::text').extract()
			
			#Get socials
			socials_twitter = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(17) > td a::attr(href)').extract()
			socials_facebook = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(20) > td a::attr(href)').extract()
			
			#Get website
			website = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(14) > td a::attr(href)').extract()
				
			try:
				print "Romanized", romanized_name[0]
				#Format romanized_name
				name = util.get_formatted_name(romanized_name[0])
				
				#Format images
				formatted_image = []
				for image in images:
					image_array = image.split('.')
					new_image = {}
					new_image['url'] = image
					new_image['extension'] = image_array.pop()
					new_image['name'] = image_array.pop()
					formatted_image.append(new_image)
				
				#Format associated names
				alias = []
				for names in associated_names:
					names = util.get_formatted_name(names)
					if(names):
						alias.append(names)
					
				#Format native names
				natives = []
				for native in native_name:
					native = util.get_formatted_name(native)
					if(native):
						natives.append(native)
				
				#Format birthplace
				birth_place = util.sanitize_content(birth_place)
			
				#Format birthdate
				birth_date = util.sanitize_content(birth_date)
				if(birth_date == 'N/A'):
					birth_date = None
					
				
				#Format country
				country_id = None
				
				if birth_place:
					country = []
					country.append(birth_place)
					country_id = self.dbase.get_var('country', ['id'], "%s LIKE '%' || name || '%'", country)
					if(country_id == None):
						#check native name.
						if natives:
							text_language = natives[0]
							lang = langid.classify(text_language['name'])
							country_id = self.dbase.get_country_from_language(lang[0])
				
				if not country_id:
					country_id = self.dbase.country_jp
				
				#Format gender
				gender = util.sanitize_title(gender[0])
				
				#Format description
				description = util.sanitize_content(description)
				
				#Format blood type
				blood_type = util.sanitize_title(blood_type[0])
				if blood_type:
					new_blood = re.sub(self.pattern_blood, '', blood_type)
					blood_name = []
					blood_name.append(new_blood)
					blood_type_id = self.dbase.get_var('blood_type', ['id'], 'name = %s', blood_name)
					
					#get rh from blood_type
					new_rh = re.sub(self.pattern_blood_rh,'', blood_type)
					rh_name = []
					rh_name.append(new_rh)
					blood_rh_type_id = self.dbase.get_var('blood_rh_type', ['id'], 'name = %s', rh_name)
				else:
					blood_type_id = None
					blood_rh_type_id = None
					
				#Format socials
				socials = []
				#Social Twitter
				for url in socials_twitter:
					social_twitter = {}
					social_twitter['type_id'] = self.dbase.create_social_type_from_url(url)
					social_twitter['url'] = url
					social_twitter['last_checked'] = None
					socials.append(social_twitter)
					
				#Social Facebook
				for url in socials_facebook:
					social_facebook = {}
					social_facebook['type_id'] = self.dbase.create_social_type_from_url(url)
					social_facebook['url'] = url
					social_facebook['last_checked'] = None
					socials.append(social_facebook)
				
				#Format website.
				if website:
					website = website[0]
				
				print "Website", website
			except ValueError as e:
				print "Error on formatting and getting IDs to save Author", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Author", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)
				
				people_id = self.dbase.create_people(name['name'], name['lastname'], country_id, gender, birth_place, birth_date, blood_type_id, blood_rh_type_id, website, description, alias, [], natives, [], [], [], [], formatted_image, socials, update_id)
				
				#Add url to spider_item
				self.dbase.add_spider_item('people', people_id, response.url, True)
				self.dbase.commit()
				print "Success"
			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Author", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Author", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
		
		"""
			Method used to get the information from publisher. 
			This method will not make any relationship between entity and company.
		"""
		def parse_publishers(self, response):
			print response.url
			#Parse publisher content html and extract texts from TR. Why Table?!! Why!!!! 
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				update_id = self.dbase.get_spider_item_id(response.url, 'company')
			except ValueError as e:
				print "Error on getting dummy id on Publishers", e.message
			except:
				print "Error on getting dummy on Publishers", sys.exc_info()[0]
				util.PrintException()
				
				
			#Get romanized_name
			romanized_name = response.css('span.tabletitle b::text').extract()
	
			#Get type for country origin
			type = response.css('#main_content table table table table tr:nth-child(4) > td:nth-child(1) > table tr:nth-child(5) > td:nth-child(1)::text').extract()
					
			#Get alternated names
			alternate_name = response.css('#main_content table table table table tr:nth-child(4) > td:nth-child(1) > table tr:nth-child(2) > td:nth-child(1)').extract()
				
			#Get website
			website = response.css('#main_content table table table table table tr:nth-child(5) > td:nth-child(1) a::attr(href)').extract()
			
			#Get comments	
			comments = response.css('#main_content table table table table tr:nth-child(4) > td:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)::text').extract()		
			
			try:
				#Format romanized_name
				name = util.sanitize_title(romanized_name[0])
				print "Parse publisher: ", name
			
				#Format alias
				aliases = []
				for alternate in alternate_name:
					code = []
					code.append(langid.classify(alternate)[0])
					language = self.dbase.get_var('language', ['id'], "code = %s", code)
					if(language == None):
						language = self.dbase.language_ja
					alias = {}
					alias['name'] = util.sanitize_title(alternate)
					alias['language_id'] = language
					aliases.append(alias)
				
				use_alias = False
				
				language_id = None
				country_origin_id = None 
				#Format country_origin_id
				type = util.sanitize_title(type[0])
				if(type):
					if 'English' in type:
						country_origin_id = self.dbase.country_us
						language_id - self.dbase.language_en
					elif type != '--':						
						lang = []
						lang.append(type)
						language_id = self.dbase.get_var('language', ['id'], "name = %s", lang)
						if(language_id):
							#Get country from language:
							country_origin_id = self.dbase.get_country_from_language_id(language_id, self.dbase.country_us)
				
				if not country_origin_id:
					language_country = {'ja': self.dbase.country_jp, 'ko': self.dbase.country_kr, 'zn': self.dbase.country_cn}
					language_test = {'ja': 0, 'ko': 0, 'zn' : 0}
					for title in aliases:
						if title['language_id'] == self.dbase.language_ja:
							language_test['ja'] += 1
						elif title['language_id'] == self.dbase.language_ko:
							language_test['ko'] += 1
						elif title['language_id'] == self.dbase.language_zn:
							language_test['zn'] += 1
					
					if(language_test['ja'] == language_test['ko'] and language_test['ko'] == language_test['zn']):
						language_id = language_country['ja']
					else:
						language, value = max(language_test.iteritems(), key=lambda x: x[1])
						language_id =  self.dbase.get_var('language', ['id'], "code = %s", language)
					
					country_origin_id = language_country[language]
					print "Here country id:", country_origin_id 
					
				if not language_id:
					language_id = self.dbase.get_language_from_country_id(country_origin_id, self.dbase.language_en)
					
				#Format website
				if(website):
					website = util.sanitize_title(website[0])
						
				#Format comments
				comments = util.sanitize_content(comments)
					
			except ValueError as e:
				print "Error on formatting and getting IDs to save Publisher", e.message
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				print "Error on formatting Publisher", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				print "Country id", country_origin_id
				self.dbase.set_auto_transaction(False)
				company_id = self.dbase.create_company(name, language_id, country_origin_id, None, None, None, website, None, [], [], [], [], [], [], [], aliases, update_id)	
				if comments:
					self.dbase.add_comment('Crawler note', comments, 1, company_id, 'company')
				
				#Add url to spider_item
				self.dbase.add_spider_item('company', company_id, response.url, True)
				self.dbase.commit()
				print "Success"
			except ValueError as e:
				self.dbase.rollback()
				print "Error on save Publisher", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on save Publisher", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)