from django.urls import path, re_path
from rest_framework import routers 
from facerecognition import views




router = routers.DefaultRouter()

# URL to register person face
router.register('reg', views.PersonViewSet)


'''

GET - recog/reg/ - JSON of all Person with images
POST - recog/reg/ ->body -> BASE64 Images and identification in an HTML Form - creates Person  

'''

urlpatterns = [
    path('retrain', views.rtrain),
    path('responser/detect/', views.accept),
    path('responser/entry/', views.entry)
]

urlpatterns += router.urls

'''


'''
# TODO;
# Change REGEX basesd on required rtsp stream






