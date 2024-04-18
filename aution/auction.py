import unittest
from Setting.Base import *


class Auction(unittest.TestCase, Information):

    # 获取机构信息
    @classmethod
    def setUpClass(cls):
        # 使用机构名称作为项目名称，拼接时间
        cls.cunInfo = Information().getorg_info(cls.villageHeaders)
        cls.auditInfo = Information().getorg_info(cls.auditHeaders)
        cls.get_sys_user = Information().get_sys_user(cls.vPhone, cls.villageHeaders)
        cls.project_type = "12"  # 00 出租无资质；01出租有资质；10出让无资质；11出让有资质；12永久出让；20出售无资质；21出售有资质
        cls.enroll = 3
        cls.startDate = 5
        cls.endDate = 9
        prefix = Information().getorg_info(cls.villageHeaders)["organizationName"][0:6]
        time = (datetime.datetime.now()).strftime('%y%m%d%H%M')
        cls.assetName = cls.projectName = prefix + time + '竞价测试'
        cls.asset = "耕地"

    def test_01(self):
        """资产登记"""
        print(self.assetName)
        resource = self.save_asset_resource(self.assetName, self.asset)
        print("01资产登记")
        self.assertEqual(resource["message"], '操作成功')

    def test_02(self):
        """立项申请"""
        # asst_info = self.get_asset_detail(self.assetName)
        url = "/api/admin/v1/assetProject/saveProjectApply"
        data = self.apply_data(self.assetName, self.project_type)
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
        asset_project_id = self.get_project_info_page(self.assetName)
        url1 = "/api/admin/v1/sysUiaUser/getPersonalMessage"
        data1 = {"assetProjectId": asset_project_id, "type": ""}
        req1 = self.post(url1, data1, self.auditHeaders)
        # 详情
        url2 = "/api/admin/v1/assetProject/getProjectDetail"
        data2 = {"assetProjectId": asset_project_id, "type": ""}
        req2 = self.post(url2, data2, self.auditHeaders)
        # 发布交易公告
        get_activiti_page = self.get_activiti_page(project_name=self.assetName)
        task_id = get_activiti_page['taskId']
        business_key = get_activiti_page['businessKey']
        url = "/api/admin/v1/assetInformation/saveAssetInformation"
        data = {
            "taskId": task_id,
            "businessKey": business_key,
            "assetProjectId": asset_project_id,
            "auctionStartDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.startDate))[0:19],
            "auctionEndDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.endDate))[0:19],
            "contact": req2["data"]["assetProject"]["contact"],
            "phone": req2["data"]["assetProject"]['phone'],
            "earnestMoneyPayEndDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.enroll))[0:19],
            "enrollEndDate": str(datetime.datetime.now() + datetime.timedelta(minutes=self.enroll))[0:19],
            "extendSecond": 180,
            "maxExtend": 999,
            "resultPostPeriod": 5,
            "contractDeadlinePeriod": 4,
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
        req = self.sigh_up(self.assetName, self.project_type)
        print("05报名-确定", req)
        self.assertEqual(req["message"], '操作成功')

    def test_06(self):
        """缴纳保证金并查看"""
        req = self.get_earenst_money_for_portal(self.assetName, 3)
        print("06确认保证金", req)
        self.assertEqual(req["message"], '操作成功')
        t1 = int(self.enroll * 60 + 5)
        sleep(t1)

    def test_07(self):
        """资格审核-审核"""
        if self.project_type == "01" or self.project_type == "11" or self.project_type == "21":
            for _ in range(3):
                asset_project_id = self.get_project_info_page(self.assetName)
                asset_project_enroll_id = self.get_enroll_audit_detail(asset_project_id)[0]["assetProjectEnrollId"]
                url = "/api/admin/v1/assetProjectEnroll/audit"
                data = {"assetProjectEnrollId": asset_project_enroll_id, "type": 0, "remark": "通过"}
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
        asset_project_id = self.get_project_info_page(self.assetName)
        user_header = [self.user_headers_1, self.user_headers_2, self.user_headers_3]
        url1 = "/api/auction/v2/auctions/open/getAuctionPageList"
        data1 = {"projectName": self.assetName, "tradeMode": "01", "current": 1, "size": 16, "isShowPushData": 1,
                 "isShowTestData": "0"}
        req1 = self.post(url1, data1, self.user_headers_1)['data']['records'][0]
        url2 = "/api/auction/v2/auctions/auction"
        min_bid_rang = 0
        for n in user_header:
            price = float(req1["floorPrice"]) + min_bid_rang
            data2 = {"assetProjectId": asset_project_id, "assetProjectAuctionId": req1["assetProjectAuctionId"],
                     "offerAPrice": price}
            req2 = self.post(url2, data2, n)
            min_bid_rang += 1000
            sleep(2)
        print("08出价", req2)
        self.assertEqual(req2["message"], '操作成功')
        sleep(390)

    # @unittest.skipIf(1, "跳过")
    def test_09(self):
        """上传合同"""
        req = self.upload_contract(self.assetName, self.project_type)
        print("09上传合同", req)
        return self.assertEqual(req["message"], '操作成功')

    @unittest.skipIf(test_09 is None, "跳过")
    def test_10(self):
        """合同审核"""
        req = self.activiti_instance(self.assetName)
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
