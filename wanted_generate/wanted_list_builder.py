import os
import cv2

from tqdm import tqdm

from .wanted_card_generator import WantedCardGenerator
from card_info_manager.card_image_generator import CardImageGenerator

class WantedListBuilder:
  def __init__(self):
    self.img_num_per_row = 8
    self.wanted_card_generator = WantedCardGenerator()
    self.card_image_generator = CardImageGenerator()
    self.output_dir = "./output/"
    self.save_single_img = True

  def gen_wanted_list(self, info_list):
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)
    for idx in tqdm(range(len(info_list))):
      img = self.card_image_generator.get_cn_card_image(info_list[idx])
      img = self.wanted_card_generator.gen_wanted_card(img, info_list[idx])
      if self.save_single_img:
        cv2.imwrite(os.path.join(self.output_dir,"{}.jpg".format(idx)), img)



