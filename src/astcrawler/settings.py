BOT_NAME = 'astcrawler'

SPIDER_MODULES = ['astcrawler.spiders']
NEWSPIDER_MODULE = 'astcrawler.spiders'

# Enable the HTTP cache middleware for local caching of responses
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 100,
}
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# (Optional) Other settings such as USER_AGENT, DOWNLOAD_DELAY, etc.
