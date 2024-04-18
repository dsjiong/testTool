import unittest
import time
from Setting.Base import *
from Setting.Retry import *

class testOpenConsult(unittest.TestCase, Information):

    @classmethod
    # 获取机构信息
    def setUpClass(self) -> None:
        # 使用机构名称作为项目名称，拼接时间
        self.cunInfo = Information().getorg_info(self.villageHeaders)
        self.auditInfo = Information().getorg_info(self.auditHeaders)
        self.getSysUser = Information().get_sys_user(self.vPhone, self.villageHeaders)
        self.projectName = self.assetName = Information().getorg_info(self.villageHeaders)["organizationName"][0:3] + \
                                            (datetime.datetime.now()).strftime('%y%m%d%H%M') + '协商测试'
        self.asset = '集体经营性建设用地'

    def test_01(self):
        """资产登记"""
        print(self.assetName)
        resource = self.save_asset_resource(self.assetName, self.asset)
        print("*" * 10, resource, "*" * 10)
        self.assertEqual(resource["message"], '操作成功')

    def test_02(self):
        """发布遴选公告"""
        # 利用资产名称查询资产信息
        asst_info = self.get_asset_detail(self.assetName)
        url = "/api/admin/v1/openConsult/selectApply"
        data = {
            "tradeMode": "02",
            "tradeType": "01",
            "projectStartDate": str(datetime.datetime.now() + datetime.timedelta(days=0))[0:19],  # 租赁开始时间,出售类型时间为空
            "projectEndDate": str(datetime.datetime.now() + datetime.timedelta(days=30))[0:19],  # 租赁开始时间,出售类型时间为空
            "projectTradeYear": "30天",
            "organizationId": asst_info["sysOrganizationId"],
            "organizationName": asst_info["sysOrganizationName"],
            "provinceId": asst_info["provinceId"],
            "province": asst_info["province"],
            "cityId": asst_info["cityId"],
            "city": asst_info["city"],
            "areaId": asst_info["areaId"],
            "area": asst_info["area"],
            "streetId": asst_info["streetId"],
            "street": asst_info["street"],
            "address": self.cunInfo["address"],
            "contact": self.getSysUser['fullName'],
            "phone": self.getSysUser['phone'],
            "projectName": self.assetName,
            "projectType": asst_info['assetGroupCodeLevel3'],
            "projectTypeName": asst_info['assetGroupLevel3Name'],
            "remarkIndustryRequire": "行业要求",
            "remarkFireControl": "消防情况说明",
            "remarkOther": "其他重要情况说明",
            "remarkOtherClause": "合同其他条款",
            "remarkTaxation": "税费承担说明",
            "remark": "备注",
            "detailParamList": [{
                "assetId": asst_info['assetId'],
                "sysOrganizationId": asst_info["sysOrganizationId"],
                "sysOrganizationName": asst_info["sysOrganizationName"],
                "assetName": self.assetName,
                "assetCode": asst_info['assetCode'],
                "assetStatus": asst_info['assetStatus'],
                "assetNature": asst_info['assetNature'],
                "assetType": "01",
                "assetTypeName": "资源类",
                "assetCategory": asst_info['assetCategory'],
                "assetCategoryName": asst_info['assetCategoryName'],
                "disposalMethod": asst_info['disposalMethod'],
                "acquiredDate": None,
                "purpose": asst_info['purpose'],
                "purposeExplain": asst_info["purposeExplain"],
                "province": asst_info["province"],
                "provinceId": asst_info["provinceId"],
                "city": asst_info["city"],
                "cityId": asst_info["cityId"],
                "area": asst_info["area"],
                "areaId": asst_info["areaId"],
                "street": asst_info["street"],
                "streetId": asst_info["streetId"],
                "assetAddress": asst_info["address"],
                "originalValue": None,
                "buildArea": None,
                "buildAreaUnit": None,
                "landOccupation": asst_info['landOccupation'],
                "landOccupationUnit": asst_info['landOccupationUnit'],
                "mainPicture": "asset/440112000000/202306/86c1c80f-3f8a-4849-9330-3a6d18c42ad2.jpg",
                "temporaryAssets": 1,
                "contractEndDate": str(datetime.datetime.now() + datetime.timedelta(days=30))[0:19],
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
                "oriUserName": None,
                "oriUserType": None,
                "oriIdCardType": None,
                "oriIdCardNo": None,
                "oriUserPhone": None,
                "images": ["asset/441702000000/202401/b8d0a04b-0657-47ed-abf7-db4ef5fe948e.jpg"],
                "perfect": "true",
                "assetWorth": 500000,
                "assetGroupCode": asst_info['assetGroupCodeLevel3'],
                "assetProjectId": None
            }],
            "fileSaveParams": [{
                "fileType": 1,
                "fileUrl": "project/441702000000/202307/38625b13-5963-48d2-a6ef-ef1144dcf3e1.png",
                "fileName": "民主表决书"
            }, {
                "fileType": 2,
                "fileUrl": "project/441702000000/202307/0cc60767-d50b-4523-b212-daa2ceff3e71.doc",
                "fileName": "合同样本"
            }, {
                "fileType": 7,
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
            "requires": False,
            "remarkCondition": "无",
            "auditMaterialsSaveParams": [],
            "enrollType": 0,  # 允许报名用户类型
            "blacklistEnter": "false",  # 是否禁止警示名单报名 0=否 1=是
            "payTradeEarnestMoney": "true",
            "tradeEarnestMoney": 1,
            "floorPrice": 5168,
            "assetDeliverDay": 5,
            "progressiveIncrease": "",  # 是否递增付款金额 0=否 1=是
            "progressiveIncreaseWay": "",  # 递增方式 1=按比例递增 2=按固定金额递增
            "progressiveIncreaseAmount": '',  # 每次递增固定金额
            "progressiveIncreaseStartMonth": '',  # 从第n个月开始递增
            "progressiveIncreaseMonth": '',  # 每n个月递增一次
            "progressiveIncreaseIncrease": None,  # 每次递增幅度为上期缴纳租金的n百分比
            "rentFree": "false",  # 是否有免租期
            "rentFreePeriod": None,  # 免租天数
            "rentCollectMethod": 0,  # 租金收取方式 0=按月 1=按季 3=按年 4=一次性
            "perpetualAssignment": "false",  # 是否永久出让 0=否 1=是
            "volumeRate": 5,  # 地上容积率
            "volumeRateAcreage": 6,  # 总计算容积率建筑面积（平方米）
            "buildingDensity": 7,  # 建筑密度（%）
            "buildingLimitHeight": 8,  # 建筑限高（米）
            "investmentIntensity": 9,  # 总投资强度（万元/亩）
            "contractExpirationDate": 1,  # 合同截止天数
            "isSubmit": 1,
            "taskId": None,
            "agent": "false",  # 是否代办
            "applyType": 1
        }
        req = self.post(url, data, self.villageHeaders)
        print("02发布遴选公告", req)
        self.assertEqual(req["message"], '操作成功')

    def test_03(self):
        """遴选审核"""
        req = self.audit(self.projectName, mode='02', status=101)
        print("03遴选审核", req)
        self.assertEqual(req["message"], '操作成功')

    @Retry(max_n=2)
    def test_04(self):
        """意向人申请"""
        projectId = self.get_project_info_page(self.projectName)
        url = '/api/auction/v1/assetProjectEnroll/saveAssetProjectEnroll'
        data = {"assetProjectId": projectId, "files": []}
        req = self.post(url, data, self.user_headers_3)
        print("04意向人申请", req)
        sleep(20)
        self.assertEqual(req["message"], '操作成功')

    def test_05(self):
        """转立项"""
        # 获取projectId
        projectId = self.get_project_info_page(self.projectName)
        # 获取项目assetProjectEnrollId
        # url1 = '/api/admin/v1/assetProject/getProjectDetail'
        # data1 = {"assetProjectId": projectId, "type": ""}
        # req1 = self.post(url1, data1, self.villageHeaders)
        # # 转立项申请
        # url2 = '/api/admin/v1/openConsult/auditSelectEnroll'
        # data2 = {"assetProjectId": projectId,
        #          "assetProjectEnrollId": req1["data"]["enrollInfo"][0]["assetProjectEnrollId"], "type": 0,
        #          "remark": None}
        # req2 = self.post(url2, data2, self.villageHeaders)
        # 获取遴选申请详情
        url3 = '/api/admin/v1/assetProject/getProjectDetail'
        data3 = {"assetProjectId": projectId, "type": ""}
        detail = self.post(url3, data3, self.villageHeaders)['data']
        # 获取assetProjectSchemeConsultId
        url4 = '/api/admin/v1/assetProject/getProjectApply'
        data4 = {"assetProjectId": projectId, "type": ""}
        apply = self.post(url4, data4, self.villageHeaders)['data']
        # 遴选转申请
        url = '/api/admin/v1/openConsult/selectApply'
        data = {
            "assetProjectOtherId": detail['projectOther']['assetProjectOtherId'],
            "assetProjectId": projectId,
            "remarkCondition": "无",
            "remarkIndustryRequire": "行业要求",
            "remarkFireControl": "消防说明",
            "remarkOther": None,
            "remarkOtherClause": None,
            "remarkTaxation": None,
            "remark": None,
            "gmtCreate": detail['projectOther']['gmtCreate'],
            "gmtModified": detail['projectOther']['gmtModified'],
            "createUserId": detail['projectOther']['createUserId'],
            "modifiedUserId": None,
            "organizationName": self.cunInfo['organizationName'],
            "organizationId": self.cunInfo['sysOrganizationId'],
            "projectName": self.projectName,
            "htmlContent": None,
            "projectAmount": detail['assetProject']['projectAmount'],
            "projectAmountUnit": detail['assetProject']['projectAmountUnit'],
            "projectType": detail['assetProject']['projectType'],
            "projectNo": detail['assetProject']['projectNo'],
            "originalProjectNo": None,
            "tradeNo": detail['assetProject']['tradeNo'],
            "businessKey": detail['assetProject']['businessKey'],
            "tradeType": detail['assetProject']['tradeType'],
            "tradeMode": detail['assetProject']['tradeMode'],
            "projectStatus": detail['assetProject']['projectStatus'],
            "initiateDate": detail['assetProject']['initiateDate'],
            "passDate": detail['assetProject']['passDate'],
            "auctionStartDate": None,
            "auctionEndDate": None,
            "publicStartDate": None,
            "publicEndDate": None,
            "enrollStartDate": None,
            "enrollEndDate": None,
            "contractUploadDate": None,
            "contractDeadlineDate": None,
            "examineDeadlineDate": None,
            "provinceId": apply["details"]["provinceId"],
            "province": apply["details"]["province"],
            "cityId": apply["details"]["cityId"],
            "city": apply["details"]["city"],
            "areaId": apply["details"]["areaId"],
            "area": apply["details"]["area"],
            "streetId": apply["details"]["streetId"],
            "street": apply["details"]["street"],
            "address": self.cunInfo["address"],
            "contact": self.getSysUser['fullName'],
            "phone": self.getSysUser['phone'],
            "auctionUserName": apply['project']['auctionUserName'],
            "auctionUserId": None,
            "contactPhone": None,
            "auctionPrice": None,
            "legalIdCard": None,
            "auctionDate": None,
            "rentCollectMethod": 0,  # 租金收取方式 0=按月 1=按季 2=按半年 3=按年 4=一次性
            "projectStartDate": detail['assetProject']['projectStartDate'],
            "projectEndDate": detail['assetProject']['projectEndDate'],
            "projectTradeYear": detail['assetProject']['projectTradeYear'],
            "createUserName": detail['assetProject']['createUserName'],
            "requires": False,
            "projectCloseType": None,
            "initOrganizationId": detail['assetProject']['initOrganizationId'],
            "initOrganizationName": detail['assetProject']['initOrganizationName'],
            "initUserId": detail['assetProject']['initUserId'],
            "initUserName": detail['assetProject']['initUserName'],
            "complaintCall": detail['assetProject']['complaintCall'],
            "complaintEmail": "",
            "mainPicture": detail['assetProject']['mainPicture'],
            "appKey": None,
            "detailUrl": None,
            "detailUrlType": None,
            "assetType": None,
            "assetTypeName": None,
            "assetCategory": None,
            "assetCategoryName": None,
            "tradeReleaseDate": None,
            "checkCode": detail['assetProject']['checkCode'],
            "showTestData": detail['assetProject']['showTestData'],
            "contactIdx": detail['assetProject']['contactIdx'],
            "phoneIdx": detail['assetProject']['phoneIdx'],
            "contactPhoneIdx": None,
            "legalIdCardIdx": None,
            "tradeOrganizationId": detail['assetProject']['tradeOrganizationId'],
            "tradeOrganizationName": detail['assetProject']['tradeOrganizationName'],
            "tradeOrganizationAddress": detail['assetProject']['tradeOrganizationAddress'],
            "tradeOrganizationUserName": detail['assetProject']['tradeOrganizationUserName'],
            "tradeOrganizationUserPhone": detail['assetProject']['tradeOrganizationUserPhone'],
            "tradeCode": detail['assetProject']['tradeCode'],
            "provinceCode": detail['assetProject']["provinceCode"],
            "cityCode": detail['assetProject']["cityCode"],
            "areaCode": detail['assetProject']["areaCode"],
            "streetCode": detail['assetProject']["streetCode"],
            "assetProjectCloud": False,
            "sevenDayStatus": 0,
            "isOrganizationActTimerConfig": detail['assetProject']['isOrganizationActTimerConfig'],
            "assetInformationId": None,
            "projectStatusText": None,
            "applicantsCount": 0,
            "perpetualAssignment": False,
            "projectTypeName": detail['assetProject']['projectTypeName'],
            "assetGroupCode": detail['assetProject']['assetGroupCode'],
            "assetGroupName": detail['assetProject']['assetGroupName'],
            "flowAssetProjectId": None,
            "contractExpirationDate": 1
            ,
            "assetProjectSchemeConsultId": apply["scheme"]["assetProjectSchemeConsultId"],
            "assetContact": detail['assetProject']['assetContact'],
            "assetPhone": detail['assetProject']['assetPhone'],
            "modifiedUserName": None,
            "predictDeliveryTime": None,
            "projectRepeatType": None,
            "listAmount": detail['assetProject']['projectAmount'],
            "blacklistEnter": True,
            "enrollType": 0,
            "payTradeEarnestMoney": True,
            "tradeEarnestMoney": detail['projectScheme']['tradeEarnestMoney'],
            "floorPrice": detail['projectScheme']['floorPrice'],
            "floorPriceUnit": detail['projectScheme']['floorPriceUnit'],
            "assetDeliverDay": detail['projectScheme']['assetDeliverDay'],
            "progressiveIncrease": detail['projectScheme']['progressiveIncrease'],
            "progressiveIncreaseWay": detail['projectScheme']['progressiveIncreaseWay'],
            "progressiveIncreaseStartMonth": detail['projectScheme']['progressiveIncreaseStartMonth'],
            "progressiveIncreaseMonth": detail['projectScheme']['progressiveIncreaseMonth'],
            "progressiveIncreaseIncrease": detail['projectScheme']['progressiveIncreaseIncrease'],
            "progressiveIncreaseAmount": detail['projectScheme']['progressiveIncreaseAmount'],
            "rentFree": detail['projectScheme']['rentFree'],
            "rentFreePeriod": detail['projectScheme']['rentFreePeriod'],
            "volumeRate": 5,
            "volumeRateAcreage": 6,
            "buildingDensity": 7,
            "buildingLimitHeight": 8,
            "investmentIntensity": 9,
            "detailParamList": [{
                "assetProjectDetailId": apply['details']['assetProjectDetailId'],
                "assetProjectId": projectId,
                "sysOrganizationId": self.cunInfo['sysOrganizationId'],
                "sysOrganizationName": self.cunInfo['organizationName'],
                "assetId": detail['assetDetails'][0]['assetId'],
                "assetType": None,
                "assetTypeName": None,
                "assetCategory": None,
                "assetCategoryName": None,
                "assetNature": None,
                "assetCode": detail['assetDetails'][0]['assetCode'],
                "assetName": detail['assetDetails'][0]['assetName'],
                "purpose": None,
                "purposeExplain": detail['assetDetails'][0]['purposeExplain'],
                "originalValue": detail['assetDetails'][0]['originalValue'],
                "buildArea": detail['assetDetails'][0]['buildArea'],
                "buildAreaUnit": detail['assetDetails'][0]['buildAreaUnit'],
                "landOccupation": detail['assetDetails'][0]['landOccupation'],
                "landOccupationUnit": detail['assetDetails'][0]['landOccupationUnit'],
                "threeCapitalsOwnershipNo": None,
                "sharedArea": None,
                "sharedAreaUnit": None,
                "unitNo": None,
                "provinceId": apply["details"]["provinceId"],
                "province": apply["details"]["province"],
                "cityId": apply["details"]["cityId"],
                "city": apply["details"]["city"],
                "areaId": apply["details"]["areaId"],
                "area": apply["details"]["area"],
                "streetId": apply["details"]["streetId"],
                "street": apply["details"]["street"],
                "assetAddress": apply["details"]["assetAddress"],
                "gmtCreate": apply["details"]["gmtCreate"],
                "createUserId": apply["details"]["createUserId"],
                "gmtModified": apply["details"]["gmtModified"],
                "modifiedUserId": None,
                "videoUrl": None,
                "videoThumbnailUrl": None,
                "provinceCode": apply["details"]["provinceCode"],
                "cityCode": apply["details"]["cityCode"],
                "areaCode": apply["details"]["areaCode"],
                "streetCode": apply["details"]["streetCode"],
                "mainPicture": apply["details"]["mainPicture"],
                "images": apply["details"]["images"],
                "assetGroupCode": detail['assetDetails'][0]['assetGroupCode'],
                "assetGroupLevel1Name": apply["details"]["assetGroupLevel1Name"],
                "assetGroupLevel2Name": apply["details"]["assetGroupLevel2Name"],
                "assetGroupLevel3Name": apply["details"]["assetGroupLevel3Name"],
                "assetGroupLevel4Name": apply["details"]["assetGroupLevel4Name"],
                "assetGroupLevel5Name": apply["details"]["assetGroupLevel5Name"],
                "contractEndDate": apply["details"]["contractEndDate"],
                "temporaryAssets": apply["details"]["temporaryAssets"]
            }],
            "fileSaveParams": [{
                "fileType": 1,
                "fileUrl": "project/441702000000/202307/38625b13-5963-48d2-a6ef-ef1144dcf3e1.png",
                "fileName": "民主表决书"
            }, {
                "fileType": 2,
                "fileUrl": "project/441702000000/202307/0cc60767-d50b-4523-b212-daa2ceff3e71.doc",
                "fileName": "合同样本"
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
            "auditMaterialsSaveParams": [],
            "confirmedPrice": detail['projectScheme']['floorPrice'],
            "isSubmit": 1,
            "taskId": None,
            "agent": "false",
            "applyType": 2
        }
        req = self.post(url, data, self.villageHeaders)
        print('05指定意向人并转立项申请', req)
        self.assertEqual(req["message"], '操作成功')

    def test_07(self):
        # 立项审核
        req = self.audit(self.projectName, mode='02', status=11)
        self.assertEqual(req["message"], '操作成功')
        print('07立项审核', req)

    def test_08(self):
        # 意向人同意
        project = self.get_project_management_list(self.projectName)
        url = '/api/auction/v1/openConsult/intentConfirm'
        data = {"assetProjectId": project['assetProjectId'],
                "businessKey": project['businessKey'], "status": 1, "annotation": ""}
        req = self.post(url, data, self.user_headers_3)
        print('08意向人同意', req)
        self.assertEqual(req["message"], '操作成功')

    def test_09(self):
        # 缴纳保证金并查询
        req = self.get_earenst_money_for_portal(self.projectName, 2)
        print('09查询保证金', req)
        self.assertEqual(req["message"], '操作成功')
        time.sleep(310)

    def test_10(self):
        # 上传合同
        req = self.upload_contract(self.projectName)
        print("10上传合同", req)
        self.assertEqual(req["message"], '操作成功')

    def test_11(self):
        # 合同审核
        req = self.activiti_instance(self.projectName)
        print("11合同审核", req)
        self.assertEqual(req["message"], '操作成功')

    def test_12(self):
        # 查询成交公告
        req = self.search_notice(self.assetName)
        print("12查询成交公告", req)
        self.assertEqual(req["data"]["records"][0]["projectName"], self.projectName)

    @classmethod
    def tearDownClass(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
