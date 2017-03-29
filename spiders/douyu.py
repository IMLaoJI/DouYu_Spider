# -*- coding: utf-8 -*-
import scrapy
from test0713_001.items import DouyuItem
import json

class DouyuSpider(scrapy.Spider):
    name = "douyu"
    allowed_domains = ["douyucdn.cn"]
    offset = 0

    start_urls = (
         'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='+str(offset),
    )

    def parse(self, response):
        data=json.loads(response.text)['data']
        if not data :
            return

        for it in data:
            item = DouyuItem()
            item['image_urls']=it['vertical_src']
            #item['image_urls'] = ['http://n.sinaimg.cn/mil/crawl/20160708/tHs5-fxtwiht3360399.jpg']
            item['name']=it['nickname']

            yield item

        self.offset+=20
        yield scrapy.Request('http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset=%s'%str(self.offset),callback=self.parse)
       
