# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ManningItem(Item):
	# define the fields for your item here like:
	# name = Field()
	isbn = Field()
	title = Field()
	url = Field()
	year = Field()
	ebook_price = Field()
	image_url = Field()
	ebook_formats = Field()
	authors = Field()
