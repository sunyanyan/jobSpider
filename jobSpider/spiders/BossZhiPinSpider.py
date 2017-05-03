import scrapy

class BossZhiPinSpider(scrapy.Spider):
    name = "BossZhiPinSpider"
    host = "https://www.zhipin.com"

    # 这个例子中只指定了一个页面作为爬取的起始url
    # 当然从数据库或者文件或者什么其他地方读取起始url也是可以的
    start_urls = [
        "https://www.zhipin.com/c101210100-p100203/"
    ]

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        for url in self.start_urls:
            # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
            # scrapy会自行调度，并访问该url然后把内容拿回来
            yield scrapy.Request(url=url, callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self,response):
        selector = scrapy.Selector(response)
        job_list = selector.xpath("//div[@class='job-list']/ul[1]/li/a")
        for job_list_content in job_list:
            url = self.host + job_list_content.xpath("@href").extract_first()
            print("帖子 链接是:  "+url)
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            yield scrapy.Request(url=url,callback=self.parse)
        # 可以在此处解析翻页信息，从而实现爬取版区的多个页面


    #具体的招聘信息
    def parse_topic(self,response):
        selector = scrapy.Selector(response)

        #时间 工作类别 工资 年限 公司 地址
        job_primary = selector.xpath("//div[@class='job-primary']")
        info_primary = job_primary.xpath("//div[@class='info-primary']")
        time = info_primary.xpath("//div[@class='job-author']/span[@class='time']").extract_first()

        info_primary_name = info_primary.xpath("//div[@class='name']")
        job_type = info_primary_name.xpath("//text()").extract_first()
        job_pay = info_primary_name.xpath("//span[@class='badge']").extract_first()

        info_primary_p = info_primary.xpath("//p")
        job_city = info_primary_p.xpath("//text()").extract_first()



