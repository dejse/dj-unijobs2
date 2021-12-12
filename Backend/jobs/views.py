from django.shortcuts import render
from .models import Job, Uni
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def index(request):
  jobs = Job.objects.filter(lang="de").order_by("deadline")
  paginator = Paginator(jobs, 50)
  page_number = request.GET.get("page", 1)
  page_obj = paginator.get_page(page_number)
  return render(request, "index.html", { "jobs": page_obj })


def search(request):
  pass 