# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class RepositorySpider(scrapy.Spider):
    name = 'repository'

    @property
    def start_urls(self):
        url_tmpl = "https://github.com/shiyanlou?page={}&tab=repositories"
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repos in response.css('li.col-12'):
            item = ShiyanlougithubItem({
                "name": repos.xpath('.//a[contains(@itemprop, "name codeRepository")]/text()').re_first('[^\w]*(\w*)'),
                "update_time": repos.xpath('.//relative-time/@datetime').extract_first()
                })
            yield item
