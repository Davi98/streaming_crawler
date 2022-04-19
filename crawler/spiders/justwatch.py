import scrapy
from scrapy.utils.project import get_project_settings
import json


class JustWatch(scrapy.Spider):
    settings = get_project_settings()
    name = "justwatch"
    file_path = settings.get('FILE_PATH')
    custom_settings = {
        'FEED_URI': f'downloads/{name}.csv',
        'FEED_FORMAT': 'csv'
    }
    headers = {}
    
    big_data = []
    
    

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

    def build_payload(self,cursor):
        payload  = json.dumps({
        "operationName": "GetPopularTitles",
        "variables": {
            "popularTitlesSortBy": "ALPHABETICAL",
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
                "dnp","hbm","nfx","pmp","prv","srp","gop"
            ],
            "excludeIrrelevantTitles": False,
            "presentationTypes": [],
            "monetizationTypes": []
            },
            "watchNowFilter": {
            "packages": [
                "dnp","hbm","nfx","pmp","prv","srp","gop"
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

        yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload(""))
        

    def crawl_catalog(self,response):
        data = (response.json())
        has_next = data.get("data").get("popularTitles").get("pageInfo").get("hasNextPage")
        movies_array = data.get("data").get("popularTitles").get("edges")
        next_cursor = data.get("data").get("popularTitles").get("pageInfo").get("endCursor")
        for movie in movies_array:
            movie_id = movie.get("node").get("objectId")
            yield scrapy.Request(method="GET",url=f"https://apis.justwatch.com/content/titles/movie/{movie_id}/locale/pt_BR?language=pt", callback=self.crawl_movie_data,headers=self.header,meta=movie)
        
        if has_next is True:
            yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload(next_cursor))
        
    
        
    def crawl_movie_api_data(self,response):
        print(response)

        return None