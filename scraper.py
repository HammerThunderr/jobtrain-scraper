#!/usr/bin/env python3
"""
JobTrain Job Scraper - With Network Retry Logic
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
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
        """Fetch with retry logic"""
        params = {
            'Skip': str(skip),
            'what': '', 'Miles': '', 'Salary': '', 'LocationId': '',
            'Regions': '', 'DivisionIds': '', 'ClientCategory': '',
            'Departments': '', 'SchoolLocationId': '', 'JobLevels': '',
            'SchoolSubjectId': '', 'JobTypeIds': '', 'lat': '0',
            'long': '0', 'EmploymentType': '', 'postedDate': '',
        }
        
        # Retry logic
        for attempt in range(5):  # Try 5 times
            try:
                logger.info(f"Fetching page (Skip={skip}, Attempt {attempt + 1}/5)...")
                response = self.session.get(
                    self.base_url, 
                    params=params, 
                    timeout=60  # LONGER timeout
                )
                response.raise_for_status()
                logger.info(f"✅ Success! Got {len(response.text)} bytes")
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 4:
                    wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4, 8, 16 seconds
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after 5 attempts")
                    return None
    
    def parse_jobs(self, html):
        """Parse jobs from HTML"""
        if not html:
            return []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            jobs = []
            job_cards = soup.find_all('div', class_='job-card')
            logger.info(f"Found {len(job_cards)} job cards")
            
            for card in job_cards:
                try:
                    job = {}
                    
                    title_elem = card.find(['h2', 'h3', 'h4', 'span'])
                    if title_elem:
                        job['job_title'] = title_elem.text.strip()
                    
                    location_elem = card.find(class_=lambda x: x and 'location' in x.lower() if x else False)
                    if location_elem:
                        job['location'] = location_elem.text.strip()
                    
                    salary_elem = card.find(class_=lambda x: x and ('salary' in x.lower() or 'pay' in x.lower()) if x else False)
                    if salary_elem:
                        job['salary'] = salary_elem.text.strip()
                    
                    link_elem = card.find('a', href=True)
                    if link_elem:
                        job_url = link_elem.get('href')
                        if job_url:
                            if job_url.startswith('/'):
                                job['job_url'] = 'https://www.jobtrain.co.uk' + job_url
                            elif job_url.startswith('http'):
                                job['job_url'] = job_url
                    
                    if 'job_title' in job:
                        jobs.append(job)
                
                except Exception as e:
                    logger.warning(f"Error parsing job: {e}")
                    continue
            
            return jobs
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return []
    
    def scrape(self, max_pages=None):
        """Scrape all jobs"""
        logger.info("🚀 Starting to scrape jobs from JobTrain IoM...")
        
        skip = 0
        page = 1
        empty_pages = 0
        
        while True:
            if max_pages and page > max_pages:
                break
            
            logger.info(f"\n📄 Fetching page {page} (Skip={skip})...")
            
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
                logger.info(f"✅ Total jobs so far: {len(self.jobs)}")
            
            skip += 12
            page += 1
            time.sleep(1)  # Be nice to server
        
        logger.info(f"\n✨ Success! Scraped {len(self.jobs)} total jobs")
        return self.jobs
    
    def save_to_json(self, filename='jobs.json'):
        """Save jobs to JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Saved {len(self.jobs)} jobs to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving: {e}")
            return False

if __name__ == '__main__':
    scraper = JobTrainScraper()
    scraper.scrape()
    scraper.save_to_json()
