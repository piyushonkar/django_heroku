from django.urls import path,re_path
from . import views
from django.conf.urls import url

app_name='games'

urlpatterns =[
    path("",views.start,name='start'),
    path("calculate/",views.calculate,name='calculate'),
    re_path(r'^add_deletion/$',views.add_deletion,name='add_deletion'),
    path("add_deletion/add_symptom/",views.add_symptom,name='add_symptom'),
    path("add_deletion/add_disease/",views.add_disease,name='add_disease'),
    path("add_deletion/add_dominant/",views.add_dominant,name='add_dominant'),
    path("add_deletion/view_symptom/",views.view_symptom,name='view_symptom'),
    path("add_deletion/view_disease/",views.view_disease,name='view_disease'),
    path("add_deletion/delete_symptom/",views.delete_symptom,name='delete_symptom'),
]