#!/usr/bin/python2
#-*- coding: utf-8 -*-
from scrapy.settings import CrawlerSettings
import argparse
from manning import settings
from scrapy import log
import sys
from scrapy.crawler import CrawlerProcess
import re

class MyCrawlerSettings(CrawlerSettings):
	def __setitem__(self, opt_name, val_name):
		self.values[opt_name] = val_name

	def __contains__(self, item):
		return bool(CrawlerSettings.__getitem__(self, item))

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=['list', 'parse', 'all'])
parser.add_argument('-url', help='url argument is used only and in necessary mode with mode value equal with parse')

args = parser.parse_args()
#I'm verifying if all arguments have a good state and introduce them in MySettings
if args.mode == 'parse':
		
	try:
		re.match(r'http://www.manning.com/[a-zA-Z0-9_]+$', args.url or '').group()
	except AttributeError:
		parser.print_help()
		print("The value 'parse' of positional parameters is used only in combination with optional parameter -url")
		print("The parameter -url must be of the form: http://www.manning.com/[a-zA-z0-9_]+$")
		sys.exit(1)
elif args.mode == 'list': 
	args.url = "http://www.manning.com/catalog/mobile"
else:
	args.url = "http://www.manning.com/catalog"

MySettings = MyCrawlerSettings(settings_module=settings)
MySettings['CommandLineParameter'] = [args.mode, args.url]

print(MySettings['CommandLineParameter'])

MyCrawler = CrawlerProcess(MySettings)

MyCrawler.configure()
log.start_from_crawler(MyCrawler)
log.msg(message="manning_scrape.py started with the parameters mode: {0[0]}, url: {0[1]}".format(MySettings['CommandLineParameter']), _level=log.INFO)


for spider_object in MyCrawler.spiders._spiders.itervalues():
	MyCrawler.crawl(spider_object())


MyCrawler.start()
