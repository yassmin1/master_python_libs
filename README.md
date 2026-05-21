# Pandas Pathway

An interactive Python app for learning Pandas from beginner to advanced level.

## Run

From PowerShell:

```powershell
cd C:\Users\ryass\OneDrive\Documents\GitHub\Python_apps\pandas-learning-app
python -m streamlit run streamlit_app.py
```

If Streamlit is not installed:

```powershell
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## What is included

- Pandas mastery roadmap
- Concept library explaining the mental model behind the syntax
- Beginner, intermediate, and advanced Pandas lessons
- Cheat sheets grouped by task
- Real Pandas DataFrame playground
- Filters, sorting, groupby summaries, and charts
- Common Pandas mistakes with better patterns
- Mastery drills for active recall
- Quiz questions with explanations
- Project ideas with deliverables
- Guided Jupyter notebooks that teach Pandas with synthetic practice datasets
- Suggested eight-week study plan

The main app file is `streamlit_app.py`. It contains comments explaining how the app is organized and how the Pandas examples work.

## Project notebooks

The guided notebooks are in the `notebooks` folder:

- `01_movie_ratings_explorer.ipynb`
- `02_personal_budget_tracker.ipynb`
- `03_retail_sales_analysis.ipynb`
- `04_support_ticket_operations.ipynb`
- `05_time_series_feature_builder.ipynb`
- `06_reusable_cleaning_pipeline.ipynb`

Each notebook includes a project description, business goal, step-by-step tasks, synthetic dataset generation, commented Pandas code, practice prompts for changing the data, and final reflection prompts.

To make the project cards open notebooks in Google Colab, push this folder to GitHub and set these environment variables before running Streamlit:

```powershell
$env:GITHUB_REPO_SLUG="your-github-user-or-org/your-repo"
$env:GITHUB_BRANCH="main"
$env:GITHUB_PROJECT_PATH="pandas-learning-app"
python -m streamlit run streamlit_app.py
```
