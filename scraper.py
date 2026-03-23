#!/usr/bin/env python3
"""
JobTrain Job Scraper - Enhanced to extract ALL job details
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
        """Fetch a single page of results"""
        params = {
            'Skip': str(skip),
            'what': '', 'Miles': '', 'Salary': '', 'LocationId': '',
            'Regions': '', 'DivisionIds': '', 'ClientCategory': '',
            'Departments': '', 'SchoolLocationId': '', 'JobLevels': '',
            'SchoolSubjectId': '', 'JobTypeIds': '', 'lat': '0',
            'long': '0', 'EmploymentType': '', 'postedDate': '',
        }
        
        for attempt in range(5):
            try:
                logger.info(f"Fetching page (Skip={skip}, Attempt {attempt + 1}/5)...")
                response = self.session.get(
                    self.base_url, 
                    params=params, 
                    timeout=60
                )
                response.raise_for_status()
                logger.info(f"✅ Success! Got {len(response.text)} bytes")
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 4:
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after 5 attempts")
                    return None
    
    def extract_text_between_labels(self, text, label):
        """Helper to extract text after a label"""
        if label in text:
            # Find the position after the label
            start = text.find(label) + len(label)
            # Get text until next newline or HTML tag
            end = text.find('\n', start)
            if end == -1:
                end = len(text)
            return text[start:end].strip()
        return None
    
    def parse_jobs(self, html):
        """Parse jobs from HTML - Extract ALL details"""
        if not html:
            return []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            jobs = []
            job_cards = soup.find_all('div', class_='job-card')
            logger.info(f"Found {len(job_cards)} job cards")
            
            for i, card in enumerate(job_cards):
                try:
                    job = {}
                    
                    # ========== 1. JOB TITLE ==========
                    title_elem = None
                    for heading in card.find_all(['h2', 'h3', 'h4']):
                        text = heading.text.strip()
                        if text and text != "NEW" and text != "New":
                            title_elem = heading
                            break
                    
                    if not title_elem:
                        card_body = card.find('div', class_='card-body')
                        if card_body:
                            for elem in card_body.find_all(['span', 'p', 'div']):
                                text = elem.text.strip()
                                if text and text != "NEW" and text != "New" and len(text) > 3:
                                    if 'location' not in text.lower() and 'salary' not in text.lower():
                                        title_elem = elem
                                        break
                    
                    if title_elem:
                        job['job_title'] = title_elem.text.strip()
                    else:
                        job['job_title'] = "Unknown"
                    
                    logger.info(f"Job {i+1}: {job.get('job_title', 'Unknown')}")
                    
                    # ========== 2. LOCATION ==========
                    location_elem = card.find(class_=lambda x: x and 'location' in x.lower() if x else False)
                    if location_elem:
                        location_text = location_elem.text.strip()
                        location_text = location_text.replace('Location:', '').replace('Location', '').strip()
                        job['location'] = location_text
                    
                    # ========== 3. SALARY ==========
                    salary_elem = card.find(class_=lambda x: x and ('salary' in x.lower() or 'pay' in x.lower()) if x else False)
                    if salary_elem:
                        salary_text = salary_elem.text.strip()
                        salary_text = salary_text.replace('Salary:', '').replace('Salary', '').strip()
                        job['salary'] = salary_text
                    
                    # ========== 4. EMPLOYMENT TYPE ==========
                    employment_elem = card.find(class_=lambda x: x and 'employment' in x.lower() if x else False)
                    if employment_elem:
                        employment_text = employment_elem.text.strip()
                        employment_text = employment_text.replace('Employment Type:', '').replace('Type:', '').strip()
                        job['employment_type'] = employment_text
                    
                    # ========== 5. HOURS PER WEEK ==========
                    # Look for hours information
                    for elem in card.find_all(['span', 'p', 'div']):
                        text = elem.text.strip()
                        if 'hours per week' in text.lower() or 'hours/week' in text.lower():
                            job['hours_per_week'] = text
                            break
                    
                    # ========== 6. CLOSING DATE ==========
                    closing_elem = card.find(class_=lambda x: x and 'closing' in x.lower() if x else False)
                    if closing_elem:
                        closing_text = closing_elem.text.strip()
                        closing_text = closing_text.replace('Closing Date:', '').replace('Closing:', '').strip()
                        job['closing_date'] = closing_text
                    
                    # If not found with class, search in text
                    if 'closing_date' not in job:
                        card_text = card.get_text()
                        if 'closing date' in card_text.lower():
                            for elem in card.find_all(['span', 'p', 'div']):
                                text = elem.text.strip()
                                if 'closing date' in text.lower():
                                    closing_text = text.replace('Closing Date:', '').replace('Closing:', '').strip()
                                    if closing_text:
                                        job['closing_date'] = closing_text
                                        break
                    
                    # ========== 7. DEPARTMENT ==========
                    dept_elem = card.find(class_=lambda x: x and ('department' in x.lower() or 'dept' in x.lower()) if x else False)
                    if dept_elem:
                        dept_text = dept_elem.text.strip()
                        dept_text = dept_text.replace('Department:', '').replace('Dept:', '').strip()
                        job['department'] = dept_text
                    
                    # ========== 8. JOB TYPE / CATEGORY ==========
                    # Look for job type/category information
                    for elem in card.find_all(['span', 'p', 'div']):
                        text = elem.text.strip()
                        if 'full-time' in text.lower() or 'part-time' in text.lower() or 'temporary' in text.lower():
                            if 'job_type' not in job or len(text) > len(job.get('job_type', '')):
                                job['job_type'] = text
                    
                    # ========== 9. JOB URL ==========
                    link_elem = card.find('a', href=True)
                    if link_elem:
                        job_url = link_elem.get('href')
                        if job_url:
                            if job_url.startswith('/'):
                                job['job_url'] = 'https://www.jobtrain.co.uk' + job_url
                            elif job_url.startswith('http'):
                                job['job_url'] = job_url
                    
                    # ========== 10. DESCRIPTION / SUMMARY ==========
                    # Try to get a brief description
                    for elem in card.find_all(['p', 'div']):
                        text = elem.text.strip()
                        if text and len(text) > 20 and len(text) < 500:
                            if not any(keyword in text.lower() for keyword in ['location', 'salary', 'closing', 'hours', 'employment']):
                                if 'description' not in job:
                                    job['description'] = text
                                    break
                    
                    # Only add if we got the title (and it's not "NEW")
                    title = job.get('job_title', '').strip()
                    if title and title.upper() != 'NEW':
                        jobs.append(job)
                
                except Exception as e:
                    logger.warning(f"Error parsing job {i+1}: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(jobs)} jobs from this page")
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
                logger.info(f"Reached max pages limit: {max_pages}")
                break
            
            logger.info(f"\n📄 Fetching page {page} (Skip={skip})...")
            
            html = self.fetch_page(skip)
            if not html:
                empty_pages += 1
                logger.warning(f"Empty page {page}")
                if empty_pages >= 2:
                    logger.info("Got 2 empty pages in a row, stopping")
                    break
                continue
            
            jobs = self.parse_jobs(html)
            
            if not jobs:
                empty_pages += 1
                logger.warning(f"No jobs found on page {page}")
                if empty_pages >= 2:
                    logger.info("Got 2 empty pages in a row, stopping")
                    break
            else:
                empty_pages = 0
                self.jobs.extend(jobs)
                logger.info(f"✅ Total jobs so far: {len(self.jobs)}")
            
            skip += 12
            page += 1
            time.sleep(0.5)
        
        logger.info(f"\n✨ Success! Scraped {len(self.jobs)} total jobs")
        return self.jobs
    
    def save_to_json(self, filename='jobs.json'):
        """Save jobs to JSON file"""
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
