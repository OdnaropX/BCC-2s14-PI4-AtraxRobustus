# -*- coding: utf-8 -*-
import scrapy
import re
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database

class MangaUpdatesSpider(CrawlSpider):
		name = "mangaupdates_part3"
		"""
			Domain list that are allowed to be followed and parsed.
		"""
		allowed_domains = ["www.mangaupdates.com"]
		start_urls = ["http://www.mangaupdates.com/genres.html",
		"http://www.mangaupdates.com/categories.html?page=1&",
		]
		
		dbase = None
		login_page = 'http://www.mangaupdates.com/login.html'
		
		"""
			Rules for the crawler know what parse and what follow. 
		"""
		rules = (
		#Follow
		Rule(LinkExtractor(allow=['categories\.html\?page=[0-9]{1,}&?'])),
		#Parse series genre and categories. Series genre page will be add from request on genre parse. 
		#Follow
		Rule(LinkExtractor(allow=(
		#Parse genre
		'genres\.html',
		#Parse genre from followed links and
		#Parse genre from request on demand items
		'series\.html\?(page=[0-9]{1,}&)?genre=[a-zA-Z+_%0-9/-]{1,}',
		#Parse category from followed links and
		#Parse category from request on demand items
		'series\.html\?(page=[0-9]{1,}&)?category=[a-zA-Z+_%0-9/-]{1,}',
		), deny=('members')), callback='parse_items', follow=False),
		)
		
		pattern_categories_series = re.compile(ur'series\.html\?(page=[0-9]{1,}&)?category=[a-zA-Z+_%0-9/]{1,}')
		pattern_genres_series = re.compile(ur'series\.html\?(page=[0-9]{1,}&)?genre=[a-zA-Z+_%0-9/]{1,}')
		pattern_genres = re.compile(ur'genres\.html')
	
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
			if(re.search(self.pattern_categories_series, response.url) != None):
				#Parse Series categories.
				self.parse_categories_series(response)
				
			elif(re.search(self.pattern_genres_series, response.url) != None):
				#Parse Series genres.
				self.parse_genres_series(response)
			
			elif(re.search(self.pattern_genres, response.url) != None):
				#Parse Genres.
				self.parse_genres(response)
				
			#Dont need to parse categories because it is handle by the rules.	
		

		"""
			Method used to save all genres on database and pass initial genre link to be crawled.
			The genre link will be parsed by parse_genres_series after been requested.
			TODO: Save on database.
		"""
		def parse_genres(self, response):
			print "Genres"
			
			#Get genre name
			genres = response.css('.releasestitle b::text').extract()
			
			#Get genre link
			genres_links = response.css('#main_content td.text td.text a::attr(href)').extract()
			
			try:
				for genre in genres:
					print genre
					genre = genre.replace('+',' ')
					self.dbase.add_name_to_table(genre, 'genre')
				for	link in genres_links:
					if 'series' in link:
						Request(url=link,callback=self.parse_genres_series)
			except ValueError as e:
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				print "Error on Parse Genre", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])

		"""
			Method to parse the series.html that have genre.
			This method will update the entity classification depending on genre.
			The entities must be already save on database in order for this method to work, else a unknown exception is returned.
		"""
		def parse_genres_series(self, response):
			print "Genre series"
			genre = res = re.sub('.*genre=','', response.url)
			genre = util.sanitize_title(genre.replace('+',' '))
			genre_id = self.dbase.add_name_to_table(genre, 'genre')
			
			series = response.css('td.text.col1 a::text').extract()
			series_url = response.css('td.text.col1 a::attr(href)').extract()
			
			#Get next url for the crawler
			next_url = response.css("td.specialtext[align='right'] a::attr(href)").extract()
			
			
			adult_content = False
			value = []
			value.append(self.dbase.classification_type_18)
			
			#check if content is adult.
			if "Adult" in genre:
				adult_content = True
			elif "Hentai" in genre:
				adult_content = True
			elif "Doujin" in genre:
				adult_content = True
			
			if(adult_content == False and "Seinen" in genre):
				value[0] = self.dbase.classification_type_16
			
			try:
				
				for index, serie in enumerate(series):
					#Get series id from spider_item, if there isn't create dummy.
					series_id = self.dbase.get_spider_item_id(series_url[index], 'entity')
					if not series_id:
						if index < lenght_related_text:
							dummy_name = util.sanitize_title(serie)
						else:
							dummy_name = None
						series_id = self.dbase.create_entity(dummy_name, self.dbase.entity_type_manga, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
						self.dbase.add_spider_item('entity', series_id, series_url[index])

					self.dbase.add_multi_relation(series_id, genre_id, 'entity', 'genre')
					
					if(adult_content):
						#if genre is Hentai, Doujinshi or Adult change classification for 18+ on Series.
						where_value = []
						where_value.append(series_id)
						self.dbase.update('entity',value,['classification_type_id'], "id = %s", where_value)

			except ValueError as e:
				print e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				print "Error on parse series genre", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			
			if(next_url):
				Request(url=next_url[0],callback=self.parse_genres_series)
				
			
		"""
			Method to parse the series.html that have category on URL.
			The entities must be already save on database in order for this method to work, else a unknown exception is returned.
		"""
		def parse_categories_series(self, response):			
			print "Categories series"
			
			category = res = re.sub('.*category=','', response.url)
			category = util.sanitize_title(category.replace('+',' '))
			category_id = self.dbase.add_name_to_table(category, 'tag')
			
			series = response.css('td.text.col1 a::text').extract()
			series_url = response.css('td.text.col1 a::attr(href)').extract()
			
			#Get next url for the crawler
			next_url = response.css("td.specialtext[align='right'] a::attr(href)").extract()
				
			try:
				for index in range(len(series)):
					#Get series id from spider_item, if there isn't create dummy.
					series_id = self.dbase.get_spider_item_id(series_url[index], 'entity')
					if not series_id:
						if index < lenght_related_text:
							dummy_name = util.sanitize_title(serie)
						else:
							dummy_name = None
						series_id = self.dbase.create_entity(dummy_name, self.dbase.entity_type_manga, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
						self.dbase.add_spider_item('entity', series_id, series_url[index])
						
					self.dbase.add_multi_relation(series_id, genre_id, 'entity', 'tag')
					
					#Change type to Web Novel if there category is Web Novel
					#if 'Web Novel' in category:
			
			except ValueError as e:
				print e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				print "Unknown exception"
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			
			if(next_url):
				Request(url=next_url[0],callback=self.parse_categories_series)