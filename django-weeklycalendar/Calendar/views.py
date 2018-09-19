from django.shortcuts import render
from datetime import date, timedelta, datetime
from .models import Activity
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def convert_data(activities_object):
    """
    get result of query and translate it serializable format
    """
    data = []
    for i in activities_object:
        data.append({'id':i.id, 'title':i.__str__(), 'color':i.color, 'date':str(i.date.day),
            'start_time':str(int(str(i.start_time)[0:2])), 'finish_time':str(int(str(i.finish_time)[0:2]))})
    return data


@login_required()
def calendar(request):
    first_day = date.today().weekday()
    first_day = timedelta(days=first_day)
    first_day = date.today() - first_day
    way = [-1,1]
    try:
        way[0] = int(request.GET['n']) - 1
        way[1] = int(request.GET['n']) + 1
        delta = timedelta(days=int(request.GET['n']) * 7)
        first_day = first_day + delta
    except:
        pass
    # get activities between monday and sunday
    activities = Activity.objects.filter(user=request.user, date__range=(first_day, first_day+timedelta(days=6)))
    activities = convert_data(activities)   # get this data with js for draw activies on table
    week = []
    year = first_day.year
    month = first_day.month
    for i in range(7):
        delta = timedelta(days=i)
        week.append(datetime.strftime((first_day+delta), "%d-%B"))
    return render(request, "Calendar/WeaklyCalendar.html", {'activities' : activities,'week' : week,
                            'year' : year, 'range7' : range(7), 'range24' : range(24), 'month' : month, 'way' : way})


def view_page(request, user):
    first_day = date.today().weekday()
    first_day = timedelta(days=first_day)
    first_day = date.today() - first_day
    way = [-1,1]
    try:
        way[0] = int(request.GET['n']) - 1
        way[1] = int(request.GET['n']) + 1
        delta = timedelta(days=int(request.GET['n']) * 7)
        first_day = first_day + delta
    except:
        pass

    try:
        user = User.objects.get(username=user)
        activities = Activity.objects.filter(user=user, private=False, date__range=(first_day, first_day + timedelta(days=6)))
    except:
        return HttpResponseNotFound()

    activities = convert_data(activities)   # get this data with js for draw activies on table
    week = []
    year = first_day.year
    month = first_day.month
    for i in range(7):
        delta = timedelta(days=i)
        week.append(datetime.strftime((first_day+delta), "%d-%B"))
    return render(request, "Calendar/ReadCalendar.html", {'activities' : activities,'week' : week,
                            'year' : year, 'range7' : range(7), 'range24' : range(24), 'month' : month, 'way' : way})




@login_required()
def get_data(request, id):
    if(request.method != 'GET'):
        return HttpResponseNotFound()
    try:
        data = Activity.objects.get(id=id)
        data = Activity.objects.filter(title=data.title, start_time=data.start_time,
                                      finish_time=data.finish_time).first()
    except:
        return HttpResponseNotFound()
    data = {'id':data.id, 'title':data.title, 'date':data.date.__str__(), 'start_time':data.start_time.__str__(),
            'finish_time':data.finish_time.__str__(), 'repeat_fre':data.repeat_fre, 'repeat_time':data.repeat_time,
            'location':data.location, 'color':data.color, 'private':data.private, 'comment':data.comment}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def delete_data(request, id):
    if(request.method != 'GET'):
        return HttpResponseNotFound()
    try:
        Activity.objects.get(id=id).delete()
        return HttpResponse()
    except:
        return HttpResponseNotFound()


@login_required()
def save_data(request, id):
    # id = 0 means new activity
    if(id != "0"):
        try:
            act = Activity.objects.get(id=id, user_id=request.user.id)
        except:
            return HttpResponseNotFound()
    else:
        act = Activity(user_id=request.user.id)

    act.title = request.POST['title']
    act.date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
    act.start_time = datetime.strptime(request.POST.get('start_time'), '%H:%M:%S')
    act.finish_time = datetime.strptime(request.POST.get('finish_time'), '%H:%M:%S')
    act.location = request.POST['location']
    act.color = request.POST['color']
    act.private = request.POST['private'] == 'true'
    act.comment = request.POST['comment']
    act.repeat_fre = request.POST['repeat_fre']
    act.repeat_time = int(request.POST['repeat_time'])
    act.save()

    return HttpResponse(json.dumps({'success': True}),content_type="application/json")
