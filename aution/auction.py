import unittest
from Setting.Base import *


class Auction(unittest.TestCase, Information):

    # 获取机构信息
    @classmethod
    def setUpClass(cls):
        # 使用机构名称作为项目名称，拼接时间
        cls.cunInfo = Information().getorgInfo(cls.villageHeaders)
        cls.auditInfo = Information().getorgInfo(cls.auditHeaders)
        cls.Type = "21"  # 00 出租无资质；01出租有资质；10出让无资质；11出让有资质；12永久出让；20出售无资质；21出售有资质
        cls.enroll = 2
        cls.startDate = 5
        cls.endDate = 9
        prefix = Information().getorgInfo(cls.villageHeaders)["organizationName"][0:6]
        projectType = '勰测试'
        time = (datetime.datetime.now()).strftime('%y%m%d%H%M')
        cls.assetName = cls.projectName = prefix + time + projectType

    def test_01(self):
        """资产登记"""
        print(self.assetName)
        resource = self.saveAssetResource(self.assetName)
        print("01资产登记")
        self.assertEqual(resource["message"], '操作成功')

    def test_02(self):
        """立项申请"""
        url = "/api/admin/v1/assetProject/saveProjectApply"
        data = self.applyData(self.assetName, Type=self.Type)
        req = self.post(url, data, self.villageHeaders)
        print("02立项申请", req)
        self.assertEqual(req["message"], '操作成功')

    def test_03(self):
        """调用Base类方法立项审核"""
        req = self.audit(self.assetName, status=11)
        print("03立项审核", req)
        self.assertEqual(req["message"], '操作成功')

    # @skip_dependent("test_03")
    def test_04(self):
        """发布交易公告"""
        assetProjectId = self.getProjectInfoPage(self.assetName)
        url1 = "/api/admin/v1/sysUiaUser/getPersonalMessage"
        data1 = {"assetProjectId": assetProjectId, "type": ""}
        req1 = self.post(url1, data1, self.auditHeaders)
        # 详情
        url2 = "/api/admin/v1/assetProject/getProjectDetail"
        data2 = {"assetProjectId": assetProjectId, "type": ""}
        req2 = self.post(url2, data2, self.auditHeaders)
        # 发布交易公告
        getActivitiPage = self.getActivitiPage(projectName=self.assetName)
        taskId = getActivitiPage['taskId']
        businessKey = getActivitiPage['businessKey']
        url = "/api/admin/v1/assetInformation/saveAssetInformation"
        data = {
            "taskId": taskId,
            "businessKey": businessKey,
            "assetProjectId": assetProjectId,
            "auctionStartDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.startDate))[0:19],
            "auctionEndDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.endDate))[0:19],
            "contact": req2["data"]["assetProject"]["contact"],
            "phone": req2["data"]["assetProject"]['phone'],
            "earnestMoneyPayEndDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.enroll))[0:19],
            "enrollEndDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.enroll))[0:19],
            "extendSecond": 180,
            "maxExtend": 999,
            "resultPostPeriod": 5,
            "contractDeadlinePeriod": 10,
            "releaseUser": req1["data"]["name"],
            "sysOrganizationId": self.auditInfo["sysOrganizationId"],
            "releaseOrganizationName": self.auditInfo["organizationName"],
            "releaseDate": str(datetime.datetime.now() + datetime.timedelta(days=0))[0:19],
            "publicStartDate": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "publicEndDate": (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "informationTitle": self.assetName + "交易公告",
            "projectName": self.assetName
        }
        req = self.post(url, data, self.auditHeaders)
        print("04发布交易公告", req)
        self.assertEqual(req["message"], '操作成功')

    def test_05(self):
        """报名"""
        assetProjectId = self.getProjectInfoPage(self.assetName)
        url1 = "/api/auction/v1/assetProjectAuditMaterials/getAssetProjectAuditMaterials"
        data1 = {"assetProjectId": assetProjectId}
        req1 = self.post(url1, data1, self.userHeaders)
        # 报名-确定
        url = "/api/auction/v1/assetProjectEnroll/saveAssetProjectEnroll"
        data = {"assetProjectId": assetProjectId}
        if self.Type == "01" or self.Type == "11" or self.Type == "21":
            data["files"] = [{"assetProjectAuditMaterialsId": req1["data"][0]["assetProjectAuditMaterialsId"],
                              "fileUrl": "cqjy/000000/202211/679e7a2c-2b1f-439a-a11c-104d6134b3fb.jpg"}]
        req = self.post(url, data, self.userHeaders)
        print("05报名-确定", req)
        self.assertEqual(req["message"], '操作成功')

    def test_06(self):
        """缴纳保证金并查看"""
        req = self.getEarenstMoneyForPortal(self.assetName, 3602019309200000266)
        print("06确认保证金", req)
        self.assertEqual(req["message"], '操作成功')
        t1 = int(self.enroll * 60 + 5)
        sleep(t1)

    def test_07(self):
        """资格审核-审核"""
        if self.Type == "01" or self.Type == "11" or self.Type == "21":
            assetProjectId = self.getProjectInfoPage(self.assetName)
            assetProjectEnrollId = self.getEnrollAuditProjectDetail(assetProjectId)
            url = "/api/admin/v1/assetProjectEnroll/audit"
            data = {"assetProjectEnrollId": assetProjectEnrollId, "type": 0, "remark": "通过"}
            req = self.post(url, data, self.auditHeaders)
            print("07资格审核", req)
            self.assertEqual(req["message"], '操作成功')
        else:
            print("07自动审核")
            self.assertEqual(1, 1)
        t1 = int((self.startDate - self.enroll) * 60 + 25)
        sleep(t1)

    def test_08(self):
        """出价"""
        assetProjectId = self.getProjectInfoPage(self.assetName)
        url1 = "/api/auction/v1/auctions/open/getAuctionPageList"
        data1 = {"projectName": self.assetName, "tradeMode": "01", "current": 1, "size": 16, "isShowPushData": 1,
                 "isShowTestData": "0"}
        req1 = self.post(url1, data1, self.userHeaders)['data']['records'][0]
        url2 = "/api/auction/v1/auctions/auction"
        data2 = {"assetProjectId": assetProjectId, "assetProjectAuctionId": req1["assetProjectAuctionId"],
                 "offerAPrice": 91688}
        req2 = self.post(url2, data2, self.userHeaders)
        print("08出价", req2)
        self.assertEqual(req2["message"], '操作成功')
        # sleep(390)

    # @unittest.skipIf(1, "跳过")
    def test_09(self):
        """上传合同"""
        req = self.uploadContract(self.assetName, self.Type)
        print("09上传合同", req)
        self.assertEqual(req["message"], '操作成功')

    # @unittest.skipIf(1, "跳过")
    def test_10(self):
        """合同审核"""
        req = self.activitiInstance(self.assetName)
        print("10合同审核", req)
        self.assertEqual(req["message"], '操作成功')

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
    # suite1 = unittest.TestLoader().loadTestsFromTestCase(Auction)
    # suite = unittest.TestSuite(suite1)
    # unittest.TextTestRunner(verbosity=2).run(suite)
