from django.shortcuts import render
from .models import Job, Uni
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
def hello(request):
  return HttpResponse("Hello World")

def index(request):
  jobs = Job.objects.filter(lang="de")
  paginator = Paginator(jobs, 50)
  page_number = request.GET.get("page", 1)
  page_obj = paginator.get_page(page_number)
  return render(request, "index.html", { "jobs": page_obj })