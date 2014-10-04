# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

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
		Rule(LinkExtractor(allow=['genres\.html?']), callback='parse_genres'),
		Rule(LinkExtractor(allow=('series\.html'), deny=('letter', 'orderby', 'filter', 'category', 'act')), 'parse_series'),
		#Rule(LinkExtractor(allow=['publishers\.html']), 'parse_publishers'),
		#Rule(LinkExtractor(allow=['categories\.html']), 'parse_categories'),
		#Rule(LinkExtractor(allow=['groups\.html']), 'parse_groups'),
		#Rule(LinkExtractor(allow=['authors\.html']), 'parse_authors'),
		)
		
		#rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
		#)
	
		def parse(self, response):
			filename = response.url.replace("?", "-");
			filename = filename.replace("http://", "");
			filename = filename.replace("/", "-");
			#with open(filename, 'wb') as f:
				#f.write(response.body)
		
		
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
				f.write(response.body)
				f.write("2")

		#def parse_groups(self, response):
		

		#def parse_authors(self, response):
		
		
		#def parse_publishers(self, response):
			
			
		#def parse_categories(self, response):
		
		def parse_genres(self, response):
			with open("teste.txt", 'w') as f:
				f.write("2")
				