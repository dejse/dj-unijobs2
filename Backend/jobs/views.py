from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Job, Uni
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape
from django.utils.translation import get_language, activate
from pprint import pprint


# Create your views here.
def index(request):
  # request parameters
  language = get_language()
  page_number = request.GET.get("page", 1)
  htmx = bool(request.headers.get("Hx-Request", False))

  # ORM
  jobs = Job.objects.filter(lang=language).order_by("deadline")
  paginator = Paginator(jobs, 50)
  page_obj = paginator.get_page(page_number)

  # response
  if htmx:
    response = render(request, "components/fragments/hx_table.html", { "jobs": page_obj })
  else:
    response = render(request, "index.html", { "jobs": page_obj, "search_input": "" })
  response.set_cookie("django-language", language, max_age = 60*60*24*365, secure=True, httponly=True)
  return response


def search(request):
  # request parameters
  language = get_language()
  q = escape(request.GET.get("q", "").strip())
  search_params = q.lower().split(" ")

  # not more than three words
  if len(q) > 0 and len(search_params) <= 3: 
    qs = Job.objects.filter(lang=language).select_related("uni")
    data = Job.objects.none()
    for s in search_params:
      data = data.union(qs.filter(
        Q(institute__icontains=s) 
        | Q(title__icontains=s)
        | Q(uni__name_de__icontains=s) 
      ))
    data = data.order_by("deadline")
    return render(request, "index.html", { "jobs": data, "search_input": q })
  else: 
    return redirect(reverse("jobs:index"))