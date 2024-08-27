import json
from PIL import Image
import cv2
import pytesseract 
import os
import numpy as np
import re
import datetime
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def regit(texts):
    depart = np.nan
    amount = np.nan
    age = np.nan
    sex = np.nan
    duration = np.nan
    for text in texts:
        d0 = re.search(r"global hospital",text)
        # print(d0)
        if d0:
            d1 = re.search(r"(\s*)date(\s*)of(\s*)admission",text)
            if d1:
                # print(d1)
                r1 = re.findall(r": (\d{1,2})-(\d{1,2})-(\d{4})",text[(d1.span()[1])-2:(d1.span()[1])+15])
                date_of_admission=r1[0]
                #print(r1)
                
            d2 = re.search(r"(\s*)discharge(\s*)date",text)
            if d2:
                # print(d2)
                r2 = re.findall(r": (\d{1,2})-(\d{1,2})-(\d{4})",text[(d2.span()[1])-2:(d2.span()[1])+15])
                date_of_discharge=r2[0]
                #print(r2)
            
            d3 = re.search(r"(\s*)age/sex:(\s*)",text)
            if d3:
                if "female" in text[(d3.span()[1])-1:(d3.span()[1])+19]:
                    sex = 0
                elif " male" in text[(d3.span()[1])-1:(d3.span()[1])+17]:
                    sex = 1
                if re.search(r"(\d*)",text[(d3.span()[1])-1:(d3.span()[1])+19]):
                    r3 = re.findall(r"[0-9]{2}",text[(d3.span()[1])-1:(d3.span()[1])+19])
                    age = int(r3[0])
            try:
                i=datetime.date(int(date_of_admission[2]),int(date_of_admission[1]),int(date_of_admission[0]))
                j=datetime.date(int(date_of_discharge[2]),int(date_of_discharge[1]),int(date_of_discharge[0]))
                temp_date=j-i
                duration = abs(temp_date.days)
            except(Exception) as e:
                print(e)
        d4 = re.search(r"(\s*)total(\s*)amount:(\s*)",text)
        if d4:
            if re.search(r"(\d*)",text[(d4.span()[1])-1:]):
                r4 = re.findall(r"(\d*)(.{1})(\d*)(\.)(\d*)",text[(d4.span()[1])-1:])
                r4 = float(r4[0][0]+r4[0][2]+"."+r4[0][4])
                amount = r4
        d5 = re.search(r"admitted(\s*)in",text.replace("admutted","admitted"))
        d6 = re.search(r"(\s*)department(\s*)",text)
        if d5 and d6:
            r5 = (text[(d5.span()[1]):(d6.span()[0])]).replace("\n"," ").strip(" ")
            if r5.endswith(" medicme"):
                r5 = r5.replace("medicme","medicine")
            if r5.endswith(" medicime"):
                r5 = r5.replace("medicime","medicine")
            if r5 == 'nephrology':
                r5 = 0
            if r5 == 'neurology':
                r5 = 1
            if r5 == 'general medicine':
                r5 = 2
            if r5 == 'cardiology':
                r5 = 3
            if r5 == 'orthopedic':
                r5 = 4
            depart = r5    
    
    data = [age,sex,duration,depart,amount]
    with open("rasa/data5.json","w") as f:
        json.dump(data,f)
    return "completed"


def extract(brief):
    texts=[]
    print(os.listdir(brief))
    for page in os.listdir(brief):
        print(page)
        try:
            cv_img=cv2.imread(brief+"/"+page,1)
            kernel = np.ones((1, 1), np.uint8)
            cv_img = cv2.dilate(cv_img, kernel, iterations=1)
            cv_img = cv2.erode(cv_img, kernel, iterations=1)
            img=Image.fromarray(cv_img)
            text = str(pytesseract.image_to_string(img))
            text = text.replace('-\n', '')
            text = text.lower()
            texts.append(text)
        except(Exception) as e:
            print(e)
            print("error",page,"error")
    regit(texts)

