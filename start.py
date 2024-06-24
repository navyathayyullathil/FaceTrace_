from tkinter import *

import cv2

cap = cv2.VideoCapture(0)
WORD = re.compile(r'\w+')
import time
from tkinter import *
cap = cv2.VideoCapture(0)
WORD = re.compile(r'\w+')
import pymysql
face_cascade = cv2.CascadeClassifier("./static/opencv-files/haarcascade_frontalface_alt.xml")
con=pymysql.connect(host='localhost', port=3306,user='root',password='',db='attendance_face')
cmd=con.cursor()
while (True):
    try:
        ret, img = cap.read()
        # img=cv2.imread(fn)
        print(ret)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print("length" + str(len(faces)))
        # for (x,y,w,h) in faces:
        # 	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image


        emolist = []
        cv2.imshow("Frame", img)
        if len(faces) > 0:

            # enf("static/pic/"+fn)
            nm = "s" + str(logid)
            i = i + 1
            if i <= 10:
                static_folder = os.path.join(app.root_path, 'static/training-data')
                directory_path = os.path.join(static_folder, nm)
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                pth = 'static/training-data/' + nm + '/'
                fn = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
                cv2.imwrite(pth + fn, img)
                cmd.execute("insert into images values(null,'" + str(session['lid']) + "','" + fn + "')")
                con.commit()

        if cv2.waitKey(60) & 0xFF == 27:
            break
    except Exception as e:
        print(e)
        pass