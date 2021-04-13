import requests
from bs4 import BeautifulSoup
URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class" : "s-pagination"})
  pages = pagination.find_all("span")
  last_page = pages[-2].string
  # pages[-2].get_text(strip=True) 라고 써도 된다
  return int(last_page)

# page 1 url is problem...
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Stack Overflow page {page + 1}")
    result = requests.get(f"{URL}&pg={page + 1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class" : "-job"})
    for result_title in results:
      job = extract_job_detail(result_title)
      jobs.append(job)
      # print(result_title["data-jobid"])

  return jobs

def extract_job_detail(html):
  title = html.find("h2", {"class" : "mb4"}).find("a")["title"]
  # location_raw = html.find("h3", {"class" : "fc-black-700"}).find("span")
  # span 안에 span 이 있는 경우 방지하기 위해서
  # 두 개의 span 이 있다는 것을 알고 있을 경우 이렇게 써줄 수 있다.
  company_raw, location_raw = html.find("h3", {"class" : "fc-black-700"}).find_all("span", recursive=False)
  company = company_raw.get_text(strip=True)
  location = location_raw.get_text(strip=True)
  job_id = html.find("div", {"class" : "data-jobid"})
  
  return {"title" : title , "company": company, "location" : location, "link":f"https://stackoverflow.com/jobs/{job_id}"}
  
def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  
  return jobs
