# Scrapy settings for manning project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'manning'

SPIDER_MODULES = ['manning.spiders']
NEWSPIDER_MODULE = 'manning.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'manning (+http://www.yourdomain.com)'
LOG_FILE = "crawl.log"
SPIDER_MODULES = ['manning.spiders.man_spider']
ITEM_PIPELINES = ['manning.pipelines.ManningPipeline']
