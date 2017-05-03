import scrapy

class TestZhiPinSpider(scrapy.Spider):

    name = "TestZhiPinSpider"
    start_urls = [
        "https://www.zhipin.com/c101210100-p100203/"
    ]

    def parse(self, response):
        print(" stsParse ")
        selector = scrapy.Selector(response)
        job_list = selector.xpath("//div[@class='job-list']/ul/li/a")
        for job_content in job_list :
            x = job_content.extract()
            print(" x: "+x)
            url = job_content.xpath("./@href").extract_first()
            print(" url: "+url)

            job_city_age_adu \
                = job_content.xpath("./div[@class='job-primary']/div[@class='info-primary']/p/text()").extract()

            for job_city_age_adu_content in job_city_age_adu:
                print("job_city_age_adu_content: "+job_city_age_adu_content)
            print(" -------------------------------------------------------------- ")
