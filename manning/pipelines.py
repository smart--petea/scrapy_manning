#Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
from scrapy import log


class ManningPipeline(object):
	def __init__(self):
		self.fields_to_export = {'list':[ 
										'title',
										'url',
										],
								 'all':[
								 		'isbn',
										'title',
										'url',
										'year', 
										'authors',
										'image_url',
										'ebook_price',
								 		],
								'parse':[
										'isbn',
										'title',
										'url',
										'year',
										'authors',
										'image_url',
										'ebook_price',
										],
								}
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		dispatcher.connect(self.engine_started, signals.engine_started)

		log.msg(message="ManningPipeline, __init__", _level=log.INFO)

	def spider_opened(self, spider):
		self.spider = spider
	
	def engine_started(self):
		self.json_file = open("result.json", "w")
		self.json_exporter = JsonItemExporter(self.json_file, fields_to_export=self.fields_to_export[self.spider._crawler.settings['CommandLineParameter'][0]]) 
		self.json_exporter.start_exporting()
		log.msg(message="ManningPipeline, engine_started, mode=%s"%self.spider._crawler.settings['CommandLineParameter'][0])


	def process_item(self, item, spider):
		log.msg(message="ManningPipeline, process_item", _level=log.INFO)
		self.json_exporter.export_item(item)
		return item

	def spider_closed(self, spider):
		self.json_exporter.finish_exporting()
		self.json_file.close()
		log.msg(message="ManningPipeline, spider_closed", _level=log.INFO)
