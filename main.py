# -*- coding: utf-8 -*-


import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

from PIL import Image, ImageGrab
import numpy as np
import easyocr
import pyperclip

def read_img_from_clipboard():
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        # print("Image: size : %s, mode: %s" % (img.size, img.mode))   
        return np.array(img)

class Main(FlowLauncher): 
    
    def query(self, keyword):

        results = list()
        if ImageGrab.grabclipboard():
            results.append({
                    "Title": '剪贴板内检测到截图',
                    "SubTitle": '进行文字识别,并将结果粘贴至剪贴板。',
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method": 'ocr',
                        "parameters": [],
                    }
                }) 
        else:
            results.append({
                "Title": '剪贴板内未检测到截图',
                "SubTitle": '请将截图添加至剪贴板进行文字识别。',
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": None,
                    "parameters": None,
                }
            })
              
        return results
    
    def ocr(self):

        img_array = read_img_from_clipboard()
        # OCR识别截图
        reader = easyocr.Reader(['ch_sim', 'en'])
        result = reader.readtext(img_array, detail=0)
        out = ''
        for i in result:
            out = out + '\n' + i
        pyperclip.copy(out)

if __name__ == "__main__":
    Main()

