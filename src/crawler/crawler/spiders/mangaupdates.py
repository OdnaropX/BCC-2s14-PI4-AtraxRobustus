# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
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
		
		rules = (
		Rule(LinkExtractor(allow=('series\.html\?page=[0-9]{1,}'), deny=('letter', 'orderby', 'filter', 'categories', 'act'))),
		Rule(LinkExtractor(allow=('publishers\.html\?page=[0-9]{1,}'))),
		Rule(LinkExtractor(allow=['categories\.html?page=[0-9]{1,}'])),
		Rule(LinkExtractor(allow=['groups\.html\?page=[0-9]{1,}'])),
		Rule(LinkExtractor(allow=['authors\.html\?page=[0-9]{1,}'])),
		Rule(LinkExtractor(allow=('id=', 'genres\.html')), callback='parse', follow=False)
		)
		
		pattern_series = re.compile(ur'series\.html\?id=[0-9]{1,}')
		pattern_publishers = re.compile(ur'publishers\.html\?id=[0-9]{1,}')
		pattern_groups = re.compile(ur'groups\.html\?id=[0-9]{1,}')
		pattern_categories = re.compile(ur'categories\.html\?id=[0-9]{1,}')
		pattern_authors = re.compile(ur'authors\.html\?id=[0-9]{1,}')
		pattern_genres = re.compile(ur'genres\.html')
	
		def parse(self, response):
			if(re.search(self.pattern_series, response.url) != None):
				#Parse Series.
				self.parse_series(self, response)
				
			elif(re.search(self.pattern_groups, response.url) != None):
				#Parse Groups.
				self.parse_groups(self, response)
				
			elif(re.search(self.pattern_genres, response.url) != None):
				#Parse Genres.
				self.parse_genres(self, response)
				
			elif(re.search(self.pattern_categories, response.url) != None):
				#Parse Categories.
				self.parse_categories(self, response)
				
			elif(re.search(self.pattern_authors, response.url) != None):
				#Parse Authors.
				self.parse_authors(self, response)
				
			elif(re.search(self.pattern_publishers, response.url) != None):
				#Parse Publisher.
				self.parse_publishers(self, response)
			
			#filename = response.url.replace("?", "-");
			#filename = filename.replace("http://", "");
			#filename = filename.replace("/", "-");
			#with open("urls.txt", 'a') as f:
			#	f.write(response.url + "\n")
			
		
		#def parse_start_url(self, response):
		#	list(self.parse_links(response))
		
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

		def parse_groups(self, response):
			

		def parse_authors(self, response):
			
		
		def parse_publishers(self, response):
			
		
		def parse_categories(self, response):
		
		def parse_genres(self, response):
			with open("teste.txt", 'a') as f:
				f.write("2")
				