# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MovieItem(scrapy.Item):
    jw_entity_id = Field()
    id = Field()
    title = Field()
    full_path = Field()
    full_paths = Field()
    poster = Field()
    poster_blur_hash = Field()
    backdrops = Field()
    short_description = Field()
    original_release_year = Field()
    object_type = Field()
    original_title = Field()
    offers = Field()
    scoring = Field()
    credits = Field()
    external_ids = Field()
    genre_ids = Field()
    age_certification = Field()
    runtime = Field()
    production_countries = Field()
    permanent_audiences = Field()
