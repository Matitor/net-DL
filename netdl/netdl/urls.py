from django.urls import include,path
from dl import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
  path(r'dl/',views.get,name='dl-get')    
]
