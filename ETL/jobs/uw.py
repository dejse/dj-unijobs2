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

    url = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D43DEDD-72BD-DF5E-F655-2B545C9F1E0D_k4451D10F-3431-0C0D-DF27-76BA81377154"
    page.goto(url)
    page.wait_for_timeout(30*1000)

    while(True):
      d = page.eval_on_selector_all("tr.even, tr.odd", 
      """
      arr => {
        arr.shift();    // remove table header
        let jobsData = [];
        arr.forEach(el => {
          let jobTitle = el.querySelectorAll("td")[2].textContent.trim();
          let institute = el.querySelectorAll("td")[1].textContent.trim();
          let deadline = el.querySelectorAll("td")[3].textContent.trim();
          let href = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D14C0D7-E4AB-7F5C-6D0F-825FF8609A90_kE4379819-2246-3840-D387-0280CFF83E58";
        
          let id = el.querySelectorAll("td > a")[0].href;
          let pattern = /\d+\.\d+/;
          id = "&tid=" + pattern.exec(id)[0];
          href = href + id;
          jobsData.push({ jobTitle, href, institute, deadline });
        });
      return jobsData;
      }
      """)
      data.extend(d)
      next =  page.locator("xpath=//a[contains(., 'nächste') or contains(., 'next')]")
      if next.count() > 0:
        next.first.click()
        page.wait_for_timeout(30*1000)
        continue
      break
    browser.close()
  return data

# English Scrapper
def scrap_en():
  data = list()
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=en-UK,en", "--start-maximized"])
    context = browser.new_context(locale="en-UK", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()

    url = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D43DEDD-72BD-DF5E-F655-2B545C9F1E0D_k4451D10F-3431-0C0D-DF27-76BA81377154"
    page.goto(url)
    page.wait_for_timeout(30*1000)

    while(True):
      d = page.eval_on_selector_all("tr.even, tr.odd", 
      """
      arr => {
        arr.shift();    // remove table header
        let jobsData = [];
        arr.forEach(el => {
          let jobTitle = el.querySelectorAll("td")[2].textContent.trim();
          let institute = el.querySelectorAll("td")[1].textContent.trim();
          let deadline = el.querySelectorAll("td")[3].textContent.trim();
          let href = "https://univis.univie.ac.at/ausschreibungstellensuche/flow/bew_ausschreibung-flow?_flowExecutionKey=_c0D14C0D7-E4AB-7F5C-6D0F-825FF8609A90_kE4379819-2246-3840-D387-0280CFF83E58";
        
          let id = el.querySelectorAll("td > a")[0].href;
          let pattern = /\d+\.\d+/;
          id = "&tid=" + pattern.exec(id)[0];
          href = href + id;
          jobsData.push({ jobTitle, href, institute, deadline });
        });
      return jobsData;
      }
      """)
      data.extend(d)
      next =  page.locator("xpath=//a[contains(., 'nächste') or contains(., 'next')]")
      if next.count() > 0:
        next.first.click()
        page.wait_for_timeout(30*1000)
        continue
      break
    browser.close()
  return data


# Write German JSON
file = data_path / "uw-de.json"
data = scrap()
JSON = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)


# Write English JSON
file = data_path / "uw-en.json"
data = scrap_en()
JSON = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)