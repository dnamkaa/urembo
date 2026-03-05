# GitHub Testing Guide - Smart Retail System

## 📋 Setup Instructions

### Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **New Repository**
3. Repository name: `smart-retail-system` (or your preferred name)
4. Description: `Point of Sale & Inventory Management System for Tanzania`
5. Choose: **Public** (to allow GitHub Actions free tier)
6. **Do NOT** initialize with README, .gitignore, or license (we have our own)
7. Click **Create repository**

### Step 2: Push Your Code to GitHub

```bash
# Navigate to your project directory
cd c:\Users\knamk\Desktop\urembo

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your code
git commit -m "Initial commit: Smart Retail System with POS and Reports modules"

# Add remote repository (replace USERNAME and REPO)
git remote add origin https://github.com/USERNAME/smart-retail-system.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 3: Verify GitHub Actions

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see "Smart Retail Tests" workflow
4. It will automatically run on your push ✨

## 🧪 Automated Testing

### What GitHub Actions Does

**File:** `.github/workflows/tests.yml`

When you push code to `main` or `develop` branches, GitHub automatically:

1. ✅ Spins up Linux test runners
2. ✅ Installs Python 3.9, 3.10, 3.11
3. ✅ Installs dependencies from `requirements.txt`
4. ✅ Runs all POS Module tests (17 tests)
5. ✅ Runs all Reports Module tests (21 tests)
6. ✅ Reports results back to your repository

### Expected Test Results

#### ✅ Success Case
```
Test run ID: f4d3e2a1 | Testing POS Module
✓ test_1_product_search
✓ test_2_add_to_cart
✓ test_3_update_quantity
... (14 more tests)
✓ test_17_inactive_product_rejection

Test run ID: f4d3e2a1 | Testing Reports Module
✓ test_1_dashboard_kpis_returned
✓ test_2_dashboard_totals_correct
... (19 more tests)
✓ test_21_profit_snapshot_cost_assumptions

Result: ✅ All tests passed
```

#### ❌ Failure Case
If a test fails, you'll see:
```
FAIL: test_5_checkout_reduces_stock
AssertionError: Expected 15 remaining stock, got 20
```

You can click the failed test to see the full error and fix it.

## 📊 View Test Results

### Method 1: GitHub Web Interface
1. Go to your repository
2. Click **Actions**
3. Click the latest workflow run
4. Expand **Run POS Module Tests** or **Run Reports Module Tests**
5. See full test output

### Method 2: Pull Request Badge
Add this to your README if you want a test status badge:

```markdown
![Tests](https://github.com/YOUR_USERNAME/smart-retail-system/workflows/Smart%20Retail%20Tests/badge.svg)
```

### Method 3: Branch Protection
Require tests to pass before merging:
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable "Require status checks to pass"
4. Select "Smart Retail Tests"

## 🔄 Workflow Triggers

Tests automatically run on:

| Event | Trigger |
|-------|---------|
| **Push** | Any commit to `main` or `develop` |
| **Pull Request** | When creating/updating PR against `main` or `develop` |
| **Manual** | Click "Run workflow" on GitHub Actions tab |

## 🛠️ Troubleshooting

### Tests Pass Locally but Fail on GitHub

**Possible causes:**
- Environment differences (OS, Python version)
- Missing dependencies in `requirements.txt`
- Hardcoded paths (Windows vs Linux)
- Database file location issues

**Fix:**
```bash
# Make sure requirements.txt is up to date
pip freeze > requirements.txt

# Test on multiple Python versions locally
python -m unittest discover -v
```

### Workflow File Not Found

**Error:** "No such file or directory: .github/workflows/tests.yml"

**Fix:**
```bash
# Files are case-sensitive on Linux
# Make sure the directory structure is correct:
# .github/
#   └─ workflows/
#       └─ tests.yml

git add .github/workflows/tests.yml
git commit -m "Add GitHub Actions workflow"
git push
```

### Tests Timeout on GitHub

**Error:** "The operation timed out after 5 minutes"

**Fix:** Set longer timeout in workflow file:
```yaml
- name: Run POS Module Tests
  timeout-minutes: 10  # Increase this value
  run: python -m unittest tests_pos.TestPOSSalesModule -v
```

## 📚 GitHub Actions Concepts

### What is GitHub Actions?
- Free CI/CD (Continuous Integration/Continuous Deployment)
- Automatically runs scripts when you push code
- Great for running tests, building, deploying
- Works with Ubuntu, Windows, macOS runners

### Benefits for Your Project
✅ **Catch bugs early** - Tests run before you merge  
✅ **Verify multi-version support** - Test on Python 3.9/3.10/3.11  
✅ **Team confidence** - Everyone knows code is tested  
✅ **Documentation** - Workflow shows how to run tests  
✅ **Free** - GitHub provides free minutes for public repos  

### Naming Convention
```
.github/
└── workflows/
    └── tests.yml          # CI workflow (what you have)
    ├── deploy.yml         # Deployment (future)
    └── lint.yml           # Code quality (future)
```

## 🚀 Next Steps

1. **Push to GitHub** using instructions above
2. **Watch GitHub Actions run** in the Actions tab
3. **Verify all tests pass** with green checkmarks
4. **Enable branch protection** to prevent unverified merges
5. **Add collaborators** and enable code review
6. **Monitor test coverage** for quality metrics

## 💡 Pro Tips

### Tip 1: Add Requirements
Keep requirements.txt updated:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
```

### Tip 2: Commit Messages
Use clear, descriptive commits:
```bash
git commit -m "Fix: Discount validation should not exceed subtotal"
```

### Tip 3: Branch Strategy
```bash
# Create feature branch
git checkout -b feature/inventory-reports

# Make changes and test locally
python -m unittest discover -v

# Push to feature branch
git push -u origin feature/inventory-reports

# Create Pull Request on GitHub
# GitHub Actions runs tests automatically
# Review and merge if tests pass ✅
```

### Tip 4: Local Testing Before Push
Always test locally before pushing:
```bash
# Full test run
python -m unittest discover -v

# Or specific suite
python -m unittest tests_pos.TestPOSSalesModule -v
```

## 📖 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [GitHub Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

**Happy testing! 🎉**

If you have questions about GitHub Actions or the test setup, refer to the main README.md or check the `.github/workflows/tests.yml` file.
