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

DBNAME = 'crawler'
DBUSERNAME = 'postgres'
DBPASSWORD = ''
DBHOST = 'localhost'
DBPORT = '5432'
MUUSERNAME = ''
MUPASSWORD = ''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
