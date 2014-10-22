# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database
import re
import urlparse

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
			
			if(re.search(self.pattern_groups, response.url) != None):
				#Parse Groups.
				self.parse_groups(response)
				
			elif(re.search(self.pattern_authors, response.url) != None):
				#Parse Authors.
				self.parse_authors(response)
				
			elif(re.search(self.pattern_publishers, response.url) != None):
				#Parse Publisher.
				self.parse_publishers(response)
					
			
					

		def parse_groups(self, response):	
			content = response.selector
			for item in content:
				print item
			#Parse group content html and extract texts from right TDs.
			#content = response.css('td.text.table_content tbody tr td + td').__nonzero__()#.extract()
			
			#print content
			print "Groups"
			#Extract content from TDs
			#print vars(content)
			#Add group to database. If group already exists will not be duplicated.
		
		def parse_authors(self, response):
			content = response.selector
			for item in content:
				print item
			#Parse author content html and extract texts from TR. Why Table?!! Why!!!! 
			content = response.css('#main_content table table table table tbody tr').__nonzero__()#.extract()
			#for item in content:
			#	print item
			#print content
			print "Authors"
			#print vars(content)
		
		def parse_publishers(self, response):
			content = response.selector
			for item in content:
				print item
			#Parse publisher content html and extract texts from TR. Why Table?!! Why!!!! 
			content = response.css('#main_content.text table table table table tbody tr').__nonzero__()#.extract()
			#for item in content:
			#	print item
			#print content
			print "Publisher"
			#print vars(content)
			#Get series published by publisher

			#if not on database create series and associated, or think in another method to do this. 
			#maybe it is not necessary.
		
