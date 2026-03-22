#!/usr/bin/env python3
"""
Quick diagnostic to see what JobTrain website is returning
Run this to debug the JSON error
"""

import requests
from bs4 import BeautifulSoup

print("=" * 70)
print("🔍 JOBTRAIN WEBSITE DIAGNOSTIC")
print("=" * 70)

# The URL we're trying to access
url = "https://www.jobtrain.co.uk/iomgovjobs/Home/_JobCard"

params = {
    "Skip": "0",
    "what": "",
    "Miles": "",
    "Salary": "",
    "LocationId": "",
    "Regions": "",
    "DivisionIds": "",
    "ClientCategory": "",
    "Departments": "",
    "SchoolLocationId": "",
    "JobLevels": "",
    "SchoolSubjectId": "",
    "JobTypeIds": "",
    "lat": "0",
    "long": "0",
    "EmploymentType": "",
    "postedDate": "",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("\n📡 TEST 1: Can we reach the website?")
print("-" * 70)

try:
    response = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"✅ Website is reachable!")
    print(f"   Status Code: {response.status_code}")
    print(f"   Content Type: {response.headers.get('content-type', 'Not specified')}")
    print(f"   Response Size: {len(response.text)} characters")
except requests.exceptions.Timeout:
    print(f"❌ TIMEOUT: Website took too long to respond")
    print(f"   Try again in a few minutes")
except requests.exceptions.ConnectionError as e:
    print(f"❌ CONNECTION ERROR: Can't reach website")
    print(f"   Error: {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

print("\n📊 TEST 2: What type of data is being returned?")
print("-" * 70)

try:
    if response.status_code == 200:
        # Check if it's HTML
        if "<html" in response.text.lower() or "<!doctype" in response.text.lower():
            print("📄 Website returned: HTML (web page)")
            print("   This is normal for the first page load")
            
            # Try to find job listings in HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and 'job' in x.lower() if x else False)
            
            if job_cards:
                print(f"✅ Found {len(job_cards)} job elements in the HTML")
                print("   The website structure might have changed")
                print("   You may need to update the scraper selectors")
            else:
                print("❌ No job elements found in the HTML")
                print("   The website structure has definitely changed")
                print("   The scraper needs to be updated")
        
        elif response.headers.get('content-type', '').startswith('application/json'):
            print("📊 Website returned: JSON (data)")
            print("   This is what we expect!")
            try:
                import json
                data = json.loads(response.text)
                print(f"✅ JSON is valid!")
                print(f"   Number of items: {len(data) if isinstance(data, list) else 'N/A'}")
            except:
                print("❌ JSON is invalid or corrupted")
        else:
            print(f"❓ Website returned: {response.headers.get('content-type', 'Unknown type')}")
            print(f"   First 200 characters:\n{response.text[:200]}")
    
    else:
        print(f"❌ Website returned error: {response.status_code}")
        if response.status_code == 429:
            print("   Too many requests - website is rate limiting you")
            print("   Wait 30 minutes and try again")
        elif response.status_code == 403:
            print("   Access forbidden - website blocked your request")
            print("   Try again later or from different network")
        elif response.status_code == 404:
            print("   Page not found - URL might be wrong or endpoint removed")
        
except Exception as e:
    print(f"❌ Error checking response: {e}")

print("\n📋 TEST 3: Sample of response content")
print("-" * 70)

print("First 500 characters of response:\n")
print(response.text[:500])
print("\n...")

print("\n" + "=" * 70)
print("🎯 DIAGNOSIS SUMMARY")
print("=" * 70)

if response.status_code != 200:
    print("❌ Website returned an error status code")
    print("   This might be temporary")
elif "<html" in response.text.lower():
    print("⚠️  Website returned HTML instead of JSON")
    print("   The website structure has probably changed")
    print("   The scraper selectors need updating")
    print("\n📝 What to do:")
    print("   1. Check FIX_JSON_ERROR.md for detailed instructions")
    print("   2. Update selectors in scraper.py")
    print("   3. See CONFIGURATION.md for selector examples")
else:
    print("✅ Response looks normal")
    print("   If scraper still fails, check FIX_JSON_ERROR.md")

print("\n" + "=" * 70)
