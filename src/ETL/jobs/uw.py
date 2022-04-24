from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep
import re
from helpers import save_file


# German 
def scrap_de():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=de-DE,de", "--start-maximized"])
    context = browser.new_context(locale="de-DE", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()
    url = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D43DEDD-72BD-DF5E-F655-2B545C9F1E0D_k4451D10F-3431-0C0D-DF27-76BA81377154"
    page.goto(url)
    page.wait_for_timeout(30*1000)
    html = ""
    while(True):
      tables = [e.inner_html() for e in page.query_selector_all("table")]
      html = html + "".join(tables)
      next = page.locator("xpath=//a[contains(., 'nächste') or contains(., 'next')]")
      if next.count() > 0:
        next.first.click()
        page.wait_for_timeout(30*1000)
        continue
      break
    browser.close()
  return html 

def process_de(html_doc):
  data = []
  soup = BeautifulSoup(html_doc, 'html.parser')
  for el in soup.select("tr.even, tr.odd"):
    # exclude table headings
    if len(el.select("th.h1")) > 0:
      continue
    title = el.select("td")[2].get_text().strip()
    deadline = el.select("td")[3].get_text().strip()
    institute = el.select("td")[1].get_text().strip()
    href = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D14C0D7-E4AB-7F5C-6D0F-825FF8609A90_kE4379819-2246-3840-D387-0280CFF83E58"
    id = el.select("td > a")[0].get("href") 
    href = href + "&tid=" + re.search("\d+\.\d+", id).group()
    d = {"title": title, "href": href, "deadline": deadline, "href": href, "institute": institute}
    data.append(d)
  return data 


# English
def scrap_en():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=en-UK,en", "--start-maximized"])
    context = browser.new_context(locale="en-UK", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()
    url = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D43DEDD-72BD-DF5E-F655-2B545C9F1E0D_k4451D10F-3431-0C0D-DF27-76BA81377154"
    page.goto(url)
    page.wait_for_timeout(30*1000)
    html = ""
    while(True):
      tables = [e.inner_html() for e in page.query_selector_all("table")]
      html = html + "".join(tables)
      next = page.locator("xpath=//a[contains(., 'nächste') or contains(., 'next')]")
      if next.count() > 0:
        next.first.click()
        page.wait_for_timeout(30*1000)
        continue
      break
    browser.close()
  return html 


def process_en(html_doc):
  data = []
  soup = BeautifulSoup(html_doc, 'html.parser')
  for el in soup.select("tr.even, tr.odd"):
    # exclude table headings
    if len(el.select("th.h1")) > 0:
      continue
    title = el.select("td")[2].get_text().strip()
    deadline = el.select("td")[3].get_text().strip()
    institute = el.select("td")[1].get_text().strip()
    href = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D43DEDD-72BD-DF5E-F655-2B545C9F1E0D_k4451D10F-3431-0C0D-DF27-76BA81377154"
    id = el.select("td > a")[0].get("href") 
    href = href + "&tid=" + re.search("\d+\.\d+", id).group()
    d = {"title": title, "href": href, "deadline": deadline, "href": href, "institute": institute}
    data.append(d)
  return data 



# Main 
if __name__ == "__main__":
  html_doc = scrap_de()
  data = process_de(html_doc)
  save_file(data, filename="uw-de.json")

  html_doc = scrap_en()
  data = process_en(html_doc)
  save_file(data, filename="uw-en.json")
