from django.urls import path 
from . import views 

urlpatterns = [
    path("suche/", views.search, name = "jobs.suche"),
    path("", views.index, name = "jobs.index")
]
