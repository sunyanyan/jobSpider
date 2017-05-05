import scrapy
from jobSpider.items import JobDetailItem


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
            yield scrapy.Request(url=url,callback=self.parse_job_detail)
        # 可以在此处解析翻页信息，从而实现爬取版区的多个页面


    #具体的招聘信息
    def parse_job_detail(self, response):
        selector = scrapy.Selector(response)

        job_url = response.request.url
        print(" 解析 job_detail  --------url:"+job_url)
        #时间 工作类别 工资 年限 公司 地址 工作要求
        # 详情页
        job_primary = selector.xpath("//div[@class='job-primary']")
        info_primary = job_primary.xpath("./div[@class='info-primary']")
        info_company = job_primary.xpath("./div[@class='info-company']")

        job_time = info_primary.xpath("./div[@class='job-author']/span/text()").extract_first()
        job_type = info_primary.xpath("./div[@class='name']/text()").extract_first()
        job_pay = info_primary.xpath("./div[@class='name']/span/text()").extract_first()

        job_city_age_edu = info_primary.xpath("./p/text()").extract()
        job_city_age_edu_str = ""
        for job_city_age_edu_content in job_city_age_edu:
            job_city_age_edu_str = job_city_age_edu_str +" "+ job_city_age_edu_content

        job_city = ""
        job_age = ""
        job_edu = ""
        job_city_age_edu_length = len(job_city_age_edu)
        if job_city_age_edu_length >= 1:
            job_city = job_city_age_edu[0]
        if job_city_age_edu_length >= 2:
            job_age = job_city_age_edu[1]
        if job_city_age_edu_length >= 3:
            job_edu = job_city_age_edu[2]

        job_company_info = info_company.xpath("./p/text()").extract()
        job_company_info_str = ""
        for job_company_info_content in job_company_info:
            job_company_info_str = job_company_info_str +" "+ job_company_info_content

        #公司规模可能为空
        job_company_name = ""
        job_company_type = ""
        job_company_kind = ""
        job_company_pn = ""
        job_company_info_length = len(job_company_info)
        if job_company_info_length >= 1:
            job_company_name = job_company_info[0]
        if job_company_info_length >= 2:
            job_company_type = job_company_info[1]
        if job_company_info_length >= 3:
            job_company_kind = job_company_info[2]
        if job_company_info_length >= 4:
            job_company_kind = job_company_info[2]
            job_company_pn = job_company_info[3]


        job_company_add = selector.xpath("//div[@class='location-address']/text()").extract_first()
        job_company_long_lat = selector.xpath("//div[@id='map-container']").xpath('@data-long-lat').extract_first()
        job_desc_list = selector.xpath("//div[@class='text']/text()").extract()
        job_desc = ""
        for job_desc_content in job_desc_list:
            job_desc = job_desc +  job_desc_content


        item = JobDetailItem()
        item["job_time"] = job_time
        item["job_type"] = job_type
        item["job_pay"] = job_pay
        item["job_city"] = job_city
        item["job_age"] = job_age
        item["job_edu"] = job_edu
        item["job_company_name"] = job_company_name
        item["job_company_type"] = job_company_type
        item["job_company_kind"] = job_company_kind
        item["job_company_pn"] = job_company_pn
        item["job_company_add"] = job_company_add
        item["job_company_long_lat"] = job_company_long_lat
        item["job_desc"] = job_desc
        item["job_company_info_str"] = job_company_info_str
        item["job_city_age_edu_str"] = job_city_age_edu_str
        item["job_url"] = job_url
        yield item

