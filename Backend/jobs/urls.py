from django.urls import path 
from . import views 

urlpatterns = [
    path("hello/", views.hello, name="jobs.hello"),
    path("", views.index, name = "jobs.index")
]
