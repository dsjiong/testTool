import pandas as pd
import os
import re

# 读取Excel文件
excel_file_path = './file.xlsx'
df_excel = pd.read_excel(excel_file_path, 'Sheet1')
asset_code = df_excel['asset_code']
name = df_excel['asset_name']
clinch_amount = df_excel['clinch_amount']
# print(asset_code, name, clinch_amount)

# 获取当前脚本所在目录
script_directory = os.path.dirname(os.path.realpath(__file__))

# 构建日志文件夹的完整路径
log_folder_path = os.path.join(script_directory, '20231219')

# 获取日志文件夹下的所有文件
log_files_list = os.listdir(log_folder_path)

# 创建字典，用于存储code对应的挂牌金额
code_listed_amount_dict = {}

# 遍历所有日志文件，将数据添加到字典中
"""Extract data from infile behind the keywords"""
# 遍历所有日志文件，将数据添加到字典中
# 遍历所有日志文件，将数据添加到字典中
for x in range(len(asset_code)):
    for log_file_name in log_files_list:
        # 构建完整的日志文件路径
        log_file_path = os.path.join(log_folder_path, log_file_name)
        with open(log_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 构造要搜索的字符串
        search_str = f"表格内容:.*{re.escape(name[x])}.*{re.escape(str(asset_code[x]))}"

        # 在文件内容中查找匹配的行
        match_lines = [line for line in lines if re.search(search_str, line)]

        # 如果有匹配的行，提取挂牌金额
        if match_lines:
            match_line = match_lines[0]
            print('match_line:', match_line)
            values = re.findall(r'\[.*?\]', match_line)
            # print('values:', values)
            if values:
                for value in values:
                    # 使用正则表达式匹配指定关键值前面的值
                    result = re.search(r'(.+?),\s*' + re.escape(str(clinch_amount[x])), value)
                    print('result&&clinch_amount=', result, clinch_amount[x])
                    if result:
                        # 将结果存储到字典中，确保转换为字符串
                        code_listed_amount_dict[x] = str(result.group(1))

# 根据Excel文件中的code列更新listed_amount列
df_excel['listed_amount'] = df_excel.index.map(code_listed_amount_dict)

# 将更新后的数据写回Excel文件
df_excel.to_excel(excel_file_path, index=False)
