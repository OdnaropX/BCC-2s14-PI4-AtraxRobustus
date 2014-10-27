# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database
import re
import urlparse
from .. import langid
from .. import groups_website
import sys
import urllib2
import json 
from .. import groups

class MangaUpdatesSpider(CrawlSpider):
		name = "mangaupdates_part1"
		"""
			Domain list that are allowed to be followed and parsed.
		"""
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/groups.html?page=1&",
		#"http://www.mangaupdates.com/authors.html?page=1&",
		#"http://www.mangaupdates.com/publishers.html?page=1&",
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
			print "Initialized database and parse"
			
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
			Method used to insert
		"""
		def parse_groups(self, response):	
			name = response.css('span.specialtext').extract()
			name = name[0].strip()
			
			country_id = self.dbase.country_us
			
			website = []
			
			try:
				#self.load_website()
				id = urlparse.urlparse(response.url)
				qs = urlparse.parse_qs(id[4])
				index = qs['id']
				website.append(groups.groups[index[0]])
			except:
				print "Website not found for group %s" % (response.url)
				
			irc = response.css('#main_content table table table tr:nth-child(2) > td:nth-child(2)::text').extract()
			if(irc):
				irc = irc[0].strip()
				if(irc == 'No IRC'):
					irc = None
			
			socials = []
			#Social Twitter
			for url in response.css('#main_content table table table tr:nth-child(3) > td:nth-child(2) a::attr(href)').extract():
				social_twitter = {}
				social_twitter['type_id'] = self.dbase.create_social_type_from_url(url)
				social_twitter['url'] = url
				social_twitter['last_checked'] = None
				socials.append(social_twitter)
				
			#Social Facebook
			for url in response.css('#main_content table table table tr:nth-child(4) > td:nth-child(2) a::attr(href)').extract():
				social_facebook = {}
				social_facebook['type_id'] = self.dbase.create_social_type_from_url(url)
				social_facebook['url'] = url
				social_facebook['last_checked'] = None
				socials.append(social_facebook)
			
			comments = response.css('#main_content table table table tr:nth-child(11) > td:nth-child(2)::text').extract()
			if(comments != None):
				comments = "\n".join(comments)
			
			try:
				#Add group to database. If group already exists will not be duplicated.
				collaborator_id = self.dbase.create_collaborator(name, country_id, None, irc, None,[], [], [], socials, [])
				#Add group comment
				self.dbase.add_comment('Crawler note', comments, 1, collaborator_id, 'collaborator')
			except ValueError as e:
				print e.message
			except:
				print "Error on Group", sys.exc_info()[0]
		"""
			Method used to format the name.
		"""
		def get_formatted_name(self, name, name_first = False):
			names = name.split()
			name = {}
			name['name'] = ""
			name['lastname'] = ""
			
			length_names = len(names)
			if(length_names > 1):
				if(name_first):
					name['name'] = names[0] 
					names.remove[0]
					name['lastname'] = " ".join(names) 
				else:
					name['name'] = names.pop()
					name['lastname'] = " ".join(names)
			elif(length_names == 1):
				name['name'] = names[0]
				name['lastname'] = ""
			
			name['name'] = name['name'].strip()
			name['lastname'] = name['lastname'].strip()
			return name;
				
		"""
			Method used to retrieve the author information.
		"""
		def parse_authors(self, response):
			#Parse author content html and extract texts from TR. Why Table?!! Why!!!! 
			
			romanized_name = response.css('#main_content .tabletitle > b::text').extract()
			name = self.get_formatted_name(romanized_name[0])
			
			images = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(2) > td img').xpath('@src').extract()
			formatted_image = []
			for image in images:
				image_array = image.split('.')
				new_image = {}
				new_image['url'] = image
				new_image['extension'] = image_array.pop()
				new_image['name'] = image_array.pop()
				formatted_image.append(new_image)
				

			associated_names = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(5) > td::text').extract()
			alias = []
			for names in associated_names:
				alias.append(self.get_formatted_name(names))
				
			#print associated_names
			
			native_name = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(8) > td::text').extract()
			natives = []
			for native in native_name:
				if(native != 'N/A'):
					natives.append(self.get_formatted_name(native))
					
			#print native_name
			#associated_names = response.css().extract()
			
			birth_place = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(11) > td::text').extract()
			birth_place = ".\n".join(birth_place)
			
			birth_date = response.css('#main_content > table table table table td:nth-child(1) > table tr:nth-child(14) > td::text').extract()
			if(birth_date[0] == 'N/A'):
				birth_date = None
			else:
				#check if date has year.
				date_match = re.compile(ur'[0-9]{4}')
				if(re.search(date_match, birth_date[0]) != None):
					#has year, so must have day and month (I Hope)
					try:
						birth_date = datetime.strptime(birth_date[0], '%Y %B %d')
						birth_date = birth_date.strftime('%Y-%m-%d')
					except:
						birth_date = None
				else:
					birth_date = None
					
			
			country = []
			country.append(birth_place)
			country_id = self.dbase.get_var('country', ['id'], "%s LIKE name = '%' || name || '%'", country)
			if(country_id == None):
				#check native name.
				if(len(natives) > 0):
					text_language = natives[0]
					lang = langid.classify(text_language['name'])
					country_id = self.dbase.get_country_from_language(lang)
			else:
				country_id = countries[0]
				
			#gender
			gender = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(8) > td::text').extract()
			
			description = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(2) > td::text').extract()
			description = "\n".join(description)
			
			blood_type = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(5) > td::text').extract()
			blood_type = blood_type[0].strip()
			if(blood_type != 'N/A'):
				new_blood = re.sub('[-+]', '', blood_type)
				blood_name = []
				blood_name.append(new_blood)
				blood_type_id = self.dbase.get_var('blood_type', ['id'], 'name = %s', blood_name)
			
			new_rh = re.sub('[a-zA-Z]{1,}','', blood_type)
			rh_name = []
			rh_name.append(new_rh)
			blood_rh_type_id = self.dbase.get_var('blood_rh_type', ['id'], 'name = %s', rh_name)
			
			print "BT"
			print blood_rh_type_id
			
			if(blood_rh_type_id != None):
				blood_rh_type_id = blood_rh_type_id[0]
			
			print "BT"
			print blood_rh_type_id
			
			socials = []
			#Social Twitter
			for url in response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(17) > td a::attr(href)').extract():
				social_twitter = {}
				social_twitter['type_id'] = self.dbase.create_social_type_from_url(url)
				social_twitter['url'] = url
				social_twitter['last_checked'] = None
				socials.append(social_twitter)
				
			#Social Facebook
			for url in response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(20) > td a::attr(href)').extract():
				social_facebook = {}
				social_facebook['type_id'] = self.dbase.create_social_type_from_url(url)
				social_facebook['url'] = url
				social_facebook['last_checked'] = None
				socials.append(social_facebook)
				
			#website
			website = response.css('#main_content > table table table table td:nth-child(3) > table tr:nth-child(14) > td a::attr(href)').extract()
				
			try:
				people_id = self.dbase.create_people(name['name'], name['lastname'], country_id, gender[0], birth_place, birth_date, blood_type_id, blood_rh_type_id, website[0], description, alias, [], natives, [], [], [], [], formatted_image, socials)
				#Add url to spider_item
				self.dbase.add_spider_item('people', people_id, response.url, True)
			except ValueError as e:
				print e.message
			except:
				print "Error on Author", sys.exc_info()[0]
		
		"""
			Method used to get the information from publisher. 
			This method will not make any relationship between entity and company.
		"""
		def parse_publishers(self, response):
			#Parse publisher content html and extract texts from TR. Why Table?!! Why!!!! 
			romanized_name = response.css('span.tabletitle b::text').extract()
			name = romanized_name[0]
			
			type = response.css('#main_content table table table table tr:nth-child(4) > td:nth-child(1) > table tr:nth-child(5) > td:nth-child(1)::text').extract()
			if(type):
				if(type[0] == 'English'):
					country_origin_id = self.dbase.country_us
				elif(type[0] == '--'):
					country_origin_id = None
				else:
					lang = []
					lang.append(type[0])
					language = self.dbase.get_var('language', ['id'], "name = %s", lang)
					#Get country from language:
					country_origin_id = self.dbase.get_country_from_language(language, self.dbase.country_us)
					
			alternate_name = response.css('#main_content table table table table tr:nth-child(4) > td:nth-child(1) > table tr:nth-child(2) > td:nth-child(1)').extract()
			aliases = []
			for alternate in alternate_name:
				code = []
				code.append(langid.classify(alternate))
				language = self.dbase.get_var('language', ['id'], "code = %s", code)
				if(language == None):
					language = self.dbase.language_jp
				alias = {}
				alias['name'] = alternate
				alias['language_id'] = language
				aliases.append(alias)
				
			website = response.css('#main_content table table table table table tr:nth-child(5) > td:nth-child(1) a::attr(href)').extract()
			if(website):
				print website
				website = website[0]
				
			comments = response.css('#main_content table table table table tr:nth-child(4) > td:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)::text').extract()		
			if(comments != None):
				comments = "\n".join(comments)
				
			try:
				company_id = self.dbase.create_company(name, country_origin_id, None, None, None, website, None, [], [], [], [], [], [], [], aliases)	
				self.dbase.add_comment('Crawler note', comments, 1, company_id, 'company')
				#Add url to spider_item
				self.dbase.add_spider_item('collaborator', company_id, response.url, True)
			except ValueError as e:
				print e.message
			except:
				print "Error on Publisher", sys.exc_info()[0]
				