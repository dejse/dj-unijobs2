from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Job, Uni
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape
from pprint import pprint


# Create your views here.
def index(request):
  jobs = Job.objects.filter(lang="de").order_by("deadline")
  paginator = Paginator(jobs, 50)
  page_number = request.GET.get("page", 1)
  page_obj = paginator.get_page(page_number)
  htmx = bool(request.headers.get("Hx-Request", False))
  if htmx:
    return render(request, "components/fragments/hx_table.html", { "jobs": page_obj })
  else:
    return render(request, "index.html", { "jobs": page_obj, "search_input": "" })


def search(request):
  q = escape(request.GET.get("q", "").strip())
  search_params = q.lower().split(" ")
  if len(q) > 0 and len(search_params) <= 3: 
    qs = Job.objects.filter(lang="de").select_related("uni")
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
    return redirect(reverse("jobs.index"))
