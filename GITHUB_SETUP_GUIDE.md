# GitHub Actions Job Scraper Setup Guide

This guide will help you set up automatic job scraping in your GitHub repository.

## 📋 Prerequisites

- A GitHub account
- A GitHub repository (create a new one if needed)
- Git installed on your local machine

## 🚀 Quick Start (5 minutes)

### Step 1: Create or Navigate to Your Repository

```bash
# If you don't have a repo yet:
mkdir jobtrain-scraper
cd jobtrain-scraper
git init
```

### Step 2: Create the GitHub Actions Workflow File

The workflow file should be placed at:
```
.github/workflows/scrape-jobs.yml
```

**Copy the entire workflow content from the `scrape-jobs.yml` file provided.**

### Step 3: Create Initial Files

Create a `.gitignore` file:
```
node_modules/
.DS_Store
*.log
```

Create a `README.md` file:
```markdown
# JobTrain IoM Job Scraper

Automatically scrapes all job listings from JobTrain Isle of Man and saves them as JSON.

## 📊 Data

Job listings are automatically scraped daily and saved to `data/all_jobs.json`

## 🔄 How It Works

- Runs daily at 2 AM UTC (customizable)
- Can also be triggered manually from GitHub Actions
- Fetches all paginated job listings
- Saves complete data to JSON format
- Auto-commits changes to repository

## 📁 File Structure

```
.github/
  workflows/
    scrape-jobs.yml          # GitHub Actions workflow
data/
  all_jobs.json              # Generated job data (auto-updated)
README.md
.gitignore
```

## ⚙️ Configuration

### Change Schedule

Edit `.github/workflows/scrape-jobs.yml` and modify the cron schedule:

```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

**Common cron patterns:**
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight UTC
- `0 9 * * 1` - Every Monday at 9 AM UTC
- `*/30 * * * *` - Every 30 minutes

### Manual Trigger

To run the scraper manually:
1. Go to **Actions** tab on GitHub
2. Select **Scrape JobTrain IoM Jobs**
3. Click **Run workflow**

## 📤 Push to GitHub

```bash
# Initialize git (if new repo)
git init
git add .
git commit -m "Initial commit: Add job scraper workflow"
git branch -M main

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR-USERNAME/jobtrain-scraper.git
git push -u origin main
```

## ✅ Verify It's Working

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see the workflow listed
4. Click on it to see execution details
5. After first run, check `data/all_jobs.json` for scraped jobs

## 📊 JSON Output Format

```json
{
  "metadata": {
    "totalJobs": 48,
    "scrapedAt": "2024-03-21T10:30:00.000Z",
    "source": "https://www.jobtrain.co.uk/iomgovjobs/",
    "description": "All job listings from JobTrain Isle of Man Government Jobs"
  },
  "jobs": [
    {
      "id": "12345",
      "title": "Software Developer",
      "department": "IT",
      ...
    },
    ...
  ]
}
```

## 🔧 Troubleshooting

### Workflow not appearing
- Make sure file is at `.github/workflows/scrape-jobs.yml`
- File must be on the `main` or `default` branch
- Refresh the page and wait a few seconds

### Jobs not being committed
- Check that the repository has write permissions enabled
- Go to **Settings** > **Actions** > **Workflow permissions**
- Select "Read and write permissions"

### Script errors
- Check the **Actions** tab to see detailed logs
- Click the failed workflow run to see error messages

## 🛡️ Security Notes

- The workflow uses GitHub's built-in environment
- No credentials needed for this public API
- Auto-commits are made by GitHub Action Bot
- No sensitive data is handled

## 📝 Advanced Customization

### Change Output Location
Edit the scraper script path in `scrape-jobs.yml`:
```yaml
const outputPath = 'data/all_jobs.json';
```

### Add Notifications
Add to workflow to notify on completion:
```yaml
- name: 📧 Notify on completion
  if: always()
  run: echo "Scraping completed at $(date)"
```

### Save Multiple Formats
Modify the script to also save as CSV, XML, etc.

## 📞 Support

If you encounter issues:
1. Check the workflow logs in **Actions** tab
2. Verify the `.github/workflows/scrape-jobs.yml` file syntax
3. Ensure your GitHub account has appropriate permissions

---

**Last Updated:** March 2024
**Status:** Working ✅
