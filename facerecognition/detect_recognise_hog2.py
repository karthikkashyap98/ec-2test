#import essentials
import cv2
import os
import pickle
import numpy as np
from PIL import Image
import face_recognition
from datetime import datetime
# from mtcnn.mtcnn import MTCNN
from backend.settings import BASE_DIR, MODEL_ROOT, MEDIA_ROOT, UNKNOWN_ROOT


start = datetime.now()

# create the detector, using default weights
# detector = MTCNN()

#set detection threshold, lesser values gives stronger detection i,e chances of unknowns are high



#define paths
VISITOR_MEDIA_DIR = os.path.join(MEDIA_ROOT, 'users')
MODEL_DIR =  os.path.join(MODEL_ROOT,"user_face_encodings") 
UNKNOWN_DIR = os.path.join(MEDIA_ROOT, 'unknown')
UNKNOWN_MODEL_DIR = os.path.join(MODEL_ROOT, "unknown_face_encodings")
# PRESENT_VISITOR_MODEL_DIR = "/home/pawan/Documents/FG002-VMS/codes/data/models/present_visitor_model_dir"


#load existing models
try:
	with (open(os.path.join(MODEL_DIR,"encodings.pickle"), "rb")) as openfile:
		while True:
			try:
				users_data = pickle.load(openfile)
				known_face_encodings = users_data["encodings"]
				known_face_names  = users_data["names"]
			except EOFError:
				print("known_faces initialised")
				break
except:
	known_face_encodings = []
	known_face_names = []
	print("empty known_faces initialised")

try:
	with (open(os.path.join(UNKNOWN_MODEL_DIR,"unknown_encodings.pickle"), "rb")) as openfile:
		while True:
			try:
				unknown_users_data = pickle.load(openfile)
				unknown_face_encodings = unknown_users_data["encodings"]
				unknown_face_names  = unknown_users_data["names"]
			except EOFError:
				break
except:
	unknown_face_encodings = []
	unknown_face_names = [] 
	print("empty unknown_faces initialised")
			
# try:
#     with (open(os.path.join(PRESENT_VISITOR_MODEL_DIR,"present_visitor_encodings.pickle"), "rb")) as openfile:
#         while True:
#             try:
#                 present_visitor_data = pickle.load(openfile)
#                 present_visitor_face_encodings = present_visitor_data["encodings"]
#                 present_visitor_face_names  = present_visitor_data["names"]
#             except EOFError:
#                 break
# except:
#     present_visitor_face_encodings = []
#     present_visitor_face_names = []   
#     print("empty present_visitor_faces initialised")
	 

if not os.path.isdir(VISITOR_MEDIA_DIR):
	os.mkdir(VISITOR_MEDIA_DIR)
if not os.path.isdir(MODEL_DIR):
	os.mkdir(MODEL_DIR)
if not os.path.isdir(UNKNOWN_DIR):
	os.mkdir(UNKNOWN_DIR)
if not os.path.isdir(UNKNOWN_MODEL_DIR):
	os.mkdir(UNKNOWN_MODEL_DIR)
# if not os.path.isdir(PRESENT_VISITOR_MODEL_DIR):          #This is handle current visitors
	# os.mkdir(PRESENT_VISITOR_MODEL_DIR) 
print("All directories checked and created")
	
	
	
#function to match faces
def recognise_face(roi, sensitivity, faces, frame, get_unknowns):
	face_locations = []
	face_locations.append(faces)
	#print(face_locations)
	face_encodings = face_recognition.face_encodings(roi, face_locations)
	if len(known_face_encodings)>0:
		"""this function checks the faces and returns detected users
		face_recognition api is used here"""
		face_names = []
		det_user=[]
		matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
		#commpare if all value of match is true
		face_distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
		best_match_index = np.argmin(face_distances)
		# print(face_distances)
		if matches[best_match_index] and face_distances[best_match_index]<= sensitivity:
			name = known_face_names[best_match_index]
			#print(name)              #Check: detected users
			return name
		else:
			unknown_user = "Unknown"
			if get_unknowns== True:
				unknown_user = handle_unknowns(frame, sensitivity, faces, face_encodings)
			#cv2.imwrite(f_name, u_roi)
			return unknown_user
	else:
			unknown_user = "Unknown"
			if get_unknowns== True:
				unknown_user = handle_unknowns(frame, sensitivity, faces, face_encodings)
			#cv2.imwrite(f_name, u_roi)
			return unknown_user

