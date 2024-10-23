import math

import pandas as pd

class InputAdaptor:
  def __init__(self):
    pass

  def trans_from_xlsx(self, xlsx_path, sheet_name):
    df = pd.read_excel(xlsx_path,sheet_name=sheet_name)
    # print(df.values)
    list_cnt = -1
    card_cnt = 0
    curr_name = ""
    key_word_list = ['卡名', '罕贵', '编号', '价格']
    res_list = []
    for col in df.columns:
      for val in df[col]:
        if val in key_word_list:
          curr_name = val
          card_cnt = 0
          if val == '卡名':
            list_cnt+=1
            res_list.append([])
          continue
        if (isinstance(val, str)) or (not math.isnan(val)):
          if curr_name == "卡名":
            res_list[list_cnt].append({curr_name: val})
          elif curr_name != "":
            res_list[list_cnt][card_cnt][curr_name] = val
          card_cnt+=1
    return res_list