# -*- coding: utf-8 -*-
import scrapy
import re
import urlparse
import sys

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
from .. import database
from .. import util

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
		Rule(LinkExtractor(allow=['categories\.html\?page=[0-9]{1,}&?'], deny=('orderby', 'act', 'letter'))),
		#Follow genre from genre.html page
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

			if(re.search(self.pattern_genres_series, response.url) != None):
				#Parse Series genres.
				return self.parse_genres_series(response)
				
			elif(re.search(self.pattern_genres, response.url) != None):
				#Parse Genres.
				return self.parse_genres(response)
			
			elif(re.search(self.pattern_categories_series, response.url) != None):
				#Parse Series categories.
				return self.parse_categories_series(response)
			#Dont need to parse categories because it is handle by the rules.	
			

		"""
			Method used to save all genres on database and pass initial genre link to be crawled.
			The genre link will be parsed by parse_genres_series after been requested.
			TODO: Save on database.
		"""
		def parse_genres(self, response):
			print "Genres"
			print "Response url: ", response.url
			
			#Get genre name
			genres = response.css('.releasestitle b::text').extract()
			
			#Get genre link
			genres_links = response.css('#main_content td.text td.text a::attr(href)').extract()
			
			try:
				for genre in genres:
					genre = genre.replace('+',' ')
					genre = genre.replace('%2F',"'")
					print genre
					self.dbase.add_name_to_table(genre, 'genre')
				print "Success"
				
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
			print "Response url: ", response.url
			
			#Get genre
			genre = res = re.sub('.*genre=','', response.url)
			genre = res = re.sub('&.*','', genre)
			
			#Get series
			series = response.css('td.text.col1 a::text').extract()
			series_url = response.css('td.text.col1 a::attr(href)').extract()
			
			#Get next url for the crawler
			next_url = response.css("td.specialtext[align='right'] a::attr(href)").extract()
			
			
			try:
				self.dbase.set_auto_transaction(False)
				
				#Format genre
				genre = util.sanitize_title(genre.replace('+',' '))
				genre_id = self.dbase.add_name_to_table(genre, 'genre')
			
				if genre_id:
					#Format classification
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
					
					if(not adult_content and "Seinen" in genre):
						value[0] = self.dbase.classification_type_16
					elif(not adult_content):
						value[0] = self.dbase.classification_type_12
				
					for index, serie in enumerate(series):
						#Get series id from spider_item, if there isn't create dummy.
						series_id = self.dbase.get_spider_item_id(series_url[index], 'entity')
						if not series_id:
							dummy_name = util.sanitize_title(serie)
							series_id = self.dbase.create_entity(dummy_name, self.dbase.entity_type_manga, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
							self.dbase.add_spider_item('entity', series_id, series_url[index])

						self.dbase.add_multi_relation(series_id, genre_id, 'entity', 'genre')
						
						if(adult_content):
							#if genre is Hentai, Doujinshi or Adult change classification for 18+ on Series.
							where_value = []
							where_value.append(series_id)
							self.dbase.update('entity',value,['classification_type_id'], "id = %s", where_value)
					
				self.dbase.commit()
				
				print "Success"
				
			except ValueError as e:
				self.dbase.rollback()
				print e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on parse series genre", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
				
			if(next_url):
				#print "Next: ", next_url
				util.Log(response.url, "Has next url {}".format(next_url[0]), False)
				return Request(url=next_url[0],callback=self.parse_genres_series)
				
		"""
			Method to parse the series.html that have category on URL.
			The entities must be already save on database in order for this method to work, else a unknown exception is returned.
		"""
		def parse_categories_series(self, response):			
			print "Categories series"
			print "Response url: ", response.url
			
			#Get category name 
			category = re.sub('.*category=','', response.url)
			category = re.sub('&.*','', category)
			
			
			#Get series
			series = response.css('td.text.col1 a::text').extract()
			series_url = response.css('td.text.col1 a::attr(href)').extract()
			
			#Get next url for the crawler
			next_url = response.css("td.specialtext[align='right'] a::attr(href)").extract()
				
			try:
				self.dbase.set_auto_transaction(False)
				
				#Format category 
				category = category.replace('%2F',"'")
				category = util.sanitize_title(category.replace('+',' '))
				
				#Format category id
				category_id = self.dbase.add_name_to_table(category, 'tag')
				
				if category_id:
					for index, serie in enumerate(series):
						#Get series id from spider_item, if there isn't create dummy.
						series_id = self.dbase.get_spider_item_id(series_url[index], 'entity')
						if not series_id:
							dummy_name = util.sanitize_title(serie)
							series_id = self.dbase.create_entity(dummy_name, self.dbase.entity_type_manga, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
							self.dbase.add_spider_item('entity', series_id, series_url[index])
							
						self.dbase.add_multi_relation(series_id, category_id, 'entity', 'tag')
					
						#Change type to Webtoons if there category is Webtoons
						#if 'Web Novel' in category:
				
				self.dbase.commit()
				print "Success"
				
			except ValueError as e:
				self.dbase.rollback()
				print e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Unknown exception"
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
			
			
			if(next_url):
				#print "Next: ", next_url
				util.Log(response.url, "Has next url {}".format(next_url[0]), False)
				return Request(url=next_url[0],callback=self.parse_categories_series)
			