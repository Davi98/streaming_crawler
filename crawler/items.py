# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MovieItem(scrapy.Item):
    
    imdbScore = Field()
    packageId = Field()
    packageName = Field()
    id = Field()
    title = Field()
    full_path = Field()
    website_url = Field()
    api_url = Field()
    short_description = Field()
    original_release_year = Field()
    object_type = Field()
    original_title = Field()
    age_certification = Field()
    runtime = Field()
    production_countrie = Field()
    tmbdScore = Field()
    justwatchScore = Field()
    imbdPopularity = Field()
    imdbVotes = Field()
    tmdbPopularity = Field()
    lower_title = Field()
    movie_genre = Field()


