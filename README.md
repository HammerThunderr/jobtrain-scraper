# JobTrain IoM Job Scraper 🚀

Automatically scrape all job listings from JobTrain Isle of Man and save them as JSON.

## 📦 What's Included

This package contains everything you need to scrape jobs using GitHub Actions or run locally.

```
jobtrain-scraper/
├── .github/workflows/
│   ├── scrape-jobs.yml              ← GitHub Actions (Node.js) ⭐ RECOMMENDED
│   └── scrape-jobs-python.yml       ← GitHub Actions (Python)
├── job_scraper.js                   ← Local Node.js script
├── job_scraper.py                   ← Local Python script
├── setup.sh                         ← Auto-setup script
├── GITHUB_SETUP_GUIDE.md            ← Full GitHub Actions guide
├── FILE_LOCATION_GUIDE.md           ← File index & navigation
├── all_jobs.json                    ← Sample output format
└── README.md                        ← This file
```

---

## 🎯 Quick Start (Choose One)

### Option 1: GitHub Actions (Automatic - Recommended ⭐)

**Best for:** Automated daily scraping, no local setup needed

1. **Create a GitHub repo:**
   ```bash
   mkdir jobtrain-scraper
   cd jobtrain-scraper
   git init
   ```

2. **Copy workflow file:**
   - Copy `.github/workflows/scrape-jobs.yml` to your repo
   - Keep the folder structure: `.github/workflows/scrape-jobs.yml`

3. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit: Add job scraper workflow"
   git remote add origin https://github.com/YOUR-USERNAME/jobtrain-scraper.git
   git push -u origin main
   ```

4. **Monitor:**
   - Go to GitHub → **Actions** tab
   - See the workflow run automatically
   - Check `data/all_jobs.json` for results

**Schedule:** Runs daily at 2 AM UTC (customizable in YAML file)

---

### Option 2: Run Locally (Manual)

**Best for:** One-time scraping or testing

#### Node.js Version:
```bash
# Requires Node.js 18+
node job_scraper.js
# Output: all_jobs.json
```

#### Python Version:
```bash
# Requires Python 3.7+
pip install requests
python3 job_scraper.py
# Output: all_jobs.json
```

---

### Option 3: Quick GitHub Setup (Use Script)

**For Linux/Mac users:**
```bash
chmod +x setup.sh
./setup.sh
```

This automatically:
- Creates folder structure
- Adds workflow files
- Initializes git
- Creates `.gitignore`

---

## 📊 Output Format

The scraper creates `all_jobs.json` with this structure:

```json
{
  "metadata": {
    "totalJobs": 48,
    "scrapedAt": "2024-03-21T02:00:00.000Z",
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

---

## ⚙️ Configuration

### Change Scraping Schedule

Edit `.github/workflows/scrape-jobs.yml` and modify the cron:

```yaml
schedule:
  - cron: '0 2 * * *'  # Current: Daily at 2 AM UTC
```

**Common patterns:**
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight UTC
- `0 9 * * 1` - Every Monday at 9 AM UTC
- `*/30 * * * *` - Every 30 minutes

### Manual Trigger

1. Go to GitHub → **Actions**
2. Select "Scrape JobTrain IoM Jobs"
3. Click "Run workflow"
4. Done! ✅

---

## 📖 Documentation Files

### GITHUB_SETUP_GUIDE.md
- Complete step-by-step setup instructions
- Troubleshooting tips
- Advanced customization
- Security information

### FILE_LOCATION_GUIDE.md
- Detailed file descriptions
- Which files you actually need
- Setup checklist
- Common issues & solutions

---

## 🔧 System Requirements

**For GitHub Actions:**
- GitHub account (free)
- GitHub repository (free)
- That's it! ✅

**For Local Execution:**

*Node.js version:*
- Node.js 18+ ([download](https://nodejs.org/))
- No dependencies needed

*Python version:*
- Python 3.7+ ([download](https://python.org/))
- `requests` library: `pip install requests`

---

## ✨ Features

✅ **Automatic pagination handling** - Scrapes all pages (Skip=0, 12, 24, etc.)  
✅ **Error handling** - Graceful failures, detailed logs  
✅ **Rate limiting** - Respectful delays between requests  
✅ **Timestamp** - Knows exactly when data was scraped  
✅ **Auto-commit** - Changes automatically committed to GitHub  
✅ **Metadata** - Total job count, source, timestamp included  

---

## 🐛 Troubleshooting

### Workflow not appearing in GitHub Actions
- Make sure `.github/workflows/scrape-jobs.yml` is on the `main` branch
- Wait 30 seconds and refresh the page

### "No jobs found" or empty JSON
- Check internet connection
- Verify the API is still accessible
- Check GitHub Actions logs for details

### Permission denied on setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

### Python: requests module not found
```bash
pip install requests
# or
pip3 install requests
```

### Node.js: Syntax error
- Make sure you have Node.js 18+
- Check: `node --version`

---

## 📝 Example Usage

### Process the JSON data:

**Node.js:**
```javascript
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('all_jobs.json', 'utf-8'));
console.log(`Total jobs: ${data.metadata.totalJobs}`);
data.jobs.forEach(job => console.log(job.title));
```

**Python:**
```python
import json
with open('all_jobs.json') as f:
    data = json.load(f)
print(f"Total jobs: {data['metadata']['totalJobs']}")
for job in data['jobs']:
    print(job['title'])
```

---

## 🔒 Security & Privacy

- ✅ No credentials needed (public API)
- ✅ No sensitive data stored
- ✅ GitHub Action Bot makes commits (read the logs)
- ✅ All code is visible and auditable
- ✅ Uses HTTPS only

---

## 📊 Data Source

**Endpoint:** `https://www.jobtrain.co.uk/iomgovjobs/Home/_JobCard`

**Pagination:** 12 items per page (Skip parameter increments by 12)

**Format:** JSON API

**Terms:** Please review JobTrain's terms of service before using

---

## 🤝 Contributing

Found a bug? Want to improve it?
1. Edit the scraper script
2. Test locally
3. Commit and push
4. Let me know!

---

## 📄 License

These scripts are provided as-is for your use. Please respect JobTrain's terms of service.

---

## 🚀 Getting Help

1. **Check the docs:**
   - `GITHUB_SETUP_GUIDE.md` - GitHub Actions setup
   - `FILE_LOCATION_GUIDE.md` - File descriptions

2. **Review script comments:**
   - `job_scraper.js` - Well-commented source
   - `job_scraper.py` - Documented code

3. **Check GitHub Actions logs:**
   - GitHub → Repository → Actions → Recent runs → Click run → Logs

---

## 📋 Checklist for GitHub Actions

- [ ] Downloaded `scrape-jobs.yml`
- [ ] Created `.github/workflows/` folder
- [ ] Placed workflow file in correct location
- [ ] Created GitHub repository
- [ ] Pushed files to GitHub
- [ ] Checked Actions tab - workflow visible
- [ ] Clicked "Run workflow" - job ran successfully
- [ ] Checked `data/all_jobs.json` - has job data

---

## 💡 Next Steps

1. **Set up GitHub Actions** (5 minutes) - Automated daily scraping
2. **Test locally** (2 minutes) - Make sure it works
3. **Customize schedule** (1 minute) - Change when it runs
4. **Monitor results** (ongoing) - Check Actions tab weekly

---

**Happy scraping! 🎉**

For detailed instructions, see `GITHUB_SETUP_GUIDE.md`

---

*Last Updated: March 2024*  
*Status: ✅ Working*  
*Tested with: Node.js 18+, Python 3.7+, GitHub Actions*
