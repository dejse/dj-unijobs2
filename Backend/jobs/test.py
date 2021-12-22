from django.test import TestCase 
from django.urls import reverse

class TestSite(TestCase):
  def test_index(self):
    response = self.client.get(reverse("jobs:index"))
    self.assertEqual(response.status_code, 200)

  def test_index_de(self):
    response = self.client.get("/de")
    self.assertEqual(response.status_code, 301)

  def test_index_en(self):
    response = self.client.get("/en")
    self.assertEqual(response.status_code, 301)

  def test_search_form_empty(self):
    response = self.client.post("/suche", { "job": "", "uni": "" })
    self.assertEqual(response.status_code, 302)

  def test_search_formy(self):
    response = self.client.post("/suche", { "job": "prof", "uni": "Wien" })
    self.assertEqual(response.status_code, 200)
