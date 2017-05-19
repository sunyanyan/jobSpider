# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jobSpider.items import JobDetailItem
from jobSpider.items import TestJobDetailItem
import sqlite3
import os
import shutil
from collections import OrderedDict

class JobspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class FilePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JobDetailItem):
            print("文件流 FilePipeline ")
            return item

class Sqlite3Pipeline(object):

    def __init__(self, sqlite_file, sqlite_base_file, sqlite_ZhiPin_table, sqlite_Test_ZhiPin_table):
        self.sqlite_file = sqlite_file
        self.sqlite_base_file = sqlite_base_file
        self.sqlite_ZhiPin_table = sqlite_ZhiPin_table
        self.sqlite_Test_ZhiPin_table = sqlite_Test_ZhiPin_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE_PATH'), # 从 settings.py 提取
            sqlite_base_file=crawler.settings.get('SQLITE_BASE_FILE_PATH'),
            sqlite_ZhiPin_table = crawler.settings.get('SQLITE_ZHI_PIN_ITEM_TABLE'),
            sqlite_Test_ZhiPin_table=crawler.settings.get('SQLITE_TEST_ZHI_PIN_ITEM_TABLE')
        )

    def open_spider(self, spider):
        print("\n Sqlite3Pipeline open_spider\n")
        self.create_sql_db()
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        print("\n Sqlite3Pipeline close_spider\n")
        self.conn.close()

    def process_item(self, item, spider):
        print("\n Sqlite3Pipeline process_item\n")
        if isinstance(item, JobDetailItem):
            print(" sqlite3 处理 JobDetailItem ")

            orderedDict = OrderedDict(sorted(item.items(), key=lambda t: t[0]))
            keys = list(orderedDict.keys())
            values = list(orderedDict.values())
            insert_sql = "insert into {0}({1}) values ({2})".format(self.sqlite_ZhiPin_table,
                                                                ', '.join(keys),
                                                                ', '.join(['?'] * len(keys)))

            self.cur.execute(insert_sql, values)
            self.conn.commit()
            return item
        elif isinstance(item,TestJobDetailItem):
            print(" sqlite3 处理 TestJobDetailItem ")
            insert_sql = "insert into {0}({1}) values ({2})".format(self.sqlite_Test_ZhiPin_table,
                                                                ', '.join(list(item.fields.keys())),
                                                                ', '.join(['?'] * len(list(item.fields.keys()))))
            print(" insert_sql: "+insert_sql)
            print(" list(item.fields.keys()): ", list(item.fields.keys()))
            print(" list(item.values()): ", list(item.values()))
            self.cur.execute(insert_sql, list(item.values()))
            self.conn.commit()
            return item
        else:
            print(" item 类型不对 sqlite3不处理")
            return item

    def create_sql_db(self):
        #复制原始数据库，（也可以直接新建一个，只不过懒得写SQL……
        sql_db_path = os.path.abspath(self.sqlite_file)
        sql_base_db_path = os.path.abspath(self.sqlite_base_file)
        print("\n create_sql_db  \n  ", sql_db_path, sql_base_db_path)
        if not os.path.exists(sql_db_path):
            shutil.copyfile(sql_base_db_path, sql_db_path)
