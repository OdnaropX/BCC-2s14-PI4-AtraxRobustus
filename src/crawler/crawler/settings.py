# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
LOG_FILE = 'logs.txt'

DBNAME = 'te'
DBUSERNAME = 'teste'
DBPASSWORD = '123456'
DBHOST = 'localhost'
DBPORT = '5432'
MUUSERNAME = 'Teste2352'
MUPASSWORD = '=QWZ;=w)WZ;=w)@!)G'

#Delay used on animecharactersdatabase.
#CONCURRENT_REQUESTS_PER_IP = 5
#DOWNLOAD_DELAY = 0.5
#DUPEFILTER_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
