import requests
from bs4 import BeautifulSoup
from app import models
from app.database import session, engine
from sqlalchemy import exc
db = session()
models.Base.metadata.create_all(bind=engine)

def get_monster_jobs(end):
    url = "https://www.monster.com/jobs/search/?q=software-engineer-intern&where=94583&stpage=1&page=" + str(end)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find(id="ResultsContainer")
    jobs = res.find_all('section', class_="card-content")
    #rint(jobs)

    for job in jobs:
        try:

            mjob_id = job.get('data-jobid')
            #print(mjob_id)
            job_url = url + '&jobid=' + str(mjob_id)
            title = job.find('h2', class_='title').find('a').text.replace('\n', "")
            company = job.find('div', class_="company").find('span', class_="name").text.replace("\n", "")
            location = job.find('div', class_="location").find('span', class_="name").text.replace("\n", "")
            db_job = models.Job(job_id= mjob_id, title=title, company=company, location=location, url=job_url, source = "Monster")
                
            db.add(db_job)
            try:
                db.commit()
            except exc.IntegrityError:
                db.rollback()
                continue
        except AttributeError:
            continue
            


def url_incr(base_url, curr_start):
    base_url += "&start=" + str(curr_start + 10)
    return base_url
url = "https://www.indeed.com/jobs?q=software+engineer+intern&l=San+Ramon%2C+CA"
print(url_incr(url, 0))

def get_indeed_jobs(limit):
    url = "https://www.indeed.com/jobs?q=software+engineer+intern&l=San+Ramon%2C+CA"
    start = 0
    
    excluded = 0
    while start < limit:

        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        res = soup.find(id='resultsCol')
        jobs = res.find_all('div', class_='result')
        for job in jobs:
     
            ijob_id = job.get('data-jk')

            job_url = url + ijob_id
            title = job.find('a', class_="jobtitle").text.replace("\n", "")
            try:
                location = job.find('span', class_="location").text
            except AttributeError:
                location = ""
            try:
                company = job.find('a', {"data-tn-element":"companyName"}).text.replace("\n", "")
            except AttributeError:
                company = job.find('span', class_="company").text.replace("\n", "")
            db_job = models.Job(job_id= ijob_id, title=title, company=company, location=location, url=job_url, source= "Indeed")
            db.add(db_job)
            try:
                db.commit()
            except exc.IntegrityError:
                print(ijob_id)
                excluded += 1
                db.rollback()
                continue
        url = url_incr(url, start)
        start += 10
    print(excluded)
    #db.commit()
get_indeed_jobs(50)
get_monster_jobs(10)

