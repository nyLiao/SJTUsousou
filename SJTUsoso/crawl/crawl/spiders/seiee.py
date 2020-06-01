# -*- coding: utf-8 -*-
import scrapy
import re

from crawl.items import ArticleItem
from crawl.spiders.cleaner import fmt_text
from soso.genKw import get_kw, get_view

class SeieeSpider(scrapy.Spider):
    name = 'seiee'
    allowed_domains = ['seiee.sjtu.edu.cn']
    # start_urls = ['http://www.seiee.sjtu.edu.cn/seiee/list/682-1-20.htm']
    start_urls = ['http://www.seiee.sjtu.edu.cn/seiee/list/681-1-500.htm']

    def parse(self, response):
        urls = response.xpath('//*[@id="MMiddle_2_div"]/ul/li/a//@href').extract()
        for url in urls:
            fullurl = response.urljoin(url)
            # print(fullurl)
            yield scrapy.Request(url=fullurl, callback=self.parse_page)

    def parse_page(self, response):
        def cln_text(text):
            text = re.sub('\$\(([\s\S]*?)\}\);', '', text)
            return fmt_text(text)

        article = ArticleItem()
        article['url'] = response.url[:128]
        article['title'] = response.xpath('//h2//text()').extract_first()[:256]
        article['date'] = response.xpath('//*[contains(@class,"date")]/span[1]//text()').extract_first().strip()
        article['view'] = response.xpath('//*[contains(@id,"readTime")]//text()').extract_first()
        article['text'] = cln_text(response.xpath('string(//*[contains(@class,"content")])').extract_first())
        article['category'] = "新闻快讯"

        content = article['title'] + ' ' + article['text']
        (kw1, kw2, kw3) = get_kw(content)
        article['kw1'] = kw1
        article['kw2'] = kw2
        article['kw3'] = kw3
        article['view'] = get_view()
        
        # print(article['text'])
        yield article
