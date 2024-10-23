import os
import cv2

from common.constant import common_path
from .card_info import CardInfo


class CardImageGenerator:
  def __init__(self):
    self.card_image_url_template = "https://cdn.233.momobako.com/ygopro/pics/{}.jpg"
    self.specify_image_dir = os.path.join(common_path, "card_info_manager", "data_base", "image_data")
  
  def get_cn_card_image(self, card_info: CardInfo):
    k_id = card_info.card_id
    cap = cv2.VideoCapture(self.card_image_url_template.format(k_id))
    _,img = cap.read()
    cap.release()
    return img
  
  def get_sample_card_image(self):
    raise NotImplementedError("TODO")
  
  def get_image_from_local(self, key_str):
    raise NotImplementedError("TODO")
    
