from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static 
from facerecognition.views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index), 
    path('recog/', include('facerecognition.urls')),
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)