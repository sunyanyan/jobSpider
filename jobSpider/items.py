# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class JobspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobDetailItem(Item):
    job_time = Field()
    job_type = Field()
    job_pay = Field()
    job_city = Field()
    job_age = Field()
    job_edu = Field()
    job_company_name = Field()
    job_company_type = Field()
    job_company_kind = Field()
    job_company_pn = Field()
    job_company_add = Field()
    job_company_long_lat = Field()
    job_desc = Field()