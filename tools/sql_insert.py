import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
from Setting.Base import *


class Insert(Information):

    def upload_image(self, cloud_id):

        # 替换为你要上传的图片路径
        image_path = 'D:\B2BWings\文档资料\测试数据\图片/2.jpg'

        # 替换为上传图片的接口URL
        upload_url = 'https://cqjy-test.b2bwings.com/api/file/v1/picture/uploadBatchCloudFilesOnObs'

        # 创建一个multipart编码器
        multipart_encoder = MultipartEncoder(
            fields={'files': ('2.jpg', open(image_path, 'rb'), 'image/jpeg'), 'folderName': cloud_id}
        )

        # 设置请求头
        session = self.login(self.villagePhone, self.village)
        headers = {'Content-Type': multipart_encoder.content_type, "sessionid": session, "channel": 'admin'}

        try:
            # 发送请求
            response = requests.post(upload_url, data=multipart_encoder, headers=headers, verify=False)

            # 检查请求是否成功
            if response.status_code == 200:
                print("图片上传成功！")
            else:
                print("图片上传失败，状态码：", response.status_code)
        except Exception as e:
            print("发生异常：", str(e))

    def for_insert(self, cloud_id):
        connet = self.connect('cqjy-cms')
        cur = connet.cursor()
        sql1 = "INSERT INTO `cqjy-cms`.`t_project_cloud` (`project_cloud_id`, `project_cloud_release_date`, `project_cloud_end_date`, `organization_name`, `organization_contact`, `organization_phone`, `organization_address`, `asset_picture`, `asset_name`, `asset_organization_name`, `asset_type`, `asset_area`, `asset_address`, `project_name`, `project_no`, `project_trade_no`, `project_trade_mode`, `project_trade_type`, `project_type`, `other_remark_fire_control`, `other_remark_industry_require`, `project_start_date`, `project_end_date`, `project_day`, `trade_earnest_money`, `floor_price`, `asset_deliver_day`, `project_files`, `blacklist_enter`, `enroll_type`, `remark_condition`, `province_code`, `city_code`, `area_code`, `street_code`, `organization_id`, `number_of_participants`, `vot_status`, `other_import_explain`, `other_terms_contract`, `tax_payment_special_explain`, `remark`, `remark_condition_files`, `gmt_create`) VALUES (" + cloud_id + ", '2024-03-22', '2024-03-22', '红丰镇红丰村民委员会', '二弟', '13751964423', '红丰镇红丰村民委员会', 'asset/440112000000/202306/3682bf2c-1211-4b46-a386-2a35fdbc4dc8.png', '红丰镇表决测试0001', '红丰镇红丰村民委员会', 'Z000000', '12平方米', '红丰村委', '红丰镇表决测试0001', 'BJ0000001', 'BJ0000001', '公开协商', '出让', '耕地出让', '消防说明说明', '其他要求说明', '2024-03-22', '2024-03-22', '1', '1元', '5168', '1', '[{\"fileName\": \"合同1\", \"fileUrl\": \"https://cqjy-test.b2bwings.com/obs/asset/441704000000/202403/a1dde342-5fbe-4c81-b732-53ee83d1a7ac.doc\"},{\"fileName\": \"合同1\",  \"fileUrl\": \"https://cqjy-test.b2bwings.com/obs/asset/441704000000/202403/a1dde342-5fbe-4c81-b732-53ee83d1a7ac.doc\"},{  \"fileName\": \"合同1\",  \"fileUrl\": \"https://cqjy-test.b2bwings.com/obs/asset/441704000000/202403/a1dde342-5fbe-4c81-b732-53ee83d1a7ac.doc\"}]', '禁止参与交易', '所有', '无', '440000000000', '441700000000', '441704000000', '441704110000', 1628654846546690049, 5, '通过', '说明', '说明', '说明', '说明', '[{\"materialsName\": \"材料1\",\"remark\": \"说明1\"},{ \"materialsName\": \"材料2\",\"remark\": \"说明2\"},{\"materialsName\": \"材料3\",\"remark\": \"说明3\"},{\"materialsName\": \"材料4\",\"remark\": \"说明4\"},{\"materialsName\": \"材料5\",\"remark\": \"说明5\"},{\"materialsName\": \"材料6\",\"remark\": \"说明6\"},{\"materialsName\": \"材料7\",\"remark\": \"说明7\"}]', '2024-03-26 09:25:28');"
        cur.execute(sql1)
        for _ in range(5):
            record_id = time.strftime('%Y%m%d%H%M%S')
            sql2 = "INSERT INTO `cqjy-cms`.`t_project_cloud_vote_record` (`project_cloud_vote_record_id`, `project_cloud_id`, `user_name`, `id_card`, `phone`, `cloud_vote_date`, `cloud_vote_result`, `gmt_create`) VALUES (" + record_id + ", " + cloud_id + ", '测试', '2', '13751964417', '2024-03-25', '同意', '2024-03-25 14:18:55');"
            cur.execute(sql2)
            sleep(1)
        try:
            connet.commit()
        except Exception as e:
            connet.rollback()
        cur.close()
        connet.close()
        print("插入成功")


if __name__ == '__main__':
    for _ in range(5):
        cloud_id = time.strftime('%Y%m%d%H%M%S')
        Insert().upload_image(cloud_id)
        Insert().for_insert(cloud_id)
