from django import forms 

class SearchForm(forms.Form):
  job = forms.CharField(label="jobs", max_length=100, required=False)
  uni = forms.CharField(label="uni", max_length=100, required=False)