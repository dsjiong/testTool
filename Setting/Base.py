import pymysql
import datetime
from time import sleep
from Setting.Publics import *
from select_asset.select_asset import *

urllib3.disable_warnings()


class Information(Public, AssetInfo):
    header = Public().get_header()
    villageHeaders = header[0]
    auditHeaders = header[1]
    user_headers_1 = header[2]
    user_headers_2 = header[3]
    user_headers_3 = header[4]

    # 数据库
    def connect(self, database):
        mysql = pymysql.connect(host='39.108.128.154',
                                port=3307,
                                user='b2bwings',
                                password='b2bwings666!',
                                database=database)
        # print('连接成功', mysql)
        return mysql

    # 根据手机号获取账号成员信息
    def get_sys_user(self, phone, header):
        url = "/api/admin/v1/sysUser/getSysUser"
        data = {"phone": phone, "current": 1, "size": 10}
        req = self.post(url, data, header)
        return req["data"]['records'][0]

    # 获取组织机构信息
    def getorg_info(self, header):
        url = "/api/admin/v1/sysOrganization/getOrganizationRegion"
        req = self.post(url, {}, header)
        # print(req)
        return req["data"]

    def get_organization_and_parent_info(self, header):
        sys_organization_id = self.getorg_info(header)['sysOrganizationId']
        url = '/api/admin/v1/investmentAttraction/getOrganizationAndParentInfo'
        data = {"organizationId": sys_organization_id, "executiveLevel": 4}
        req = self.post(url, data, header)
        return req['data']

    # 资产分类groupId
    def get_by_parent_id(self, parent_id):
        url = '/api/admin/v1/assetGroup/getByParentId'
        data = {"parentId": parent_id}
        response = self.post(url, data, self.villageHeaders)['data']

        return response

    # IT信息管理项目查询
    def get_project_info_page(self, project_name):
        url = "/api/admin/v1/assetProject/getProjectInfoPage"
        data = {"projectName": project_name, "current": 1, "size": 10}
        req = self.post(url, data, self.auditHeaders)
        # print(req)
        return req["data"]["records"][0]["assetProjectId"]

    # 项目详情跟踪
    def get_project_management_list(self, project_name):
        url = "/api/admin/v1/assetProject/getProjectManagementList"
        data = {"projectName": project_name, "current": 1, "size": 10, "actNode": 2}
        req = self.post(url, data, self.auditHeaders)
        # print(req)
        return req["data"]["records"][0]

    # 资产登记
    def save_asset_resource(self, asset_name, asset):
        """资源性资产&非+经营性资产"""
        # n默认1，使用资源性资产
        asset_info = self.find_hierarchy_by_name(asset)
        if len(asset_info) < 4:
            asset_info.insert(3, {'name': None, 'code': None})
            asset_info.insert(4, {'name': None, 'code': None})
        elif len(asset_info) < 5:
            asset_info.insert(4, {'name': None, 'code': None})
        getorg_info = self.getorg_info(self.villageHeaders)
        resource_url = "/api/admin/v1/assetInfoResource/saveAssetResource"
        fix_url = "/api/admin/v1/assetInfoFixed/saveAssetFixed"
        data = {
            "assetCode": None,
            "sysOrganizationName": None,
            "assetName": asset_name,
            "assetSelfCode": asset_name,
            "remark": None,
            "assetWorth": "59990",
            "newAssetStatusStr": None,
            "newAssetStatus": "1",  # 新增资产状态
            "threeCapitalsOwnershipNo": None,
            "provinceId": getorg_info["provinceId"],
            "province": getorg_info["province"],
            "cityId": getorg_info["cityId"],
            "city": getorg_info["city"],
            "areaId": getorg_info["areaId"],
            "area": getorg_info["area"],
            "streetId": getorg_info["streetId"],
            "street": getorg_info["street"],
            "address": "科华街251号",
            "purpose": None,
            "purposeExplain": asset,
            "videoUrl": None,
            "videoThumbnailUrl": None,
            "images": [
                "asset/440112000000/202306/86c1c80f-3f8a-4849-9330-3a6d18c42ad2.jpg",
                "asset/440112000000/202306/3682bf2c-1211-4b46-a386-2a35fdbc4dc8.png",
                "asset/441702000000/202307/c0a09fc8-d223-4071-ae89-b7a4f3c07ec3.jpg"
            ],
            "developmentType": None,
            "developmentReason": None,
            "disposalMethod": None,  # 资产处置方式
            "assetGroupCodeLevel1": asset_info[0]["code"],  # "Z000000",
            "assetGroupLevel1Name": asset_info[0]["name"],  # "资源性资产",
            "assetGroupCodeLevel2": asset_info[1]["code"],  # "Z020000",
            "assetGroupLevel2Name": asset_info[1]["name"],  # "建设用地",
            "assetGroupCodeLevel3": asset_info[2]["code"],  # "Z020600",
            "assetGroupLevel3Name": asset_info[2]["name"],  # "集体经营性建设用地",
            "assetGroupCodeLevel4": asset_info[3]["code"],
            "assetGroupLevel4Name": asset_info[3]["name"],
            "assetGroupCodeLevel5": asset_info[4]["code"],
            "assetGroupLevel5Name": asset_info[4]["name"],
            "sysOrganizationId": getorg_info["sysOrganizationId"],
        }
        # print(asset_info[2]["code"][0:5])
        if asset_info[0]["code"][0] == "Z":
            url = resource_url
            # data["unitNo"] = None  # 单元号
            # data["cadastreNo"] = None  # 地籍号
            # data["landNo"] = None  # 宗地系列号
            # data["adjunctiveResourceNo"] = None  # 附属资源号
            # data["attribute"] = None  # 所有属性
            data["landUsufructNo"] = asset_info[0]["code"]  # 土地使用权证号
            # data["landUser"] = None  # 土地使用权人
            # data["landOwner"] = None  # 土地所有权人
            # data["startDate"] = None  # 启用日期
            # data["selfUse"] = None  # 是否自用
            # data["coordinate"] = None  # 坐标信息
            data["landOwnershipNo"] = asset_name  # 土地所有权证号
            data["landBoundaryPoint"] = "上到上，下到下，左到左，右到右"  # 土地界址
            data["landOccupation"] = 15
            data["landOccupationUnit"] = 3
        elif asset_info[2]["code"][0:5] == "J0202" or asset_info[2]["code"][0:5] == "F0202":
            url = fix_url
            data["otherParam"] = {
                "brand": "品牌",
                "gear": None,
                "impetusType": "动力类型",
                "size": "外形尺寸",
                "type": "类型",
                "model": "型号",
                "tyre": None,
                "wheelbase": None,
                "powerWaste": None,
                "weight": None
            }
        else:
            url = fix_url
            data["buildArea"] = 100
            data["buildAreaUnit"] = 1
            data["sharedArea"] = None
            data["sharedAreaUnit"] = 1
            data["acquiredDate"] = str(datetime.datetime.now() + datetime.timedelta(days=-365))[0:19]
        req = self.post(url, data, self.villageHeaders)
        # print("创建资产", req)
        return req

    def get_asset_detail(self, asset_name):
        pageulr = '/api/admin/v1/asset/getAssetPageList'
        pagedata = {"assetName": asset_name, "current": 1, "size": 10}
        page = self.post(pageulr, pagedata, self.villageHeaders)['data']['records'][0]
        detail_url = '/api/admin/v1/assetInfoResource/getAssetResourceById'
        detail_data = {"assetId": page['assetId']}
        detail = self.post(detail_url, detail_data, self.villageHeaders)['data']
        return detail

    def apply_data(self, asset_name, project_type="00"):
        """立项申请data参数调用函数，默认Type=00,出租无资质要求"""
        cun_info = self.getorg_info(self.villageHeaders)
        get_sys_user = self.get_sys_user(self.vPhone, self.villageHeaders)
        asst_info = self.get_choose_asset_list(asset_name, cun_info["sysOrganizationId"])
        data = {
            "tradeMode": "01",
            "tradeType": "01",
            "organizationId": cun_info["sysOrganizationId"],
            "organizationName": cun_info["organizationName"],
            "provinceId": cun_info["provinceId"],
            "province": cun_info["province"],
            "cityId": cun_info["cityId"],
            "city": cun_info["city"],
            "areaId": cun_info["areaId"],
            "area": cun_info["area"],
            "streetId": cun_info["streetId"],
            "street": cun_info["street"],
            "address": cun_info["address"],
            "contact": get_sys_user['fullName'],
            "phone": get_sys_user['phone'],
            "projectName": asset_name,
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
                "sysOrganizationId": cun_info["sysOrganizationId"],
                "sysOrganizationName": cun_info["organizationName"],
                "assetName": asset_name,
                "assetCode": asst_info['assetCode'],
                "assetStatus": asst_info['assetStatus'],
                "assetNature": asst_info['assetNature'],
                "assetType": asst_info["assetType"],
                "assetTypeName": asst_info["assetTypeName"],
                "assetCategory": asst_info['assetCategory'],
                "assetCategoryName": asst_info['assetCategoryName'],
                "disposalMethod": asst_info['disposalMethod'],
                "acquiredDate": asst_info['acquiredDate'],
                "purpose": asst_info['purpose'],
                "purposeExplain": asst_info["purposeExplain"],
                "province": cun_info["province"],
                "provinceId": cun_info["provinceId"],
                "city": cun_info["city"],
                "cityId": cun_info["cityId"],
                "area": cun_info["area"],
                "areaId": cun_info["areaId"],
                "street": cun_info["street"],
                "streetId": cun_info["streetId"],
                "assetAddress": asst_info["assetAddress"],
                "originalValue": asst_info['originalValue'],
                "buildArea": asst_info['buildArea'],
                "buildAreaUnit": asst_info['buildAreaUnit'],
                "landOccupation": asst_info['landOccupation'],
                "landOccupationUnit": asst_info['landOccupationUnit'],
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
            "auditMaterialsSaveParams": [],
            "enrollType": 0,  # 允许报名用户类型
            "blacklistEnter": "false",  # 是否禁止警示名单报名 0=否 1=是
            "priorityOriginalLessee": "false",  # 是否原承租方优先权 0=否 1=是
            "payTradeEarnestMoney": "true",
            "tradeEarnestMoney": 1,
            "floorPrice": 4168,
            "minBidRange": 1000,
            "maxBidRange": 9000,
            "assetDeliverDay": 5,
            "progressiveIncrease": "false",  # 是否递增付款金额 0=否 1=是
            "progressiveIncreaseWay": "",  # 递增方式 1=按比例递增 2=按固定金额递增
            "progressiveIncreaseAmount": '',  # 每次递增固定金额
            "progressiveIncreaseStartMonth": '',  # 从第n个月开始递增
            "progressiveIncreaseMonth": '',  # 每n个月递增一次
            "progressiveIncreaseIncrease": None,  # 每次递增幅度为上期缴纳租金的n百分比
            "rentFree": "false",  # 是否有免租期
            "rentFreePeriod": None,  # 免租天数
            "rentCollectMethod": '0',  # 租金收取方式 0=按月 1=按季 3=按年 4=一次性
            "projectStartDate": str(datetime.datetime.now() + datetime.timedelta(days=0))[0:19],  # 租赁开始时间,出售类型时间为空
            "projectEndDate": str(datetime.datetime.now() + datetime.timedelta(days=30))[0:19],  # 租赁开始时间,出售类型时间为空
            "projectTradeYear": "30天",
            "perpetualAssignment": "false",  # 是否永久出让 0=否 1=是
            "repostAssetProject": "true",  # 流拍是否自动挂牌
            "volumeRate": 5,  # 地上容积率
            "volumeRateAcreage": 5,  # 总计算容积率建筑面积（平方米）
            "buildingDensity": 5,   # 建筑密度（%）
            "buildingLimitHeight": 10,  # 建筑限高（米）
            "investmentIntensity": 10,  # 总投资强度（万元/亩）
            "contractExpirationDate": 1,    # 合同截止天数
            "isSubmit": 1,
            "taskId": None,
            "agent": "false"    # 是否代办
        }
        if project_type == "00":
            # 出租不变
            pass
        elif project_type == "01":
            # 出租+资格
            data["requires"] = 'true'
            data["auditMaterialsSaveParams"] = [{"materialsName": "身份证", "remark": "备注"}]
        elif project_type == "10":
            # 出让
            data["tradeType"] = "02"
        elif project_type == "11":
            # 出让+资格
            data["tradeType"] = "02"
            data["requires"] = 'true'
            data["auditMaterialsSaveParams"] = [{"materialsName": "身份证", "remark": "备注"}]
        elif project_type == "12":
            """永久出让"""
            data["tradeType"] = "02"
            data["projectEndDate"] = None
            data["projectTradeYear"] = "永久出让"
            data["perpetualAssignment"] = "true"
        elif project_type == "20":
            # 出售
            data["tradeType"] = "03"
            del data["rentCollectMethod"], data["projectStartDate"], data["projectEndDate"], data["projectTradeYear"]
        elif project_type == "21":
            # 出售+资格
            data["tradeType"] = "03"
            data["requires"] = 'true'
            del data["rentCollectMethod"], data["projectStartDate"], data["projectEndDate"], data["projectTradeYear"]
            data["auditMaterialsSaveParams"] = [{"materialsName": "身份证", "remark": "备注"}]
        elif project_type == '101':
            # 协商+出租
            del data["priorityOriginalLessee"], data["minBidRange"], data["maxBidRange"], data["repostAssetProject"],
            data['tradeMode'] = 2
            data['agent'] = False
            data["applyType"] = 1
        return data

    # 资产选择列表,增加Id避免接口多次调用
    def get_choose_asset_list(self, asset_name, organization_id=None):
        url = '/api/admin/v1/asset/getChooseAssetList'
        data = {
            "sysOrganizationId": organization_id,
            "current": 1,
            "size": 10,
            "type": 0,
            "assetName": asset_name
        }
        return self.post(url, data, self.villageHeaders)['data']['records'][0]

    # 审核、发布工作流项目列表  默认mode=01公开竞价；status=20待发布交易公告；tradeType=01出租
    def get_activiti_page(self, mode="01", status=20, project_name=None):
        url = "/api/admin/v1/activiti/getActivitiPage"
        data = {"current": 1, "size": 10, "tradeMode": mode, "projectStatusList": [status],
                "projectName": project_name}
        req = self.post(url, data, self.auditHeaders)
        return req['data']['records'][0]

    # 项目查询->审核
    def audit(self, project_name, mode='01', status=20):
        # 根据projectName查询项目任务id等信息,mode默认01代表公开竞价审核列表，status默认20是发布公告查询列表
        proejct_info = self.get_activiti_page(mode, status, project_name=project_name)
        print(proejct_info["assetProjectId"])
        trade_no = proejct_info['tradeNo']
        # 审核
        url = '/api/admin/v1/activiti/activitiInstance'
        data = {"assetProjectId": proejct_info["assetProjectId"],
                "taskId": proejct_info["taskId"],
                "businessKey": proejct_info["businessKey"],
                "status": 1, "annotation": "通过"}
        self.set_sub_account(trade_no, project_name)
        return self.post(url, data, self.auditHeaders)

    def set_sub_account(self, trade_no, project_name):
        """测试环境手动生成子账号"""
        mysql = self.connect("cqjy-account")  # 连接数据库
        cursor = mysql.cursor()  # 建立游标
        time = (datetime.datetime.now()).strftime('%Y%m%d%H%M%S')
        time1 = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        sql = ("INSERT INTO `cqjy-account`.`t_sub_account`(`sub_account_id`, `app_id`, `app_name`, `sub_app_id`, "
               "`sub_account_no`, `sub_account_name`, `sub_req_no`, `organization_name`, `organization_id`, "
               "`main_account_no`, `account_bank_code`, `main_account_name`, `open_bank_name`,  `project_trade_no`, "
               "`auth_code`, `account_status`, `gmt_create`, `project_name`) "
               "VALUES (" + time + ", 'gdnccqjy', '广东省农村产权流转交易管理服务平台', '100000', '95588" + time + "', "
               "'八赏冒乐蹬饥符曾绍亥猴睹崎等佑', \'" + time + "\', '清远市清新区集体资产交易中心', 1531213778436427778, "
               "'3602023929200100926', '102', '八赏冒乐蹬饥符曾绍亥猴睹崎等佑', "
               "'中国工商银行广州支行',  \'" + trade_no + "\', \'" + time + "\', '00', '" + time1 + "', '" + project_name +
               "');")
        # print(sql)
        cursor.execute(sql)
        try:
            mysql.commit()
        except Exception as e:
            mysql.rollback()
        cursor.close()
        mysql.close()

    def sigh_up(self, asset_name, project_type):
        """报名"""
        user_header = [self.user_headers_1, self.user_headers_2, self.user_headers_3]
        asset_project_id = self.get_project_info_page(asset_name)
        url1 = "/api/auction/v1/assetProjectAuditMaterials/getAssetProjectAuditMaterials"
        data1 = {"assetProjectId": asset_project_id}
        req1 = self.post(url1, data1, self.user_headers_1)
        # 报名-确定
        url = "/api/auction/v1/assetProjectEnroll/saveAssetProjectEnroll"
        data = {"assetProjectId": asset_project_id}
        for n in user_header:
            if project_type == "01" or project_type == "11" or project_type == "21":
                data["files"] = [{"assetProjectAuditMaterialsId": req1["data"][0]["assetProjectAuditMaterialsId"],
                                  "fileUrl": "cqjy/000000/202211/679e7a2c-2b1f-439a-a11c-104d6134b3fb.jpg"}]
            sign_up = self.post(url, data, n)
        return sign_up

    def get_earenst_money_for_portal(self, project_name, is_user=3):
        """查看保证金子账号并缴纳后查询"""
        user_header = [self.user_headers_1, self.user_headers_2, self.user_headers_3]
        mysql = self.connect("cqjy")
        cursor = mysql.cursor()
        time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        # # 查询子账号
        asset_project_id = self.get_project_info_page(project_name)
        sql = ("UPDATE cqjy.t_asset_project_enroll SET system_feedback_status = 1, pay_earnest_money_date = '" + time +
               "', pay_earnest_money = 1 WHERE asset_project_id = " + asset_project_id + " ;")
        cursor.execute(sql)
        try:
            mysql.commit()
        except Exception as e:
            mysql.rollback()
        cursor.close()
        mysql.close()
        # 查询保证金
        url = "/api/auction/v1/assetProjectEnroll/getEarenstMoneyForPortal"
        data = {"assetProjectId": asset_project_id}
        if is_user == 3:
            for n in user_header:
                req = Public().post(url, data, n)
        else:
            req = Public().post(url, data, user_header[is_user])
        return req

    def get_enroll_audit_detail(self, project_id):
        """意向人审核列表"""
        url = "/api/admin/v1/assetProject/getEnrollAuditProjectDetail"
        data = {"assetProjectId": project_id, "current": 1, "size": 10}
        req = self.post(url, data, self.auditHeaders)
        return req["data"]["records"]

    def upload_contract(self, project_name, trade=None):
        # 查询项目id，No
        project = self.get_project_management_list(project_name)
        url = '/api/admin/v1/assetProjectContract/saveAssetProjectContract'
        data = {
            "type": 1,
            "assetProjectId": project["assetProjectId"],
            "tradeNo": project["tradeNo"],
            "contractStartDate": str(datetime.datetime.now())[0:10],
            "contractYear": 0,
            "contractMonth": 0,
            "contractDay": 30,
            "contractEndDate": str(datetime.datetime.now() + datetime.timedelta(days=30))[0:10],
            "payDateUnit": 0,
            "firstPayDate": str(datetime.datetime.now())[0:10],
            "payDays": 2,
            "paymentDays": 0,
            "idCardBackFile":
                "ZW5jcnlwdC9jb250cmFjdC80NDA4ODIwMDAwMDAvMjAyMzAzLzcxNDAxN2IxLWZjNTMtNDUxYy1hOTgwLTdkNWQ2ODU0NDljNy5qcGc=",
            "idCardFrontFile":
                "ZW5jcnlwdC9jb250cmFjdC80NDA4ODIwMDAwMDAvMjAyMzAzLzBhNzE3NzRkLTVlNDUtNGNhYi1hZTFlLTQ1MzdhYWQ2MWRiZi5qcGc=",
            "files": [{
                "fileName": "1.png",
                "fileUrl": "contract/441802000000/202311/20028cc3-734b-4e0d-a043-f85a89921fe4.png"}]}
        if trade == '20':
            del data['contractStartDate'], data['contractYear'], data['contractMonth'], data['contractDay'], (
                data)['contractEndDate'], data['payDateUnit']
            return data
        return self.post(url, data, self.villageHeaders)

    def activiti_instance(self, project_name):
        """合同审核"""
        project = self.get_project_management_list(project_name)
        url = '/api/admin/v1/activiti/activitiInstance'
        data = {"actNode": "contractFirstInstance", "assetProjectId": project["assetProjectId"],
                "businessKey": project["businessKey"], "status": 1, "annotation": "通过"}
        return self.post(url, data, self.auditHeaders)

    def search_notice(self, assetName):
        """查询成交公告"""
        url = '/api/admin/v1/assetInformation/getPostInfoPageList'
        data = {"informationTitle": assetName, "current": 1, "size": 10, "informationType": 3}
        return self.post(url, data, self.auditHeaders)


if __name__ == '__main__':
    pass
