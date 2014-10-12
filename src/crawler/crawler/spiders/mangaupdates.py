# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database
import re

class MangaUpdatesSpider(CrawlSpider):
		name = "mangaupdates"
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/groups.html?page=1&",
		"http://www.mangaupdates.com/authors.html?page=1&",
		"http://www.mangaupdates.com/publishers.html?page=1&",
		"http://www.mangaupdates.com/genres.html",
		"http://www.mangaupdates.com/series.html?page=1&",
		"http://www.mangaupdates.com/categories.html?page=1&"]
		dbase = None
		login_page = 'http://www.mangaupdates.com/login.html'
		
		rules = (
		Rule(LinkExtractor(allow=('series\.html\?page=[0-9]{1,}'), deny=('letter', 'orderby', 'filter', 'categories', 'act'))),
		Rule(LinkExtractor(allow=('publishers\.html\?page=[0-9]{1,}'))),
		Rule(LinkExtractor(allow=['categories\.html?page=[0-9]{1,}'])),
		Rule(LinkExtractor(allow=['groups\.html\?page=[0-9]{1,}'])),
		Rule(LinkExtractor(allow=['authors\.html\?page=[0-9]{1,}'])),
		Rule(LinkExtractor(allow=('id=', 'genres\.html')), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'series\.html\?id=[0-9]{1,}')
		pattern_publishers = re.compile(ur'publishers\.html\?id=[0-9]{1,}')
		pattern_groups = re.compile(ur'groups\.html\?id=[0-9]{1,}')
		pattern_categories = re.compile(ur'categories\.html\?id=[0-9]{1,}')
		pattern_authors = re.compile(ur'authors\.html\?id=[0-9]{1,}')
		pattern_genres = re.compile(ur'genres\.html')
	
		def start_requests(self):
			yield Request(
				url=self.login_page,
				callback=self.login,
				dont_filter=True
			)
	
		#def init_request(self):
			#Function call before the crawl begins.
		#	return Request(url=self.login_page, callback=self.login)

		def login(self, response):
			print "login"
			return FormRequest.from_response(response,
                    formdata={'username': Settings().get('MUUSERNAME'), 'password': Settings().get('MUPASSWORD')},
                    callback=self.after_login,
					#dont forget dont_filter, without it the after_login will not be loaded.
					dont_filter=True)

		def after_login(self, response):
			print "here3"
			if "You are currently logged in as" in response.body:
				self.log("Successfully logged in. Let's start crawling!")
				print "Successfully logged in. Let's start crawling!"
				#Now the crawling can begin..
				#return self.initialized()
				return super(MangaUpdatesSpider, self).start_requests()
			else:
				self.log("Bad times :(")
				print "Error login"
				# Something went wrong, we couldn't log in, so nothing happens.
			
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
			
		def parse_items(self, response):
			self.instancialize_database()
			print "Initialized database and parse"
			if(re.search(self.pattern_series, response.url) != None):
				#Parse Series.
				self.parse_series(response)
		
			elif(re.search(self.pattern_groups, response.url) != None):
				#Parse Groups.
				self.parse_groups(response)
				
			elif(re.search(self.pattern_genres, response.url) != None):
				#Parse Genres.
				self.parse_genres(response)
				
			elif(re.search(self.pattern_categories, response.url) != None):
				#Parse Categories.
				self.parse_categories(response)
				
			elif(re.search(self.pattern_authors, response.url) != None):
				#Parse Authors.
				self.parse_authors(response)
				
			elif(re.search(self.pattern_publishers, response.url) != None):
				#Parse Publisher.
				self.parse_publishers(response)
					
		def parse_series(self, response):
			
			#self.log('Hi, this is an item page! %s' % response.url)
			# item = scrapy.Item()
			# item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
			# item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
			#item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        
			#filename = response.url.split("/")[-2]
			filename = response.url.replace("?", "-");
			filename = filename.replace("http://", "");
			filename = filename.replace("/", "-");
			
			with open(filename, 'wb') as f:
				#f.write(response.body)
				f.write("2")
				#filename = response.url.replace("?", "-");
				#filename = filename.replace("http://", "");
				#filename = filename.replace("/", "-");
				#with open("urls.txt", 'a') as f:
				#	f.write(response.url + "\n")
				
		def parse_groups(self, response):	
			#Parse group content html and extract texts from right TDs.
			content = response.css('td.text.table_content tbody tr td + td::text')
			#Extract content from TDs
			print vars(content)
			#Add group to database. If group already exists will not be duplicated.
			
			
			
		
		def parse_authors(self, response):
			print "Authors"
		
		def parse_publishers(self, response):
			print "Publisher"
		
		def parse_categories(self, response):
			#Visita cada link.
			#Para cada link visitado, pega o id da série e associa com a categoria no banco de dados.
			print "Categories"
		
		def parse_genres(self, response):
			self.dbase.insert('function_type', ['teste'], ['name'])
			print vars(self.dbase.get_var('function_type'))
			
			with open("teste.txt", 'a') as f:
				f.write("2")
				