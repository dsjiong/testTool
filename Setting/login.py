import json
import os
import requests
import urllib3

# cert_file = '/path/to/certificate.pem'
urllib3.disable_warnings()
os.environ["http_proxy"] = 'http://192.168.123.177:28'
os.environ["https_proxy"] = 'http://192.168.123.177:28'


class Login:
    test_host = "https://cqjy-test.b2bwings.com"
    online_host = "https://cqjy.gdagri.gov.cn"
    uat_host = "https://cqjy-uat.b2bwings.com"
    admin = "/api/admin/v1/sysUser/open/loginByCode"
    phone = input("输入登录手机号：")
    system = input("请选择系统：\n 1、test 2、uat 3、online \n")
    if system == "1":
        host = test_host
    elif system == "2":
        host = uat_host
    else:
        host = online_host

    def post(self, url, data, header):
        # header = self.getSessionId()
        post = requests.post(url=self.host + url, headers=header, data=json.dumps(data), verify=False)
        try:
            post.raise_for_status()
            return post.json()
        except requests.exceptions.RequestException as e:
            print("请求接口失败:", e)

    def get_session(self):
        header = {"Content-Type": "application/json"}
        data = {"phone": self.phone, "code": "888888"}
        session = self.post(self.admin, data, header)
        return session["data"]["sessionid"]

    def header(self):
        # 在下面的代码行中使用断点来调试脚本。
        if self.system == "1" or "2":
            session = self.get_session()
            return {"sessionid": session, "Content-Type": "application/json", "channel": "admin"}
        else:
            session = input("请输入sessionId：")
            return {"sessionid": session, "Content-Type": "application/json", "channel": "admin"}
