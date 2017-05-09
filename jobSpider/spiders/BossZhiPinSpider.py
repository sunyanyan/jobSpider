import scrapy
from jobSpider.items import JobDetailItem
import sqlite3
import os
from urllib.request import urlretrieve

class BossZhiPinSpider(scrapy.Spider):
    name = "BossZhiPinSpider"
    host = "https://www.zhipin.com"
    login_url = "https://www.zhipin.com/user/login.html?ka=header-login"
    login_post_url = "https://www.zhipin.com/login/account.json"
    start_iOS_hangzhou_url = "https://www.zhipin.com/job_detail/?query=iOS&scity=101210100"

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        self.jobDetailItemDB = JobDetailItemDB(self)

        print("\n 登录 \n")
        yield scrapy.Request(url=self.login_url,
                             meta={'cookiejar': 1},
                             callback=self.request_captcha)


    #获取验证码
    def request_captcha(self, response):
        selector = scrapy.Selector(response)
        captcha_url = selector.xpath("//img[@class='verifyimg']").xpath("./@src").extract_first()
        randomKey = selector.xpath("//input[@class='randomkey']").xpath("./@value").extract_first()

        full_captcha_url = self.host + captcha_url
        fileName = self.captcha_file_path()
        urlretrieve(full_captcha_url, fileName)

        open_image_command = "open "+fileName
        os.system(open_image_command)

        captcha_str = input("请输入验证码:")
        return scrapy.FormRequest.from_response(
            response,
            formdata={"regionCode": "+86",
                      "account": "18868831855",
                      "password": "wk657934388",
                      "captcha": captcha_str,
                      "randomKey": randomKey},
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.after_login
        )

    def after_login(self, response):
        print("after_login")
        yield scrapy.Request(url=self.host,
                             meta={'cookiejar': response.meta['cookiejar']},
                             callback=self.open_host_page)

    def open_host_page(self, response):
        selector = scrapy.Selector(response)
        login_info = selector.xpath("//div[@class='user-nav']").extract_first()
        print("\n 登录信息 \n", login_info)

        print("\n 开始爬虫 \n")

        yield scrapy.Request(url=self.start_iOS_hangzhou_url,
                             meta={'cookiejar': response.meta['cookiejar']},
                             callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self, response):
        print("\n 开始 解析版面上的具体招聘帖子的链接\n")

        selector = scrapy.Selector(response)
        job_list = selector.xpath("//div[@class='job-list']/ul[1]/li/a")
        for job_list_content in job_list:
            url = self.host + job_list_content.xpath("@href").extract_first()
            print("\n帖子 链接是:  "+url+"\n")
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            yield scrapy.Request(url=url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_job_detail)

        # 在此处解析翻页信息，从而实现爬取版区的多个页面
        next_page_url = selector.xpath("//a[@ka='page-next']").xpath("@href").extract_first()
        next_page_class = selector.xpath("//a[@ka='page-next']").xpath("@class").extract_first()
        if next_page_class == "next":
            next_page_full_url = self.host + next_page_url
            print("\n 下一页链接为: "+next_page_full_url+"\n")
            yield scrapy.Request(url=next_page_full_url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.parse_page)
        else:
            print("\n 没有下一页了\n")



    #具体的招聘信息
    def parse_job_detail(self, response):
        selector = scrapy.Selector(response)

        job_url = response.request.url
        print("\n 当前帖子链接为  --------url:"+job_url+"\n")
        if self.jobDetailItemDB.if_contain_url(job_url):
            print("\n  该链接重复 不解析这个item \n")
            return

        print("\n 开始处理这个item \n")

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

    #验证码图片保存路径
    def captcha_file_path(self):
        captcha_file_name = "./image/captcha.jpg"
        directory = os.path.dirname(captcha_file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return captcha_file_name

#判断具体招聘页面是否爬取过
class JobDetailItemDB:
    sqlite_db_path = ''
    sqlite_ZhiPin_table = ''
    visited_detail_urls = []

    def __init__(self, spider):
        self.sqlite_db_path = spider.settings.attributes["SQLITE_FILE_PATH"].value
        self.sqlite_ZhiPin_table = spider.settings.attributes["SQLITE_ZHI_PIN_ITEM_TABLE"].value
        conn = sqlite3.connect(self.sqlite_db_path)
        cur = conn.cursor()
        selected_sql = "SELECT job_url  FROM {0}".format(self.sqlite_ZhiPin_table)
        cur.execute(selected_sql)
        self.visited_detail_urls = cur.fetchall()
        conn.close()

    def if_contain_url(self, job_url):
        if len(self.visited_detail_urls) == 0:
            return False

        for x in self.visited_detail_urls:
            url = list(x)[0]
            if url in job_url:
                return True
            if job_url in url:
                return True

        return False