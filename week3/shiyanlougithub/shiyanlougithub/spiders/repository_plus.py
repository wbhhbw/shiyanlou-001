# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class RepositoryPlusSpider(scrapy.Spider):
    name = 'repository_plus'

    @property
    def start_urls(self):
        url_tmpl = "https://github.com/shiyanlou?page={}&tab=repositories"
        return (url_tmpl.format(i) for i in range(1, 5))
        

    def parse(self, response):
        for repos in response.css('li.col-12'):
            item = ShiyanlougithubItem()
            item['name'] =  repos.xpath('.//a[contains(@itemprop, "name codeRepository")]/text()').re_first('[^\w]*(\w*)')
            item['update_time'] = repos.xpath('.//relative-time/@datetime').extract_first()
            repos_url = response.urljoin(repos.xpath('.//a[contains(@itemprop, "name codeRepository")]/@href').extract_first())
            request = scrapy.Request(url=repos_url, callback=self.parse_repos)
            request.meta['item'] = item
            yield request

    def parse_repos(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('(//span[@class="num text-emphasized"])[1]/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['branches'] = response.xpath('(//span[@class="num text-emphasized"])[2]/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['releases'] = response.xpath('(//span[@class="num text-emphasized"])[3]/text()').re_first('[^\d]*(\d*)[^\d]*')
        yield item
