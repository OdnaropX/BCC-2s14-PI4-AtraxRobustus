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
		name = "mangaupdates_part2"
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/series.html?page=1&"]
		dbase = None
		login_page = 'http://www.mangaupdates.com/login.html'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=('series\.html\?page=[0-9]{1,}?'), deny=('letter', 'orderby', 'filter', 'categories', 'act'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(allow=('id=',
		#Parse release from request on demand items
		'releases\.html\?(page=[0-9]{1,}&)?search=[0-9]{1,}&stype=series',
		), deny=('members')), callback='parse_items', follow=False)
		)
		
		pattern_series = re.compile(ur'series\.html\?id=[0-9]{1,}')
		pattern_series_releases = re.compile(ur'releases\.html\?(page=[0-9]{1,}&)?search=[0-9]{1,}&stype=series')
	
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
			if(re.search(self.pattern_series, response.url) != None):
				#Parse Series.
				self.parse_series(response)
		
			elif(re.search(self.pattern_series_releases, response.url) != None):
				#Parse Groups.
				self.parse_series_releases(response)
					
			
		def parse_series(self, response):
			content = response.selector
			romanized_title = content.css('span.releasestitle.tabletitle::text').extract()
			description = content.css('div.sContainer:nth-child(3) > div:nth-child(1) > div:nth-child(2)::text').extract()
			
			
			"""
			entity_type_id
			classification_type_id
			genre_id
			collection_id
			language_id = japones
			country_id = japao, china ou korea
			launch_year = content.css('div.sContainer:nth-child(4) > div:nth-child(1) > div:nth-child(23)::text').extract()
			titles = 
			subtitles
			synopsis
			wiki
			descriptions
			categories #is the genre in mangaupdates
			tags #categories in mangaupdates.
			#personas
			companies
			romanize_subtitle
			
			dbase.create_entity(romanized_title, entity_type_id, classification_type_id, genre_id, collection_id, language_id, country_id, launch_year, collection_started = 0, 
	titles = [], subtitles = [], synopsis = [], wiki = [], descriptions = [], categories = [], tags = [], personas = [], companies = [], romanize_subtitle = None)
			'"""
			print text
			
			#for item in content:
			#	print item
			#content = response.css('.text.series_content_cell > div').__nonzero__()#.extract()
			#for item in content:
			#	print item
			#print content
			print "Series"
			#print vars(content)
			#self.log('Hi, this is an item page! %s' % response.url)
			# item = scrapy.Item()
			# item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
			# item['name'] = response.xpath('//td[@id="item_name"]/text()').__nonzero__()#.extract()
			#item['description'] = response.xpath('//td[@id="item_description"]/text()').__nonzero__()#.extract()

		
		"""
			Method used to save all genres on database and pass initial genre link to be crawled.
			The genre link will be parsed by parse_genres_series after been requested.
			TODO: Save on database.
		"""
		def parse_series_releases(self, response):
			print "Genres"
			genres = response.css('.releasestitle b::text').extract()
			genres_links = response.css('#main_content td.text td.text a::attr(href)').extract()
			
			try:
				for genre in genres:
					print genre
					self.dbase.add_name_to_table(genre, 'genre')
				for	link in genres_links:
					if 'series' in link:
						Request(url=link,callback=self.parse_genres_series)
			#		print link
			except ValueError as e:
				print self.dbase.last_error
				print self.dbase.status_message
				print self.dbase.last_query
			
		#def check_series_type(self, response):
			#from response check what is the type, if is dounjinshi check has tag dounjinshi, if novel check name, if other check Type.
		
		#def check_derivate_from(self, response):
			#check if series is derivate from another work.

			#if it is add derivate type if is a new one and create original work if it was not save on database yet using website url to identify the item. 
		
		#def check_adult_content(self, response):
			#if have tag adult or (+18) on content.
		
		#def get_collection(self,):
			"""
				Pega coleção. Se não for prequel, sequel, spin-off, spinoff, derivate, doujinshi or fanart retorna o nome do trabalho atual.
					como detectar quando a coleção é Gundam, exemplo:
					Kidou Senshi Gundam
		"""	
			
		#def log_error(self, error):
			
				