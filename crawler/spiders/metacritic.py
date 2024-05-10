
import scrapy
from scrapy.utils.project import get_project_settings
from crawler.items import MetacriticItem
import re


class Metacritic(scrapy.Spider):
    settings = get_project_settings()
    name = "metacritic"
    file_path = settings.get('FILE_PATH')

    custom_settings = {
        'FEEDS': {f'downloads/{name}.csv': {'format': 'csv', 'overwrite': True}},
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
        return f"https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2023&page={page_number}"
        
    def build_movie_url(self,url):
        return f"https://www.metacritic.com{url}"
    
    
    def start_requests(self):
        yield scrapy.Request(method='GET',url=self.build_catalog_url(1),callback=self.get_number_pages)
        
        
    def get_number_pages(self,response):
        last_page_number = int(response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/main/section/div[4]/span[2]/span[4]/span/span/span/text()').get().replace(" ","").replace("\n", "").replace(",",""))

        movies_links = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/main/section/div[3]/div/div/a/@href').extract()
        

        if movies_links is not None or movies_links != []:
            for link in movies_links:
                yield scrapy.Request(method='GET',url=self.build_movie_url(link),callback=self.parse)        


        # for index in range(2,last_page_number):
        #     yield scrapy.Request(method='GET',url=self.build_catalog_url(index),callback=self.navigate)
    
    
    def navigate(self,response):
        movies_links = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/main/section/div[3]/div/div/a/@href').extract()
        if movies_links is not None or movies_links != []:
            for link in movies_links:
                yield scrapy.Request(method='GET',url=self.build_movie_url(link),callback=self.parse)
    
    def parse(self,response):
        item = MetacriticItem()
        
        
        title_with_year = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]/div/text()').get()

        if title is not None:
            title.replace(" ","").replace("\n", "").replace(",","").strip()
        item['title'] = title

        year = response.xpath('')

        # item['title'] = response.xpath('//*[@id="main_content"]/div[1]/div[1]/div/table/tr/td[2]/div/table/tr/td[1]/div/div/div[1]/div/h1/text()').get()

        # if item['title'] is None:
        #     item['title'] = response.xpath('//*[@id="main_content"]/div[1]/div[1]/div/div/div[1]/div/h1/text()').get()

        # if item['title'] is not None:
        #     item['lower_title'] = item['title'].lower().replace(" ","")
        
        # item['meta_score'] = response.xpath('//*[@id="nav_to_metascore"]/div[1]/div[2]/div[1]/a/div/text()').get()
        # item['meta_score_positive'] = response.xpath('//*[@id="nav_to_metascore"]/div[1]/div[2]/div[2]/a/div[2]/div[2]/div[2]/text()').get()
        # item['meta_score_mixed'] = response.xpath('//*[@id="nav_to_metascore"]/div[1]/div[2]/div[2]/span[1]/div[2]/div[2]/div[2]/text()').get()
        # item['meta_score_negative'] = response.xpath('//*[@id="nav_to_metascore"]/div[1]/div[2]/div[2]/span[2]/div[2]/div[2]/div[2]/text()').get()

        # item['user_score'] = response.xpath('//*[@id="nav_to_metascore"]/div[2]/div[2]/div[1]/a/div/text()').get()
        # item['user_score_positive'] = response.xpath('//*[@id="nav_to_metascore"]/div[2]/div[2]/div[2]/a[1]/div[2]/div[2]/div[2]/text()').get()
        # item['user_score_mixed'] = response.xpath('//*[@id="nav_to_metascore"]/div[2]/div[2]/div[2]/a[2]/div[2]/div[2]/div[2]/text()').get()
        # item['user_score_negative'] = response.xpath('//*[@id="nav_to_metascore"]/div[2]/div[2]/div[2]/a[3]/div[2]/div[2]/div[2]/text()').get()
        

        # runtime = response.xpath('//*[@id="main_content"]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[5]/div[4]/span[2]/text()').get()

        # if runtime is None:
        #     runtime = response.xpath('//*[@id="main_content"]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[5]/div[3]/span[2]/text()').get()
        
        # if runtime is not None:
        #     item['runtime'] = runtime.replace("min","")
        
        # genre = response.xpath('//*[@id="main_content"]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[5]/div[2]/span[2]/span/text()').get()
        
        # if genre is None:
        #     genre = response.xpath('//*[@id="main_content"]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[4]/div[2]/span[2]/span/text()').get()
        
        # item['genre'] = genre

        # item['movie_url'] = response.url
        # return item
    
