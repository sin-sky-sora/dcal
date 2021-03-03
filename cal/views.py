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
DayTimeFormatStyle = "%Y-%m-%d %H:%M"
DayOnlyFormatStyle = "%Y-%m-%d"
def index(request):
    if request.method == "GET":
        return render(request,"cal/index.html")
    elif request.method == "POST":
        context = {"type":"failed"}
        title = request.POST["title"]
        days = request.POST["thisDay"]
        startTime = request.POST["startTime"]
        endTime = request.POST["endTime"]
        alldays = request.POST["types"]
        if title and days and endTime and startTime and alldays:
            if alldays == "times":
                all_day = False
                start = days + " " +startTime
                start_time = datetime.strptime(start,DayTimeFormatStyle).astimezone(JST)
                end = days + " " + endTime
                end_time = datetime.strptime(end,DayTimeFormatStyle).astimezone(JST)
            elif alldays == "allday":
                all_day = True
                start = days + " 09:00"
                start_time = datetime.strptime(start,DayTimeFormatStyle).astimezone(JST)
                end = days + " 10:00"
                end_time = datetime.strptime(end,DayTimeFormatStyle).astimezone(JST)
            else:
                context["error"] = "radio"
                context["message"] = "incorrect for radio"
                return render(request,"cal/index.html",{"context":context})
            if(end_time > start_time):
                context["type"] = "success"
                model = TestModel()
                model.title = title
                model.startDay = start_time
                model.endDay = end_time
                model.allday = all_day
                model.save()
            else:
                context["message"] = "incorrect for date"
                context["error"] = "date"
        else:
            context["message"] = "Not enough information"
            context["error"] = "lack"
    else:
        context["message"] = "incorrect for method"
        context["error"] = "method"
    return render(request,"cal/index.html",{"context":context})
    
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
        if data.allday:
            eve["start"] = data.startDay.strftime("%Y-%m-%d")
        else:
            eve["start"] = data.startDay.strftime("%Y-%m-%dT%H:%M")
            eve["end"] = data.endDay.strftime("%Y-%m-%dT%H:%M")
        event.append(eve)
    return JsonResponse(event,safe=False)
def event_regist(request):
    context = {
        "foo": "登録フォーム"
    }
    return render(request,"cal/post.html",{"context":context})


