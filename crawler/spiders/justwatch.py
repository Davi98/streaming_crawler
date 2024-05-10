from cgitb import reset
from flatten_json import flatten
import scrapy
from scrapy.utils.project import get_project_settings
from crawler.items import JustWatchItem
import json
import re
import datetime


class JustWatch(scrapy.Spider):
    settings = get_project_settings()
    name = "justwatch"
    file_path = settings.get('FILE_PATH')
    exec_date = datetime.date.today().strftime("%d%m%Y")

    custom_settings = {
        # 'FEED_URI': f'downloads/{name}.csv',
        # 'FEED_FORMAT': 'csv',
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
    
    def build_movie_payload(self,fullPath):

        url = "https://apis.justwatch.com/graphql"

        payload = json.dumps({
        "operationName": "GetUrlTitleDetails",
        "variables": {
            "platform": "WEB",
            "fullPath": fullPath,
            "language": "pt",
            "country": "BR",
            "episodeMaxLimit": 20,
            "allowSponsoredRecommendations": {
            "appId": "3.8.2-webapp#b8e3074",
            "country": "BR",
            "language": "pt",
            "pageType": "VIEW_TITLE_DETAIL",
            "placement": "DETAIL_PAGE",
            "platform": "WEB",
            "supportedObjectTypes": [
                "MOVIE",
                "SHOW",
                "GENERIC_TITLE_LIST"
            ],
            "supportedFormats": [
                "IMAGE",
                "VIDEO"
            ]
            }
        },
        "query": "query GetUrlTitleDetails($fullPath: String!, $country: Country!, $language: Language!, $episodeMaxLimit: Int, $platform: Platform! = WEB, $allowSponsoredRecommendations: SponsoredRecommendationsInput, $format: ImageFormat, $backdropProfile: BackdropProfile) {\n  urlV2(fullPath: $fullPath) {\n    id\n    metaDescription\n    metaKeywords\n    metaRobots\n    metaTitle\n    heading1\n    heading2\n    htmlContent\n    node {\n      id\n      __typename\n      ... on MovieOrShowOrSeason {\n        plexPlayerOffers: offers(\n          country: $country\n          platform: $platform\n          filter: {packages: [\"pxp\"]}\n        ) {\n          id\n          standardWebURL\n          package {\n            id\n            packageId\n            clearName\n            technicalName\n            shortName\n            __typename\n          }\n          __typename\n        }\n        disneyOffersCount: offerCount(\n          country: $country\n          platform: $platform\n          filter: {packages: [\"dnp\"]}\n        )\n        objectType\n        objectId\n        offerCount(country: $country, platform: $platform)\n        offers(country: $country, platform: $platform) {\n          monetizationType\n          elementCount\n          package {\n            id\n            packageId\n            clearName\n            __typename\n          }\n          __typename\n        }\n        watchNowOffer(country: $country, platform: $platform) {\n          id\n          standardWebURL\n          __typename\n        }\n        promotedBundles(country: $country, platform: $platform) {\n          promotionUrl\n          __typename\n        }\n        availableTo(country: $country, platform: $platform) {\n          availableCountDown(country: $country)\n          availableToDate\n          package {\n            id\n            shortName\n            __typename\n          }\n          __typename\n        }\n        fallBackClips: content(country: \"US\", language: \"en\") {\n          videobusterClips: clips(providers: [VIDEOBUSTER]) {\n            ...TrailerClips\n            __typename\n          }\n          dailymotionClips: clips(providers: [DAILYMOTION]) {\n            ...TrailerClips\n            __typename\n          }\n          __typename\n        }\n        content(country: $country, language: $language) {\n          backdrops {\n            backdropUrl\n            __typename\n          }\n          fullBackdrops: backdrops(profile: S1920, format: JPG) {\n            backdropUrl\n            __typename\n          }\n          clips {\n            ...TrailerClips\n            __typename\n          }\n          videobusterClips: clips(providers: [VIDEOBUSTER]) {\n            ...TrailerClips\n            __typename\n          }\n          dailymotionClips: clips(providers: [DAILYMOTION]) {\n            ...TrailerClips\n            __typename\n          }\n          externalIds {\n            imdbId\n            __typename\n          }\n          fullPath\n          genres {\n            shortName\n            __typename\n          }\n          posterUrl\n          fullPosterUrl: posterUrl(profile: S718, format: JPG)\n          runtime\n          isReleased\n          scoring {\n            imdbScore\n            imdbVotes\n            tmdbPopularity\n            tmdbScore\n            jwRating\n            __typename\n          }\n          shortDescription\n          title\n          originalReleaseYear\n          originalReleaseDate\n          upcomingReleases(releaseTypes: DIGITAL) {\n            releaseCountDown(country: $country)\n            releaseDate\n            label\n            package {\n              id\n              packageId\n              shortName\n              clearName\n              __typename\n            }\n            __typename\n          }\n          ... on MovieOrShowContent {\n            originalTitle\n            ageCertification\n            credits {\n              role\n              name\n              characterName\n              personId\n              __typename\n            }\n            interactions {\n              dislikelistAdditions\n              likelistAdditions\n              votesNumber\n              __typename\n            }\n            productionCountries\n            __typename\n          }\n          ... on SeasonContent {\n            seasonNumber\n            interactions {\n              dislikelistAdditions\n              likelistAdditions\n              votesNumber\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        popularityRank(country: $country) {\n          rank\n          trend\n          trendDifference\n          __typename\n        }\n        __typename\n      }\n      ... on MovieOrShow {\n        watchlistEntryV2 {\n          createdAt\n          __typename\n        }\n        likelistEntry {\n          createdAt\n          __typename\n        }\n        dislikelistEntry {\n          createdAt\n          __typename\n        }\n        customlistEntries {\n          createdAt\n          genericTitleList {\n            id\n            __typename\n          }\n          __typename\n        }\n        similarTitlesV2(\n          country: $country\n          allowSponsoredRecommendations: $allowSponsoredRecommendations\n        ) {\n          sponsoredAd {\n            ...SponsoredAdTitleDetail\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Movie {\n        permanentAudiences\n        seenlistEntry {\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      ... on Show {\n        permanentAudiences\n        totalSeasonCount\n        seenState(country: $country) {\n          progress\n          seenEpisodeCount\n          __typename\n        }\n        tvShowTrackingEntry {\n          createdAt\n          __typename\n        }\n        seasons(sortDirection: DESC) {\n          id\n          objectId\n          objectType\n          totalEpisodeCount\n          availableTo(country: $country, platform: $platform) {\n            availableToDate\n            availableCountDown(country: $country)\n            package {\n              id\n              shortName\n              __typename\n            }\n            __typename\n          }\n          content(country: $country, language: $language) {\n            posterUrl\n            seasonNumber\n            fullPath\n            title\n            upcomingReleases(releaseTypes: DIGITAL) {\n              releaseDate\n              releaseCountDown(country: $country)\n              package {\n                id\n                shortName\n                __typename\n              }\n              __typename\n            }\n            isReleased\n            originalReleaseYear\n            __typename\n          }\n          show {\n            id\n            objectId\n            objectType\n            watchlistEntryV2 {\n              createdAt\n              __typename\n            }\n            content(country: $country, language: $language) {\n              title\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        recentEpisodes: episodes(\n          sortDirection: DESC\n          limit: 3\n          releasedInCountry: $country\n        ) {\n          id\n          objectId\n          content(country: $country, language: $language) {\n            title\n            shortDescription\n            episodeNumber\n            seasonNumber\n            isReleased\n            upcomingReleases {\n              releaseDate\n              label\n              __typename\n            }\n            __typename\n          }\n          seenlistEntry {\n            createdAt\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Season {\n        totalEpisodeCount\n        episodes(limit: $episodeMaxLimit) {\n          id\n          objectType\n          objectId\n          seenlistEntry {\n            createdAt\n            __typename\n          }\n          content(country: $country, language: $language) {\n            title\n            shortDescription\n            episodeNumber\n            seasonNumber\n            isReleased\n            upcomingReleases(releaseTypes: DIGITAL) {\n              releaseDate\n              label\n              package {\n                id\n                packageId\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        show {\n          id\n          objectId\n          objectType\n          totalSeasonCount\n          customlistEntries {\n            createdAt\n            genericTitleList {\n              id\n              __typename\n            }\n            __typename\n          }\n          tvShowTrackingEntry {\n            createdAt\n            __typename\n          }\n          fallBackClips: content(country: \"US\", language: \"en\") {\n            videobusterClips: clips(providers: [VIDEOBUSTER]) {\n              ...TrailerClips\n              __typename\n            }\n            dailymotionClips: clips(providers: [DAILYMOTION]) {\n              ...TrailerClips\n              __typename\n            }\n            __typename\n          }\n          content(country: $country, language: $language) {\n            title\n            ageCertification\n            fullPath\n            genres {\n              shortName\n              __typename\n            }\n            credits {\n              role\n              name\n              characterName\n              personId\n              __typename\n            }\n            productionCountries\n            externalIds {\n              imdbId\n              __typename\n            }\n            upcomingReleases(releaseTypes: DIGITAL) {\n              releaseDate\n              __typename\n            }\n            backdrops {\n              backdropUrl\n              __typename\n            }\n            posterUrl\n            isReleased\n            videobusterClips: clips(providers: [VIDEOBUSTER]) {\n              ...TrailerClips\n              __typename\n            }\n            dailymotionClips: clips(providers: [DAILYMOTION]) {\n              ...TrailerClips\n              __typename\n            }\n            __typename\n          }\n          seenState(country: $country) {\n            progress\n            __typename\n          }\n          watchlistEntryV2 {\n            createdAt\n            __typename\n          }\n          dislikelistEntry {\n            createdAt\n            __typename\n          }\n          likelistEntry {\n            createdAt\n            __typename\n          }\n          similarTitlesV2(\n            country: $country\n            allowSponsoredRecommendations: $allowSponsoredRecommendations\n          ) {\n            sponsoredAd {\n              ...SponsoredAdTitleDetail\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        seenState(country: $country) {\n          progress\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n}\n\nfragment TrailerClips on Clip {\n  sourceUrl\n  externalId\n  provider\n  name\n  __typename\n}\n\nfragment SponsoredAdTitleDetail on SponsoredRecommendationAd {\n  bidId\n  holdoutGroup\n  campaign {\n    externalTrackers {\n      type\n      data\n      __typename\n    }\n    hideRatings\n    promotionalImageUrl\n    promotionalVideo {\n      url\n      __typename\n    }\n    promotionalText\n    watchNowLabel\n    watchNowOffer {\n      standardWebURL\n      presentationType\n      monetizationType\n      package {\n        id\n        packageId\n        shortName\n        clearName\n        icon\n        __typename\n      }\n      __typename\n    }\n    node {\n      nodeId: id\n      ... on MovieOrShow {\n        content(country: $country, language: $language) {\n          fullPath\n          posterUrl\n          title\n          originalReleaseYear\n          scoring {\n            imdbScore\n            __typename\n          }\n          externalIds {\n            imdbId\n            __typename\n          }\n          backdrops(format: $format, profile: $backdropProfile) {\n            backdropUrl\n            __typename\n          }\n          isReleased\n          __typename\n        }\n        objectId\n        objectType\n        offers(country: $country, platform: $platform) {\n          monetizationType\n          presentationType\n          package {\n            id\n            packageId\n            __typename\n          }\n          id\n          __typename\n        }\n        watchlistEntryV2 {\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      ... on Show {\n        seenState(country: $country) {\n          seenEpisodeCount\n          __typename\n        }\n        __typename\n      }\n      ... on GenericTitleList {\n        followedlistEntry {\n          createdAt\n          name\n          __typename\n        }\n        id\n        name\n        type\n        visibility\n        titles(country: $country) {\n          totalCount\n          edges {\n            cursor\n            node {\n              content(country: $country, language: $language) {\n                fullPath\n                posterUrl\n                title\n                originalReleaseYear\n                scoring {\n                  imdbScore\n                  __typename\n                }\n                isReleased\n                __typename\n              }\n              id\n              objectId\n              objectType\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
        })

        return payload


    def start_requests(self):

        packages = ["dnp","hbm","nfx","pmp","prv","srp","gop"]
        # packages = ['dnp']

        for pack in packages:
            if pack == "nfx":
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,1900,2018),meta={"package":pack,"releaseYearMin":1900,"releaseYearMax":2018})
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,2019,2024),meta={"package":pack,"releaseYearMin":2019,"releaseYearMax":2023})
            elif pack == "prv":
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,1900,2015),meta={"package":pack,"releaseYearMin":1900,"releaseYearMax":2015})
        
                yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,2016,2024),meta={"package":pack,"releaseYearMin":2016,"releaseYearMax":2023})   
            else:
                 yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload("",pack,1900,2024),meta={"package":pack,"releaseYearMin":1900,"releaseYearMax":2023})


    def crawl_catalog(self,response):
        data = (response.json())
        # print(data)

        has_next = data.get("data").get("popularTitles").get("pageInfo").get("hasNextPage")
        movies_array = data.get("data").get("popularTitles").get("edges")
        total = data.get("data").get("popularTitles").get("totalCount")

        next_cursor = data.get("data").get("popularTitles").get("pageInfo").get("endCursor")
        for movie in movies_array:
            movie_path = movie.get("node").get("content").get("fullPath")

            yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_movie_api_data,headers=self.header,body=self.build_movie_payload(movie_path),meta=movie)

        if has_next is True:
            response.meta['package'] = response.meta.get("package")
            response.meta['releaseYearMin'] =  response.meta.get("releaseYearMin")
            response.meta['releaseYearMax'] =  response.meta.get("releaseYearMax")
            
            yield scrapy.Request(method="POST",url="https://apis.justwatch.com/graphql", callback=self.crawl_catalog,headers=self.header,body=self.build_payload(next_cursor,response.meta.get("package"),response.meta.get("releaseYearMin"),response.meta.get("releaseYearMax")),dont_filter=True,meta=response.meta)
        
    
        
    def crawl_movie_api_data(self,response):
        data = (response.json())
        response.meta.update(data)

        # yield scrapy.Request(method="GET",url=f"https://www.justwatch.com{movie_path}", callback=self.crawl_webpage_data,headers=self.header,meta=response.meta,dont_filter=True)

        yield self.return_movie_data(response.meta) 

    
    # def crawl_webpage_data(self,response):
    #     justwatchScore = response.xpath("/html/head/script[39]").get()
    #     print(justwatchScore)
    #     if justwatchScore is not None:
    #         response.meta['justwatchScore'] = int(justwatchScore.replace(" ","").replace("\n", "").replace(",","").replace("%",""))
    #     response.meta['website_url'] = response.url
    #     movie_genre = response.xpath("//*[@id=\"base\"]/div[2]/div/div[1]/div/aside/div[1]/div[3]/div[2]/div/text()").get()
    #     response.meta['movie_genre'] = movie_genre
        
    #     yield self.return_movie_data(response.meta)        
        
    
    def return_movie_data(self,data):
        # print(data)
        item = JustWatchItem()

        
        movie_data =  data.get("data").get("urlV2").get("node")
        offers = movie_data.get("plexPlayerOffers")

        
        netflix = False
        primevideo = False
        disneyplus = False
        hbomax = False
        paramountplus = False
        starplus = False
        globoplay = False

                        
        if offers is not None:
            for offer in offers:
                if offer.get("package").get("shortName") == "nfx":
                    netflix = True
                elif offer.get("package").get("shortName") == "prv":
                    primevideo = True
                elif offer.get("package").get("shortName") == "dnp":
                    disneyplus = True
                elif offer.get("package").get("shortName") == "hbm":
                    hbomax = True
                elif offer.get("package").get("shortName") == "pmp":
                    paramountplus = True
                elif offer.get("package").get("shortName") == "srp":
                    starplus = True
                elif offer.get("package").get("shortName") == "gop":
                    globoplay = True

        
        item['id'] = movie_data.get("id")
        item['title'] = movie_data.get("content").get("title")
        item['full_path'] = movie_data.get("content").get("fullPath")
        item['website_url'] = f"www.justwatch.com{data.get('node').get('content').get('fullPath')}"
        item['original_release_year'] = movie_data.get("content").get("originalReleaseYear")
        item['object_type'] = movie_data.get("objectType")
        item['original_title'] = movie_data.get("content").get("originalTitle")
        item['age_certification'] = movie_data.get("content").get("ageCertification")
        item['runtime'] = movie_data.get("content").get("runtime")
        production_countrie = movie_data.get("content").get("productionCountries")
        if production_countrie is not None and len(production_countrie) > 0:
            item['production_countrie'] = production_countrie[0]
        item['justwatchScore'] = movie_data.get("content").get("scoring").get("jwRating")
        item['imdbScore'] = movie_data.get("content").get("scoring").get("imdbScore")
        item['imdbPopularity'] = movie_data.get("content").get("scoring").get("tmdbPopularity")
        item['imdbVotes'] = movie_data.get("content").get("scoring").get("imdbVotes")
        item['tmdbScore'] = movie_data.get("content").get("scoring").get("tmdbScore")
        item['tmdbPopularity'] = movie_data.get("content").get("scoring").get("tmdbPopularity")
        lower_title = re.sub(r'[^a-zA-Z0-9]+', '', item['original_title']).lower()
        item['lower_title'] = lower_title
        movie_genres = movie_data.get("content").get("genres")
        if movie_genres is not None and len(movie_genres) > 0:
            item['movie_genre'] = movie_genres[0].get("shortName")

     
        
        item['netflix'] = netflix
        item['primevideo'] = primevideo
        item['disneyplus'] = disneyplus
        item['hbomax'] =  hbomax
        item['paramountplus'] = paramountplus
        item['starplus'] =  starplus
        item['globoplay'] =  globoplay

        
        return item
    
