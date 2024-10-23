from tqdm import tqdm

from wanted_generate.input_adaptor import InputAdaptor
from wanted_generate.wanted_list_builder import WantedListBuilder

from card_info_manager.card_info_database import CardInfoDatabase

adaptor = InputAdaptor()
wanted_list_builder = WantedListBuilder()
card_info_database = CardInfoDatabase()

res_list = adaptor.trans_from_xlsx("XXX.xlsx", "sheet_1")

info_list = []
for card_msg in tqdm(res_list[0]):
  # print(card_msg)
  card_info = card_info_database.get_card_by_name(card_msg["卡名"])
  card_info.prize = card_msg["价格"]
  card_info.rare = card_msg["罕贵"]
  card_info.pack_msg = card_msg["编号"]
  info_list.append(card_info)

wanted_list_builder.gen_wanted_list(info_list)


