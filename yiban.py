# coding:utf-8
import re
import time
import traceback
import platform
import requests
import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from util import encrypt_passwd

print()
IMG_SAVE_PATH = ""  # 截图目录，空为当前目录
INFO_PATH = "data/"  # 帐号密码和谷歌浏览器驱动目录，相对绝对都OK
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=500x1300')  # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
if platform.system() == "Linux":
    chrome_driver = INFO_PATH + "chromedriver"  # 可能要赋予可执行权限才能正常运行
else:
    chrome_driver = INFO_PATH + "chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)


class YiBan:
    WFId = "d336f36226e932d152ed54cc2a1baf20"  # 疫情表单：固定表单值固定 每个大学可能不一样需要自行抓包 此处为长沙理工大学
    CSRF = "sui-bian-fang-dian-dong-xi"  # 随机值 随便填点东西
    COOKIES = {"csrf_token": CSRF}  # 固定cookie 无需更改
    HEADERS = {"Origin": "https://c.uyiban.com", "User-Agent": "yiban"}  # 固定头 无需更改

    def __init__(self, account, passwd):
        self.account = account
        self.passwd = passwd
        self.session = requests.session()

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            req = self.session.get(url, params=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        else:
            req = self.session.post(url, data=params, timeout=10, headers=self.HEADERS, cookies=cookies)
        try:
            # print(req.json())
            return req.json()
        except:
            return None

    def login(self):
        params = {
            "account": self.account,
            "ct": 2,
            "identify": 0,
            "v": "4.7.4",
            "passwd": encrypt_passwd(self.passwd)
        }
        r = self.request(url="https://mobile.yiban.cn/api/v2/passport/login", params=params)

        if r is not None and str(r["response"]) == "100":
            self.access_token = r["data"]["access_token"]
            self.name = r["data"]["user"]["name"]
            return r
        else:
            return None


    def auth(self):
        location = self.session.get("http://f.yiban.cn/iapp/index?act=iapp7463&v=%s" % self.access_token,
                                    allow_redirects=False).headers["Location"]
        verifyRequest = re.findall(r"verify_request=(.*?)&", location)[0]
        # print(verifyRequest)
        return self.request(
            "https://api.uyiban.com/base/c/auth/yiban?verifyRequest=%s&CSRF=%s" % (verifyRequest, self.CSRF),
            cookies=self.COOKIES)

    def getUncompletedList(self):
        return self.request("https://api.uyiban.com/officeTask/client/index/uncompletedList?CSRF=%s" % self.CSRF,
                            cookies=self.COOKIES)

    def getCompletedList(self):
        return self.request("https://api.uyiban.com/officeTask/client/index/completedList?CSRF=%s" % self.CSRF,
                            cookies=self.COOKIES)

    def getTaskDetail(self, taskId):
        return self.request(
            "https://api.uyiban.com/officeTask/client/index/detail?TaskId=%s&CSRF=%s" % (taskId, self.CSRF),
            cookies=self.COOKIES)

    def submit(self, data, extend):
        params = {
            "data": data,
            "extend": extend
        }
        return self.request(
            "https://api.uyiban.com/workFlow/c/my/apply/%s?CSRF=%s" % (self.WFId, self.CSRF), method="post",
            params=params,
            cookies=self.COOKIES)

    def getShareUrl(self, initiateId):
        return self.request(
            "https://api.uyiban.com/workFlow/c/work/share?InitiateId=%s&CSRF=%s" % (initiateId, self.CSRF),
            cookies=self.COOKIES)


if __name__ == '__main__':
    with open(INFO_PATH + "account.txt", encoding="utf-8") as f:
        allAccount = f.read().splitlines()
        for i, v in enumerate(allAccount):
            allAccount[i] = v.split()
    with open(INFO_PATH + "data.txt", encoding="utf-8") as f:
        allData = f.read().splitlines()

    print("++++++++++%s++++++++++" % time.strftime("%Y-%m-%d %H:%M:%S"))

    for index, account_detail in enumerate(allAccount):
        try:
            print(account_detail[0])
            yb = YiBan(account_detail[0], account_detail[1])
            if yb.login() is None:
                print("帐号或密码错误")
                continue
            result_auth = yb.auth()
            data_url = result_auth["data"].get("Data")
            if data_url is not None:  # 授权过期
                print("授权过期")
                print("访问授权网址")
                result_html = yb.session.get(url=data_url, headers=yb.HEADERS,
                                             cookies={"loginToken": yb.access_token}).text
                re_result = re.findall(r'input type="hidden" id="(.*?)" value="(.*?)"', result_html)
                print("输出待提交post data")
                print(re_result)
                post_data = {"scope": "1,2,3,"}
                for i in re_result:
                    post_data[i[0]] = i[1]
                print("进行授权确认")
                usersure_result = yb.session.post(url="https://oauth.yiban.cn/code/usersure",
                                                  data=post_data,
                                                  headers=yb.HEADERS, cookies={"loginToken": yb.access_token})
                if usersure_result.json()["code"] == "s200":
                    print("授权成功！")
                else:
                    print("授权失败！")
                    continue
                print("尝试重新二次登录")
                yb.auth()
            all_task = yb.getUncompletedList()
            if len(all_task["data"]) == 0:
                print("没有待完成的打卡任务")
            for i in all_task["data"]:
                task_detail = yb.getTaskDetail(i["TaskId"])["data"]
                if task_detail["WFId"] != yb.WFId:
                    print("表单已更新,得更新程序了")
                    exit()
                ex = {"TaskId": task_detail["Id"],
                      "title": "任务信息",
                      "content": [{"label": "任务名称", "value": task_detail["Title"]},
                                  {"label": "发布机构", "value": task_detail["PubOrgName"]},
                                  {"label": "发布人", "value": task_detail["PubPersonName"]}]}
                submit_result = yb.submit(allData[index], json.dumps(ex, ensure_ascii=False))
                if submit_result["code"] == 0:
                    share_url = yb.getShareUrl(submit_result["data"])["data"]["uri"]
                    driver.get(share_url)
                    driver.refresh()
                    time.sleep(5)
                    file_name = "%s%s.png" % (yb.name, time.strftime("%Y-%m-%d"))
                    driver.get_screenshot_as_file(IMG_SAVE_PATH + file_name)
                    print("已完成一次打卡，截图保存为：%s" % file_name, "链接为%s" % share_url)
                else:
                    print("打卡失败，遇到了一些错误！")
            print("-------------------------------------")
        except:
            traceback.print_exc()
            print("遇到了一些错误~")
    driver.quit()
