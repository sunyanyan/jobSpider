import scrapy
from jobSpider.items import JobDetailItem
import sqlite3
import os
from urllib.request import urlretrieve

class ZhiPinTestDetailPageSpider(scrapy.Spider):

    name = "ZhiPinTestDetailPageSpider"
    host = "https://www.zhipin.com"
    login_url = "https://www.zhipin.com/user/login.html?ka=header-login"
    login_post_url = "https://www.zhipin.com/login/account.json"
    job_detail_url = "https://www.zhipin.com/job_detail/1411310811.html"

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):

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
                      "account": "手机号",
                      "password": "密码",
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

        yield scrapy.Request(url=self.job_detail_url,
                             meta={'cookiejar': response.meta['cookiejar']},
                             callback=self.parse_job_detail)

    #具体的招聘信息
    def parse_job_detail(self, response):
        selector = scrapy.Selector(response)

        job_url = response.request.url

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
        print("\njob_company_info:\n",job_company_info)
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
            job_company_pn = job_company_info[2]
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
        item["job_time"] = job_time #工作发布时间
        item["job_type"] = job_type #招聘职业
        item["job_pay"] = job_pay #薪资
        item["job_city"] = job_city #招聘城市
        item["job_age"] = job_age #工作经历要求
        item["job_edu"] = job_edu #工作学历要求
        item["job_company_name"] = job_company_name #公司名字
        item["job_company_type"] = job_company_type #公司行业
        item["job_company_kind"] = job_company_kind #融资规模
        item["job_company_pn"] = job_company_pn #公司人数
        item["job_company_add"] = job_company_add #公司地址
        item["job_company_long_lat"] = job_company_long_lat #公司地址经纬度
        item["job_desc"] = job_desc #招聘要求
        item["job_company_info_str"] = job_company_info_str # job_company_name+job_company_type+job_company_kind+job_company_pn
        item["job_city_age_edu_str"] = job_city_age_edu_str # job_city + job_age + job_edu
        item["job_url"] = job_url

        print("\n JobDetailItem :\n ", item)

        yield item

    #验证码图片保存路径
    def captcha_file_path(self):
        captcha_file_name = "./image/captcha.jpg"
        directory = os.path.dirname(captcha_file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return captcha_file_name
