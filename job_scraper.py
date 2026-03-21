#!/usr/bin/env python3
"""
JobTrain IoM Job Scraper
Scrapes all paginated job listings and saves to JSON

Usage: python3 job_scraper.py
Requirements: Python 3.7+, requests library
    Install: pip install requests
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = 'https://www.jobtrain.co.uk/iomgovjobs/Home/_JobCard'
QUERY_PARAMS = {
    'Skip': 0,
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
    'postedDate': ''
}

ITEMS_PER_PAGE = 12
MAX_PAGES = 100
REQUEST_TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 0.5  # seconds


def fetch_all_jobs():
    """Fetch all job listings from all pages"""
    all_jobs = []
    skip_value = 0
    page_count = 0
    has_more_jobs = True

    print('🚀 Starting to scrape jobs from JobTrain IoM...\n')

    while has_more_jobs and page_count < MAX_PAGES:
        page_count += 1
        query_params = QUERY_PARAMS.copy()
        query_params['Skip'] = skip_value

        try:
            print(f'📄 Fetching page {page_count} (Skip={skip_value})...')
            response = requests.get(BASE_URL, params=query_params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            jobs = response.json()

            if not isinstance(jobs, list) or len(jobs) == 0:
                print(f'✅ No more jobs found. Total pages: {page_count - 1}')
                has_more_jobs = False
                break

            print(f'   ✓ Found {len(jobs)} jobs on this page')
            all_jobs.extend(jobs)

            # If we get fewer items than expected, we're on the last page
            if len(jobs) < ITEMS_PER_PAGE:
                print(f'✅ Last page reached ({len(jobs)} jobs < {ITEMS_PER_PAGE})')
                has_more_jobs = False

            skip_value += ITEMS_PER_PAGE

            # Be respectful to the server
            time.sleep(DELAY_BETWEEN_REQUESTS)

        except requests.exceptions.RequestException as e:
            print(f'❌ Error fetching page {page_count}: {str(e)}')
            break

    return all_jobs


def main():
    """Main function"""
    try:
        jobs = fetch_all_jobs()

        output = {
            'metadata': {
                'totalJobs': len(jobs),
                'scrapedAt': datetime.now().isoformat(),
                'source': 'https://www.jobtrain.co.uk/iomgovjobs/',
                'description': 'All job listings from JobTrain Isle of Man Government Jobs'
            },
            'jobs': jobs
        }

        # Save to JSON file
        output_path = './all_jobs.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        file_size_kb = os.path.getsize(output_path) / 1024

        print(f'\n✨ Success!')
        print(f'📊 Total jobs scraped: {len(jobs)}')
        print(f'📁 Saved to: {output_path}')
        print(f'📦 File size: {file_size_kb:.2f} KB')

    except Exception as e:
        print(f'Fatal error: {str(e)}')
        exit(1)


if __name__ == '__main__':
    import os
    main()
