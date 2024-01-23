from Setting.login import *

header = Login().header()


def get_page_list(url, data):
    page_list = Login().post(url, data, header)["data"]
    return page_list


def delete_items(url, page_list, delete_url, delete_key):
    num = int(page_list["total"])
    for n in range(0, num):
        item_id = page_list["records"][n][delete_key]
        delete_data = {delete_key: item_id}
        Login().post(delete_url, delete_data, header)


def delete_contract():
    page_list_url = "/api/admin/v1/assetProjectExternalContractHi/getPageList"
    page_list_data = {"current": 1, "size": 10}
    page_list = get_page_list(page_list_url, page_list_data)
    delete_url = "/api/admin/v1/assetProjectExternalContractHi/deleteContractHi"
    delete_items(page_list_url, page_list, delete_url, "assetProjectExternalContractHiId")


def delete_asset():
    page_list_url = "/api/admin/v1/asset/getAssetPageList"
    page_list_data = {"current": 1, "size": 10}
    page_list = get_page_list(page_list_url, page_list_data)
    delete_url = "/api/admin/v1/asset/deleteAsset"
    delete_items(page_list_url, page_list, delete_url, "assetId")


def project_list():
    list_url = "/api/admin/v1/assetProject/getProjectInfoPage"
    list_data = {"provinceId": "6879694216377704448", "projectName": "测试资产", "current": 1}
    list = Login().post(list_url, list_data, header)
    print(list)


if __name__ == '__main__':
    pass
