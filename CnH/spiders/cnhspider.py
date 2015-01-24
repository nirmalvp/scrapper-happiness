from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from CnH.items import CnHItem
from scrapy.http import Request
import urlparse

class CnHSpider(CrawlSpider):

    name = 'cyanide'
    allowed_domains = ['explosm.net']
    filename=""
    start_urls = ['http://explosm.net/comics/3811/']
    rules = [Rule(LinkExtractor(allow=['/comics/\d+/'],restrict_xpaths = ("//a[@class='previous-comic']") ), 'parse_torrent',follow=True)]

    def parse_torrent(self, response):
        self.filename=response.url.split('/')[-2]+'.'
        for url in response.xpath("//img[@id='main-comic']/@src").extract() : 
            self.filename+= url.split('.')[-1] 
            if('http' not in url):
                yield Request(urlparse.urljoin('http:',url), callback=self.save_pdf)
            else:
                yield Request(url, callback=self.save_pdf)

    def save_pdf(self, response):
        path = '/home/nirmal/Pictures/Cyanide/' + self.filename
        with open(path, "wb") as f:
            f.write(response.body)

    
            