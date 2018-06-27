from django.urls import path
from . import views
from django.conf.urls import url

app_name='games'

urlpatterns =[
    path("",views.start,name='start'),
    path("calculate/",views.calculate,name='calculate')
]