import os
import sys
 
import numpy as np
from optparse import OptionParser
 
import json
import cv2
import datetime
from flask import Flask
UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


import face_recognition as fr
#from app import app

#UPLOAD_FOLDER = 'static/uploads'
base_dir = r"D:\python_project\facematch"

 

def check_similarity(image1fullpath,image2fullpath):
    print("In check similarity method")
    image1fullpath = os.path.join(base_dir,image1fullpath)
    image2fullpath = os.path.join(base_dir,image2fullpath)
    print(image1fullpath,image2fullpath)
    img1 = fr.load_image_file(image1fullpath)
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    face_location1 = fr.face_locations(img1)[0]
    face_encoding1 = fr.face_encodings(img1)[0]
    face_rectangle1 = cv2.rectangle(img1, (face_location1[3],face_location1[0]),(face_location1[1],face_location1[2]),(19, 244, 239),2)
 
    img2 = fr.load_image_file(image2fullpath)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
    face_location2 = fr.face_locations(img2)[0]
    face_encoding2 = fr.face_encodings(img2)[0]
    face_rectangle2 = cv2.rectangle(img2, (face_location2[3],face_location2[0]),(face_location2[1],face_location2[2]),(19, 244, 239),2)
 
    image1_new = os.path.splitext(os.path.basename(image1fullpath))[0]+str("_cropped_face1")
    image2_new = os.path.splitext(os.path.basename(image2fullpath))[0]+str("_cropped_face2")
    #print("image 1 fullpath------"+image1fullpath)
    #print("image 2 fullpath------"+image2fullpath)
 
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],str(image1_new)+".jpg"), face_rectangle1)
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],str(image2_new)+".jpg"), face_rectangle2)
 
    #print(face_encoding1)
    #print(face_encoding2)
 
    comparison = fr.compare_faces([face_encoding1],face_encoding2,tolerance = 0.57)
    distance = fr.face_distance([face_encoding1],face_encoding2)
 
    print(comparison,distance)
 
    RESPONSE =  {"RESULTS":  { "OUTPUT_FILE1_NAME" : os.path.join(app.config['UPLOAD_FOLDER'],str(image1_new)+".jpg"), "OUTPUT_FILE2_NAME" : os.path.join(app.config['UPLOAD_FOLDER'],str(image2_new)+".jpg"),"Comparison ":comparison[0]}}
 
    print("RESPONSE:", RESPONSE)
    retStr = ''
    for key1 in RESPONSE.keys():
        #retStr = retStr +"<div class='col-12' style='margin-top:3%'><h4>"+str(key1)+"</h4></div>"
        for key2 in RESPONSE[key1].keys():
            if key2 == 'OUTPUT_FILE1_NAME':
                retStr = retStr+ "<div class='col-4'><h6>IMAGE 1</h6><img src=\""+ str(RESPONSE[key1][key2]).replace("\\","/") + "\" class='img-fluid rounded shadow' width='300'/></div>"
            elif key2 == 'OUTPUT_FILE2_NAME':
                retStr = retStr+ "<div class='col-4'><h6>IMAGE 2</h6><img src=\""+ str(RESPONSE[key1][key2]) + "\" class='img-fluid rounded shadow' width='300'/></div>"
            else:
                retStr = retStr+str(key2)+" : "+ str(RESPONSE[key1][key2]).upper() + "<br/>"
 
    #print(retStr)      
    return retStr
   # return RESPONSE
 
 
def fs_driver(image1,image2):
    print(image1)
    print(image2)
    return check_similarity(image1,image2)