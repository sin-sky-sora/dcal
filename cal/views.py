from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.core.serializers import serialize
from django.views.generic import TemplateView,FormView
from .models import CalendarModel,TestModel
# Create your views here.
import json
from datetime import datetime,timezone,timedelta

# タイムゾーンの作成
JST = timezone(timedelta(hours=9),"JST")

def index(request):
    return render(request,"cal/index.html",{"test":"text"})

def get_event(request):
    start = request.GET["start"]
    end = request.GET["end"]
    # 2021-02-28T00:00:00+09:00
    # 2021-04-11T00:00:00+09:00
    print(start,end)
    start_time = datetime.strptime(start,"%Y-%m-%dT%H:%M:%S%z")
    end_time = datetime.strptime(end,"%Y-%m-%dT%H:%M:%S%z")
    print(start_time.isoformat(),end_time.isoformat())
    # 開始日がstart以上で終了日がend未満
    datas = TestModel.objects.filter(startDay__gte=start_time,endDay__lt=end_time)
    event = []
    for data in datas:
        eve = {}
        eve["id"] = data.pk
        eve["title"] = data.title
        eve["start"] = data.startDay
        eve["end"] = data.endDay
        event.append(eve)
    return JsonResponse(event,safe=False)
def event_regist(request):
    context = {
        "foo": "登録フォーム"
    }
    return render(request,"cal/post.html",{"context":context})
    
TimeFormatStyle = "%Y-%m-%d %H:%M"
def event_set(request):
    context = {"type":"failed"}
    if request.method == "POST":
        title = request.POST["title"]
        start = request.POST["startDay"]
        start_time = datetime.strptime(start,TimeFormatStyle).astimezone(JST)
        end = request.POST["endDay"]
        end_time = datetime.strptime(end,TimeFormatStyle).astimezone(JST)

        if(title and end_time > start_time):
            context["type"] = "success"
            model = TestModel()
            model.title = title
            model.startDay = start_time
            model.endDay = end_time
            model.save()
        elif title:
            context["message"] = "incorrect for date"
            context["error"] = "date"
        elif end_time > start_time:
            context["message"] = "incorrect for title"
            context["error"] = "title"
        else:
            context["message"] = "incorrect for all"
            context["error"] = "all"
    else:
        context["message"] = "incorrect for method"
        context["error"] = "method"
    return render(request,"cal/index.html",{"context":context})