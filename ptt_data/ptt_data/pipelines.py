# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class PttDataPipeline(object):
    def open_spider(self, spider):
        self.ip = spider.ip
        self.client = pymongo.MongoClient("mongodb://%s:27017/" % self.ip)
        self.db = self.client['ptt_data']
        self.col = self.db['ptt_cache']
        
    def process_item(self, item, spider):
        self.insert_article(item)
#        pass
    
    #直接運用replace_one判斷canonicalUrl是否有重複的，若有則不重複插入
    def insert_article(self, item):
        self.col.replace_one({'canonicalUrl': item['canonicalUrl']}, item, upsert=True) 
    
    def close_spider(self, spider):
        self.client.close()
#        pass