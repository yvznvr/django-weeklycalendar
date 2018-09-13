from django.shortcuts import render
from datetime import date, timedelta, datetime
from .models import Activity
import json

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

