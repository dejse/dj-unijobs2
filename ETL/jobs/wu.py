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

    url = "https://recruiting.wu.ac.at/de/"
    page.goto(url, wait_until="domcontentloaded")

    data = page.eval_on_selector_all("tr.alternative_1, tr.alternative_0", 
    """
    arr => { 
      let jobData = [];
      arr.forEach(e => {
        let jobTitle = e.querySelectorAll("td.real_table_col1")[0].textContent.trim();
        let href = "https://recruiting.wu.ac.at/?" + e.querySelectorAll("td.real_table_col1 > a")[0].href.trim().split("?")[1];
        let institute = e.querySelectorAll("td.real_table_col2")[0].textContent.trim()
        let deadline = null;
        jobData.push({ jobTitle, href, institute, deadline });
      });
      return jobData;
    }
    """
    )

    for i in range(len(data)):
      page.goto(data[i].get("href"), wait_until="domcontentloaded")
      deadline = page.text_content("xpath=//li[contains(., 'Publizierung bis') or contains(., 'published till')]")
      data[i]["deadline"] = deadline.split(":")[1].strip()

    browser.close()
  return data


# English Scrapper
def scrap_en():
  data = list()
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=en-UK,en", "--start-maximized"])
    context = browser.new_context(locale="en-UK", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()

    url = "https://recruiting.wu.ac.at/eng/?filter[job_field_310]=999"
    page.goto(url, wait_until="domcontentloaded")

    data = page.eval_on_selector_all("tr.alternative_1, tr.alternative_0", 
    """
    arr => { 
      let jobData = [];
      arr.forEach(e => {
        let jobTitle = e.querySelectorAll("td.real_table_col1")[0].textContent.trim();
        let href = "https://recruiting.wu.ac.at/eng/?" + e.querySelectorAll("td.real_table_col1 > a")[0].href.trim().split("?")[1];
        let institute = e.querySelectorAll("td.real_table_col2")[0].textContent.trim()
        let deadline = null;
        jobData.push({ jobTitle, href, institute, deadline });
      });
      return jobData;
    }
    """
    )

    for i in range(len(data)):
      page.goto(data[i].get("href"), wait_until="domcontentloaded")
      deadline = page.text_content("xpath=//li[contains(., 'Publizierung bis') or contains(., 'published till')]")
      data[i]["deadline"] = deadline.split(":")[1].strip()

    browser.close()
  return data


# Write German JSON
file = data_path / "wu-de.json"
data = scrap()
JSON = json.dumps(data, ensure_ascii=False).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)


# Write English JSON
file = data_path / "wu-en.json"
data = scrap_en()
JSON = json.dumps(data, ensure_ascii=False).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)