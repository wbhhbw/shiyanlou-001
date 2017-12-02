import scrapy

class ShiyanlouGithubSpider(scrapy.Spider):
    name = "shiyanlou_github"
    
    @property
    def start_urls(self):
        url_tmpl = "https://github.com/shiyanlou?page={}&tab=repositories"
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repos in response.css('li.col-12'):
            yield {
                "name": repos.xpath('.//a[contains(@itemprop, "name codeRepository")]/text()').re_first('[^\w]*(\w*)'),
                "update_time": repos.xpath('.//relative-time/@datetime').extract_first()
            }
        
        
