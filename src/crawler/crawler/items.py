# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MangaUpdatesItem(scrapy.Item):
	#Todos os campos a serem utilizados ficam aqui.
	#Scrapy crawl ao redor de um único item com várias propriedades, por isso pipeline só usa um tipo de item por crawler.
	author = []
	publisher = []
	


class MangaUpdates_Author(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title = scrapy.Field()
	name = scrapy.Field()

class MangaUpdates_Publisher(scrapy.Item):

class MangaUpdates_Group(scrapy.Item):

class MangaUpdates_Serie(scrapy.Item):

class MangaUpdates_Genre(scrapy.Item):

class MangaUpdates_Categories(scrapy.Item):
	
	
class AnimeBlade_Group(scrapy.Item):

class AnimeBlade_Release(scrapy.Item):



