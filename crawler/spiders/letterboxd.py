from flatten_json import flatten
import scrapy
from scrapy.utils.project import get_project_settings
from crawler.items import LetterboxdItem
import ast



class LetterBoxd(scrapy.Spider):
    settings = get_project_settings()
    name = "letterboxd"
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
    
    def get_number_movies(self,text):
        number = int(text.replace("There are","").replace("films.","").replace(" ","").replace(",","").strip())
        return number

    def build_catalog_url(self,page_number):
        if page_number is not None:
            return f"https://letterboxd.com/films/ajax/popular/size/small/page/{page_number}/"
    
    def build_movie_url(self,movie_url):
        if movie_url is not None:
            return f"https://letterboxd.com{movie_url}"
    
    def start_requests(self):
        yield scrapy.Request(method='GET',url=self.build_catalog_url(1),callback=self.start_navigate)


    def start_navigate(self,response):
        number_movies = self.get_number_movies((response.xpath('/html/body/section/p/text()').get()))
        number_pages = number_movies//72
        movies_links = response.css('li[data-average-rating]').xpath('./div/@data-target-link').extract()
        for link in movies_links:
            yield scrapy.Request(method="GET",url=self.build_movie_url(link),callback=self.crawl_website_data,meta={"page_number":1})
        
        for num in range(2,number_pages+2):
            yield scrapy.Request(method="GET",url=self.build_catalog_url(num),callback=self.pre_crawl_website_data,meta={"page_number":num})
    
    def pre_crawl_website_data(self,response):
        movies_links = response.css('li[data-average-rating]').xpath('./div/@data-target-link').extract()

        for link in movies_links:
            yield scrapy.Request(method="GET",url=self.build_movie_url(link),callback=self.crawl_website_data,meta={"page_number":response.meta.get('page_number')})
            
    def crawl_website_data(self,response):
        item = LetterboxdItem()

        item['title'] = response.xpath('//*[@id="film-page-wrapper"]/div[2]/section[1]/div/h1/span/text()').get()
        item['foreign_title'] = response.xpath('//*[@id="film-page-wrapper"]/div[2]/section[1]/div/div/h2/text()').get()
        item['foreign'] = False
        if item['title'] is not None:
            item['lower_title'] =  item['title'].replace(" ","").lower()
        if item['foreign_title'] is not None:
            item['lower_foreign_title'] =  item['foreign_title'].lower()
            item['foreign'] = True
        item['original_release_year'] = response.xpath('//*[@id="film-page-wrapper"]/div[2]/section[1]/div/div/div/a/text()').get()

        raw_text = response.xpath('//script[contains(@type, "application/ld+json")]/text()').get()

        letterboxd_grade,number_reviews,number_grade = self.clear_data_text(raw_text)
        item['letterboxd_grade'] = letterboxd_grade
        item['number_reviews'] = number_reviews
        item['number_grade'] = number_grade
        item['page_number'] = response.meta['page_number']
        item['url'] = response.url

        
        return item
        
    
    def clear_data_text(self,string):
        print(string)
        if string is not  None or string != "":
            
            string = string.replace("/* <![CDATA[ */","").replace("/* ]]> */","")
            data_dict = ast.literal_eval(string)
            if data_dict is not None:
                if "aggregateRating" in data_dict:
                    aggregateRating = data_dict.get("aggregateRating")
                    rating_value = aggregateRating.get("ratingValue")
                    review_count = aggregateRating.get("reviewCount")
                    rating_count = aggregateRating.get("ratingCount")
            
                    return rating_value,review_count,rating_count
                
                return None,None,None
        else:   
            return None,None,None
