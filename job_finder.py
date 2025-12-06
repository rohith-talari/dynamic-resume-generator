import requests
from bs4 import BeautifulSoup

def find_jobs(skill, location="India", max_results=5):
    jobs = []
    try:
        search_url = f"https://in.indeed.com/jobs?q={skill.replace(' ', '+')}&l={location.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for div in soup.select('a.tapItem')[:max_results]:
            job_title = div.find('h2', class_='jobTitle')
            company = div.find('span', class_='companyName')
            location_elem = div.find('div', class_='companyLocation')
            url = "https://in.indeed.com" + div['href']
            jobs.append(
                f"{job_title.text.strip() if job_title else 'No Title'} - "
                f"{company.text.strip() if company else 'No Company'} "
                f"({location_elem.text.strip() if location_elem else 'No Location'}) [Apply Here]({url})"
            )
        if not jobs:
            jobs.append("No jobs found or blocked by Indeed. Try another keyword.")
    except Exception as e:
        jobs.append(f"Error searching Indeed: {str(e)}")
    return jobs
