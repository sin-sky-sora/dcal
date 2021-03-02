from django.urls import path,include
from .views import index,get_event
urlpatterns = [
    path("",index,name="index"),
    path("g/",get_event,name="get_event"),
]