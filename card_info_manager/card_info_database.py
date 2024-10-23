import os
import zipfile
import re
import requests
import json

from tqdm import tqdm

from common.constant import common_path
from .card_info import CardInfo


class CardInfoDatabase:
  def __init__(self, check_data = False):
    self.data_base_path = os.path.join(common_path, "card_info_manager", "database")
    self.data_version_file_path = os.path.join(self.data_base_path, "data_version.txt")
    self.cards_zip_path = os.path.join(self.data_base_path, "cards.zip")
    self.cards_json_path = os.path.join(self.data_base_path, "cards.json")
    self.get_data_version_url = "https://ygocdb.com/api/v0/cards.zip.md5"
    self.get_data_url = "https://ygocdb.com/api/v0/cards.zip"
    self.enable_data_check = check_data
    self.cards_list = []
    # self.cards_num = 0
    self.name_keys = [
      "cn_name", "sc_name", "nwbbs_n", "cnocg_n", "jp_ruby", "jp_name", "en_name", "md_name"]
    self.name_2_idx_dict = {}
    for name in self.name_keys:
      self.name_2_idx_dict[name] = {}
    self.__load_data()

  def get_card_by_name(self, card_name, name_type="cn_name"):
    # 根据卡名搜索卡片
    # 需要名字完全匹配
    # 默认按照 cn_name->sc_name->nwbbs_n->cnocg_n->jp_ruby->jp_name->en_name->md_name 的顺序查找
    # 如果有提供 name_type，那么优先在对应的 name_type 里找
    if name_type in self.name_keys:
      if card_name in self.name_2_idx_dict[name_type].keys():
        return self.cards_list[self.name_2_idx_dict[name_type][card_name]]

    for name_key in self.name_keys:
      if name_key == name_type:
        continue
      if card_name in self.name_2_idx_dict[name_key].keys():
        return self.cards_list[self.name_2_idx_dict[name_key][card_name]]

    return None
  
  def get_card_by_card_pack_msg(self, card_pack_msg):
    # 通过类似 MUCR-JPXXX 的编号获取卡片信息
    raise NotImplementedError("TODO")

  def __update_data(self):
    resp = requests.get(self.get_data_url)
    with open(self.cards_zip_path, 'wb') as f:
      f.write(resp.content)

    f = zipfile.ZipFile(self.cards_zip_path, 'r')
    for file in f.namelist():
      f.extract(file, self.data_base_path)
    f.close()

  def __load_data(self):
    if not os.path.exists(self.data_base_path):
      os.makedirs(self.data_base_path)
    if self.enable_data_check:
      old_version = ""
      if os.path.exists(self.data_version_file_path):
        with open(self.data_version_file_path, 'r') as f:
          old_version = f.readlines()[0]
      version_resp = requests.get(self.get_data_version_url)
      new_version = version_resp.json()
      if (old_version == new_version):
        print("======== no need to update data! ========")
      else:
        print("======== update data from {} to {} ========".format(old_version, new_version))
        self.__update_data()
        with open(self.data_version_file_path, 'w') as f:
          f.write(new_version)
    
    with open(self.cards_json_path, 'r') as f:
      cards_database_json = json.load(f)
      self.__format_database(cards_database_json)
  
  def __format_database(self, database_json):
    curr_idx = 0
    for key in tqdm(database_json.keys()):
      if "id" in database_json[key].keys() and database_json[key]["id"] != 0:
        new_card = CardInfo(database_json[key]["id"])
        new_card.set_attr(database_json[key])
        self.cards_list.append(new_card)
        for name_key in self.name_2_idx_dict.keys():
          if hasattr(self.cards_list[curr_idx], name_key):
            name = getattr(self.cards_list[curr_idx], name_key)
            if name != None:
              if name in self.name_2_idx_dict[name_key] and self.name_2_idx_dict[name_key][name] != curr_idx:
                name = name + "_2"
                # print("error in {}!!!!  ".format(name_key) + name)
                # print(self.cards_list[self.name_2_idx_dict[name_key][name]].card_id)
                # print(self.cards_list[curr_idx].card_id)
              self.name_2_idx_dict[name_key][name] = curr_idx
        curr_idx+=1
