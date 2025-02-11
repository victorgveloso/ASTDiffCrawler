# myproject/__main__.py

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from astcrawler.spiders.astdiff_spider import AstdiffSpider

def main():
    # Load settings from myproject/settings.py (or your project settings)
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(AstdiffSpider)
    process.start()

if __name__ == "__main__":
    main()
