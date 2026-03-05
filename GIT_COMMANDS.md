# Quick Git Commands for GitHub

## First-Time Setup (One-time only)

```bash
# Navigate to project directory
cd c:\Users\knamk\Desktop\urembo

# Initialize git (only if not already initialized)
git init

# Configure git with your GitHub account
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Smart Retail System with POS and Reports modules"

# Add GitHub remote (replace USERNAME/REPO)
git remote add origin https://github.com/USERNAME/smart-retail-system.git

# Rename branch to 'main' (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Daily Workflow (After each change)

```bash
# Check what changed
git status

# Stage your changes
git add .
# OR stage specific files:
git add app.py templates/pos/terminal.html

# Create meaningful commit message
git commit -m "Feature: Add discount validation to POS checkout"

# Push to GitHub
git push origin main
```

## Creating a Feature Branch (Best Practice)

```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name

# Make your changes, test them locally:
python -m unittest discover -v

# Stage and commit
git add .
git commit -m "your descriptive message"

# Push feature branch
git push -u origin feature/your-feature-name

# On GitHub, create Pull Request from web interface
# GitHub Actions will auto-run tests on your PR
# Fix any test failures if needed
# Merge to main when tests pass ✅
```

## Useful Commands

```bash
# View commit history
git log --oneline

# See what files changed
git status

# View diff of changes
git diff

# Undo last commit (but keep changes)
git reset --soft HEAD~1

# Undo changes to a file
git checkout -- filename.py

# View all branches
git branch -a

# Switch to different branch
git checkout branch-name

# Delete local branch
git branch -d branch-name

# View configured remotes
git remote -v
```

## Troubleshooting

### Command: "git: command not found"
✅ **Solution:** Install Git from https://git-scm.com/

### Error: "fatal: not a git repository"
```bash
# Initialize git in the directory
git init
```

### Error: "Permission denied (publickey)"
✅ **Solution:** Set up SSH keys or use HTTPS:
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/USERNAME/smart-retail-system.git
```

### Forgot to add a file
```bash
# Add the file and amend previous commit
git add forgotten_file.py
git commit --amend --no-edit
git push -f origin branch-name
```

### Want to undo last push
```bash
# ⚠️ Only if not merged to main!
git reset --hard HEAD~1
git push -f origin branch-name
```

## GitHub Authentication

### Option 1: Personal Access Token (Recommended)
1. GitHub Settings → Developer settings → Personal access tokens
2. Create new token with `repo` scope
3. Use token as password when pushing: `git push` → enter username → paste token as password

### Option 2: SSH Keys
1. Generate SSH key: `ssh-keygen -t ed25519`
2. Add to GitHub: Settings → SSH and GPG keys
3. Use SSH URLs: `git@github.com:USERNAME/repo.git`

### Option 3: GitHub CLI
```bash
# Install: https://cli.github.com/
gh auth login
# Then use normal git commands
```

## Checking Test Results

After pushing:
```bash
# View workflow runs
gh workflow view

# View logs of latest run
gh run view

# View specific run
gh run view RUN_ID
```

---

## Essential Links

- **Repository:** `https://github.com/USERNAME/smart-retail-system`
- **Actions:** `https://github.com/USERNAME/smart-retail-system/actions`
- **Commits:** `https://github.com/USERNAME/smart-rental-system/commits/main`
- **Branches:** `https://github.com/USERNAME/smart-retail-system/branches`

Replace `USERNAME` and `smart-retail-system` with your actual GitHub username and repository name.

---

**Ready to push?** Run the First-Time Setup commands above! 🚀
