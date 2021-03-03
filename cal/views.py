from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.core.serializers import serialize
from django.views.generic import TemplateView,FormView
from .models import CalendarModel
# Create your views here.
import json
from datetime import datetime,timezone,timedelta

def index(request):
    return render(request,"cal/index.html",{"test":"text"})

def get_event(request):
    start = request.GET["start"]
    end = request.GET["end"]
    print(start)
    # 2021-02-28T00:00:00+09:00
    print(end)
    # 2021-04-11T00:00:00+09:00
    # create_time = datetime(2021,3,3,15,0,0).isoformat() + "+09:00"
    
    time_format = datetime(2021,3,3,15,0,0,tzinfo=timezone(timedelta(hours=9))).isoformat()
    # '2021-03-03T15:00:00+09:00'
    # model save時
    # model.start = datetime(2021,3,3,15,0,0,tzinfo=timezone(timedelta(hours=9)))
    print(datetime.fromisoformat(time_format) > datetime.fromisoformat(start))
    event = [
        {
            "title":"経験値3倍",
            "start":"2021-03-04",
            "end":"2021-03-04"
        },
        {
            "title":"経験値3倍",
            "start":"2021-03-08T10:00:00",
            "end":"2021-03-08T21:00:00"
        },{
            "title":"メンテ",
            "start": "2021-03-10T10:30:00",
            "end": "2021-03-10T16:00:00"
        }
        ]
    data = CalendarModel.objects.all()
    event = []
    for k in data:
        event.append(k.cal_data)
    return JsonResponse(event,safe=False)
def event_regist(request):
    context = {
        "foo": "poster"
    }
    return render(request,"cal/post.html",{"context":context})

def event_set(request):
    if request.method == "POST":
        return HttpResponse("POST")
    return HttpResponse("GET")