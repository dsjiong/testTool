import os
from re import search


class DataExtractor(object):
    """提取日志文件数据"""

    def __init__(self, infile, outfile, *keywords):
        """
        :param self:
        :param infile: 输入日志文件路径
        :param outfile: 输出提取的数据excel
        :param keywords: 查询日志文件的关键字
        :return:
        """

        self.infile = infile
        self.outfile = outfile
        self.keywords = keywords

    def data_from_keyword(self):
        """Extract data from infile behind the keywords"""

        for x in range(len(asset_code)):
            for log_file_name in log_files_list:
                # 构建完整的日志文件路径
                log_file_path = os.path.join(log_folder_path, log_file_name)
                with open(log_file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                # 构造要搜索的字符串
                search_str = f"{re.escape(name[x])}.*{re.escape(str(asset_code[x]))}"

                # 在文件内容中查找匹配的行
                match_lines = [line for line in lines if re.search(search_str, line)]

                # 如果有匹配的行，提取挂牌金额
                if match_lines:
                    match_line = match_lines[0]
                    values = re.findall(r'\[.*?\]', match_line)
                    if values:
                        for value in values:
                            # 使用正则表达式匹配指定关键值前面的值
                            result = str(re.search(r'(.+?),\s*' + re.escape(str(clinch_amount)), value))
                            print(result)
                            if result:
                                # 将结果存储到字典中，确保转换为字符串
                                code_listed_amount_dict[x] = str(result.group(1))
                            return result.group(1)

            return None
