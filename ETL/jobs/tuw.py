from pprint import pprint
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

data_path = Path("./ETL/data").resolve()

# German Scrapper
def scrap():
  data = list()
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=de-DE,de", "--start-maximized"])
    context = browser.new_context(locale="de-DE", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()

    url = "https://tuwien.bewerberportal.at/Jobs"
    page.goto(url, wait_until="domcontentloaded")
    page.click("css=button[data-consent='true']")

    data = page.eval_on_selector_all("tr", 
    """
    arr => { 
      arr.shift();    // remove table header
      let jobsData = [];
      arr.forEach(e => {
        let jobTitle = e.querySelectorAll("div.job-title")[0].textContent.trim();
        let href = e.querySelectorAll("div.job-title > a")[0].href;
        let step = e.querySelectorAll("td.location")[0].textContent.split("|");
        let institute = step[1].trim();
        let deadline = step[0].slice(5).trim();
        jobsData.push({ jobTitle, href, institute, deadline });
      })
      return jobsData;}
    """
    )
    browser.close()
  return data


# English Scrapper
def scrap_en():
  data = list()
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=en-UK,en", "--start-maximized"])
    context = browser.new_context(locale="en-UK", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()

    url = "https://jobs.tuwien.ac.at/Jobs?culture=en"
    page.goto(url, wait_until="domcontentloaded")
    page.click("css=button[data-consent='true']")

    data = page.eval_on_selector_all("tr", 
    """
    arr => { 
      arr.shift();    // remove table header
      let jobsData = [];
      arr.forEach(e => {
        let jobTitle = e.querySelectorAll("div.job-title")[0].textContent.trim();
        let href = e.querySelectorAll("div.job-title > a")[0].href;
        let step = e.querySelectorAll("td.location")[0].textContent.split("|");
        let institute = step[1].trim();
        let deadline = step[0].slice(5).trim();
        jobsData.push({ jobTitle, href, institute, deadline });
      })
      return jobsData;}
    """
    )
    browser.close()
  return data


# Write German JSON
file = data_path / "tuw-de.json"
data = scrap()
JSON = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)


# Write English JSON
file = data_path / "tuw-en.json"
data = scrap_en()
JSON = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)