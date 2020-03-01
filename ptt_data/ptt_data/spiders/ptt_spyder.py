# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 17:51:29 2020

@author: hyps4
"""

import scrapy
from scrapy.http import FormRequest
from ptt_data.items import PttDataItem
from scrapy.exceptions import CloseSpider

from datetime import datetime
import logging

class spyder(scrapy.Spider):
    name = 'ptt'
    domains = 'ptt.cc'
    start_urls = ['https://www.ptt.cc/bbs/']
    handle_httpstatus_list = [404]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }
    
    DATE = datetime.strftime(datetime.now(), "%m/%d")
    RETRY = 0
    MAX_RETRY = 10
    
    
    def __init__(self,ip='localhost', board='Beauty', 
                 start_date = DATE, end_date = DATE, *args, **kwargs):
        self.board_name = board
        self.ip = ip
        
        if start_date != self.DATE:
            self.start_date = datetime.strftime(datetime.strptime(start_date, '%m/%d'), '%m/%d')
            self.end_date = datetime.strftime(datetime.strptime(end_date, '%m/%d'), '%m/%d')
        else:
        	self.start_date = start_date
        	self.end_date = end_date
            
        super(spyder, self).__init__(*args, **kwargs)
    
    def parse_board(self, response):
        
        if response.status == 404:
            logging.warning('This board is not exists!.')
            
        #判斷是否有未成年提示
        elif len(response.xpath('//div[@class="over18-notice"]')):
              if self.RETRY < spyder.MAX_RETRY:
                  self.RETRY += 1
                  logging.warning('retry {} times...'.format(self.RETRY))
                  yield FormRequest.from_response(response,
                                                  formdata={'yes': 'yes'},
                                                  callback=self.parse_board)
              else:
                  logging.warning("You can not pass!")
                  
                  
        #爬取指定時間區間的文章，若無則跳出提示
        else:
            count = 0
            for article in response.css('.r-ent'):
                article_date = article.css('.meta > div.date::text').extract_first()
                
                #判斷日期是否符合
                if (self.start_date <= article_date.replace(" ",'0') and
                   self.end_date >= article_date.replace(" ",'0')):
                    count += 1
                    url = article.css('div.title > a::attr(href)').extract_first()
                    yield scrapy.Request(response.urljoin(url),
                                         callback=self.parse_article,
                                         priority=1)
            
            if count != 0:
                next_page = response.xpath(
                  '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    yield scrapy.Request(url, self.parse_board)
                else:
                    logging.warning('no next page')
                    
            else:
                logging.warning('no more article in this date range.')
                
    #爬取文章內文  
    def parse_article(self, response):
        item = PttDataItem()
        author = response.css(
                '#main-content > div:nth-child(1) > span.article-meta-value::text'
                ).extract_first()
        
        item['authorid'] = author.split(" ")[0]
        item['authorName'] = author.split(" ")[1][1:-1]
        
        item['title'] = response.css(
                '#main-content > div:nth-child(3) > span.article-meta-value::text'
                ).extract_first()
        
        datetime_str = response.css(
                '#main-content > div:nth-child(4) > span.article-meta-value::text'
                ).extract_first()
        
        item['publishedTime'] = int(datetime.timestamp(
                datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y'))*1000)
        
        item['content'] = response.xpath('//*[@id="main-content"]/text()')[0].extract()
        item['canonicalUrl'] = response.url
        item['createdTime'] = datetime.strftime(datetime.now(), '%a %b %d %H:%M:%S %Y')
        item['updateTime'] = datetime.strftime(datetime.now(), '%a %b %d %H:%M:%S %Y')
        
        comments = []
        
        for comment in response.xpath('//div[@class="push"]'):
            push_user = comment.css('span.push-userid::text')[0].extract()
            push_content = comment.css('span.push-content::text')[0].extract()
            push_time = comment.css('span.push-ipdatetime::text')[0].extract().strip('\t\n\r')
            
            comments.append({'commentId': push_user,
                             'commentContent': push_content,
                             'commentTime': push_time})
        
        item['comments'] = comments
        
        yield item
        
    #進入指定的看板
    def parse(self, response):
        url = response.urljoin(self.board_name)
        yield scrapy.Request(url,dont_filter=True,
                                 callback=self.parse_board)
            
            
          
            
    