
django-weeklycalendar
=====================


django-weeklycalendar is a simple calendar that keep activities and publish it with people in weekly form.

Quick Start
-----------

1. Install django-weeklycalendar and python-dateutil
    
    pip install django-weeklycalendar
    pip install python-dateutil
    
2. Add django-weeklycalendar to your INSTALLED_APPS in setting.py

    INSTALLED_APPS = [
        ...
        'Calendar',
    ]
    
3. Include the polls URLconf in your project urls.py
    path('calendar', include("Calendar.urls"))
    
4. Make migrations
    ./manage.py makemigrations
    ./manage.py migrate
    
5. Start your project and test app

![](https://screenshotscdn.firefoxusercontent.com/images/eb6f9804-7615-4613-859c-944efa795de0.png)

![](https://screenshotscdn.firefoxusercontent.com/images/74a4ce0c-3d11-4d26-b926-7085eaad684a.png)
