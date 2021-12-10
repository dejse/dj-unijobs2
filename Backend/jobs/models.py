from django.db import models
from django.db.models import indexes
from django.db.models.base import Model

# Create your models here.
class Uni(models.Model):
  id = models.AutoField(primary_key=True)
  short = models.TextField(unique=True)
  name_de = models.TextField(null=False)
  name_en = models.TextField(null=False)
  location_de = models.TextField()
  location_en = models.TextField()

  class Meta:
    indexes = [ 
      models.Index(fields=["name_de"], name="idx_name_de"), 
      models.Index(fields=["name_en"], name="idx_name_en")
    ]

  def __str__(self):
    return self.name_de


class Job(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=300, unique=True)
  href = models.URLField()
  institute = models.TextField()
  deadline = models.CharField(max_length=10)
  uni = models.ForeignKey(Uni, to_field="short", default="NONE", on_delete=models.SET_DEFAULT)
  lang = models.CharField(max_length=2, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    indexes = [ models.Index(fields=["title"], name="idx_title" ) ]


  def __str__(self):
    return self.title