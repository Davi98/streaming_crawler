from urllib import response
from flatten_json import flatten
import scrapy
from scrapy.utils.project import get_project_settings
from crawler.items import RottenTomatoesItem
import ast



class RottenTomatoes(scrapy.Spider):
    settings = get_project_settings()
    name = "rottentomatoes"
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
    

    def build_catalog_url(self,cursor):
        return f"https://www.rottentomatoes.com/napi/browse/movies_at_home/?after={cursor}"
    
    
    def start_requests(self):
        
        yield scrapy.Request(method='GET',url=self.build_catalog_url(""),callback=self.start_navigate)
        
        
    def start_navigate(self,response):
        data = response.json()
        hasNext = (data.get("pageInfo").get("hasNextPage"))
        movies_array = data.get("grids")[0].get("list")
        if movies_array is not None or movies_array != []:
            for movie in movies_array:
                yield self.parse(movie)
        
        if hasNext is True:
            cursor = (data.get("pageInfo").get("endCursor"))
            yield scrapy.Request(method='GET',url=self.build_catalog_url(cursor),callback=self.start_navigate)
        

    def parse(self,data):
        
        item = RottenTomatoesItem()

        item['title'] = data.get('title')
        audienceScore = data.get("audienceScore")
        
        if audienceScore is not None:
            item['audienceScore'] = audienceScore.get("score")
            item['audienceScore_sentiment'] = audienceScore.get("sentiment")
        
        criticsScore = data.get("criticsScore")
        
        if criticsScore is not None:
            item['criticsScore'] = criticsScore.get("score")
            item['criticsScore_sentiment'] = criticsScore.get("sentiment")
            if criticsScore.get("certifiedAttribute") == "criticscertified":
                item['criticsScore_certifiedAttribute'] = True
            else:
                item['criticsScore_certifiedAttribute'] = False
        
        item['lower_title'] = data.get("title").lower().replace(" ","")
        
        return item
