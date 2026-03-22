
import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobTrainScraper:
    def __init__(self):
        self.base_url = "https://www.jobtrain.co.uk/iomgovjobs/Home/_JobCard"
        self.jobs = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, skip=0):
        """Fetch a single page of results"""
        params = {
            'Skip': str(skip),
            'what': '',
            'Miles': '',
            'Salary': '',
            'LocationId': '',
            'Regions': '',
            'DivisionIds': '',
            'ClientCategory': '',
            'Departments': '',
            'SchoolLocationId': '',
            'JobLevels': '',
            'SchoolSubjectId': '',
            'JobTypeIds': '',
            'lat': '0',
            'long': '0',
            'EmploymentType': '',
            'postedDate': '',
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page with Skip={skip}: {e}")
            return None
    
    def parse_jobs(self, html):
        """Parse jobs from HTML"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        # Find all job cards
        job_cards = soup.find_all('div', class_='job-card')
        logger.info(f"Found {len(job_cards)} job cards")
        
        for card in job_cards:
            try:
                job = {}
                
                # Extract job title
                title_elem = card.find('h2')
                if title_elem:
                    job['job_title'] = title_elem.text.strip()
                
                # Extract location
                location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower() if x else False)
                if location_elem:
                    job['location'] = location_elem.text.strip()
                
                # Extract salary
                salary_elem = card.find(['span', 'div'], class_=lambda x: x and 'salary' in x.lower() if x else False)
                if salary_elem:
                    job['salary'] = salary_elem.text.strip()
                
                # Extract job URL
                link_elem = card.find('a', href=True)
                if link_elem:
                    job_url = link_elem.get('href')
                    if job_url.startswith('/'):
                        job['job_url'] = 'https://www.jobtrain.co.uk' + job_url
                    else:
                        job['job_url'] = job_url
                
                if 'job_title' in job:  # Only add if we got the title
                    jobs.append(job)
            
            except Exception as e:
                logger.warning(f"Error parsing job card: {e}")
                continue
        
        return jobs
    
    def scrape(self, max_pages=None):
        """Scrape all jobs"""
        logger.info("🚀 Starting to scrape jobs from JobTrain IoM...")
        
        skip = 0
        page = 1
        empty_pages = 0
        
        while True:
            if max_pages and page > max_pages:
                break
            
            logger.info(f"📄 Fetching page {page} (Skip={skip})...")
            
            html = self.fetch_page(skip)
            if not html:
                empty_pages += 1
                if empty_pages >= 2:
                    logger.info("No more pages found")
                    break
                continue
            
            jobs = self.parse_jobs(html)
            if not jobs:
                empty_pages += 1
                if empty_pages >= 2:
                    logger.info("No more pages found")
                    break
            else:
                empty_pages = 0
                self.jobs.extend(jobs)
                logger.info(f"✅ Found {len(jobs)} jobs on page {page}")
            
            skip += 12  # Next page
            page += 1
            time.sleep(0.5)  # Be nice to the server
        
        logger.info(f"✨ Success! Scraped {len(self.jobs)} total jobs")
        return self.jobs
    
    def save_to_json(self, filename='jobs.json'):
        """Save jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Saved {len(self.jobs)} jobs to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            return False

if __name__ == '__main__':
    scraper = JobTrainScraper()
    scraper.scrape()
    scraper.save_to_json()
