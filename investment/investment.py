from Setting.Base import *
import unittest


class MyTestCase(unittest.TestCase, Information):

    @classmethod
    def setUpClass(cls):
        cls.baseInfo = Information().get_organization_and_parent_info(cls.villageHeaders)
        projectType = '招商测试'
        time = (datetime.datetime.now()).strftime('%m%d%H%M%S')
        name = cls.baseInfo['organizationName'][0:3]
        cls.projectName = name + time + projectType
        print(cls.projectName)

    def test_01(self):
        ulr = '/api/admin/v1/investmentAttraction/saveOrUpdateInvestmentAttraction'
        data = {
            "organizationAdminPhone": self.vPhone,
            "organizationAdminName": self.baseInfo['organizationAdminName'],
            "organizationAddress": self.baseInfo['organizationAddress'],
            "organizationName": self.baseInfo['organizationName'],
            "parentOrganizationName": self.baseInfo['parentOrganizationName'],
            "parentOrganizationAdminName": self.baseInfo['organizationAdminName'],
            "parentOrganizationAdminPhone": self.baseInfo['organizationAdminPhone'],
            "projectName": self.projectName,
            "referenceValue": 9168888.888,
            "assetType": "商业店铺",
            "assetPhotos": [{"fileUrl": "project/441704000000/202403/1c9d6a95-be7d-4844-a80d-b0c362a314fb.jpg"},
                            {"fileUrl": "project/441704000000/202403/d7281711-1f28-413f-98e6-0db673ad35b3.jpg"},
                            {"fileUrl": "project/441704000000/202403/4f5af5de-7d63-4f3c-b626-932e05b88dcf.png"},
                            {"fileUrl": "project/441704000000/202403/855ae4b7-f1a2-40c9-94fd-a39b10598cea.gif"},
                            {"fileUrl": "project/441704000000/202403/aba02c01-8d07-4139-a0e3-f93fa7cedb7c.png"}],
            "content": "<h1 class=\"ql-align-center\">关于启用广东省农村产权流转交易管理服务平台的通知（潮湘农通[2023] 8号）</h1>"
                       "<h2 class=\"ql-align-center\">来源：广东省农村产权流转交易管理服务平台&nbsp;日期：2023-12-15 10:28:37"
                       "</h2><p class=\"ql-align-center\"><br></p><h3 class=\"ql-align-center\">关于启用广东省农村产权流转交易"
                       "</h3><h3 class=\"ql-align-center\">管理服务平台的通知</h3><p>&nbsp;</p><p>各镇人民政府（带农街道办事处）"
                       "：</p><p>\t\t为贯彻落实“百县千镇万村高质量发展工程”的部署要求，全面推进我区农村产权流转交易管理服务平台扩容提质，"
                       "加快农村产权流转交易全流程电子化管理，根据省农业农村厅《广东省农村产权流转交易管理服务平台接口规范（试行）》的通知"
                       "（粤农农办〔2022〕108号）文件精神，现就有关事项通知如下：</p><p>一、我局定于2023年12月20日起启用广东省农村产权流"
                       "转交易管理服务平台（网址<a href=\"https://cqjy.gdagri.gov.cn/\" rel=\"noopener noreferrer\" "
                       "target=\"_blank\" style=\"color: windowtext;\">https://cqjy.gdagri.gov.cn/）并进入试运行阶段；"
                       "2024年1月1日，广东省农村产权流转交易管理服务平台将在我区正式运行，原湘桥区农村集体资产资源管理交易平台停止使用，"
                       "各镇（带农街道）要及时对平台的相关数据资料进行保存。</a></p><p>二、开展平台试运行培训。为确保平台运行顺利，"
                       "我局定于2023年12月下旬开展平台培训工作。具体培训事项另行通知。</p><p>三、请各镇（带农街道）要站在建立全区统一要素"
                       "市场、发展壮大新型农村集体经济、实现共同富裕的高度，重视广东省农村产权流转交易平台的启用和运行工作，认真落实，"
                       "做好平台宣传工作，做到应上尽上。</p><p>&nbsp;</p><p>&nbsp;</p><p><br></p><p><span style=\"background"
                       "-color: rgb(255, 255, 255);\">附件：</span><a href=\"https://cqjy.gdagri.gov.cn/obs/file/"
                       "%E6%BD%AE%E6%B9%98%E5%86%9C%E9%80%9A[2023]8%E5%8F%B7%20%E5%85%B3%E4%BA%8E%E5%90%AF%E7%94%A8%E5%"
                       "B9%BF%E4%B8%9C%E7%9C%81%E5%86%9C%E6%9D%91%E4%BA%A7%E6%9D%83%E6%B5%81%E8%BD%AC%E4%BA%A4%E6%98%93"
                       "%E7%AE%A1%E7%90%86%E6%9C%8D%E5%8A%A1%E5%B9%B3%E5%8F%B0%E7%9A%84%E9%80%9A%E7%9F%A5.pdf\" rel="
                       "\"noopener noreferrer\" target=\"_blank\" style=\"background-color: rgb(255, 255, 255); color: "
                       "inherit;\">启用广东省农村产权流转交易管理服务通知</a></p>",
            "parentOrganizationId": self.baseInfo['parentOrganizationId'],
            "organizationId": self.baseInfo['organizationId'],
            "recruitStartTime": str(datetime.datetime.now() + datetime.timedelta(days=0))[0:19],  # 招商开始时间
            "recruitEndTime": str(datetime.datetime.now() + datetime.timedelta(days=3))[0:19],  # 招商截止时间
            "temporarySave": False
        }
        response = self.post(ulr, data, self.villageHeaders)
        self.assertEqual(response["message"], '操作成功')  # add assertion here

    def test_02(self):
        url1 = '/api/admin/v1/investmentAttraction/getInvestmentAttractionPageList'
        data1 = {"organizationName": "", "projectName": self.projectName, "current": 1, "pageSize": 10,
                 "projectStatus": 1}
        response1 = self.post(url1, data1, self.auditHeaders)['data']['records'][0]
        print(response1['investmentAttractionId'])
        url2 = '/api/admin/v1/investmentAttraction/auditInvestmentAttraction'
        data2 = {"auditOpinion": "通过", "auditStatus": 0,
                 "investmentAttractionId": response1['investmentAttractionId']}
        response2 = self.post(url2, data2, self.auditHeaders)
        self.assertEqual(response2["message"], '操作成功')  # add assertion here

    @classmethod
    def tearDownClass(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
