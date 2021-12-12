from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Job, Uni
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape


# Create your views here.
def index(request):
  jobs = Job.objects.filter(lang="de").order_by("deadline")
  paginator = Paginator(jobs, 50)
  page_number = request.GET.get("page", 1)
  page_obj = paginator.get_page(page_number)
  return render(request, "index.html", { "jobs": page_obj })


def search(request):
  if request.method == "GET":
    q = escape(request.GET.get("q", ""))
    if len(q) > 0: 
      q = q.lower().split(" ")
      return HttpResponse("It works!")
    else: 
      return redirect(reverse("jobs.index")) 
  pass 