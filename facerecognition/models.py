from django.db import models
from django.db.models.signals import post_delete, pre_save, post_save
from facerecognition.retrain import retrain
from django.dispatch import receiver
from backend.settings import MEDIA_ROOT
from pip._vendor.distlib._backport import shutil
from django.core.files import File
from django.core.files.base import ContentFile
from importlib import reload
from PIL import Image
import cv2
import os




# TODO; 
# This does not work for PUT request. FIX ASAP 

def get_person_folder(instance, filename):
	# file will be uploadedto MEDIA/ROOT/<identification>/<filename>
	return '%s/%s/%s' %('users', instance.identification, filename)


# Person Model

# Django primary key is overridden and is set to the uuid (identification)
class Person(models.Model):
	'Initialise Main table of face and its databases.........'
	identification = models.CharField(primary_key=True, max_length=200, unique=True)
	Front_Face = models.ImageField(upload_to= get_person_folder, blank=False)
	Top_Face = models.ImageField(upload_to= get_person_folder, blank=False)
	Right_Face = models.ImageField(upload_to= get_person_folder, blank=False)
	Left_Face = models.ImageField(upload_to= get_person_folder, blank=False)
	Bottom_Face = models.ImageField(upload_to= get_person_folder, blank=False)

	Front_Face_masked = models.ImageField(upload_to= get_person_folder, blank=True)
	Top_Face_masked = models.ImageField(upload_to= get_person_folder, blank=True)
	Right_Face_masked = models.ImageField(upload_to= get_person_folder, blank=True)
	Left_Face_masked = models.ImageField(upload_to= get_person_folder, blank=True)
	Bottom_Face_masked = models.ImageField(upload_to= get_person_folder, blank=True)

	time_reg=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.identification



# After the deletion of a Person object, it's files are deleted and
# the encodings are retrained
@receiver(post_delete, sender=Person)
def delete_person(sender, instance, **kwargs):
	# instance.Front_Face.storage.delete(instance.Front_Face.name)
	if os.path.exists(MEDIA_ROOT + "/users/" + instance.identification):
		shutil.rmtree(MEDIA_ROOT + "/users/" + instance.identification)
	# retrain() # To retrain after deletion




class Config(models.Model):
	attendance_frame_threshold = models.IntegerField(default=5)
	detection_sensitivity = models.DecimalField(max_digits=4, decimal_places=2, default=0.45)
	stayback_frame_theshold = models.IntegerField(default=2)
	no_teacher_frame_threshold = models.IntegerField(default=2)
	frame_rate = models.IntegerField(default=1)
	ai_model = models.CharField(max_length=200, default="mtcnn")

	def __str__(self):
		return 'CONFIG'
	
		
