import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from card_info_manager.card_info import CardInfo
from common.constant import font_path


class WantedCardGenerator:
  def __init__(self):
    pass
  
  def gen_wanted_card(self, image, card_info):
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    draw.rectangle(xy=(0,420,400,580), outline="yellow", fill="yellow", width=2)
    draw.rectangle(xy=(0,0,400,580), outline="red", width=2)
    draw.rectangle(xy=(0,420,400,470), outline="blue", width=2)
    draw.rectangle(xy=(0,470,70,580), outline="blue", width=2)
    fontText = ImageFont.truetype(font_path, 88, encoding="utf-8")
    fontText2 = ImageFont.truetype(font_path, 33, encoding="utf-8")

    text2 = "罕贵：" + str(card_info.rare)
    if "-" in card_info.pack_msg:
      text2 += " " + card_info.pack_msg
    else:
      text2 += " 卡包：" + card_info.pack_msg
    draw.text((10,430), text2, "red", font=fontText2, stroke_width=1)
    draw.text((10,480), "回", (255,100,200), font=fontText2)
    draw.text((10,510), "收", (255,100,200), font=fontText2)
    draw.text((10,540), "价", (255,100,200), font=fontText2)
    draw.text((80,480), "￥" + '{:.1f}'.format(card_info.prize), "red", font=fontText, stroke_width=2)

    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img
