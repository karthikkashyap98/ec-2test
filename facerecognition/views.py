from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
#use celery from libary as decorator
from rest_framework import viewsets
from facerecognition.models import Person, Config
from facerecognition.serializers import PersonSerializer
from facerecognition.retrain import retrain
import base64
from django.core.files.base import ContentFile
from django.core.files import File
from facerecognition.feed import responser2, entry_detect
import json
from django.shortcuts import get_object_or_404
from . import detect_recognise_hog2
from importlib import reload 
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import os
import cv2
from backend.settings import MEDIA_ROOT

def index(request):
			
	return render(request, 'frontend/index.html')


# Person Viewset

# This now handles BASE64 responses 
 
class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer

	def create(self, request):
		identification = request.data['identification']
		Front_Face = request.data['Front_Face']
		Top_Face = request.data['Top_Face']
		Right_Face = request.data['Right_Face']
		Left_Face = request.data['Left_Face']
		Bottom_Face = request.data['Bottom_Face']
		
		formt_front, imgstr_front = Front_Face.split(';base64,')
		ext_front = formt_front.split('/')[-1]
		
		formt_top, imgstr_top = Top_Face.split(';base64,')
		ext_top = formt_top.split('/')[-1]

		formt_right, imgstr_right = Right_Face.split(';base64,')
		ext_right = formt_right.split('/')[-1]

		formt_left, imgstr_left = Left_Face.split(';base64,')
		ext_left = formt_left.split('/')[-1]
		
		formt_bottom, imgstr_bottom = Bottom_Face.split(';base64,')
		ext_bottom = formt_bottom.split('/')[-1]

		Front_Face = ContentFile(base64.b64decode(imgstr_front), name='front.' + ext_front)			# front.jpeg

		Top_Face = ContentFile(base64.b64decode(imgstr_top), name='top.' + ext_top)					# top.jpeg
		
		Right_Face = ContentFile(base64.b64decode(imgstr_right), name='right.' + ext_right)			# right.jpeg

		Left_Face = ContentFile(base64.b64decode(imgstr_left), name='left.' + ext_left)				# left.jpeg

		Bottom_Face = ContentFile(base64.b64decode(imgstr_bottom), name='bottom.' + ext_bottom)		# bottom.jpeg

		person = Person(identification = identification,
		Front_Face= Front_Face,
		Right_Face = Right_Face,
		Left_Face = Left_Face,
		Bottom_Face = Bottom_Face,
		Top_Face = Top_Face)

		person.save()

		return HttpResponse()



	# PATCH request is handled by first deleting the previous entry from the db and recreating the object 
	# This is done so because, the PATCH request by itself does not save the images dynamically. And also by deleting the object, the images linked to that model are deleted and a new object is created (which stores the images dynamically). 

	def partial_update(self, request, pk):
		Front_Face = request.data['Front_Face']
		Top_Face = request.data['Top_Face']
		Right_Face = request.data['Right_Face']
		Left_Face = request.data['Left_Face']
		Bottom_Face = request.data['Bottom_Face']
		
		formt_front, imgstr_front = Front_Face.split(';base64,')
		ext_front = formt_front.split('/')[-1]
		
		formt_top, imgstr_top = Top_Face.split(';base64,')
		ext_top = formt_top.split('/')[-1]

		formt_right, imgstr_right = Right_Face.split(';base64,')
		ext_right = formt_right.split('/')[-1]

		formt_left, imgstr_left = Left_Face.split(';base64,')
		ext_left = formt_left.split('/')[-1]
		
		formt_bottom, imgstr_bottom = Bottom_Face.split(';base64,')
		ext_bottom = formt_bottom.split('/')[-1]

		Front_Face = ContentFile(base64.b64decode(imgstr_front), name='front.' + ext_front)

		Top_Face = ContentFile(base64.b64decode(imgstr_top), name='top.' + ext_top)
		
		Right_Face = ContentFile(base64.b64decode(imgstr_right), name='right.' + ext_right)

		Left_Face = ContentFile(base64.b64decode(imgstr_left), name='left.' + ext_left)

		Bottom_Face = ContentFile(base64.b64decode(imgstr_bottom), name='bottom.' + ext_bottom)

		Person.objects.get(pk=pk).delete()
		
		Person.objects.create(
		identification = pk, 
		Front_Face= Front_Face,
		Right_Face = Right_Face,
		Left_Face = Left_Face,
		Bottom_Face = Bottom_Face,
		Top_Face = Top_Face)	
					
		return HttpResponse()



# Retrains with all faces and returns the stats of number of users added and updated

def rtrain(request):
	message = retrain()
	resp = {"msg" : message}
	return HttpResponse(json.dumps(resp))


# View to handle each frame
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def accept(request):
	frame = request.data["frame"]
	print(len(frame))
	# print(frame.shape())
	config = Config.objects.get(pk=1)
	sensitivity = config.detection_sensitivity
	detected_frame = responser2(frame, sensitivity)
	return Response({"msg": detected_frame})


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def entry(request):
	frame = request.data["frame"]
	config = Config.objects.get(pk=1)
	sensitivity = config.detection_sensitivity
	value = entry_detect(frame, sensitivity)
	print(value)
	value = {"users" : value}
	return Response(value)