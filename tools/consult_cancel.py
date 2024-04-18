from Setting.Base import *


def get_activiti_page():
    url = '/api/admin/v1/activiti/getActivitiPage'
    data = {
        "current": 1,
        "size": 500,
        "tradeMode": "02",
        "projectStatusList": [0]
    }
    records_dict = Information().post(url, data, Information().villageHeaders)['data']
    return records_dict


def cancel(num, records):
    url = '/api/admin/v1/openConsult/cancel'
    for x in range(0, num):
        tid = records[x]['assetProjectId']
        key = records[x]['businessKey']
        data = {
            "assetProjectId": tid,
            "businessKey": key
        }
        Information().post(url, data, Information().villageHeaders)
        print(x)


if __name__ == '__main__':
    records = get_activiti_page()
    num = records['total']
    records = records['records']
    # print(num, records_dict)
    cancel(int(num), records)
