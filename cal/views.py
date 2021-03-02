from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.core.serializers import serialize
from .models import CalendarModel
# Create your views here.
import json
from datetime import datetime

def index(request):
    return render(request,"cal/index.html",{"test":"text"})

def get_event(request):
    start = request.GET["start"]
    end = request.GET["end"]
    print(start)
    # 2021-02-28T00:00:00+09:00
    print(end)
    # 2021-04-11T00:00:00+09:00
    create_time = datetime(2021,3,3,15,0,0).isoformat() + "+09:00"
    
    p = datetime.fromisoformat(create_time)
    print(datetime.fromisoformat(create_time) > datetime.fromisoformat(start))
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

def set_event(request):
    return HttpResponse("HEllo")