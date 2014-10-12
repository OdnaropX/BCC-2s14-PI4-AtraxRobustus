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
		#Follow
		Rule(LinkExtractor(allow=('series\.html\?page=[0-9]{1,}?'), deny=('letter', 'orderby', 'filter', 'categories', 'act'))),
		#Follow
		Rule(LinkExtractor(allow=('publishers\.html\?page=[0-9]{1,}?'))),
		#Follow
		Rule(LinkExtractor(allow=['categories\.html?page=[0-9]{1,}?'])),
		#Follow
		Rule(LinkExtractor(allow=['groups\.html\?page=[0-9]{1,}?'])),
		#Follow
		Rule(LinkExtractor(allow=['authors\.html\?page=[0-9]{1,}?'])),
		#Parse id and series genre. Series genre page will be add from request on genre parse. 
		Rule(LinkExtractor(allow=('id=',
		#Parse genre from followed links and
		#Parse genre from request on demand items
		'series\.html\?(page=[0-9]{1,})?&genre=[a-zA-Z+_%0-9/]{1,}',
		#Parse category from followed links and
		#Parse category from request on demand items
		'series\.html\?(page=[0-9]{1,}&)?category=[a-zA-Z+_%0-9/]{1,}',
		)), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'series\.html\?id=[0-9]{1,}')
		pattern_publishers = re.compile(ur'publishers\.html\?id=[0-9]{1,}')
		pattern_groups = re.compile(ur'groups\.html\?id=[0-9]{1,}')
		pattern_categories = re.compile(ur'categories\.html\?id=[0-9]{1,}')
		pattern_categories_series = re.compile(ur'series\.html\?(page=[0-9]{1,}&)?category=[a-zA-Z+_%0-9/]{1,}')
		pattern_genres_series = re.compile(ur'series\.html\?(page=[0-9]{1,}&)?genre=[a-zA-Z+_%0-9/]{1,}')
		pattern_authors = re.compile(ur'authors\.html\?id=[0-9]{1,}')
		pattern_genres = re.compile(ur'genres\.html')
	
		def start_requests(self):
			yield Request(
				url=self.login_page,
				callback=self.login,
				dont_filter=True
			)

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
			if(re.search(self.pattern_categories_series, response.url) != None):
				#Parse Series categories.
				self.parse_categories_series(response)
				
			elif(re.search(self.pattern_genres_series, response.url) != None):
				#Parse Series genres.
				self.parse_genres_series(response)
			
			elif(re.search(self.pattern_series, response.url) != None):
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
			
			content = response.css('')
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
			#Parse author content html and extract texts from TR. Why Table?!! Why!!!! 
			content = response.css('#main_content table table table table tbody tr')
			print "Authors"
		
		
		def parse_publishers(self, response):
			#Parse publisher content html and extract texts from TR. Why Table?!! Why!!!! 
			content = response.css('#main_content.text table table table table tbody tr')
			print "Publisher"
			#Get series published by publisher

			#if not on database create series and associated, or think in another method to do this. 
			#maybe it is not necessary.
		
		def parse_genres_series(self, response):
			content = response.css('')
			
		def check_series_type(self, response):
			#from response check what is the type, if is dounjinshi check has tag dounjinshi, if novel check name, if other check Type.
		
		def check_derivate_from(self, response):
			#check if series is derivate from another work.

			#if it is add derivate type if is a new one and create original work if it was not save on database yet using website url to identify the item. 
		
		def check_adult_content(self, response):
			#if have tag adult or (+18) on content.
		
		def parse_categories_series(self, response):
			content = response.css('') 
		
		def parse_categories(self, response):
			#Visita cada link de page=1&. Loop já é feito nas regras.
			#Para cada link visitado, pega o id da série e associa com a categoria no banco de dados.
			content = response.css('table.text.series_rows_table tbody tr')
			#get content until a message "There are no series in the database." is show
			#first td valign top is the page area to page links. 
			print "Categories"
			#pega o numero da pagina no link visitado e avança para a próxima enquanto não é a ultima pagina. 
			
			
		def parse_genres(self, response):
			content = response.css('')
			#self.dbase.insert('function_type', ['teste'], ['name'])
			#print vars(self.dbase.get_var('function_type'))
			
			#with open("teste.txt", 'a') as f:
			#	f.write("2")
				