from django.shortcuts import render
from datetime import date, timedelta, datetime
from .models import Activity
import json
from django.http import HttpResponse, HttpResponseNotFound

def convert_data(activities_object):
    """
    get result of query and translate it serializable format
    """
    data = []
    for i in activities_object:
        data.append({'id':i.id, 'title':i.__str__(), 'date':str(i.date.day), 
            'start_time':str(int(str(i.start_time)[0:2])), 'finish_time':str(int(str(i.finish_time)[0:2]))})
    return data


def calendar(request):
    first_day = date.today().weekday()
    first_day = timedelta(days=first_day)
    first_day = date.today() - first_day
    # get activities between monday and sunday
    activities = Activity.objects.filter(user=request.user, date__range=(first_day, first_day+timedelta(days=6)))
    activities = convert_data(activities)   # get this data with js for draw activies on table
    week = []
    year = first_day.year
    for i in range(7):
        delta = timedelta(days=i)
        week.append(datetime.strftime((first_day+delta), "%d-%B"))
    return render(request, "WeaklyCalendar.html", {'activities' : activities,'week' : week,
                            'year' : year, 'range7' : range(7), 'range24' : range(24)})


def get_data(request, id):
    if(request.method != 'GET'):
        return HttpResponseNotFound()
    try:
        data = Activity.objects.get(id=id)
    except:
        return HttpResponseNotFound()
    data = {'id':data.id, 'title':data.title, 'date':data.date.__str__(), 'start_time':data.start_time.__str__(),
            'finish_time':data.finish_time.__str__(), 'repeat_fre':data.repeat_fre, 'repeat_time':data.repeat_time,
            'location':data.location, 'color':data.color, 'private':data.private, 'comment':data.comment}
    return HttpResponse(json.dumps(data), content_type="application/json")