def det_recog_engine_hog(frame, sensitivity, recog = True,get_unknowns=True ):
	"""This function will detect faces and returns bounding boxes
	if the boolean of recog is set true then detected faces are returned
	with name"""   
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	face_locations = face_recognition.face_locations(rgb, model = 'hog')
	#print("Faces detected, ", len(faces))   #chcek for number of faces detected
	detected_users_list = []
	area = 0
	for face in face_locations:
			#try:
			#print(face, type(face))
			y,width,height,x= face
			if recog==True:
				#roi= rgb[y:height, x:width]
				detected_user = recognise_face(rgb, sensitivity, face, frame,get_unknowns)
				detected_users_list.append(detected_user)
				cv2.putText(frame, detected_user, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)    
			# get coordinates
			frame = cv2.rectangle(frame, (x,y), (width, height), (255,0,0), 1)
			"""area = (x-width)*(y-height)
			cv2.putText(frame, str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)"""
				#cv2.imshow("recog", frame)   #check for knowing detected faces
				
			"""except:
				  return frame,detected_users_list,area"""
	return frame,detected_users_list



# def det_recog_engine_mtcnn(frame, sensitivity, recog = True,get_unknowns=True):
# 	"""This function will detect faces and returns bounding boxes
# 	if the boolean of recog is set true then detected faces are returned
# 	with name"""   
	
# 	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# 	mtcnn_faces = detector.detect_faces(rgb)
	
# 	# print(mtcnn_faces)
# 	# face_locations = face_recognition.face_locations(rgb, model = 'hog')
# 	#print("Faces detected, ", len(faces))   #chcek for number of faces detected
# 	detected_users_list = []
# 	area = 0
# 	for m_face in mtcnn_faces:
# 			#try:
# 			#print(face, type(face))
# 			x, y, width, height = m_face['box']
# 			face = y, x+width, y+height,x  
# 			# cv2.imwrite('mtcnnface.jpg', frame[y:y+height, x:x+width])
# 			if recog==True:
# 				#roi= rgb[y:height, x:width]
# 				detected_user = recognise_face(rgb, sensitivity, face, frame,get_unknowns)
# 				detected_users_list.append(detected_user)
# 				cv2.putText(frame, detected_user, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)    
# 			# get coordinates
# 			frame = cv2.rectangle(frame, (x,y), (x+width, y+height), (255,0,0), 1)

# 			"""area = (x-width)*(y-height)
# 			cv2.putText(frame, str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)"""
# 				#cv2.imshow("recog", frame)   #check for knowing detected faces
				
# 			"""except:
# 				  return frame,detected_users_list,area"""
# 	return frame,detected_users_list



def handle_unknowns(roi, sensitivity, faces, face_encodings):
	"""Thisfunction checks if the unknowns face was previously seen or the first time its being seen,
	new face encodings are checked with known unknown faces to return unknonws name or creates a new unknown"""
	#Checks if the Unknown encodings list has encodings or its the first time an unknown face is being seen
	if len(unknown_face_encodings)>0:
		matches = face_recognition.compare_faces(unknown_face_encodings, face_encodings[0])
		#commpare if all value of match is true
		face_distances = face_recognition.face_distance(unknown_face_encodings, face_encodings[0])
		best_match_index = np.argmin(face_distances)
		
		if matches[best_match_index] and face_distances[best_match_index]<= sensitivity:
			unknown_name = unknown_face_names[best_match_index]
			#print(name)              #Check: detected users
			un_dir = os.path.join(UNKNOWN_DIR,unknown_name)
			list_dir_len = len(os.listdir(un_dir))
			#Checks if the number of photos of the identified unknown face are less than 6
			if list_dir_len<6:
				#here, if the faces are less than 6 then the faces are checked for how different they are from existing face and then saved
				if matches[best_match_index] and face_distances[best_match_index]>= (float(sensitivity)-0.10):
					unknown_face_encodings.append(face_encodings[0])
					unknown_face_names.append(unknown_name)
					img_name = (os.path.join(un_dir, "%d.jpg"%list_dir_len))
					cv2.imwrite(img_name, roi)            
			return unknown_name
		#if the new face doesnt match with any previously known unknown face 
		else:
			unknown_face_encodings.append(face_encodings[0])
			new_unknown = "unknown_%d"%(len(unknown_face_names)+1)
			un_dir = os.path.join(UNKNOWN_DIR,new_unknown)
			if not os.path.isdir(un_dir):
				os.mkdir(un_dir)
				cv2.imwrite(os.path.join(un_dir, "1.jpg"), roi)
			unknown_face_names.append(new_unknown)
			un_users_face_encodings = {"encodings": unknown_face_encodings, "names": unknown_face_names}
			f_u = open(os.path.join(UNKNOWN_MODEL_DIR,"unknown_encodings.pickle"), "wb")
			f_u.write(pickle.dumps(un_users_face_encodings))
			f_u.close()
			return unknown_face_names[-1]
	#Executes to handle corner case, i,e first time unknown
	else:
		unknown_face_encodings.append(face_encodings[0])
		unknown_face_names.append("unknown_1")
		un_dir = os.path.join(UNKNOWN_DIR,"unknown_1")
		if not os.path.isdir(un_dir):
			os.mkdir(un_dir)
			cv2.imwrite(os.path.join(un_dir, "1.jpg"), roi)
			
		un_users_face_encodings = {"encodings": unknown_face_encodings, "names": unknown_face_names}
		f_u = open(os.path.join(UNKNOWN_MODEL_DIR,"unknown_encodings.pickle"), "wb")
		f_u.write(pickle.dumps(un_users_face_encodings))
		f_u.close()
		
		return unknown_face_names[0]
		

