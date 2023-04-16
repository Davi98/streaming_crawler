from cgitb import reset
from flatten_json import flatten
import scrapy
from scrapy.utils.project import get_project_settings
from crawler.items import JustWatchItem
import json



class JustWatch(scrapy.Spider):
    settings = get_project_settings()
    name = "justwatch"
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

    
    

    header = {
        'authority': 'apis.justwatch.com',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'device-id': 'TzHP4q6oEeyoJdp3EtuLnw',
        'origin': 'https://www.justwatch.com',
        'referer': 'https://www.justwatch.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
        }

    def build_payload(self,cursor,package,releaseYearMin, releaseYearMax):
        payload = json.dumps({
        "operationName": "GetPopularTitles",
        "variables": {
            "popularTitlesSortBy": "POPULAR",
            "first": 40,
            "platform": "WEB",
            "sortRandomSeed": 0,
            "popularAfterCursor": cursor,
            "popularTitlesFilter": {
            "ageCertifications": [],
            "excludeGenres": [],
            "excludeProductionCountries": [],
            "genres": [],
            "objectTypes": [
                "MOVIE"
            ],
            "productionCountries": [],
            "packages": [
                package
            ],
            "excludeIrrelevantTitles": False,
            "presentationTypes": [],
            "monetizationTypes": [],
            "releaseYear": {
                "min": releaseYearMin,
                "max": releaseYearMax
            }
            },
            "watchNowFilter": {
            "packages": [
                package
            ],
            "monetizationTypes": []
            },
            "language": "pt",
            "country": "BR"
        },
        "query": "query GetPopularTitles($country: Country!, $popularTitlesFilter: TitleFilter, $watchNowFilter: WatchNowOfferFilter!, $popularAfterCursor: String, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $first: Int! = 40, $language: Language!, $platform: Platform! = WEB, $sortRandomSeed: Int! = 0, $profile: PosterProfile, $backdropProfile: BackdropProfile, $format: ImageFormat) {\n  popularTitles(\n    country: $country\n    filter: $popularTitlesFilter\n    after: $popularAfterCursor\n    sortBy: $popularTitlesSortBy\n    first: $first\n    sortRandomSeed: $sortRandomSeed\n  ) {\n    totalCount\n    pageInfo {\n      startCursor\n      endCursor\n      hasPreviousPage\n      hasNextPage\n      __typename\n    }\n    edges {\n      ...PopularTitleGraphql\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PopularTitleGraphql on PopularTitlesEdge {\n  cursor\n  node {\n    id\n    objectId\n    objectType\n    content(country: $country, language: $language) {\n      title\n      fullPath\n      scoring {\n        imdbScore\n        __typename\n      }\n      posterUrl(profile: $profile, format: $format)\n      ... on ShowContent {\n        backdrops(profile: $backdropProfile, format: $format) {\n          backdropUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    likelistEntry {\n      createdAt\n      __typename\n    }\n    dislikelistEntry {\n      createdAt\n      __typename\n    }\n    watchlistEntry {\n      createdAt\n      __typename\n    }\n    watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {\n      id\n      standardWebURL\n      package {\n        packageId\n        clearName\n        __typename\n      }\n      retailPrice(language: $language)\n      retailPriceValue\n      lastChangeRetailPriceValue\n      currency\n      presentationType\n      monetizationType\n      __typename\n    }\n    ... on Movie {\n      seenlistEntry {\n        createdAt\n        __typename\n      }\n      __typename\n    }\n    ... on Show {\n      seenState(country: $country) {\n        seenEpisodeCount\n        progress\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
        })
        
        return payload
        

    def start_requests(self):

        packages = ["dnp","hbm","nfx","pmp","prv","srp","gop"]

        for pack in packages:
            if pack == "nfx":
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,1900,2018),meta={"package":pack,"releaseYearMin":1900,"releaseYearMax":2018})
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,2019,2023),meta={"package":pack,"releaseYearMin":2019,"releaseYearMax":2023})
            elif pack == "prv":
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,1900,2015),meta={"package":pack,"releaseYearMin":1900,"releaseYearMax":2015})
        
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,2016,2023),meta={"package":pack,"releaseYearMin":2016,"releaseYearMax":2023})   
            else:
                 yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,1900,2023),meta={"package":pack,"releaseYearMin":1900,"releaseYearMax":2023})

    
        

        

    def crawl_catalog(self,response):
        data = (response.json())

        has_next = data.get("data").get("popularTitles").get("pageInfo").get("hasNextPage")
        movies_array = data.get("data").get("popularTitles").get("edges")
        total = data.get("data").get("popularTitles").get("totalCount")

        next_cursor = data.get("data").get("popularTitles").get("pageInfo").get("endCursor")
        for movie in movies_array:
            movie_id = movie.get("node").get("objectId")
            yield scrapy.Request(method="GET",url=f"https://apis.justwatch.com/content/titles/movie/{movie_id}/locale/pt_BR?language=pt", callback=self.crawl_movie_api_data,headers=self.header,meta=movie)

        if has_next is True:
            response.meta['package'] = response.meta.get("package")
            response.meta['releaseYearMin'] =  response.meta.get("releaseYearMin")
            response.meta['releaseYearMax'] =  response.meta.get("releaseYearMax")
            
            yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload(next_cursor,response.meta.get("package"),response.meta.get("releaseYearMin"),response.meta.get("releaseYearMax")),dont_filter=True,meta=response.meta)
        
    
        
    def crawl_movie_api_data(self,response):
        data = (response.json())
        response.meta.update(data)
        response.meta['api_url'] = response.url
        movie_path = data.get("full_path")

        yield scrapy.Request(method="GET",url=f"https://www.justwatch.com{movie_path}", callback=self.crawl_webpage_data,headers=self.header,meta=response.meta,dont_filter=True)

    
    def crawl_webpage_data(self,response):
        justwatchScore = response.xpath("//*[@id=\"base\"]/div[2]/div/div[1]/div/aside/div[1]/div[3]/div[1]/div[2]/div/div[1]/a/text()").get()
        response.meta['justwatchScore'] = justwatchScore
        response.meta['website_url'] = response.url
        movie_genre = response.xpath("//*[@id=\"base\"]/div[2]/div/div[1]/div/aside/div[1]/div[3]/div[2]/div[2]/span[1]/text()").get()
        response.meta['movie_genre'] = movie_genre
        
        
        yield self.return_movie_data(response.meta)        
        
    
    def return_movie_data(self,data):
        
        item = JustWatchItem()
        scoring = data.get("scoring")
        if scoring is not None:
            for score in scoring:
                if score.get("provider_type") == 'imdb:votes':
                    item['imdbVotes'] = score.get("value")
                elif score.get("provider_type") == 'tmdb:score':
                    item['tmbdScore'] = score.get("value")
                elif score.get("provider_type") == 'imdb:popularity':
                    item['imbdPopularity'] = score.get("value")
                elif score.get("provider_type") == 'tmdb:popularity':
                    item['tmdbPopularity'] = score.get("value")
        
        offers = data.get("offers")
        
        netflix = False
        primevideo = False
        disneyplus = False
        hbomax = False
        paramountplus = False
        starplus = False
        globoplay = False

                        
        if offers is not None:
            for offer in offers:
                if offer.get("monetization_type") == "flatrate":
                    if offer.get("package_short_name") == "nfx":
                        netflix = True
                    elif offer.get("package_short_name") == "prv":
                        primevideo = True
                    elif offer.get("package_short_name") == "dnp":
                        disneyplus = True
                    elif offer.get("package_short_name") == "hbm":
                        hbomax = True
                    elif offer.get("package_short_name") == "pmp":
                        paramountplus = True
                    elif offer.get("package_short_name") == "srp":
                        starplus = True
                    elif offer.get("package_short_name") == "gop":
                        globoplay = True

        
        data = flatten(data)

        item['imdbScore'] = data.get("node_content_scoring_imdbScore")

        item['id'] = data.get("id")
        item['title'] = data.get("title")
        item['full_path'] = data.get("full_path")
        item['website_url'] = data.get("website_url")
        item['api_url'] = data.get("api_url")
        item['original_release_year'] = data.get("original_release_year")
        item['object_type'] = data.get("object_type")
        item['original_title'] = data.get("original_title")
        item['movie_genre'] = data.get("movie_genre")
        item['age_certification'] = data.get("age_certification")
        if item['age_certification'] == "L":
            item['age_certification'] = "0"
        item['production_countrie'] = data.get("production_countries_0")
        item['runtime'] = data.get('runtime')
        item['justwatchScore'] = data.get("justwatchScore")
        if data.get("original_title") is not None:
            item['lower_title'] = data.get("original_title").lower().replace(" ","")
        
        item['netflix'] = netflix
        item['primevideo'] = primevideo
        item['disneyplus'] = disneyplus
        item['hbomax'] =  hbomax
        item['paramountplus'] = paramountplus
        item['starplus'] =  starplus
        item['globoplay'] =  globoplay

        
        return item