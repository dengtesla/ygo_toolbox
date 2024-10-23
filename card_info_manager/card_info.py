

class CardInfo:
  def __init__(self, card_id):
    self.card_id = card_id
    self.cid = None # 百鸽维护的 id
    self.cn_name = None
    self.sc_name = None
    self.md_name = None
    self.nwbbs_n = None
    self.cnocg_n = None
    self.jp_ruby = None
    self.jp_name = None
    self.en_name = None
    self.text = None
    self.type = None
    self.pack_msg = None
    self.prize = 0.0
    self.rare = None


  def set_attr(self, attr_dict):
    for key in attr_dict.keys():
      if hasattr(self, key):
        setattr(self, key, attr_dict[key])
    # TODO: 获取魔陷怪的类型
