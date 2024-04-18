import pandas as pd

asset_dict = {}
data = pd.read_excel(r'C:\Users\joe\Desktop\工作簿1.xlsx')
data.fillna("", inplace=True)

t_list = []

for i in data.index.values:
    line = data.loc[i, ["region_id", "parent_code", "region_code", "region_name", "sort"]].to_dict()
    t_list.append(line)
asset_dict['data'] = t_list
print(asset_dict)
