from fastapi import FastAPI
from fastapi import Request, Response
import os
import string
import urllib
import uuid
import pickle
import datetime
import time
import shutil
from  numpy import asarray
import hashlib
#import tkinter as tk
import cv2
from PIL import Image

#import util
from test import test

import cv2
from fastapi import FastAPI, File, UploadFile, Form, UploadFile, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import starlette

import mysql.connector
mydb = mysql.connector.connect(
  host="3.110.34.174",
  user="admin",
  password="SrinidhiBITS123",
  database="ZTNSDP"
)
mycursor = mydb.cursor()

ATTENDANCE_LOG_DIR = './logs'
DB_PATH = './db'
for dir_ in [ATTENDANCE_LOG_DIR, DB_PATH]:
    if not os.path.exists(dir_):
        os.mkdir(dir_)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@app.middleware("http")
#async def restrict_access_to_allowed_ips(request: Request, call_next):
#    # Get the client's IP address from the request
#    client_ip = request.client.host
#    #client_ip = request.headers.get('X-Forwarded-For') or request.client.host
#    #client_ip = request.remote_addr
#    #client_ip=""
#    #response = request.get("https://httpbin.org/ip")
#    #if response.status_code == 200:
#    # Extract the public IP address from the response
#    #client_ip = response.json().get("origin")
#    #return {"public_ip": public_ip}
#    print(client_ip)
#    #print(response)
#    print("inside wrapper")
#    query="SELECT userip FROM USERS_LOGIN_ACCESS;"
#    mycursor.execute(query)
#    myresult = mycursor.fetchall() 
#    allowed_ip=[]
#    allowed_ip.append('106.79.202.177')
#    for ele in myresult:
#        allowed_ip.append(ele[0])
#    # Check if the client's IP address is in the allowed list
#    if client_ip not in allowed_ip:
#        # Return a forbidden response with a custom message
#        return Response(content="Forbidden", status_code=403)
#
#    # Pass the request to the next middleware or route handler
#    response = await call_next(request)
#
#    return response

#@app.get("/restricted")
@app.post("/login")
async def login(username:str=Form(...),password:str=Form(...),file: UploadFile = File(...)):


    print(f"Recieved data: username={username},password={password}")
    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()
    passwordh = hashlib.sha256(password.encode('utf-8')).hexdigest()
    query="SELECT password from USERS WHERE username=\'"+username+"\';"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    flag1=False
    if len(myresult)!=0:
     if passwordh==myresult[0][0]:
         msg="user verified"
         #print(msg)
         #conn.sendall(msg.encode())
         flag1=True
     else:
         msg="login credentials invalid"
         #conn.senadll(msg.encode())
         flag1=False
    else:
       print("invalid users")
    with open(file.filename, "wb") as f:
           f.write(contents)


    img_test = Image.open(file.filename)
    img_test=img_test.convert('RGB')

    print(type(file.filename))
    print(type(file))
    print(type(contents))
    print(type(cv2.imread(file.filename)))

    print("-----------------------")

    print(type(img_test))

    final_img = asarray(img_test)

    print(type(final_img))
    print(final_img.shape)
    label = test(
              #  image=cv2.imread(file.filename), # point of change
                image=final_img,
		model_dir='/home/ubuntu/Silent-Face-Anti-Spoofing/resources/anti_spoof_models',   # point of change
                device_id=0
                )
    
    if label == 1:
        # example of how you can save the file
        user_name, match_status = recognize(cv2.imread(file.filename))

        if match_status:
            epoch_time = time.time()
            date = time.strftime('%Y%m%d', time.localtime(epoch_time))
            with open(os.path.join(ATTENDANCE_LOG_DIR, '{}.csv'.format(date)), 'a') as f:
                f.write('{},{},{}\n'.format(user_name, datetime.datetime.now(), 'IN'))
                f.close()
        print("label-passed- ",label)
        print("match_status - ",match_status)
        print("user - ",user_name)
        print("user type",type(user_name))
        print("match_status - type - ",type(match_status))
        print("label - type - ",type(label))
        label=str(label)
        src_ip=""
        if flag1:
            sql = "UPDATE USERS_GATEWAY_ACCESS SET FLAG2=\"1\" WHERE username=\""+user_name+"\""+";"
            #val = (username,src_ip,"SPAMTLSUSERVD")
            mycursor.execute(sql)
            mydb.commit()
            print("all success") 
        return {'user': user_name, 'match_status': match_status, 'label': label}
    else:
        label=str(label)
        print("label-passed- 2",label)
        return {'label': label} #point of change

@app.post("/logout")
async def logout(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        f.write(contents)

    user_name, match_status = recognize(cv2.imread(file.filename))

    if match_status:
        epoch_time = time.time()
        date = time.strftime('%Y%m%d', time.localtime(epoch_time))
        with open(os.path.join(ATTENDANCE_LOG_DIR, '{}.csv'.format(date)), 'a') as f:
            f.write('{},{},{}\n'.format(user_name, datetime.datetime.now(), 'OUT'))
            f.close()

    return {'user': user_name, 'match_status': match_status}


@app.post("/register_new_user")
async def register_new_user(file: UploadFile = File(...),text=None,password:str=Form(...),username:str=Form(...)):
    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()
    print(f"Recieved data: username={username},password={password}")

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        f.write(contents)

    shutil.copy(file.filename, os.path.join(DB_PATH, '{}.png'.format(text)))

    embeddings = face_recognition.face_encodings(cv2.imread(file.filename))

    file_ = open(os.path.join(DB_PATH, '{}.pickle'.format(text)), 'wb')
    pickle.dump(embeddings, file_)
    print(file.filename, text)

    os.remove(file.filename)

    return {'registration_status': 200}


@app.get("/get_attendance_logs")
async def get_attendance_logs():

    filename = 'out.zip'

    shutil.make_archive(filename[:-4], 'zip', ATTENDANCE_LOG_DIR)

    ##return File(filename, filename=filename, content_type="application/zip", as_attachment=True)
    return starlette.responses.FileResponse(filename, media_type='application/zip',filename=filename)


def recognize(img):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found', False
    else:
        embeddings_unknown = embeddings_unknown[0]

    match = False
    j = 0

    db_dir = sorted([j for j in os.listdir(DB_PATH) if j.endswith('.pickle')])
    # db_dir = sorted(os.listdir(DB_PATH))    
    print(db_dir)
    while ((not match) and (j < len(db_dir))):

        path_ = os.path.join(DB_PATH, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)[0]

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]

        j += 1

    if match:
        return db_dir[j - 1][:-7], True
    else:
        return 'unknown_person', False