# def register_visitor_hog(uuid):
# 	"""This function to be called to register a new user from reception desk
# 	Here, a new visitors photos are picked from the media root ro create encoding, append to a list and then rewrite the pickle file"""
# 	count = 0 
# 	for visitor_images in os.listdir(os.path.join(VISITOR_MEDIA_DIR,uuid)):
# 		#checks for image type
# 		if visitor_images.endswith(".jpg") or visitor_images.endswith(".jpeg"):
# 			frame = cv2.imread(os.path.join(VISITOR_MEDIA_DIR,uuid,visitor_images))
# 			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# 			#checks for faces, change from hog to cnn for better detection with higher time complexity

# 			face_locations = get_locations(rgb)
			
			
# 			#checks if the faces are found
# 			# print(face_locations)
# 			if len(face_locations[0])>0:
# 				face_encodings = face_recognition.face_encodings(rgb, face_locations)
# 				# print(len(face_encodings))
# 				# present_visitor_face_encodings.append(face_encodings[0])
# 				# present_visitor_face_names.append(uuid)
# 				known_face_encodings.append(face_encodings[0])
# 				known_face_names.append(uuid)
# 				count += 1
	
# 	#Visitor face encodings are appended to that days visitor list
# 	# visitor_face_encodings = {"encodings": present_visitor_face_encodings, "names": present_visitor_face_names}
# 	# f_vp = open(os.path.join(PRESENT_VISITOR_MODEL_DIR,"present_visitor_encodings.pickle"), "wb")
# 	# f_vp.write(pickle.dumps(visitor_face_encodings))
# 	# f_vp.close()
	
# 	#appended to all known lists
# 	all_known_face_encodings = {"encodings": known_face_encodings, "names": known_face_names}
# 	f_kf = open(os.path.join(MODEL_DIR,"encodings.pickle"), "wb")
# 	f_kf.write(pickle.dumps(all_known_face_encodings))
# 	f_kf.close()
	
# 	print(count, "Visitor Faces Registered Succesfully")


# def register_visitor_mtcnn(uuid):
# 	"""This function to be called to register a new user from reception desk
# 	Here, a new visitors photos are picked from the media root ro create encoding, append to a list and then rewrite the pickle file"""
# 	count = 0
# 	for visitor_images in os.listdir(os.path.join(VISITOR_MEDIA_DIR,uuid)):
# 		#checks for image type
# 		if visitor_images.endswith(".jpg") or visitor_images.endswith(".jpeg"):
# 			frame = cv2.imread(os.path.join(VISITOR_MEDIA_DIR,uuid,visitor_images))
# 			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# 			mtcnn_faces = detector.detect_faces(rgb)
# 			# print(mtcnn_faces)
# 			face_locations = [[]]
# 			x, y, width, height = mtcnn_faces[0]['box']
# 			face = (y, x+width, y+height, x)
# 			face_locations[0].append(face)
# 			#checks if the faces are found
# 			print(face_locations)
# 			if len(face_locations[0])>0:
# 				face_encodings = face_recognition.face_encodings(rgb, face_locations[0])
# 				# present_visitor_face_encodings.append(face_encodings[0])
# 				# present_visitor_face_names.append(uuid)
# 				known_face_encodings.append(face_encodings[0])
# 				known_face_names.append(uuid)
# 				count += 1
	
# 	#Visitor face encodings are appended to that days visitor list
# 	# visitor_face_encodings = {"encodings": present_visitor_face_encodings, "names": present_visitor_face_names}
# 	# f_vp = open(os.path.join(PRESENT_VISITOR_MODEL_DIR,"present_visitor_encodings.pickle"), "wb")
# 	# f_vp.write(pickle.dumps(visitor_face_encodings))
# 	# f_vp.close()
	
# 	#appended to all known lists
# 	all_known_face_encodings = {"encodings": known_face_encodings, "names": known_face_names}
# 	f_kf = open(os.path.join(MODEL_DIR,"encodings.pickle"), "wb")
# 	f_kf.write(pickle.dumps(all_known_face_encodings))
# 	f_kf.close()
	
# 	print(count, "Visitor Faces Registered Succesfully")	



# def get_locations(frame):
#     faces = detector.detect_faces(frame)
#     x, y, width, height = faces[0]['box']
#     top, right, bottom, left = y, x+width, y+height, x
#     return [(top,right,bottom, left)]