import json
from PIL import Image
import cv2
import pytesseract 
import sys  
import os
import numpy as np
import re
import datetime
import joblib

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract\tesseract'
clf = joblib.load("trained_model.sav")

def pred():
    with open("data5.json","r") as f:
        data = json.load(f)
    pred = clf.predict(np.array(data).reshape(1,-1))
    ans = ["no you cannot claim your insurance","yes you can claim your insurance"]
    return ans[pred[0]]
    

if __name__ == "__main__":
    pred()
