from django.urls import path
from . import views



urlpatterns = [
    path('', views.calendar),
    path('get/<id>', views.get_data, name='get_data'),
]