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
    browser = p.chromium.launch(headless=False, slow_mo=50, args=["--lang=de-DE,de", "--start-maximized"])
    context = browser.new_context(locale="de-DE", timezone_id="Europe/Berlin", viewport={ "width": 1280, "height": 1024 })
    page = context.new_page()

    url = "https://boku.ac.at/pers/interne-jobboerse"
    page.goto(url, wait_until="domcontentloaded")

    data = page.eval_on_selector_all("article", 
    """
    arr => {
      let jobTitles = [...arr.querySelectorAll("strong")].map(e => e.textContent);
      let href = [...arr.querySelectorAll("strong > a")].map(e => e.href);
      let institute = [...arr.querySelectorAll("section > p")].map(e => e.textContent)
        .filter(e => /H[0-9]{3,4}/.test(e)).map(e => {
          let H = /H[0-9]{3,4}/.exec(e).index;
          return e.substring(H, e.length);
        });
      let deadline = [...arr.querySelectorAll("section > p")].map(e => e.textContent).
        .filter(e => /Bewerbungsfrist|Deadline/.test(e)).map(e => e.split(": ")[1]);

      deadline = deadline.map(e => {
        let germanDateFormat = /\d{2}\.\d{2}\.\d{4}/.test(e);
        if (germanDateFormat === true) {
          return e;
        } 
        else {
          let day = /\d{1,2}/.exec(e);
          let year = /\d{4}/.exec(e);
          let month = "01";
          if /Jan/.test(e) { month = "01"; }
          else if /Feb/.test(e) { month = "02"; }
          else if /Mar/.test(e) { month = "03"; }
          else if /Apr/.test(e) { month = "04"; }
          else if /May/.test(e) { month = "05"; }
          else if /Jun/.test(e) { month = "06"; }
          else if /Jul/.test(e) { month = "07"; }
          else if /Aug/.test(e) { month = "08"; }
          else if /Sep/.test(e) { month = "09"; }
          else if /Oct/.test(e) { month = "10"; }
          else if /Nov/.test(e) { month = "11"; }
          else { month = "12"; }
          return `${day}.${month}.${year}`;
        }
      })

    }

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


scrap()

# # Write German JSON
# file = data_path / "boku-de.json"
# data = scrap()
# JSON = json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8")
# with file.open(mode="w+b") as f: 
#   f.write(JSON)