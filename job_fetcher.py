import requests
from bs4 import BeautifulSoup
import time

def fetch_jobs_simple(skills, location="India", max_results=5):
    """
    Fetch job listings based on skills (simplified version using Indeed)
    
    Args:
        skills (list): List of skills to search for
        location (str): Job location
        max_results (int): Maximum number of jobs to return
    
    Returns:
        list: List of job dictionaries
    """
    jobs = []
    
    # Use Indeed job search (example - real implementation may need API key)
    for skill in list(skills)[:3]:  # Limit to top 3 skills
        try:
            # Build search URL
            skill_query = skill.lower().replace(' ', '+')
            url = f"https://www.indeed.com/jobs?q={skill_query}&l={location}"
            
            # Add headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Note: In production, use proper API or scraping service
            print(f"Would search for: {skill} in {location}")
            
            # Simulated job data (replace with actual API call)
            jobs.append({
                'title': f'{skill} Developer',
                'company': 'Tech Company',
                'location': location,
                'skills_required': [skill],
                'url': f'https://www.indeed.com/jobs?q={skill_query}'
            })
            
            if len(jobs) >= max_results:
                break
                
        except Exception as e:
            print(f"Error fetching jobs for {skill}: {e}")
            continue
    
    return jobs

def fetch_jobs_adzuna(skills, location="India", max_results=5):
    """
    Fetch jobs using Adzuna API (Free tier available)
    Sign up at: https://developer.adzuna.com/
    
    Args:
        skills (list): List of skills
        location (str): Job location
        max_results (int): Max results
    
    Returns:
        list: Job listings
    """
    # You need to register for free API keys at https://developer.adzuna.com/
    APP_ID = "YOUR_ADZUNA_APP_ID"  # Replace with your app ID
    API_KEY = "YOUR_ADZUNA_API_KEY"  # Replace with your API key
    
    jobs = []
    
    # Adzuna country code
    country = "in"  # India
    
    for skill in list(skills)[:3]:
        try:
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            params = {
                'app_id': APP_ID,
                'app_key': API_KEY,
                'what': skill,
                'where': location,
                'results_per_page': 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get('results', [])[:max_results]:
                    jobs.append({
                        'title': job.get('title', 'N/A'),
                        'company': job.get('company', {}).get('display_name', 'N/A'),
                        'location': job.get('location', {}).get('display_name', location),
                        'skills_required': [skill],
                        'url': job.get('redirect_url', '#'),
                        'salary': job.get('salary_max', 'Not specified')
                    })
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Error: {e}")
    
    return jobs

def match_jobs_to_user(user_skills, jobs):
    """
    Match jobs to user based on skills
    
    Args:
        user_skills (set): User's skills
        jobs (list): List of available jobs
    
    Returns:
        list: Matched jobs sorted by relevance
    """
    matched_jobs = []
    
    for job in jobs:
        # Count matching skills
        job_skills = set([s.lower() for s in job.get('skills_required', [])])
        user_skills_lower = set([s.lower() for s in user_skills])
        
        matches = len(job_skills.intersection(user_skills_lower))
        
        if matches > 0:
            job['match_score'] = matches
            matched_jobs.append(job)
    
    # Sort by match score
    matched_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
    
    return matched_jobs

# Test function
if __name__ == "__main__":
    test_skills = ['Python', 'Flask', 'JavaScript']
    jobs = fetch_jobs_simple(test_skills)
    print("Found jobs:", jobs)
