import scrapy
from jobSpider.items import TestJobDetailItem
from jobSpider.items import JobDetailItem
from urllib.request import urlretrieve
import  os

class TestZhiPinSpider(scrapy.Spider):

    name = "TestZhiPinSpider"
    # start_urls = [
    #     # "https://www.zhipin.com/c101210100-p100203/"
    #     # "https://www.zhipin.com/job_detail/1411294670.html"
    #     "https://www.zhipin.com/job_detail/1411310811.html"
    # ]
    #
    # def parse(self, response):
    #     print(" stsParse ")
    #
    #     print(" status ", response.status)
    #     # print(" body ", response.body)
    #
    #     selector = scrapy.Selector(response)
    #
    #     # 列表页解析
    #     # job_list = selector.xpath("//div[@class='job-list']/ul/li/a")
    #     # for job_content in job_list :
    #     #     x = job_content.extract()
    #     #     print(" x: "+x)
    #     #     url = job_content.xpath("./@href").extract_first()
    #     #     print(" url: "+url)
    #     #
    #     #     job_city_age_adu \
    #     #         = job_content.xpath("./div[@class='job-primary']/div[@class='info-primary']/p/text()").extract()
    #     #
    #     #     for job_city_age_adu_content in job_city_age_adu:
    #     #         print("job_city_age_adu_content: "+job_city_age_adu_content)
    #     #
    #     #     print("job_city_age_adu_content: " + job_city_age_adu_content[0] )
    #     #     print(" -------------------------------------------------------------- ")
    #
    #     # 详情页
    #     # job_primary = selector.xpath("//div[@class='job-primary']")
    #     # info_primary = job_primary.xpath("./div[@class='info-primary']")
    #     # info_company = job_primary.xpath("./div[@class='info-company']")
    #     #
    #     # job_time = info_primary.xpath("./div[@class='job-author']/span/text()").extract_first()
    #     # job_type = info_primary.xpath("./div[@class='name']/text()").extract_first()
    #     # job_pay = info_primary.xpath("./div[@class='name']/span/text()").extract_first()
    #     #
    #     # job_city_age_edu = info_primary.xpath("./p/text()").extract()
    #     # job_city_age_edu_str = ""
    #     # for job_city_age_edu_content in job_city_age_edu:
    #     #     job_city_age_edu_str = job_city_age_edu_str +" "+ job_city_age_edu_content
    #     #
    #     # job_city = ""
    #     # job_age = ""
    #     # job_edu = ""
    #     # job_city_age_edu_length = len(job_city_age_edu)
    #     # if job_city_age_edu_length >= 1:
    #     #     job_city = job_city_age_edu[0]
    #     # if job_city_age_edu_length >= 2:
    #     #     job_age = job_city_age_edu[1]
    #     # if job_city_age_edu_length >= 3:
    #     #     job_edu = job_city_age_edu[2]
    #     #
    #     # job_company_info = info_company.xpath("./p/text()").extract()
    #     # job_company_info_str = ""
    #     # for job_company_info_content in job_company_info:
    #     #     job_company_info_str = job_company_info_str +" "+ job_company_info_content
    #     #
    #     # #公司规模可能为空
    #     # job_company_name = ""
    #     # job_company_type = ""
    #     # job_company_kind = ""
    #     # job_company_pn = ""
    #     # job_company_info_length = len(job_company_info)
    #     # if job_company_info_length >= 1:
    #     #     job_company_name = job_company_info[0]
    #     # if job_company_info_length >= 2:
    #     #     job_company_type = job_company_info[1]
    #     # if job_company_info_length >= 3:
    #     #     job_company_kind = job_company_info[2]
    #     # if job_company_info_length >= 4:
    #     #     job_company_kind = job_company_info[2]
    #     #     job_company_pn = job_company_info[3]
    #     #
    #     #
    #     # job_company_add = selector.xpath("//div[@class='location-address']/text()").extract_first()
    #     # job_company_long_lat = selector.xpath("//div[@id='map-container']").xpath('@data-long-lat').extract_first()
    #     # job_desc_list = selector.xpath("//div[@class='text']/text()").extract()
    #     # job_desc = ""
    #     # for job_desc_content in job_desc_list:
    #     #     job_desc = job_desc +  job_desc_content
    #     #
    #     # print("job_time:  "+job_time)
    #     # print("job_type:  " + job_type)
    #     # print("job_pay:  " + job_pay)
    #     # print("job_city:  " + job_city)
    #     # print("job_age:  " + job_age)
    #     # print("job_edu:  " + job_edu)
    #     # print("job_city_age_edu_str:  " + job_city_age_edu_str)
    #     #
    #     #
    #     #
    #     # print("job_company_name:  " + job_company_name)
    #     # print("job_company_type:  " + job_company_type)
    #     # print("job_company_kind:  " + job_company_kind)
    #     # print("job_company_pn:  " + job_company_pn)
    #     # print("job_company_info_str:  " + job_company_info_str)
    #     #
    #     # print("job_company_add:  " + job_company_add)
    #     # print("job_company_long_lat:  " + job_company_long_lat)
    #     # print("job_desc:  " + job_desc)
    #
    #     #获取响应的URL
    #     url = response.request.url
    #     print("url:  ", url)
    #
    #     # 测试 item 取键 和 取值
    #     # item = TestJobDetailItem()
    #     # item["url"] = url
    #     # print("1111111 item.keys(): ", item.keys())
    #     # print("1111111 item.keys(): ", list(item.keys()))
    #     # print("2222222 list(item.values()): ", list(item.values()))
    #     # print("2222222 item.values(): ", item.values())
    #     # print("2222222 item.items(): ", item.items())
    #     # print("2222222 list(item.items()): ", list(item.items()))
    #     # print("1111111 item.fields.keys(): ", item.fields.keys())
    #     # print("1111111 item.fields.values(): ", item.fields.values())
    #     # yield item
    #
    #     # 只赋值一个 取key/value也就只有一对
    #     item = JobDetailItem()
    #     item["job_url"] = url
    #     print("2222222 item.values(): ", item.values())
    #     print("1111111 item.keys(): ", item.keys())
    #
    #     for key, value in item.items():
    #         if item[key] is None:
    #             item[key] = ""
    #
    #     print("1111111 item.keys(): ", item.keys())
    #     print("2222222 item.values(): ", item.values())

    # 测试登录
    login_url = "https://www.zhipin.com/user/login.html?ka=header-login"
    login_post_url = "https://www.zhipin.com/login/account.json"
    host = "https://www.zhipin.com"
    def start_requests(self):
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
        print("open_host_page")
        print(" response.body ", response.body)
        selector = scrapy.Selector(response)
        someThing = selector.xpath("//div[@class='user-nav']").extract_first()
        print(" someThing ", someThing)


    #验证码图片保存路径
    def captcha_file_path(self):
        captcha_file_name = "./image/captcha.jpg"
        directory = os.path.dirname(captcha_file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return captcha_file_name