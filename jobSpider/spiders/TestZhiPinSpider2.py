import scrapy
from jobSpider.items import JobDetailItem


class TestZhiPinSpider2(scrapy.Spider):
    name = "TestZhiPinSpider2"
    host = "https://www.zhipin.com"

    # 这个例子中只指定了一个页面作为爬取的起始url
    # 当然从数据库或者文件或者什么其他地方读取起始url也是可以的
    start_urls = [
        "https://www.zhipin.com/job_detail/?query=iOS&scity=101210100"
    ]

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        print(" 开始解析url ----------------------------------------------------------------------------------------")
        for url in self.start_urls:
            # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
            # scrapy会自行调度，并访问该url然后把内容拿回来
            yield scrapy.Request(url=url, callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self, response):
        print("解析  parse_page ----------------------------------------------------------------------------------------")

        selector = scrapy.Selector(response)
        job_list = selector.xpath("//div[@class='job-list']/ul[1]/li/a")
        for job_list_content in job_list:
            url = self.host + job_list_content.xpath("@href").extract_first()
            print("帖子 链接是:  "+url)
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            #yield scrapy.Request(url=url, callback=self.parse_job_detail)
        # 可以在此处解析翻页信息，从而实现爬取版区的多个页面

        next_page_url = selector.xpath("//a[@ka='page-next']").xpath("@href").extract_first()
        next_page_class = selector.xpath("//a[@ka='page-next']").xpath("@class").extract_first()

        print("next_page_url:",next_page_url)
        print("next_page_class:", next_page_class)

        if next_page_class == "next":
            next_page_full_url = self.host + next_page_url
            yield scrapy.Request(url=next_page_full_url, callback=self.parse_page)
        else:
            print("没有下一页了----------------------------------------------------------------------------")

    #具体的招聘信息
    def parse_job_detail(self, response):
        selector = scrapy.Selector(response)

        job_url = response.request.url
        print(" 解析 job_detail  --------url:"+job_url)

