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
    url = "https://tuwien.bewerberportal.at/Jobs"
    page.goto(url, wait_until="domcontentloaded")
    page.click("css=button[data-consent='true']")
    html = page.inner_html("table.jobs-list")
    browser.close()
  return html 

def process_de(html_doc):
  data = []
  soup = BeautifulSoup(html_doc, 'html.parser')
  for el in soup.find_all("tr")[1:]:
    title = el.select("div.job-title")[0].get_text().strip()
    href = el.select("div.job-title > a")[0].get("href").strip()
    href = "https://tuwien.bewerberportal.at" + href
    txt = el.select(".location")[0].get_text()
    s = re.search("\d{2}.\d{2}.\d{4}", txt).span()
    deadline = txt[s[0]:s[1]]
    institute = txt[s[1]:].strip(" |")
    d = {"title": title, "href": href, "deadline": deadline, "href": href, "institute": institute}
    data.append(d)
  return data 


# English
def scrap_en():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=en-UK,en", "--start-maximized"])
    context = browser.new_context(locale="en-UK", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()
    url = "https://jobs.tuwien.ac.at/Jobs?culture=en"
    page.goto(url, wait_until="domcontentloaded")
    page.click("css=button[data-consent='true']")
    html = page.inner_html("table.jobs-list")
    browser.close()
  return html 

def process_en(html_doc):
  data = []
  soup = BeautifulSoup(html_doc, 'html.parser')
  for el in soup.find_all("tr")[1:]:
    title = el.select("div.job-title")[0].get_text().strip()
    href = el.select("div.job-title > a")[0].get("href").strip()
    href = "https://tuwien.bewerberportal.at" + href
    txt = el.select(".location")[0].get_text()
    s = re.search("\d{2}.\d{2}.\d{4}", txt).span()
    deadline = txt[s[0]:s[1]]
    institute = txt[s[1]:].strip(" |")
    d = {"title": title, "href": href, "deadline": deadline, "href": href, "institute": institute}
    data.append(d)
  return data 


# Main 
if __name__ == "__main__":
  html_doc = scrap_de()
  data = process_de(html_doc)
  save_file(data, filename="tuw-de.json")

  html_doc = scrap_en()
  data = process_en(html_doc)
  save_file(data, filename="tuw-en.json")
