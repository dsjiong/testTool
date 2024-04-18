from Setting.Base import *
import unittest

urllib3.disable_warnings()


# @stop_on_failure
class Smalltrade(unittest.TestCase, Information):

    @classmethod
    def setUpClass(cls):
        # 使用机构名称作为项目名称，拼接时间
        cls.cunInfo = Information().getorg_info(cls.villageHeaders)
        cls.auditInfo = Information().getorg_info(cls.auditHeaders)
        cls.get_user = Information().get_sys_user(cls.vPhone, cls.villageHeaders)
        prefix = cls.cunInfo["organizationName"][0:5]
        time = (datetime.datetime.now()).strftime('%m%d%H%M%S')
        cls.assetName = cls.projectName = prefix + time + '小额出租测试'
        cls.asset = '集体经营性建设用地'

    def test_01(self):
        """创建资产"""
        print(self.assetName)
        resource = self.save_asset_resource(self.assetName, self.asset)
        print("01资产登记")
        self.assertEqual(resource["message"], '操作成功')

    def test_02(self):
        """小额立项申请"""
        asst_info = self.get_choose_asset_list(self.assetName, self.cunInfo["sysOrganizationId"])
        url = "/api/admin/v1/smallTrade/smallApply"
        data = {
            "tradeMode": "03",
            "tradeType": "01",
            "organizationId": self.cunInfo["sysOrganizationId"],
            "organizationName": self.cunInfo["organizationName"],
            "provinceId": self.cunInfo["provinceId"],
            "province": self.cunInfo["province"],
            "cityId": self.cunInfo["cityId"],
            "city": self.cunInfo["city"],
            "areaId": self.cunInfo["areaId"],
            "area": self.cunInfo["area"],
            "streetId": self.cunInfo["streetId"],
            "street": self.cunInfo["street"],
            "address": self.cunInfo["address"],
            "contact": self.get_user['fullName'],
            "phone": self.get_user['phone'],
            "projectName": self.projectName,
            "projectType": asst_info["assetGroupCodeLevel3"],
            "projectTypeName": asst_info["assetGroupLevel3Name"],
            "remarkIndustryRequire": "行业要求",
            "remarkFireControl": "消防情况说明",
            "remarkOther": "其他重要情况说明",
            "remarkOtherClause": "合同其他条款",
            "remarkTaxation": "税费承担说明",
            "remark": "备注",
            "detailParamList": [
                {
                    "assetId": asst_info['assetId'],
                    "sysOrganizationId": self.cunInfo["sysOrganizationId"],
                    "sysOrganizationName": self.cunInfo["organizationName"],
                    "assetName": self.assetName,
                    "assetCode": asst_info["assetCode"],
                    "assetStatus": asst_info["assetStatus"],
                    "assetNature": asst_info["assetNature"],
                    "assetType": asst_info["assetType"],
                    "assetTypeName": asst_info["assetTypeName"],
                    "assetCategory": asst_info['assetCategory'],
                    "assetCategoryName": asst_info['assetCategoryName'],
                    "disposalMethod": asst_info['disposalMethod'],
                    "acquiredDate": asst_info['acquiredDate'],
                    "purpose": asst_info['purpose'],
                    "purposeExplain": asst_info["assetGroupLevel5Name"],
                    "province": self.cunInfo["province"],
                    "provinceId": self.cunInfo["provinceId"],
                    "city": self.cunInfo["city"],
                    "cityId": self.cunInfo["cityId"],
                    "area": self.cunInfo["area"],
                    "areaId": self.cunInfo["areaId"],
                    "street": self.cunInfo["street"],
                    "streetId": self.cunInfo["streetId"],
                    "assetAddress": self.cunInfo["address"],
                    "originalValue": asst_info['originalValue'],
                    "buildArea": asst_info['buildArea'],
                    "buildAreaUnit": asst_info['buildAreaUnit'],
                    "landOccupation": None,
                    "landOccupationUnit": None,
                    "mainPicture": asst_info['mainPicture'],
                    "temporaryAssets": asst_info['temporaryAssets'],
                    "contractEndDate": asst_info['contractEndDate'],
                    "assetGroupCodeLevel1": asst_info['assetGroupCodeLevel1'],
                    "assetGroupCodeLevel2": asst_info['assetGroupCodeLevel2'],
                    "assetGroupCodeLevel3": asst_info['assetGroupCodeLevel3'],
                    "assetGroupCodeLevel4": asst_info['assetGroupCodeLevel4'],
                    "assetGroupCodeLevel5": asst_info['assetGroupCodeLevel5'],
                    "assetGroupLevel1Name": asst_info['assetGroupLevel1Name'],
                    "assetGroupLevel2Name": asst_info['assetGroupLevel2Name'],
                    "assetGroupLevel3Name": asst_info['assetGroupLevel3Name'],
                    "assetGroupLevel4Name": asst_info['assetGroupLevel4Name'],
                    "assetGroupLevel5Name": asst_info['assetGroupLevel5Name'],
                    "oriUserName": asst_info['oriUserName'],
                    "oriUserType": asst_info['oriUserType'],
                    "oriIdCardType": asst_info['oriIdCardType'],
                    "oriIdCardNo": asst_info['oriIdCardNo'],
                    "oriUserPhone": asst_info['oriUserPhone'],
                    "assetGroupCode": asst_info["assetGroupCodeLevel3"],
                    "assetProjectId": None,
                }
            ],
            "priorityOriginalLessee": "false",
            "payTradeEarnestMoney": 'true',
            "tradeEarnestMoney": 1,
            "floorPrice": 4168,
            "minBidRange": None,
            "maxBidRange": None,
            "assetDeliverDay": "5",
            "progressiveIncrease": "false",  # 是否递增付款金额 0=否 1=是
            "progressiveIncreaseWay": None,  # 递增方式 1=按比例递增 2=按固定金额递增
            "progressiveIncreaseAmount": None,  # 每次递增固定金额
            "progressiveIncreaseStartMonth": None,  # 从第n个月开始递增
            "progressiveIncreaseMonth": None,  # 每n个月递增一次
            "progressiveIncreaseIncrease": None,  # 每次递增幅度为上期缴纳租金的n百分比
            "rentFree": "false",
            "rentFreePeriod": None,
            # "rentCollectMethod": 0,  # 租金收取方式 0=按月 1=按季 2=按半年 3=按年 4=一次性
            # "projectStartDate": str(datetime.datetime.now() + datetime.timedelta(days=0))[0:19],  # 租赁开始时间
            # "projectEndDate": str(datetime.datetime.now() + datetime.timedelta(days=23))[0:19],  # 租赁开始时间
            # "projectTradeYear": "23天",
            "perpetualAssignment": "false",
            "repostAssetProject": "false",
            "fileSaveParams": [
                {
                    "fileType": 1,
                    "fileUrl": "project/441802000000/202301/361d7eb0-7a85-447d-8e9c-5263d36477b8.png"
                },
                {
                    "fileType": 2,
                    "fileUrl": "project/441802000000/202301/519f3e3b-a87e-4a49-be4a-cb9d2913c21a.doc"
                }, {
                    "fileType": 2,
                    "fileUrl": "project/441702000000/202307/0cc60767-d50b-4523-b212-daa2ceff3e71.doc",
                    "fileName": "合同样本"
                }, {
                    "fileType": 7,
                    "fileUrl": "project/441702000000/202401/c54daad5-f1f4-4864-bb74-74f30ab3a4b8.png",
                    "fileName": "集体土地使用权证"
                }, {
                    "fileType": 8,
                    "fileUrl": "project/441702000000/202401/1563268a-b4ec-480e-849c-4773c5b19287.png",
                    "fileName": "宗地图"
                }, {
                    "fileType": 9,
                    "fileUrl": "project/441702000000/202401/8fc5274d-5316-4d90-8252-f4df307396ef.png",
                    "fileName": "地块规划设计条件"
                }, {
                    "fileType": 10,
                    "fileUrl": "project/441702000000/202401/e5155f39-7fe3-43bd-8c3c-a9e191d83d40.png",
                    "fileName": "建设用地规划许可证"
                }],
            "requires": "false",
            "remarkCondition": "无",
            "auditMaterialsSaveParams": [
            ],
            "enrollType": 0,
            "blacklistEnter": "true",
            "isSubmit": 1,
            "agent": "false",
            "taskId": None
        }
        apply = self.post(url, data, self.villageHeaders)
        print("02小额申请", apply)
        self.assertEqual(apply['message'], '操作成功')

    def test_03(self):
        """立项审核"""
        audit = self.audit(self.projectName, mode='03', status=11)
        print("03立项审核", audit)
        self.assertEqual(audit["message"], '操作成功')

    def test_04(self):
        """04发布交易公告"""
        project_info = self.get_activiti_page(mode='03', status=20, project_name=self.projectName)
        url = '/api/admin/v1/smallTrade/releasePost'
        data = {
            "taskId": project_info['taskId'],
            "businessKey": project_info['businessKey'],
            "assetProjectId": project_info['assetProjectId'],
            "informationTitle": self.projectName + "交易公告",
            "projectName": self.projectName,
            "publicStartDate": (datetime.date.today()).strftime('%Y-%m-%d'),
            "publicEndDate": (datetime.date.today()).strftime('%Y-%m-%d'),
            "resultPostPeriod": 5,
            "contractDeadlinePeriod": 10
        }
        repost = self.post(url, data, self.auditHeaders)
        print('04发布交易公告', repost)
        self.assertEqual(repost['message'], '操作成功')

    def test_05(self):
        """05报名"""
        req = self.sigh_up(self.assetName, "00")
        print("05报名-确定", req)
        self.assertEqual(req["message"], '操作成功')

    def test_06(self):
        """06缴纳保证金"""
        pay = self.get_earenst_money_for_portal(self.assetName, 3602019309200000266)
        print("06缴纳保证金", pay)
        self.assertEqual(pay["message"], '操作成功')
        sleep(360)

    def test_07(self):
        """07上传合同"""
        req = self.upload_contract(self.assetName, trade="20")
        print("07上传合同", req)
        self.assertEqual(req["message"], '操作成功')

    def test_08(self):
        """08合同审核"""
        req = self.activiti_instance(self.assetName)
        print("08合同审核", req)
        self.assertEqual(req["message"], '操作成功')

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
