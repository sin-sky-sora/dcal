from django.urls import path,include
from .views import index,get_event,event_regist
urlpatterns = [
    path("",index,name="index"),
    path("g/",get_event,name="get_event"),
    path("post/",event_regist,name="post"),
]