# -*- coding: utf-8 -*-
from __future__ import division
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
import math

# ####################################################################################
# #################################### HOW TO RUN ####################################
# #     myfigure_items -s JOBDIR=cache/myfigure_collection --logfile=debugg18.log    #
# ####################################################################################

class MyFigureCollectionSpider(CrawlSpider):
		name = "myfigure_items"
		allowed_domains = ["myfigurecollection.net"]
		'''
		start_urls = ["http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=0&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=newest&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=500",
		"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=0&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=newest&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=500"
		]
		'''
		
		start_urls = [
		#"http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=1&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=2&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1"
		#"http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=3&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=4&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=10&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=0&goto=0&categoryid=6&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=5&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=13&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=14&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=15&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=17&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		#"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=18&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=20&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		"http://myfigurecollection.net/search.php?mode=search&root=1&goto=0&categoryid=16&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=date&order=desc&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=1",
		]
		
		dbase = None
		login_page = 'https://secure.myfigurecollection.net/signs.php?mode=in&ln=en'
		
		rules = (
		#Follow
		Rule(LinkExtractor(allow=(
		'search\.php\?mode=search&root=[01](.*)?&p=[0-9]{1,}'),
		#'search\.php\?mode=search&root=[01]&goto=0&categoryid=[0-9]{1,}&runid=-1&rating=0&scale=0&year=0&month=0&day=0&nodate=0&date_strict=0&tagid=0&nocode=0&display=grid&sort=newest&order=desc(&acc=[0-9]{1,})?&separator=0&castoff=0&bootleg=0&draft=0&region_free=0&origin_id=0&origin_p=-1&origin_strict=0&character_id=0&character_p=-1&character_strict=0&manufacturer_id=0&manufacturer_p=-1&manufacturer_strict=0&artist_id=0&artist_p=-1&artist_strict=0&type_id=0&type_p=-1&type_strict=0&material_id=0&material_p=-1&material_strict=0&pp=1&p=[0-9]{1,}'),
		deny=('kr\.myfigure','it\.myfigure','fi\.myfigure','nl\.myfigure','cn\.myfigure','af\.myfigure','sp\.myfigure','qe\.myfigure','fr\.myfigure','jp\.myfigure','ge\.myfigure', 'de\.myfigure', 'no\.myfigure','sv\.myfigure',
		'pt\.myfigure','pl\.myfigure','es\.myfigure','ja\.myfigure','zh\.myfigure','ru\.myfigure', 'database\.php\?','\.cgi')
		)
		),
		#Parse id and series release. Series release page will be add from request on series parse. 
		Rule(LinkExtractor(allow=('item/[0-9]{1,}'),
		deny=('edit','link','history','kr\.myfigure','it\.myfigure','fi\.myfigure','nl\.myfigure','cn\.myfigure','af\.myfigure','sp\.myfigure','qe\.myfigure','fr\.myfigure','jp\.myfigure','ge\.myfigure', 'de\.myfigure', 'no\.myfigure','sv\.myfigure',
		'pt\.myfigure','pl\.myfigure','es\.myfigure','ja\.myfigure','zh\.myfigure','ru\.myfigure', 'database\.php\?', '\.cgi')), callback='parse_items', follow=False)
		)
		
		pattern_items = re.compile(ur'item/[0-9]{1,}')
		pattern_images = re.compile(ur'pictures\.php')
		
		pattern_replace_name = re.compile(ur'(\(.*\)|- .*)')
		pattern_color_banners = re.compile(ur'#8[0]{5}')
		pattern_color_chan = re.compile(ur'#[Ff]{2}[0]{2}[Ff]{2}')
		pattern_color_exposition = re.compile(ur'#[0]{6}')
		pattern_color_kit = re.compile(ur'[Cc]{2}80[Cc]{2}')
		pattern_color_box = re.compile(ur'#4040[fF]{2}')
		pattern_color_collection = re.compile(ur'#[Ff]{2}8[0]{3}')
		pattern_color_bootleg = re.compile(ur'#[fF]{2}[0]{4}')
		
		pattern_free_region = re.compile(ur'\b[Rr]egion[ _-][Ff]rees?\b')
		pattern_r18 = re.compile(ur'\b[Rr]?18+?\b')
		pattern_cast_off = re.compile(ur'\b[Cc]ast[_ -][Oo][f]{1,}?\b')
		pattern_counterfeit = re.compile(ur'\b[Cc]ounterfeits?\b')
		pattern_asps = re.compile(ur'[\(\)]')
		pattern_artist = re.compile(ur'[Aa]rtists?')
		pattern_release = re.compile(ur'[Rr]elease[ _-]date')
		pattern_version = re.compile(ur'[Vv]ersions?')
		pattern_l = re.compile(ur'[Ll]')
		pattern_w = re.compile(ur'[Ww]')
		pattern_h = re.compile(ur'[Hh]')
		pattern_alpha = re.compile('[a-zA-Z]{1,}')
		pattern_dimension = re.compile(ur'(\b[cC]?[Mm]{1,}\b|[ =])')
		pattern_cm = re.compile(ur'\b[Cc][mM]\b')
		pattern_m = re.compile(ur'\b[Mm]\b')
		pattern_inside_paren = re.compile(ur'\(.*\)')
		pattern_dimensions = re.compile(ur'[Dd]imensions?')
		pattern_origin = re.compile(ur'[Oo]rigins?')
		pattern_character = re.compile(ur'[Cc]haracters?')
		pattern_companies = re.compile(ur'[Cc]ompan(y|ies)')
		pattern_classification = re.compile(ur'[Cc]lassifications?')
		pattern_categories = re.compile(ur'[Cc]ategor(y|ies)')
		pattern_price = re.compile(ur'[Pp]rices?')
		
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
			print "Login"
			return FormRequest.from_response(response,
					formname= 'tbf_signin',
                    formdata={'username': Settings().get('MUUSERNAME'), 'password': Settings().get('MUPASSWORD')},
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
					return super(MyFigureCollectionSpider, self).start_requests()
				else:
					return Request(url=response.meta['current_url'],callback=self.parse_items,dont_filter=True)
			else:
				self.log("Bad times :(")
				print "Error login."
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
				else:
					print "Initialized database and parse"
		
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
			if 'myfigurecollection.net/profile/Teste2352' in response.body:
				return True
			return False
			
		"""
			Method called to parse link from extractor.
		"""
		def parse_items(self, response):
			self.instancialize_database()
			if not self.check_logged(response):
				return self.log_in(response)
			
			#Added method to check if item was already crawled. 
			#Need to change this to check before be create a response.
			if not self.dbase.check_spider_item_crawled(response.url):
				if(re.search(self.pattern_items, response.url) != None):
					print "response url: ", response.url
					item = response.css('#more .selected::text').extract()
					item = util.sanitize_title(item)
					if item == "Figures":
						return self.parse_goods(response, False, True)
					elif item == "Goods":
						return self.parse_goods(response)
					#elif item == "Media":
					#	self.parse_goods(response, True)
				elif(re.search(self.pattern_images, response.url) != None):
					return self.parse_goods_image(response)
			else:
				print "Ignored"
					
		def parse_enciclopedia(self, response):
			pass
			
		def parse_shop(self, response):
			pass
			
		"""
			TODO: Relate entity with persona to know in what entity the persona is from in the goods.
		
		"""
		def parse_goods(self, response, media = False, figure = False):
			self.instancialize_database()
			if not self.check_logged(response):
				return self.log_in(response.url)
				
			if media:
				print "Media"
			elif figure:
				print "Figure"
			else:
				print "Goods"
			
			update_id = None
			try:
				#Check if there is a dummy, if there is update only. If there inst the id will be none
				if media:
					#Get update id from entity or from soundtrack or album
					update_id = self.dbase.get_spider_item_id_from_url(response.url)
				else:
					update_id = self.dbase.get_spider_item_id(response.url, 'goods')
			except ValueError as e:
				if media:
					print "Error on getting dummy id on Media", e.message
				else:
					print "Error on getting dummy id on Goods", e.message
			except:
				if media:
					print "Error on getting dummy on Media", sys.exc_info()[0]
				else:
					print "Error on getting dummy on Goods", sys.exc_info()[0]
				util.PrintException()
			
			#Get title
			title = response.css('#wide > h1 span[itemprop="name"]::attr(title)').extract()
			
			#Get details list
			details_list = response.css('ul.sd:nth-child(1) li')
			
			#Get release list
			release_list = response.css('#ref-releases + ul li')
			
			#Get pictures page. Get url from ID. 
			#image_link = response.css('.tab > li:nth-child(6) a::attr(href)').extract()
			main_picture = response.css('.db-picture img::attr(src)').extract()

			#Get tags
			tags = response.css('.tags a:not([title=Information]):not([title=Yes]):not([title=No])::attr(title)').extract()#Exclude No, yes, information
			
			#Get related items
			related_url = response.css('ul.item:nth-child(14) li a::attr(href)').extract()
			related_text = response.css('ul.item:nth-child(14) li a::text').extract()
			related_type = response.css('ul.item:nth-child(14) li em::text').extract()#Only use if related_type and url have the same amount.
			
			#Get observation
			observations = response.css('div.msg::text').extract()
			if not observations:
				observations = response.css('div.msg div::text').extract()
			
			try:
				#Format title
				title = util.sanitize_title(title)
				
				#Format details list
				
				price, id, scale_id, release_date, scale = None, None, None, None, None
				versions_id, categories_id, comments, companies, materials, artists, personas, entities = [], [], [], [], [], [], [], []
				counterfeit, cast_off, r18, region_free = False, False, False, False
				weight, width, length, height = None, None, None, None
				
				
				for item in details_list:
					new_item = item.css('label::text').extract()
					new_item = util.sanitize_title(new_item)
				
					new_content = item.css('div')

					if new_item and new_content:
						#print new_item
						#Check ID
						if new_item == "ID":
							id = new_content.css('::text').extract()
							id = util.sanitize_title(id)
							if id:
								id = id.replace('#','')
							
						#Check price
						elif re.search(self.pattern_price, new_item) != None:
							price = new_content.css('::text').extract()
							price = util.sanitize_title(price)
							if price:
								price = price.replace(ur'¥','')
							#print price
							
						#Check category
						elif re.search(self.pattern_categories, new_item) != None:
							#Figure category: Prepained, Action/Dolls, Trading, Garage Kits, Model Kits, Acessories
							categories = new_content.css('a::text').extract()
							
							for category in categories:
								category_name = util.sanitize_title(category)
								if category_name:
									if media:
										#Save category, return category id.
										category_id = self.dbase.add_name_to_table(category_name.title(), 'category')
										categories_id.append(category_id)
								else:
									categories_id.append(category_name.title())
									
						#Check classification
						elif re.search(self.pattern_classification, new_item) != None:
							classifications = new_content.css('span.trigger > a::text').extract()
							for classification in classifications:
								#save comment on database.
								new_comment = {}
								new_comment['title'] = 'Crawler classification'
								new_comment['content'] = util.sanitize_content(classification)
								comments.append(new_comment)
								
						#Company
						elif re.search(self.pattern_companies, new_item) != None:
							new_companies = new_content.css('span.trigger')
							for company in new_companies:
								new_aliases = []
								company_name = company.css('a:nth-child(1)::text').extract()
								company_name = util.sanitize_title(company_name)
								
								if company_name:
									language_code = langid.classify(company_name)
									language_id = self.dbase.get_language_id_from_code(language_code[0])
									if not language_id:
										language_id = self.dbase.language_ja
									new_name = {}
									new_name['name'] = company_name
									new_name['language_id'] = language_id
									new_aliases.append(new_name)
									
								company_original_name = company.css('a:nth-child(1)::attr(switch)').extract()
								company_original_name = util.sanitize_title(company_original_name)
								
								if company_original_name:
									language_code = langid.classify(company_original_name)
									language_id = self.dbase.get_language_id_from_code(language_code[0])
									if not language_id:
										language_id = self.dbase.language_ja
									new_name = {}
									new_name['name'] = company_original_name
									new_name['language_id'] = language_id
									new_aliases.append(new_name)
								
								company_url = company.css('a:nth-child(1)::attr(href)').extract()
								company_url = company_url[0]
								company_type = company.css('small::text').extract()
								company_type = util.sanitize_title(company_type)
								
								if company_type:
									company_type = re.sub(self.pattern_asps, '', company_type)
									company_type_id = self.dbase.add_type(company_type, 'company_function')
								else:
									company_type_id = self.dbase.company_function_type_creator
									
								company_id = self.dbase.get_spider_item_id(company_url, 'company')
								
								if not company_id:
									#Get company from alias
									where_values = []
									where = []
									for alias in new_aliases:
										where_values.append(alias['name'])
										where.append("name = %s")
									
									where = " or ".join(where)
									company_id = self.dbase.get_var('company_alias',['company_id'], where, where_values)

								if not company_id:
									#Create dummy
									alternate_names = []
									
									if len(new_aliases) > 1:
										alternate_names = new_aliases[1:]
												
									company_id = self.dbase.create_company(new_aliases[0]['name'], self.dbase.language_ja, self.dbase.country_jp, None, None, None, None, None, [], [], [], [], [], [], [], alternate_names)
									self.dbase.add_spider_item('company', company_id, company_url)
								else:
									#Add alias
									for alias in new_aliases:
										self.dbase.add_alias(alias['name'], company_id, alias['language_id'], 'company', self.dbase.alias_type_alias)
										
								new_company = {}
								new_company['id'] = company_id
								new_company['function_type_id'] = company_type_id
								companies.append(new_company) 

						#Character
						elif re.search(self.pattern_character, new_item):
							anchor_texts = new_content.css('span.trigger > a::text').extract()
							anchor_urls = new_content.css('span.trigger > a::attr(href)').extract()
							anchor_switchs = new_content.css('span.trigger > a::attr(switch)').extract()#original name
						
							for index, anchor_text in enumerate(anchor_texts):
								aliases = []
								anchor_text = util.sanitize_title(anchor_text)
								if anchor_text:
									aliases.append(anchor_text)
								anchor_alias = util.sanitize_title(anchor_switchs[index])
								if anchor_alias:
									aliases.append(anchor_alias)
								#Get id from spider_item
								persona_id = self.dbase.get_spider_item_id(anchor_urls[index], 'persona')
								if aliases:
									persona = {}
									persona['alias'] = aliases
									persona['id'] = persona_id
									personas.append(persona)

						#Origin
						elif re.search(self.pattern_origin, new_item):
							anchor_texts = new_content.css('span.trigger > a::text').extract()
							anchor_urls = new_content.css('span.trigger > a::attr(href)').extract()
							anchor_switchs = new_content.css('span.trigger > a::attr(switch)').extract()#original name
						
							for index, anchor_text in enumerate(anchor_texts):
								aliases = []
								#Get id from spider_item
								entity_id = self.dbase.get_spider_item_id_from_url(anchor_urls[index])
								anchor_text = util.sanitize_title(anchor_text)
								if anchor_text:
									aliases.append(anchor_text)
									
								anchor_alias = util.sanitize_title(anchor_switchs[index])
								if anchor_alias:
									aliases.append(anchor_alias)
								if aliases:
									entity = {}
									entity['alias'] = aliases
									entity['id'] = entity_id
									entities.append(entity)
							
						#Check Dimensions
						elif re.search(self.pattern_dimensions, new_item):
							dimensions = new_content.css('::text').extract()
							dimensions = util.sanitize_title(dimensions)
							if dimensions:
								new_dimensions = re.sub(self.pattern_inside_paren, '--', dimensions)
								dimen = new_dimensions.split('--')
								for d in dimen:
									multi = 1
									if re.search(self.pattern_m, d) != None:
										multi = 1000
									elif re.search(self.pattern_cm, d) != None:
										multi = 10
									
									new_d = re.sub(self.pattern_dimension, '', d)
									if re.search(self.pattern_w, new_d) != None:
										width = re.sub(self.pattern_alpha,'', new_d)
										width = util.convert_to_number(width) * multi
									elif re.search(self.pattern_h, new_d) != None:
										height = re.sub(self.pattern_alpha,'', new_d)
										height = util.convert_to_number(height) * multi
									elif re.search(self.pattern_l, new_d) != None:
										length = re.sub(self.pattern_alpha,'', new_d)
										length = util.convert_to_number(length) * multi
								#Register dimensions as comment.
								new_comment = {}
								new_comment['title'] = 'Crawler item dimensions'
								new_comment['content'] = dimensions
								comments.append(new_comment)
							
						#check version
						elif re.search(self.pattern_version, new_item) != None:
							versions = new_content.css('span.trigger > a::text').extract()
							for version in versions:
								version_id = util.sanitize_title(version)
								if version_id:
									if re.search(ur'[Rr]18', version_id) != None:
										r18 = True
									version_id = re.sub(ur'[Vv]er.?$', '', version_id)
									version_id = self.dbase.add_name_to_table(version_id.title(), 'goods_version')
									versions_id.append(version_id)
									
						#Check release date
						elif re.search(self.pattern_release, new_item) != None:
							release_date = new_content.css('a::text').extract()
							if release_date:
								release_date = release_date[0]
								
						#Scale
						elif new_item == "Scale":
							scale = new_content.css('span.trigger > a::text').extract()
							scale = util.sanitize_title(scale)
							if scale:
								scale_id = self.dbase.add_name_to_table(scale, 'scale')
								
						#Materials
						elif new_item == "Material":
							material = new_content.css('span.trigger > a::text').extract()
							material = util.sanitize_title(material)
							if material:
								material_id = self.dbase.add_name_to_table(material, 'material')
								materials.append(material_id)
								
						#Artist (People)
						elif re.search(self.pattern_artist, new_item):
							new_artists = new_content.css('span.trigger')
							for artist in new_artists:
								new_aliases = []
								artist_name = artist.css('a:nth-child(1)::text').extract()
								artist_name = util.sanitize_title(artist_name)
								
								if artist_name:
									new_name = util.get_formatted_name(artist_name)
									if new_name:
										new_aliases.append(new_name)
									
								artist_original_name = artist.css('a:nth-child(1)::attr(switch)').extract()
								artist_original_name = util.sanitize_title(artist_original_name)
								
								if artist_original_name:
									new_name = util.get_formatted_name(artist_original_name)
									if new_name:
										new_aliases.append(new_name)
								
								artist_url = artist.css('a:nth-child(1)::attr(href)').extract()
								artist_url = artist_url[0]
								artist_type = artist.css('small::text').extract()
								artist_type = util.sanitize_title(artist_type)
								
								if artist_type:
									artist_type = re.sub(self.pattern_asps, '', artist_type)
									artist_type_id = self.dbase.add_type(artist_type, 'create')
								else:
									artist_type_id = self.dbase.people_create_type_sculptor
									
								artist_id = self.dbase.get_spider_item_id(artist_url, 'people')
								
								if not artist_id:
									#Get artist from alias
									where_values = []
									where = []
									for alias in new_aliases:
										where_values.append(alias['name'])
										where_values.append(alias['lastname'])
										where.append("name = %s")
										where.append("lastname = %s")
									
									where = " or ".join(where)
									artist_id = self.dbase.get_var('people_alias',['people_id'], where, where_values)

								if not artist_id:
									#Create dummy
									alternate_names = []
									
									if len(new_aliases) > 1:
										alternate_names = new_aliases[1:]
										
									artist_id = self.dbase.create_people(new_aliases[0]['name'], new_aliases[0]['lastname'], self.dbase.country_jp, None, None, None, None, None, None, None, alternate_names)
									self.dbase.add_spider_item('people', artist_id, artist_url)
								else:
									#Add alias
									for alias in new_aliases:
										self.dbase.add_people_alias(alias['name'], alias['lastname'], artist_id, self.dbase.alias_type_alias)
								
								where_values = []
								where_values.append(artist_id)
								where_values.append(new_aliases[0]['name'])
								where_values.append(new_aliases[0]['lastname'])
								
								artist_alias_used = self.dbase.get_var('people_alias', ['id'], "people_id = %s and name = %s and lastname = %s", where_values)
								
								new_artist = {}
								new_artist['id'] = artist_id
								new_artist['alias_id'] = artist_alias_used
								new_artist['function_type_id'] = artist_type_id
								artists.append(new_artist)
								
						#Various. Types: 2140g, Counterfeit; 14 tracks, 1 disc, 01:17:00; 1 disc; Region-free; Cast off;
						elif new_item == "Various":
							content = ""
							
							text = new_content.css('span.trigger > a span::text').extract()
							text = util.sanitize_content(text)
							if text:
								content = text
								
							text = new_content.css('span::text').extract()
							text = util.sanitize_content(text)
							if text:
								content = content + " " + text
								
							text = new_content.css('a::text').extract()
							text = util.sanitize_content(text)
							if text:
								content = content + " " + text
								
							text = new_content.css('::text').extract()
							text = util.sanitize_content(text)
							if text:
								content = content + " " + text
								
							if content:
								if re.search(self.pattern_counterfeit, content) != None:
									counterfeit = True
									
								if re.search(self.pattern_cast_off, content) != None:
									cast_off = True
									
								if re.search(self.pattern_r18, content) != None:
									r18 = True
									
								#Check if is region free
								if re.search(self.pattern_free_region, content) != None:
									region_free = True
									
								new_comment = {}
								new_comment['title'] = 'Crawler new_item various'
								new_comment['content'] = content
								comments.append(new_comment)

				entities_origin_id = []
				persona_origin_id = []
				
				#Format character and origin
				for entity in entities: #Format first entities
					if entity['id']:
						entities_origin_id.append(entity['id'])
					else:
						#Check if there is a entity origin with the same name, else create dummy.
						where, where_values = [], []
						
						for alias in entity['alias']:
							where.append("name = %s")
							where_values.append(alias)
						where = " or ".join(where)
						return_items = self.dbase.get_col('entity_alias','entity_id', where, where_values)
						if return_items:
							if len(return_items) > 1:
								for return_item in return_items:
									new_comment = {}
									new_comment['title'] = 'Cralwer Not Associated Entity'
									new_comment['content'] = return_item[0]
									comments.append(new_comment)
							else:
								entities_origin_id.append(return_items[0][0])
						else:
							#Create dummy.
							entity_dummy_id = self.dbase.create_entity(entity['alias'][0], self.dbase.entity_type_anime, self.dbase.classification_type_12, self.dbase.language_ja, self.dbase.country_jp)
							entities_origin_id.append(entity_dummy_id)
							
				for persona in personas:
					if persona['id']:
						persona_origin_id.append(persona['id'])
					else:
						#Check if there is a entity origin with the same name, else create dummy.
						persona_name = util.get_formatted_name(persona['alias'])
						if persona_name:
							where_values = []
							where_values.append(persona_name['name'])
							where_values.append(persona_name['lastname'])
							return_items = self.dbase.get_col('persona_alias','persona_id', "name = %s and last_name = %s", where_values)
						if not return_items:
							persona_name = util.get_formatted_name(persona['alias'], True)
							where_values = []
							where_values.append(persona_name['name'])
							where_values.append(persona_name['lastname'])
							return_items = self.dbase.get_col('persona_alias','persona_id', "name = %s and last_name = %s", where_values)
							
						if return_items:
							if len(return_items) > 1:
								for return_item in return_items:
									new_comment = {}
									new_comment['title'] = 'Cralwer Not Associated Persona'
									new_comment['content'] = return_item[0]
									comments.append(new_comment)
							else:
								persona_origin_id.append(return_items[0][0])
						else:
							persona_name = util.get_formatted_name(persona['alias'])
							#Create dummy.
							entity_dummy_id = self.dbase.create_persona(persona_name['name'], persona_name['lastname'], 'Undefined')
							persona_origin_id.append(entity_dummy_id)	
							
				#If there is more than one dont associate.
				'''
				#Format relationship between good and entity.
				if len() == 1 or len() == 1:
					#make a relation between character and entity.
					
				else:
					#Dont make relationship, add comment.
					new_comment = {}
					new_comment['title'] = 'Cralwer Could not associated Persona'
					new_comment['content'] = return_item
					comments.append(new_comment)
				
				#Make relationship between entities
				entity_length = len(entities)
				'''
				
				if entities_origin_id:
					new_comment = {}
					new_comment['title'] = 'Cralwer Could not associated to entities'
					new_comment['content'] = util.sanitize_title(entities_origin_id)
					comments.append(new_comment)
				
				#Format picture link
				new_images = []
				for image in main_picture:
					image = re.sub(ur'\?.*','', image)
					image = re.sub(ur'\bbig\b/','large/', image)
					image_array = image.split('.')
					new_image = {}
					new_image['url'] = image
					new_image['extension'] = image_array.pop()
					new_image_name = image_array.pop()
					new_image_name = new_image_name.split('/')
					new_image['name'] = new_image_name.pop()
					new_image['image_type_id'] = self.dbase.image_good_type_main
					new_images.append(new_image)
				
				#Format tags
				tags_id = []
				for tag in tags:
					tag_id = util.get_formatted_tag(tag)
					if tag_id:
						tag_id = self.dbase.add_name_to_table(tag, 'tag')
						tags_id.append(tag_id)

					
				#Format release list
				#format release country and currency.release_date
				launch_countries = []
				for release in release_list:

					date = release.css('div:nth-child(1) .time::text').extract()
					date = util.sanitize_title(date)
					date = util.get_formatted_date(date)
					
					launch_type = release.css('div:nth-child(2) em::text').extract()
					if launch_type:
						launch_type = util.sanitize_title(launch_type[0])
						launch_type = self.dbase.add_name_to_table(launch_type, 'launch_type')
					if not launch_type:
						launch_type = self.dbase.add_name_to_table('Standard', 'launch_type')
					
					price = release.css('div:nth-child(4)::text').extract()
					price = util.sanitize_title(price)
					if price:
						price = price.replace(ur'¥', '')
					
					if not price:
						price = 0
					
					new_launch = {}
					new_launch['country_id'] = self.dbase.country_jp
					new_launch['date'] = date
					new_launch['price'] = price
					new_launch['currency_id'] = self.dbase.currency_yen
					new_launch['launch_type_id'] = launch_type
			
					#Get event
					location = util.sanitize_title(release.css('div:nth-child(3) span::attr(title)').extract())
					if location:
						new_comment = {}
						new_comment['title'] = 'Crawled location launch'
						new_comment['content'] = location + " type: " + str(launch_type) + ", " + date
						comments.append(new_comment)
					
					launch_countries.append(new_launch)
				
				#Format collection
				collection_id = None
				#Get collection from entities of origin.
				for origin in entities_origin_id:
					where_values = []
					where_values.append(origin)
					collection_id = self.dbase.get_var('entity', ['collection_id'], "id = %s", where_values)
					if collection_id:
						break			
				
				#Get collection same name as origin
				entities_origin_name = []
				if not collection_id:
					for item in entities:
						for alias in item['alias']:
							new_alias = util.normalize_collection_name(alias)
							if new_alias:
								where_values = []
								where_values.append(new_alias)
								collection_id = self.dbase.get_var('collection_alias', ['collection_id'], "name = %s", where_values)
								if not collection_id:
									entities_origin_name.append(new_alias)
								else:
									break
						if collection_id:
							break

				#Get collection name from similar collections, from the title:
				if not collection_id and len(title) > 3:
					#Check if name is similar to another collection already registered. Only check if name is larger then 3 characters.
					#This method can have mismatch collection names and collections will need to be check after all items was crawled using get_related_item.
					series_name = []
					series_name.append(title)
					collection_id = self.dbase.get_col('collection_alias', 'collection_id', "%s LIKE '%%' || name || '%%'", series_name)
					
					if not collection_id:
						collection_id = self.dbase.get_col('collection_alias', 'collection_id', "name LIKE '%%' || %s || '%%'", series_name)
						if not collection_id:
							#create new collection with the first name type, get firstname part using regex.
							original_name = re.sub(self.pattern_replace_name,'',title)
							if original_name:
								collection_id = self.dbase.create_collection(original_name)
					
					if(isinstance(collection_id, collections.Iterable) and not isinstance(collection_id, types.StringTypes)):
						#return the element most appear on list
						collections = []
						for new_id in collection_id:
							collections.append(new_id[0])
							
						collection_id = util.most_common_oneliner(collections)
				
				#Else create collection from origin name. If there is no origin name get collection from classification.
				if not collection_id:
					if entities_origin_name:
						collection_id = self.dbase.create_collection(entities_origin_name[0])
						
				#Format classification
				if cast_off or r18:
					classification_type_id = self.dbase.classification_type_18
				else:
					classification_type_id = self.dbase.classification_type_16
				
				#Format observation
				observation = util.sanitize_content(observations)

				if not media:
					#Format good type
					if categories_id:
						goods_type_id = self.dbase.add_type(categories_id[0], 'goods')
					else:
						goods_type_id = self.dbase.add_type('Unkown', 'goods')
				
				#Format figure itens
				if figure:
					#Format scale
					if not scale:	
						scale_id = self.dbase.scale_non_scale
					else:
						scale_id = self.dbase.add_name_to_table(scale, 'scale')
				

				#Format related items
				relations = []
				for index, type in enumerate(related_type):
					#Get id, else create dummy.
					if media:
						table = 'entity'
					else:
						table = 'goods'
						
					relation_id = self.dbase.get_spider_item_id(related_url[index], table)
					if not relation_id:
						#Create dummy
						if media:
							relation_id = self.dbase.create_entity(None, entity_type_id, classification_type_id, self.dbase.language_ja, self.dbase.country_jp)
						else:
							relation_id = self.dbase.create_goods(None, self.dbase.language_ja, goods_type_id, None, collection_id)
						
						self.dbase.add_spider_item(table, relation_id, related_url[index])
					
					type = util.sanitize_title(type)
					type_id = self.dbase.add_type(type.title(),'associated')
					new_relation = {}
					new_relation['id'] = relation_id
					new_relation['type_id'] = type_id
					relations.append(new_relation)
					
				#Format Draft.
				if "This entry is a draft" in response.body:
					draft = True
				else:
					draft = False
					
			except ValueError as e:
				if media:
					print "Error on formatting and getting IDs to save Media", e.message
				else:
					print "Error on formatting and getting IDs to save Goods", e.message			
				util.PrintException()
				util.Log(response.url, e.message)
				return
			except:
				if media:
					print "Error on formatting Media", sys.exc_info()[0]
				else:	
					print "Error on formatting Goods", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
				return
				
			try:
				self.dbase.set_auto_transaction(False)
				
				if media:
					pass
					#If book, video or game create edition.
					if re.search(ur'([Bb]ook|[Vv]ideo|[Gg]ame)s?', type) != None:
						pass
					
					'''
					Video, Game, Book, Music
					self.dbase.add_spider_item('soundtrack', collection_id, response.url, True)
					self.dbase.add_spider_item('audio', collection_id, response.url, True)
					self.dbase.add_spider_item('entity', collection_id, response.url, True)
					self.dbase.add_spider_item('collection', collection_id, response.url, True)
					'''
				else:
					goods_id = self.dbase.create_goods(title, self.dbase.language_ja, goods_type_id, height, collection_id, width, length, weight, observation, counterfeit, False, [], [], categories_id, tags_id, materials, persona_origin_id, companies, launch_countries, [], artists, new_images, versions_id, relations, draft, update_id)
					
					if figure:
						where_values = []
						where_values.append(goods_id)
						figure_id = self.dbase.get_var('figure', ['goods_id'], "goods_id = %s", where_values)
						#If not have figure create, else update.
						if not figure_id:
							self.dbase.add_figure(goods_id, scale_id, cast_off)
						else:
							self.dbase.update_figure(goods_id, scale_id, cast_off)
						
					for comment in comments:
						self.dbase.add_comment(comment['title'], comment['content'], 1, goods_id, 'goods')
					
					self.dbase.add_spider_item('goods', goods_id, response.url, True)
					
				self.dbase.commit()
				print "Success"

				#Request image page:
				if id:
					request_image_page = "http://myfigurecollection.net/pictures.php?mode=listview=gallery&sort=date&order=desc&poll=0&p=1&search=item:{item}".format(item=id)
					return Request(url=request_image_page, callback=self.parse_goods_image, dont_filter=True)
				
			except ValueError as e:
				self.dbase.rollback()
				if media:
					print "Error on save Media", sys.exc_info()[0]
				else:	
					print "Error on save Goods", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, e.message)
			except:
				self.dbase.rollback()
				if media:
					print "Error on save Media", sys.exc_info()[0]
				else:	
					print "Error on save Goods", sys.exc_info()[0]
				util.PrintException()
				util.Log(response.url, sys.exc_info()[0])
			finally:
				self.dbase.set_auto_transaction(True)

			
		"""
			Method used to parse the images related with a given item ID. 
		"""
		def parse_goods_image(self, response):
			print "Images"
			print response.url
			
			self.instancialize_database()
			if not self.check_logged(response):
				return self.log_in(response)
				
			next_page = None
			
			#Get image number
			number = response.css('.num::text').extract()
			number = re.sub(ur'[Pp]ictures?', '', number[0])
			number = util.convert_to_number(number)
			
			print "Numbers: ", number
			
			url = urlparse.urlparse(response.url)
			qs = urlparse.parse_qs(url[4])
				
			if number > 0:
				#Get item id.
				id = qs['search'][0]
				if id:
					id = id.replace('item:', '')
					id = id.replace('item%3A', '')
					
				#Get current page number
				p = qs['p'][0]
				if p:
					p = util.convert_to_number(p)
					number_pages = number / 60
					
				print "Page numbers: ", number_pages
				print "Current page: ", p 
				
				#Get list images
				images = response.css('a.picture img::attr(src)').extract()
				styles = response.css('a.picture img::attr(style)').extract()
				
				if images and styles:
					try:
						#Format goods or media entity_id from url id.
						where_values = []
						where_values.append(id)
						table_type = self.dbase.get_var('spider_item', ['table_name'], "url like '%%item/' || %s", where_values)
						item_id = self.dbase.get_var('spider_item', ['id'], "url like '%%item/' || %s", where_values)
						
						if table_type == 'goods':
							
							new_images = []
							#Format list images
							for index, image in enumerate(images):
								#Format type
								type = self.get_type_id_from_color(styles[index])
								
								url = image.replace('thumbnails/', '')
								image_array = url.split('.')
								extension = image_array.pop()
								new_image_name = image_array.pop()
								new_image_name = new_image_name.split('/')
								name = new_image_name.pop()
								#Add image to database 
								self.dbase.add_image_to_goods(url, extension, name, item_id, type)
									
							self.dbase.add_spider_item('goods_has_image', item_id, response.url, True)
							
							#Format next page link
							if number_pages > p:
								next_page = re.sub(ur'\bp=[0-9]{1,}\b', "p={0}".format(p + 1), response.url)
								#if self.dbase.check_spider_item_crawled(next_page):
								#	next_page = None
								
						print "Success"
					except:
						print "Error on formatting and save Images of Goods", sys.exc_info()[0]
						util.PrintException()
						util.Log(response.url, sys.exc_info()[0])

			#Request next page. If there inst one pass to next image type (if official next is bootleg page).	
			if next_page:
				return Request(url=next_page, callback=self.parse_goods_image)
		
		def next_url_type(self, type):
			if not type:
				return 5
				
			next_type = None
			
			if type == '5':#Official
				next_type = 3
			elif type == '3':#Bootleg
				next_type = 1
			elif type == '1':#Figures
				next_type = 12 
			elif type == '12':#Items
				next_type = 4
			elif type == '4':#Collections
				next_type = 6
			elif type == '6':#Space
				next_type = 8
			elif type == '8': #Loots&Boxes
				next_type = 11
			elif type == '11':#Kit&Customs 
				next_type = 14
			elif type == '14':#Expositions 
				next_type = 2
			elif type == '2':#Various 
				next_type = 7
			elif type == '7':#Chan 
				next_type = 10
				
			return next_type
			
		def get_type_id(self, type):
			if not type:
				return 11#Official
				
			type_id = None
			if type == '5':#Official
				type_id = 11
			elif type == '3':#Bootleg 
				type_id = 2
			elif type == '1':#Figures
				type_id = 10 
			elif type == '12':#Items
				type_id = 12
			elif type == '4':#Collections
				type_id = 13
			elif type == '6':#Space
				type_id = 14
			elif type == '8': #Loots&Boxes
				type_id = 15
			elif type == '11':#Kit&Customs 
				type_id = 16
			elif type == '14':#Expositions 
				type_id = 17
			elif type == '2':#Various 
				type_id = 18
			elif type == '7':#Chan 
				type_id = 19
			
			if not type_id:
				return 18
				
			return next_type
		
		def get_type_id_from_color(self, style):
			color = util.sanitize_title(style)
			
			type_id = None
			
			if "#808080" in color:#Official
				type_id = 11
			elif re.search(self.pattern_color_bootleg, color) != None:#Bootleg 
				type_id = 2
			elif "#008000" in color:#Figures
				type_id = 10 
			elif "#004000" in color:#Items
				type_id = 12
			elif re.search(self.pattern_color_collection, color) != None:#Collections
				type_id = 13
			elif "#000080" in color:#Space
				type_id = 14
			elif  re.search(self.pattern_color_box, color) != None: #Loots&Boxes
				type_id = 15
			elif  re.search(self.pattern_color_kit, color) != None:#Kit&Customs 
				type_id = 16
			elif  re.search(self.pattern_color_exposition, color) != None:#Expositions 
				type_id = 17
			elif "#800080" in color:#Various 
				type_id = 18
			elif  re.search(self.pattern_color_chan,color) != None:#Chan 
				type_id = 19
			elif  re.search(self.pattern_color_banners, color) != None:#Banners
				type_id = 21
			
			if not type_id:
				type_id = 18

			return type_id
			