from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Job, Uni
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape
from django.utils.translation import get_language, activate
from .forms import SearchForm
from pprint import pprint


# Create your views here.
def index(request):
  # request parameters
  language = get_language()
  page_number = request.GET.get("page", 1)
  is_htmx = bool(request.headers.get("Hx-Request", False))

  # ORM
  jobs = Job.objects.filter(lang=language).order_by("deadline")
  paginator = Paginator(jobs, 50)
  page_obj = paginator.get_page(page_number)

  # response
  if is_htmx:
    response = render(request, "components/fragments/hx_table.html", { "jobs": page_obj })
  else:
    response = render(request, "index.html", { "jobs": page_obj })
  return response


def search(request):
  # request parameters
  language = get_language()
  
  # form
  form = SearchForm(request.POST or None)
  if form.is_valid():
    job = form.cleaned_data["job"]
    uni = form.cleaned_data["uni"]
    
    if len(job) == 0 and len(uni) == 0: 
      return redirect(reverse("jobs:index"))
    else:
      # Filter Queryset
      qs = Job.objects.filter(lang=language).select_related("uni").order_by("deadline")
      if len(job) > 0: 
        qs = qs.filter(Q(title__icontains=job))
      if len(uni) > 0:
        qs = qs.filter(
          Q(institute__icontains=uni) 
          | Q(uni__name_de__icontains=uni) 
          | Q(uni__name_en__icontains=uni)
          )
      return render(request, "index.html", { "jobs": qs, "form": form })
  else:
    return redirect(reverse("jobs:index"))
