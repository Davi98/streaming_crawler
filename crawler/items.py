# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JustWatchItem(scrapy.Item):
    
    imdbScore = Field()
    id = Field()
    title = Field()
    full_path = Field()
    website_url = Field()
    api_url = Field()
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
    netflix = Field()
    primevideo = Field()
    disneyplus = Field()
    hbomax = Field()
    paramountplus = Field()
    starplus = Field()
    globoplay = Field()


class LetterboxdItem(scrapy.Item):
    
    title = Field()
    foreign_title = Field()
    lower_title = Field()
    lower_foreign_title = Field()
    original_release_year = Field()
    letterboxd_grade = Field()
    number_reviews = Field()
    number_grade = Field()
    url = Field()
    page_number = Field()
    foreign = Field()


class RottenTomatoesItem(scrapy.Item):
    
    title = Field()
    audienceScore = Field()
    audienceScore_sentiment = Field()
    criticsScore = Field()
    criticsScore_sentiment = Field()
    criticsScore_certifiedAttribute = Field()
    lower_title = Field()
    original_release_year = Field()

    
class FilmowItem(scrapy.Item):
    
    title = Field()
    lower_title = Field()
    year = Field()
    original_title = Field()
    original_lower_title = Field()
    score = Field()
    number_votes = Field()
    url = Field()

class MetacriticItem(scrapy.Item):    
    
    year = Field()
    title = Field()
    lower_title = Field()
    meta_score = Field()
    meta_score_positive = Field()
    meta_score_mixed = Field()
    meta_score_negative = Field()
    user_score = Field()
    user_score_positive = Field()
    user_score_mixed = Field()
    user_score_negative = Field()
    runtime = Field()
    genre = Field()
    movie_url = Field()