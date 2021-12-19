from django.urls import path 
from . import views 

app_name="jobs"
urlpatterns = [
    path("suche/", views.search, name = "search"),
    path("", views.index, name = "index")
]
