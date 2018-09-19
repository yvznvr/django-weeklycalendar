
django-weeklycalendar
=====================


django-weeklycalendar is a simple calendar that keep activities and publish it with people in weekly form.

Quick Start
-----------

1. Install django-weeklycalendar
    
    pip install django-weeklycalendar
    
2. Add django-weeklycalendar to your INSTALLED_APPS in setting.py

    INSTALLED_APPS = [
        ...
        'django-weeklycalendar',
    ]
    
3. Include the polls URLconf in your project urls.py
    path('calendar', include("Calendar.urls"))
    
4. Make migrations
    ./manage.py makemigrations
    ./manage.py migrate
    
5. Start your project and test app
