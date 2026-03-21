/**
 * JobTrain IoM Job Scraper
 * 
 * Usage: node job_scraper.js
 * Requirements: Node.js 18+ (for native fetch support)
 */

const fs = require('fs');

const BASE_URL = 'https://www.jobtrain.co.uk/iomgovjobs/Home/_JobCard?Skip=';
const QUERY_PARAMS = '&what=&Miles=&Salary=&LocationId=&Regions=&DivisionIds=&ClientCategory=&Departments=&SchoolLocationId=&JobLevels=&SchoolSubjectId=&JobTypeIds=&lat=0&long=0&EmploymentType=&postedDate=';
const ITEMS_PER_PAGE = 12;
const MAX_PAGES = 100; // Safety limit to prevent infinite loops

async function fetchAllJobs() {
  const allJobs = [];
  let skipValue = 0;
  let hasMoreJobs = true;
  let pageCount = 0;

  console.log('🚀 Starting to scrape jobs from JobTrain IoM...\n');

  while (hasMoreJobs && pageCount < MAX_PAGES) {
    const url = `${BASE_URL}${skipValue}${QUERY_PARAMS}`;
    pageCount++;

    try {
      console.log(`📄 Fetching page ${pageCount} (Skip=${skipValue})...`);
      const response = await fetch(url);

      if (!response.ok) {
        console.error(`❌ Failed to fetch page ${pageCount}: ${response.status} ${response.statusText}`);
        break;
      }

      const jobs = await response.json();

      if (!Array.isArray(jobs) || jobs.length === 0) {
        console.log(`✅ No more jobs found. Total pages: ${pageCount - 1}`);
        hasMoreJobs = false;
        break;
      }

      console.log(`   ✓ Found ${jobs.length} jobs on this page`);
      allJobs.push(...jobs);

      // If we get fewer items than expected, we're on the last page
      if (jobs.length < ITEMS_PER_PAGE) {
        console.log(`✅ Last page reached (${jobs.length} jobs < ${ITEMS_PER_PAGE})`);
        hasMoreJobs = false;
      }

      skipValue += ITEMS_PER_PAGE;

      // Add a small delay to be respectful to the server
      await new Promise(resolve => setTimeout(resolve, 500));

    } catch (error) {
      console.error(`❌ Error fetching page ${pageCount}:`, error.message);
      break;
    }
  }

  return allJobs;
}

async function main() {
  try {
    const jobs = await fetchAllJobs();

    const output = {
      metadata: {
        totalJobs: jobs.length,
        scrapedAt: new Date().toISOString(),
        source: 'https://www.jobtrain.co.uk/iomgovjobs/',
        description: 'All job listings from JobTrain Isle of Man Government Jobs'
      },
      jobs: jobs
    };

    // Save to JSON file
    const outputPath = './all_jobs.json';
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');

    console.log(`\n✨ Success!`);
    console.log(`📊 Total jobs scraped: ${jobs.length}`);
    console.log(`📁 Saved to: ${outputPath}`);
    console.log(`📦 File size: ${(fs.statSync(outputPath).size / 1024).toFixed(2)} KB`);

  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
}

main();
