import os
import requests
import math

import zipfile
import json

import pandas as pd
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm

cards_zip_path = "database/cards.zip"
cards_json_path = "database/cards.json"
cards_database = None


def update_data():
  resp = requests.get("https://ygocdb.com/api/v0/cards.zip")
  with open(cards_zip_path, 'wb') as f:
    f.write(resp.content)

  f = zipfile.ZipFile(cards_zip_path, 'r')
  for file in f.namelist():
    f.extract(file, "database/")
  f.close()


def update_card_database():
  if not os.path.exists("./database"):
    os.makedirs("./database")
  old_version = ""
  data_version_file = "database/data_version.txt"
  if os.path.exists(data_version_file):
    with open(data_version_file, 'r') as f:
      old_version = f.readlines()[0]
  version_resp = requests.get("https://ygocdb.com/api/v0/cards.zip.md5")
  # if (version)
  # data_version = 
  new_version = version_resp.json()
  if (old_version == new_version):
    print("======== no need to update data! ========")
  else:
    print("======== update data from {} to {} ========".format(old_version, new_version))
    with open(data_version_file, 'w') as f:
      f.write(new_version)
    update_data()

def load_data():
  global cards_database
  with open(cards_json_path, 'r') as f:
    cards_database = json.load(f)


'''
从 xlsx 中获取到 wanted 信息
'''
def load_xlsx(xlsx_path, sheet_name):
  df = pd.read_excel(xlsx_path,sheet_name=sheet_name)
  # print(df.values)
  list_cnt = -1
  card_cnt = 0
  curr_name = ""
  key_word_list = ['卡名', '罕贵', '编号', '价格']
  res_dict = []
  for col in df.columns:
    for val in df[col]:
      if val in key_word_list:
        curr_name = val
        card_cnt = 0
        if val == '卡名':
          list_cnt+=1
          res_dict.append([])
        continue
      if (isinstance(val, str)) or (not math.isnan(val)):
        if curr_name == "卡名":
          res_dict[list_cnt].append({curr_name: val})
        elif curr_name != "":
          res_dict[list_cnt][card_cnt][curr_name] = val
        card_cnt+=1
  return res_dict

def get_card_msg_from_json_database(card_name: str):
  cnt = 0
  return_val = None
  name_list = ["cn_name", "sc_name", "md_name", "nwbbs_n", "cnocg_n", "jp_ruby", "jp_name", "en_name"]
  # 简单的暴力，可以优化成 o(logn)
  for key in cards_database.keys():
    for name in name_list:
      if name in cards_database[key].keys() and cards_database[key][name] == card_name:
        return_val = cards_database[key]
        cnt+=1
        break
  if cnt == 1:
    return return_val
  else:
    return None

def get_card_image(msg_dict):
  card_name = msg_dict["卡名"].rstrip('（异画）')
  card_msg = get_card_msg_from_json_database(card_name)
  if card_msg != None:
    card_id = card_msg["id"]
  else:
    # TODO: 使用编号（形如 ABCD-EF001）获取 img
    print("cannot found image!!")
    return
  cap = cv2.VideoCapture("https://cdn.233.momobako.com/ygopro/pics/{}.jpg".format(card_id))
  _,img = cap.read()
  cap.release()
  return img

def get_image_from_id(card_id: str):
  pass

def make_debug_image(msg_dict, cnt):
  img = get_card_image(msg_dict)

  img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  draw = ImageDraw.Draw(img)
  draw.rectangle(xy=(0,420,400,580), outline="yellow", fill="yellow", width=2)
  draw.rectangle(xy=(0,0,400,580), outline="red", width=2)
  draw.rectangle(xy=(0,420,400,470), outline="blue", width=2)
  draw.rectangle(xy=(0,470,70,580), outline="blue", width=2)
  fontText = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 88, encoding="utf-8")
  fontText2 = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 33, encoding="utf-8")

  text2 = "罕贵：" + str(msg_dict["罕贵"])
  if "-" in msg_dict["编号"]:
    text2 += " " + msg_dict["编号"]
  else:
    text2 += " 卡包：" + msg_dict["编号"]
  draw.text((10,430), text2, "red", font=fontText2, stroke_width=1)
  draw.text((10,480), "回", (255,100,200), font=fontText2)
  draw.text((10,510), "收", (255,100,200), font=fontText2)
  draw.text((10,540), "价", (255,100,200), font=fontText2)
  draw.text((80,480), "￥" + '{:.1f}'.format(msg_dict["价格"]), "red", font=fontText, stroke_width=2)

  img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
  cv2.imwrite("output/{}.jpg".format(cnt), img)




def main():
  # 一般不需要使用该接口，因为百鸽那边的 api 时常有 hang 住的情况出现
  update_card_database()
  load_data()
  load_xlsx("test.xlsx", "test_sheet")
  cnt = 0
  os.makedirs("output/", exist_ok=True)
  for cards_list in cards_dict:
    for cards_msg in tqdm(cards_list):
      make_debug_image(cards_msg, cnt)
      cnt+=1

if __name__ == "__main__":
  main()

