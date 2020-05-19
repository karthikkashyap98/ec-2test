import cv2
from importlib import reload 
from facerecognition import detect_recognise_hog2
from django.http import StreamingHttpResponse
from backend.settings import BASE_DIR, MEDIA_ROOT, MODEL_ROOT
import json
from django.shortcuts import HttpResponse
from django.utils import timezone
from datetime import datetime
import random
import time
import os
from django.templatetags.static import static
import base64
import numpy as np


class Video(object):
	def __init__(self,urls=None):
		self.urls=urls
		self.video = cv2.VideoCapture(self.urls)


	def __del__(self):
		self.video.release()
		# Release the video camera 


	def get_frame(self):
		
		_, frame = self.video.read()
		
		################################################################
		_ret, jpeg = cv2.imencode('.jpg', frame)
		
		return jpeg.tobytes()

	def get_frame_video(self,attandance=None):
		
		ret, frame = self.video.read()
		while True:
			if ret:
			################################################################
				_ret, jpeg = cv2.imencode('.jpg', frame)
				# print( type(frame), type(jpeg))
				
				return frame, jpeg.tobytes()
			else:
				return None, None

def unique(list1): 
  
	# intilize a null list 
	unique_list = [] 
	  
	# traverse for all elements 
	for x in list1: 
		# check if exists in unique_list or not 
		if x not in unique_list: 
			unique_list.append(x) 
	return unique_list



def gen(camera):
	while True:
		frame = camera.get_frame()
		
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


		

def entry_detect(frame, sensitivity):
# Detect each frame
	frame = readb64(frame)
	detected_frame, detected_user = detect_recognise_hog2.det_recog_engine_hog(frame, sensitivity, recog = True, get_unknowns=False)
	# cv2.imwrite("test.jpg", detected_frame)     # Check
	return detected_user

# Convert Base64 to np frame
def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def responser2(frame, sensitivity):
	# frame = readb64(frame)
	frame = np.array(frame, dtype=np.uint8)
	# print(frame.shape())
	# cv2.imwrite("test.jpg", frame)     # Check
	detected_frame, detected_user = detect_recognise_hog2.det_recog_engine_hog(frame, sensitivity, recog = True, get_unknowns=False)
	return detected_user
