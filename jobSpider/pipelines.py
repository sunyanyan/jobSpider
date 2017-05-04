# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jobSpider.items import JobDetailItem

class JobspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class FilePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JobDetailItem):
            print("文件流 FilePipeline ")
            return item