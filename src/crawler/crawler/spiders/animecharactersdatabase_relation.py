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

"""
	TODO: Fix relation type, e.g. transform Step sister in Step-sister.
"""
class AnimeCharactersSpider(CrawlSpider):
		name = "animecharacter_relation"
		allowed_domains = ["www.animecharactersdatabase.com"]
		start_urls = ["http://www.animecharactersdatabase.com/relations.php?x=0&ex="]
		
		dbase = None
		login_page = 'http://www.animecharactersdatabase.com/newforum.php'
		
		rules = (
		#Follow
		Rule(LinkExtractor(
		allow=('relations\.php\?x=[0-9]{1,}&ex='),
		deny=('kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/'))),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(
		allow=('relations\.php\?(x=[0-9]{1,}&)?relation=[a-zA-Z0-9%_ +-]{1,}'
		),
		deny=('char_desc', 'mobile', 'char_asc', 'members', 'orderby', 'kr\/','cn\/','af\/','sp\/','qe\/','fr\/','jp\/','ge\/')), callback='parse_items', follow=False)
		)
		
		pattern_relation = re.compile(ur'relations\.php\?(x=[0-9]{1,}&)?relation=[a-zA-Z0-9%_ +-]{1,}')
		pattern_replace_name = re.compile(ur'(\(.*\)|\[.*\]|- .*)')
		pattern_remove_relation = re.compile(ur'(^\b[Aa]n?\b|\b([Ii][sS]|[Oo][Ff]|[Tt][Oo])\b|^ ?\b[Tt]he\b|[Ww]ith$|[Ww]hit$)')
		
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
				self.log("Bad times :(")
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
	
			#print "Initialized database and parse"
			if(re.search(self.pattern_relation, response.url) != None):
				return self.parse_relation(response)
				

		def parse_relation(self, response):
			print "Persona relationship"
			self.instancialize_database()
			
			#There isn't any update_id on persona_related_persona.
			
			#Get relation table
			relation_table = response.css('div.middleframe:nth-child(2) > div:nth-child(2) > div:nth-child(1) > table tr')
			
			#Get next url
			next_url = response.css('#newpager table tr td:nth-child(3) a::attr(href)').extract()

			try:
				self.dbase.set_auto_transaction(False)
				
				#Format relation table and already save information.
				
				
				for index,item in enumerate(relation_table):
					success = False
					
					new_item = util.sanitize_title(item.css('th::text').extract())
					if not new_item:
						new_item = util.sanitize_title(item.css('th a::text').extract())
						
					first_persona = item.css('td:nth-child(1) a::attr(href)').extract()
					second_persona =  item.css('td:nth-child(3) a::attr(href)').extract()
					relation_type = item.css('td:nth-child(2) a::text').extract()
					relation_between = item.css('td:nth-child(2)::text').extract()
					
					#Get first persona id from spider_item
					first_persona_id = self.dbase.get_spider_item_id(self.get_formatted_link(first_persona[0]), 'persona')
					first_persona_name = None
					if not first_persona_id:
						#Create dummy persona.
						if relation_between:
							first_persona_name = util.sanitize_title(relation_between[0])
							if first_persona_name:
								first_persona_name = re.sub(self.pattern_remove_relation, '', first_persona_name)
								first_persona_name = util.get_formatted_name(first_persona_name, True)
								
						if not first_persona_name:
							first_persona_name = {}
							first_persona_name['name'] = 'Unknown Cralwer'
							first_persona_name['lastname'] = 'Unknown Cralwer'
							
						#Create dummy.
						first_persona_id = self.dbase.create_persona(first_persona_name['name'], first_persona_name['lastname'], 'Undefined')
					
					#Get second persona
					second_persona_id = self.dbase.get_spider_item_id(self.get_formatted_link(second_persona[0]), 'persona')
					second_persona_name = None
					if not second_persona_id:
						#Create dummy persona.
						if relation_between:
							second_persona_name = util.sanitize_title(relation_between[0])
							if second_persona_name:
								second_persona_name = re.sub(self.pattern_remove_relation, '', second_persona_name)
								second_persona_name = util.get_formatted_name(second_persona_name, True)
								
						if not second_persona_name:
							second_persona_name = {}
							second_persona_name['name'] = 'Unknown Cralwer'
							second_persona_name['lastname'] = 'Unknown Cralwer'
							
						#Create dummy.
						second_persona_id = self.dbase.create_persona(second_persona_name['name'], second_persona_name['lastname'], 'Undefined')
					
					#Get type
					if relation_type:
						relation_type = util.sanitize_title(relation_type)
						if relation_type:
							relation_type = re.sub(self.pattern_remove_relation, '', relation_type)

							for multi_type in relation_type.split('/'):
								relation_type = util.sanitize_title(multi_type)
								#Get relation type id
								relation_type_id = self.dbase.add_type(relation_type.title(), 'related')		
							
								#Save relation between first persona e second persona.
								self.dbase.add_relation_with_type('persona', 'persona', first_persona_id, second_persona_id, 'related', relation_type_id)				
								success = True
							
					if not success:
						#Log
						util.Log(response.url, "Error on trying to insert relation between two person on row {row}".format(row=index+1), False)
						
				self.dbase.commit()
				print "Success page"
				
			except ValueError as e:
				self.dbase.rollback()
				print "Error on formatting, getting IDs and save Persona Relationship", e.message
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				print "Error on formatting and save Persona Relationship", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)
			
			if(next_url):
				next_url = self.get_formatted_link(next_url[0])
				util.Log(response.url, "Has next url {}".format(next_url), False)
				return Request(url=next_url,callback=self.parse_relation)			
				
		"""
			Method used to add the url on animecharacter if the given url is a relative path.
		"""
		def get_formatted_link(self, url):
			if "http://" in url or "https://" in url:
				return url
			else:
				return "http://www.animecharactersdatabase.com/" + url
				