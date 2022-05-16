
import scrapy
from scrapy.utils.project import get_project_settings
from crawler.items import FilmowItem



class Filmemow(scrapy.Spider):
    settings = get_project_settings()
    name = "filmemow"
    file_path = settings.get('FILE_PATH')

    custom_settings = {
        'FEED_URI': f'downloads/{name}.csv',
        'FEED_FORMAT': 'csv',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 4,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 200,
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'random_useragent.RandomUserAgentMiddleware': 403,
        }
    }
    

    def build_catalog_url(self,page_number):
        return f"https://filmow.com/filmes-todos/?pagina={page_number}"
        
    def build_movie_url(self,url):
        return f"https://filmow.com{url}"
    
    
    def start_requests(self):
        yield scrapy.Request(method='GET',url=self.build_catalog_url(1),callback=self.get_number_pages)
        
        
    def get_number_pages(self,response):
        last_page_link = response.xpath('//*[@id="body_wrapper"]/div[2]/div/div/div[1]/div[2]/div/ul/li[8]/a/@href').get()
        last_page_number = int(last_page_link.replace("/filmes-todos/?pagina=","").replace("\"",""))
         
        movies_links = response.xpath('//*[@id="movies-list"]/li/span/a[1]/@href').extract()
        if movies_links is not None or movies_links != []:
            for link in movies_links:
                yield scrapy.Request(method='GET',url=self.build_movie_url(link),callback=self.parse)
         
        for index in range(2,last_page_number+1):
            yield scrapy.Request(method='GET',url=self.build_catalog_url(index),callback=self.navigate)
    
    
    def navigate(self,response):
        movies_links = response.xpath('//*[@id="movies-list"]/li/span/a[1]/@href').extract()
        if movies_links is not None or movies_links != []:
            for link in movies_links:
                yield scrapy.Request(method='GET',url=self.build_movie_url(link),callback=self.parse)
    
    def parse(self,response):
        item = FilmowItem()
        item['title'] =  response.css('h1[itemprop]::text').get()
        if item['title'] is not None:
            item['lower_title'] = item['title'].lower().replace(" ","")
        item['year'] = response.xpath('//*[@id="body_wrapper"]/div[4]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[1]/small/text()').get()
        
        item['original_title'] = response.css('h2[class=movie-original-title]::text').get()
        if item['original_title'] is not None:
            item['original_lower_title'] = item['original_title'].lower().replace(" ","")
        item['score'] = response.xpath('//*[@id="body_wrapper"]/div[4]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/span[2]/text()').get()
        item['number_votes'] = response.xpath('//*[@id="body_wrapper"]/div[4]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/span/text()').get()
        item['url'] = response.url
        return item