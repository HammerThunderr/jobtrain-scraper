#!/bin/bash
# GitHub Actions Job Scraper - Quick Setup Script
# Run this script to initialize your repository

set -e

echo "🚀 JobTrain IoM Job Scraper - GitHub Actions Setup"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📥 Initializing git repository..."
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
else
    echo "✅ Git repository already initialized"
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p .github/workflows
mkdir -p data

# Create workflow file
echo "📝 Creating GitHub Actions workflow..."
cp scrape-jobs.yml .github/workflows/ 2>/dev/null || echo "⚠️  Workflow file not found locally"

# Create .gitignore
echo "🛡️  Creating .gitignore..."
cat > .gitignore << 'EOF'
node_modules/
.DS_Store
*.log
.env
.env.local
dist/
build/
EOF

# Create README if it doesn't exist
if [ ! -f README.md ]; then
    echo "📖 Creating README.md..."
    cat > README.md << 'EOF'
# JobTrain IoM Job Scraper

Automatically scrapes all job listings from JobTrain Isle of Man and saves them as JSON.

## 📊 Setup

1. Copy `.github/workflows/scrape-jobs.yml` to your repository
2. Push to GitHub
3. Go to Actions tab to see it run

## 📁 Files

- `data/all_jobs.json` - Generated job listings (auto-updated daily)
- `.github/workflows/scrape-jobs.yml` - GitHub Actions workflow

## 🔄 Schedule

Runs daily at 2 AM UTC (configurable)

## 📞 Support

Check the Actions tab for logs and error details
EOF
fi

# Display summary
echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Verify .github/workflows/scrape-jobs.yml exists"
echo "2. Run: git add ."
echo "3. Run: git commit -m 'Initial commit: Add job scraper workflow'"
echo "4. Run: git push -u origin main"
echo "5. Go to GitHub > Actions tab to monitor"
echo ""
echo "💡 To manually trigger: GitHub > Actions > Scrape Jobs > Run workflow"
echo ""
