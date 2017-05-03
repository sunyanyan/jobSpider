import  scrapy

class LagouSpider(scrapy.Spider):
    name = "LagouSpider"

    start_urls = [
        "https://www.lagou.com/jobs/list_iOS"
    ]

    def parse(self, response):
        print("stsParse")
        print(response.body)