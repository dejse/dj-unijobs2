from pprint import pprint
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from time import sleep

data_path = Path("./ETL/data").resolve()

# German Scrapper
def scrap():
  data = list()
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=de-DE,de", "--start-maximized"], devtools=True)
    context = browser.new_context(locale="de-DE", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()

    url = "https://boku.ac.at/pers/interne-jobboerse"
    page.goto(url, wait_until="domcontentloaded")

    data = page.eval_on_selector_all("article", 
    """
    arr => {
      let jobTitles = [...document.querySelectorAll("strong")].map(e => e.textContent);
      let hrefs = [...document.querySelectorAll("strong > a")].map(e => e.href);
      let institutes = [...document.querySelectorAll("article > section > p")].map(e => e.textContent)
        .filter(e => /H[0-9]{3,4}/.test(e)).map(e => {
          let H = /H[0-9]{3,4}/.exec(e).index;
          let inst = e.substring(H, e.length)
          return inst.substring(0, 100);
        });
      let deadlines = [...document.querySelectorAll("article > section > p")].map(e => e.textContent)
        .filter(e => /Bewerbungsfrist|Deadline/.test(e)).map(e => e.split(": ")[1]);

      deadlines = deadlines.map(e => {
        let germanDateFormat = /\d{2}\.\d{2}\.\d{4}/.test(e);
        if (germanDateFormat === true) {
          return e;
        } 
        else {
          let day = /\d{1,2}/.exec(e);
          let year = /\d{4}/.exec(e);
          let month = "01";
          if (/Jan/.test(e)) { month = "01"; }
          else if (/Feb/.test(e)) { month = "02"; }
          else if (/Mar/.test(e)) { month = "03"; }
          else if (/Apr/.test(e)) { month = "04"; }
          else if (/May/.test(e)) { month = "05"; }
          else if (/Jun/.test(e)) { month = "06"; }
          else if (/Jul/.test(e)) { month = "07"; }
          else if (/Aug/.test(e)) { month = "08"; }
          else if (/Sep/.test(e)) { month = "09"; }
          else if (/Oct/.test(e)) { month = "10"; }
          else if (/Nov/.test(e)) { month = "11"; }
          else { month = "12"; }
          return `${day}.${month}.${year}`;
        }
      });

    let jobsData = [];
    for (let i = 0; i < jobTitles.length; i++) {
      let job = {
        jobTitle: jobTitles[i],
        href: hrefs[i],
        institute: institutes[i], 
        deadline: deadlines[i]
      }
      jobsData.push(job);
    }
    return jobsData;}
    """
    )
    browser.close()
  return data


# Write German JSON
file = data_path / "boku-de.json"
data = scrap()
JSON = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
with file.open(mode="w+b") as f: 
  f.write(JSON)