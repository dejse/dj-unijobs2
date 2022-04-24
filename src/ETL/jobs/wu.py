from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep
import re
from helpers import save_file


# German
def scrap_de():
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
        let title = e.querySelectorAll("td.real_table_col1 > a")[0].textContent.trim();
        let href = "https://recruiting.wu.ac.at/?" + e.querySelectorAll("td.real_table_col1 > a")[0].href.trim().split("?")[1];
        let institute = e.querySelectorAll("td.real_table_col2")[0].textContent.trim();
        let deadline = null;
        jobData.push({ title, href, deadline, institute });
      });
      return jobData;
    }
    """
    )

    for i in range(len(data)):
      # TODO: Remove Hack when no deadline
      blacklist = [
        "https://recruiting.wu.ac.at/?yid=1353",
        "https://recruiting.wu.ac.at/?yid=1354",
        "https://recruiting.wu.ac.at/?yid=1343"
      ]
      if data[i].get("href") in blacklist:
        continue
      page.goto(data[i].get("href"), wait_until="domcontentloaded")
      deadline = page.text_content("xpath=//li[contains(., 'Publizierung bis') or contains(., 'published till')]")
      data[i]["deadline"] = deadline.split(":")[1].strip()

    browser.close()
  return data


# English
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
        let title = e.querySelectorAll("td.real_table_col1 > a")[0].textContent.trim();
        let href = "https://recruiting.wu.ac.at/eng/?" + e.querySelectorAll("td.real_table_col1 > a")[0].href.trim().split("?")[1];
        let institute = e.querySelectorAll("td.real_table_col2")[0].textContent.trim();
        let deadline = null;
        jobData.push({ title, href, deadline, institute });
      });
      return jobData;
    }
    """
    )

    for i in range(len(data)):
      # TODO: Remove Hack when no deadline
      blacklist = [
        "https://recruiting.wu.ac.at/eng/?yid=1353",
        "https://recruiting.wu.ac.at/eng/?yid=1354",
        "https://recruiting.wu.ac.at/eng/?yid=1343"
      ]
      if data[i].get("href") in blacklist:
        continue
      page.goto(data[i].get("href"), wait_until="domcontentloaded")
      deadline = page.text_content("xpath=//li[contains(., 'Publizierung bis') or contains(., 'published till')]")
      deadline = deadline.split(":")[1].strip()
      data[i]["deadline"] = datetime.strptime(deadline, "%Y-%m-%d").strftime("%d.%m.%Y")

    browser.close()
  return data


# Main 
if __name__ == "__main__":
  data = scrap_de()
  save_file(data, filename="wu-de.json")

  data = scrap_en()
  save_file(data, filename="wu-en.json")
