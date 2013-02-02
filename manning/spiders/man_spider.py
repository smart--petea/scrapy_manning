#*- coding: utf8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import Request

from scrapy.selector import HtmlXPathSelector
from scrapy import log
import re
import sys, os
from manning.items import ManningItem

reload(sys)
sys.setdefaultencoding('utf-8')

class man_spider(BaseSpider):
	name = 'manningSpider'
	#allowed_domains = ["www.manning.com"]

	def __init__(self, *arg1, **arg2):
		log.msg(message="man_spider, __init__", _level = log.INFO)
		BaseSpider.__init__(self, *arg1, **arg2)
		self.man_spider_callback = {}
		self.man_spider_callback['list'] = self.callback_list
		self.man_spider_callback['parse'] = self.callback_parse
		self.man_spider_callback['all'] = self.callback_all

	def callback_parse(self, response):
		if response.status // 100 != 2:
			log.msg(message="man_spider, callback_parse response.status = %d" % response.status, _level = log.INFO)
			return

		RItem = ManningItem()
		RItem['image_url'] = response.url + re.search("\w+_cover\w+.jpg", response.body).group()
		RItem['title'] = re.search(r'<title>(.*)</title>', response.body).group(1).split(' ', 1)[1] 
		try:
				RItem['ebook_price'] = re.search(r'\$\d+(?:\.\d+)?', response.body).group()
		except AttributeError:
				RItem['ebook_price'] = '0'
		RItem['url'] = response.url
		
		try:

			RItem['isbn'] = re.search(r'<!-- InstanceBeginEditable name="isbn" -->(.*?)<!', response.body).group(1)
		except AttributeError:

			RItem['isbn'] = re.search(r'ISBN:? (.*?)<', response.body).group(1) 

		try:
			RItem['year'] = re.search(r'<!-- InstanceBeginEditable name="date" -->.*(\d+)<!', response.body).group(1)
		except AttributeError:
			try:
				RItem['year'] = re.search(r' (\d{4}).*?\|.*?pages', response.body).group(1) 
			except AttributeError:
				RItem['year'] = '2013'


		try:
			
			RItem['authors'] = re.search(r'<!-- InstanceBeginEditable name="author" -->(.*)<!', response.body).group(1)
		except AttributeError:
			try:
				RItem['authors'] = re.search(r'<font size="\+1">.*?<b>.*?<b>(.*?)<br />', response.body, re.DOTALL).group(1)
			except AttributeError:
				RItem['authors'] = re.search(r'<font size="\+1">.*?<b>(.*?)</b', response.body, re.DOTALL).group(1)

		yield RItem
		print("Processing: ", RItem['title'])



	def callback_list(self, response):
		if response.status // 100 != 2:
			log.msg(message="man_spider, callback_list response.status = %d" % response.status, _level = log.INFO)
			return
		MyUrlTitle = re.findall(r'<li><a href="(.*)">(.*)</a></li>', response.body)
		for MyUrlItem in MyUrlTitle:
			item = ManningItem()
			item['url'] = 'http://www.manning.com'+ MyUrlItem[0]
			item['title'] = MyUrlItem[1]
			yield item
		

	def callback_all(self, response):
		
		if response.status // 100 != 2:
			log.msg(message="man_spider, callback_all response.status = %d" % response.status, _level = log.INFO)
			return
		
		MyUrlTitle = re.findall(r'<dd>.*?<a href="(.*)">', response.body)
		for MyUrlItem in MyUrlTitle:
			yield Request('http://www.manning.com' + MyUrlItem, callback=self.callback_parse)


	def start_requests(self):
		self.mode, url = self._crawler.settings['CommandLineParameter']
		yield Request(url, callback=self.man_spider_callback[self.mode])
		log.msg(message="man_spider, start_requests It's ok mode={0}, url={1}".format(self.mode, url))


