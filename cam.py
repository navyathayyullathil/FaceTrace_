import numpy as np
import cv2
from flask import render_template

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
import time
from tkinter import *
cap = cv2.VideoCapture(0)
WORD = re.compile(r'\w+')
import pymysql
con=pymysql.connect(host='localhost', port=3306,user='root',password='',db='attendance_face')
cmd=con.cursor()
fn=''


while(True):
		try:
			ret, img = cap.read()
			# img=cv2.imread(fn)
			print(ret)

			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			print("length"+str(len(faces)))
			for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image


			emolist=[]
			cv2.imshow("Frame",img)

		except Exception as e:
			print("ee",e)
