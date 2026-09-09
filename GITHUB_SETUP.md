# GitHub Setup Guide

Follow these steps to create a GitHub repository and push your AtliQ T-shirts project.

## Step 1: Initialize Git Repository

Open terminal/command prompt in your project directory and run:

```bash
# Navigate to your project directory
cd "C:\Users\Utkarsh\Desktop\Programming\WebDev\langchain\4_sqldb_tshirts"

# Initialize git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: AtliQ T-shirts LangChain MySQL app"
```

## Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `atliq-tshirts-langchain-mysql`
   - **Description**: `Natural language to SQL queries for t-shirt inventory using LangChain and Google Gemini`
   - **Visibility**: Choose Public or Private
   - **DON'T** initialize with README (since we already have one)
5. Click "Create repository"

## Step 3: Connect Local Repository to GitHub

After creating the GitHub repository, you'll see commands like these. Run them in your terminal:

```bash
# Add GitHub remote (replace with your actual GitHub username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/atliq-tshirts-langchain-mysql.git

# Set the default branch name
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Set Up Environment Variables

**IMPORTANT**: Your `.env` file is already in `.gitignore` so your secrets won't be uploaded.

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials:
   ```env
   GOOGLE_API_KEY=your_actual_google_api_key_here
   DB_PASSWORD=your_actual_mysql_password
   ```

## Step 5: Verify Repository

1. Go to your GitHub repository URL
2. Check that all files are there EXCEPT `.env` (should be ignored)
3. Verify README.md displays properly

## Step 6: Clone Instructions for Others

Add these instructions to share your project:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/atliq-tshirts-langchain-mysql.git

# Navigate to project directory
cd atliq-tshirts-langchain-mysql

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual credentials

# Run the application
streamlit run main.py
```

## Repository Structure

Your GitHub repository will contain:
```
atliq-tshirts-langchain-mysql/
├── .gitignore                 # Prevents sensitive files from being committed
├── .env.example              # Template for environment variables
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── main.py                   # Streamlit app entry point
├── langchain_helper.py       # LangChain integration logic
├── few_shots.py             # Few-shot learning examples
├── atliq_tees.png           # Project image
├── t_shirt_sales_llm.ipynb  # Development notebook
└── database/
    └── db_creation_atliq_t_shirts.sql  # Database schema
```

## Security Notes

✅ **What's Protected:**
- `.env` file (contains API keys and passwords)
- `__pycache__/` directories
- Virtual environment folders
- IDE configuration files

✅ **What's Public:**
- Source code
- `.env.example` template
- Documentation
- Database schema (no sensitive data)

Your sensitive credentials are safe and won't be exposed on GitHub!
