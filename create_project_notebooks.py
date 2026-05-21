"""Generate guided Pandas project notebooks.

The notebooks are created with plain JSON so this project does not need an
extra dependency such as nbformat. Each notebook includes:

- A real project description
- Business questions
- Step-by-step tasks
- Synthetic starter data generated inside the notebook
- Commented Pandas code
- Reflection prompts for the learner

Run from this folder:

    python create_project_notebooks.py
"""

from __future__ import annotations

import json
from textwrap import dedent
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOK_DIR = ROOT / "notebooks"


def markdown_cell(text: str) -> dict:
    """Create a Jupyter markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in dedent(text).strip().splitlines()],
    }


def code_cell(code: str) -> dict:
    """Create a Jupyter code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in dedent(code).strip().splitlines()],
    }


def notebook(cells: list[dict]) -> dict:
    """Create the minimal JSON structure expected by Jupyter notebooks."""
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


PROJECTS = {
    "01_movie_ratings_explorer.ipynb": notebook(
        [
            markdown_cell(
                """
                # Movie Ratings Explorer

                **Level:** Beginner

                ## Project description

                You are helping a streaming team understand a small movie ratings dataset.
                The team wants to know which genres perform best, which years have the most
                titles, and whether any missing values need to be fixed before analysis.

                ## Skills practiced

                - Creating a DataFrame
                - Inspecting rows, columns, and data types
                - Handling missing values
                - Grouping and sorting results
                - Writing short findings from data
                """
            ),
            markdown_cell(
                """
                ## Step 1: Import Pandas and generate synthetic starter data

                In real projects, the data usually comes from a CSV or database. For practice,
                you can generate synthetic data: realistic-looking data you create yourself.
                This keeps the notebook portable and lets you change the row count, categories,
                missing values, and random seed to make new practice datasets.
                """
            ),
            code_cell(
                """
                import pandas as pd
                import numpy as np
                import secrets

                practice_run_name = f"movie-ratings-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_movie_data(row_count=24, seed=42):
                    \"\"\"Create a synthetic movie ratings dataset for practice.\"\"\"
                    rng = np.random.default_rng(seed)
                    genres = np.array(["Drama", "Sci-Fi", "Action", "Comedy", "Documentary"])

                    movies = pd.DataFrame({
                        "title": [f"Practice Movie {number:02d}" for number in range(1, row_count + 1)],
                        "genre": rng.choice(genres, size=row_count, p=[0.25, 0.2, 0.25, 0.2, 0.1]),
                        "year": rng.integers(2018, 2027, size=row_count),
                        "rating": rng.normal(loc=7.4, scale=0.8, size=row_count).round(1),
                        "votes": rng.integers(150, 5000, size=row_count),
                    })
                    movies["rating"] = movies["rating"].clip(lower=4.0, upper=9.8)

                    # Add a few realistic data quality issues for cleaning practice.
                    movies.loc[rng.choice(movies.index, size=2, replace=False), "genre"] = None
                    movies.loc[rng.choice(movies.index, size=2, replace=False), "rating"] = np.nan
                    return movies

                movies = make_movie_data(row_count=24, seed=42)

                movies
                """
            ),
            markdown_cell(
                """
                ## Step 2: Inspect the data

                Before changing anything, inspect the dataset. Good analysts do this every
                time because assumptions about columns, missing values, and data types are
                often wrong.
                """
            ),
            code_cell(
                """
                movies.head()
                """
            ),
            code_cell(
                """
                movies.info()
                """
            ),
            code_cell(
                """
                movies.isna().sum()
                """
            ),
            markdown_cell(
                """
                ## Step 3: Clean missing values

                The `genre` column is required for genre analysis, so we label missing genre
                values as `Unknown`. The missing rating is different: replacing it with a fake
                value would distort averages, so we keep it missing for rating calculations.
                """
            ),
            code_cell(
                """
                movies_clean = movies.copy()

                # Fill only the missing genre labels.
                movies_clean["genre"] = movies_clean["genre"].fillna("Unknown")

                movies_clean
                """
            ),
            markdown_cell(
                """
                ## Step 4: Answer the business questions
                """
            ),
            code_cell(
                """
                # Which genres have the highest average rating?
                genre_summary = (
                    movies_clean
                    .groupby("genre", as_index=False)
                    .agg(
                        average_rating=("rating", "mean"),
                        movie_count=("title", "count"),
                        total_votes=("votes", "sum"),
                    )
                    .sort_values("average_rating", ascending=False)
                )

                genre_summary
                """
            ),
            code_cell(
                """
                # Which years have the most movies in this dataset?
                year_summary = (
                    movies_clean
                    .groupby("year", as_index=False)
                    .agg(movie_count=("title", "count"))
                    .sort_values(["movie_count", "year"], ascending=[False, True])
                )

                year_summary
                """
            ),
            markdown_cell(
                """
                ## Step 5: Write findings

                Replace the prompts below with your own conclusions.

                - Highest-rated genre:
                - Year with the most titles:
                - Data quality issue found:
                - One recommendation for the streaming team:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `row_count` and `seed` below to create a new practice dataset. Set
                `seed=None` when you want a randomized dataset each time the cell runs. Then
                rerun the analysis and compare whether your findings changed.
                """
            ),
            code_cell(
                """
                my_movies = make_movie_data(row_count=50, seed=7)
                my_movies.head()
                """
            ),
        ]
    ),
    "02_personal_budget_tracker.ipynb": notebook(
        [
            markdown_cell(
                """
                # Personal Budget Tracker

                **Level:** Beginner

                ## Project description

                You have a month of transaction data and need to summarize spending by
                category. The goal is to find where money is going and identify unusually
                large expenses.

                ## Skills practiced

                - Loading transaction-style data
                - Cleaning category labels
                - Creating income and expense summaries
                - Filtering unusual records
                """
            ),
            code_cell(
                """
                import pandas as pd
                import numpy as np
                import secrets

                practice_run_name = f"personal-budget-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_transaction_data(row_count=40, seed=42):
                    \"\"\"Create a synthetic personal finance dataset for practice.\"\"\"
                    rng = np.random.default_rng(seed)
                    expense_categories = np.array([
                        "Groceries", "Utilities", "Entertainment", "Dining",
                        "Housing", "Transport", "Education", "Health"
                    ])
                    merchants = {
                        "Groceries": ["Metro Grocery", "Fresh Basket", "Corner Market"],
                        "Utilities": ["City Power", "Water Works", "Mobile Plan"],
                        "Entertainment": ["StreamBox", "Cinema House", "Game Store"],
                        "Dining": ["Coffee Corner", "Noodle Bar", "Taco Stop"],
                        "Housing": ["Rent", "Home Supplies"],
                        "Transport": ["Train Pass", "Ride Share", "Fuel Station"],
                        "Education": ["Book Store", "Online Course"],
                        "Health": ["Doctor Office", "Pharmacy"],
                    }

                    dates = pd.date_range("2026-02-01", periods=28, freq="D")
                    rows = []
                    for _ in range(row_count):
                        category = rng.choice(expense_categories)
                        rows.append({
                            "date": rng.choice(dates),
                            "merchant": rng.choice(merchants[category]),
                            "category": category,
                            "amount": -round(float(rng.lognormal(mean=3.6, sigma=0.7)), 2),
                        })

                    rows.extend([
                        {"date": pd.Timestamp("2026-02-01"), "merchant": "Paycheck", "category": "Income", "amount": 2400.00},
                        {"date": pd.Timestamp("2026-02-25"), "merchant": "Paycheck", "category": "Income", "amount": 2400.00},
                    ])

                    transactions = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
                    transactions.loc[transactions.index[1], "category"] = " groceries "
                    return transactions

                transactions = make_transaction_data(row_count=40, seed=42)
                transactions
                """
            ),
            markdown_cell(
                """
                ## Step 1: Clean category labels

                Notice that one category has extra spaces and inconsistent capitalization.
                Clean text early so grouped results are accurate.
                """
            ),
            code_cell(
                """
                budget = transactions.copy()

                budget["category"] = (
                    budget["category"]
                    .str.strip()
                    .str.title()
                )

                budget
                """
            ),
            markdown_cell(
                """
                ## Step 2: Create useful columns

                Expenses are negative numbers in this dataset. We create a positive
                `expense_amount` column so spending summaries are easier to read.
                """
            ),
            code_cell(
                """
                budget["expense_amount"] = budget["amount"].where(budget["amount"] < 0, 0).abs()
                budget["income_amount"] = budget["amount"].where(budget["amount"] > 0, 0)

                budget
                """
            ),
            markdown_cell(
                """
                ## Step 3: Summarize spending by category
                """
            ),
            code_cell(
                """
                category_spending = (
                    budget
                    .groupby("category", as_index=False)
                    .agg(
                        total_spent=("expense_amount", "sum"),
                        transaction_count=("merchant", "count"),
                    )
                    .sort_values("total_spent", ascending=False)
                )

                category_spending
                """
            ),
            code_cell(
                """
                total_income = budget["income_amount"].sum()
                total_expenses = budget["expense_amount"].sum()
                net_cash_flow = total_income - total_expenses

                pd.DataFrame({
                    "metric": ["Total income", "Total expenses", "Net cash flow"],
                    "amount": [total_income, total_expenses, net_cash_flow],
                })
                """
            ),
            markdown_cell(
                """
                ## Step 4: Find unusual expenses

                For this project, define an unusual expense as any expense over $200.
                """
            ),
            code_cell(
                """
                unusual_expenses = budget.loc[budget["expense_amount"] > 200]
                unusual_expenses
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Biggest spending category:
                - Net cash flow:
                - Unusual expense found:
                - One budget change you recommend:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Create a larger or smaller month of transactions by changing `row_count` and
                `seed`. Set `seed=None` for a randomized dataset each run. You can also edit
                the merchant and category lists inside the function.
                """
            ),
            code_cell(
                """
                my_transactions = make_transaction_data(row_count=75, seed=13)
                my_transactions.head()
                """
            ),
        ]
    ),
    "03_retail_sales_analysis.ipynb": notebook(
        [
            markdown_cell(
                """
                # Retail Sales Analysis

                **Level:** Intermediate

                ## Project description

                A retail manager has separate order and product tables. Your job is to
                merge them, calculate revenue and profit, and summarize performance by
                region and product category.

                ## Skills practiced

                - Merging tables
                - Creating calculated columns
                - Grouping by multiple fields
                - Ranking categories by business metrics
                """
            ),
            code_cell(
                """
                import pandas as pd
                import numpy as np
                import secrets

                practice_run_name = f"retail-sales-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_retail_data(order_count=40, seed=42):
                    \"\"\"Create synthetic order and product tables for merge practice.\"\"\"
                    rng = np.random.default_rng(seed)
                    products = pd.DataFrame({
                        "product_id": ["P1", "P2", "P3", "P4", "P5", "P6"],
                        "product_name": [
                            "Analytics Course", "Keyboard", "Consulting Hour",
                            "Data Template", "Monitor", "Automation Workbook"
                        ],
                        "category": ["Software", "Hardware", "Services", "Software", "Hardware", "Software"],
                        "price": [120, 80, 150, 45, 220, 65],
                        "unit_cost": [30, 45, 70, 10, 140, 15],
                    })
                    orders = pd.DataFrame({
                        "order_id": range(101, 101 + order_count),
                        "date": rng.choice(pd.date_range("2026-03-01", periods=31, freq="D"), size=order_count),
                        "region": rng.choice(["West", "East", "South", "North"], size=order_count),
                        "product_id": rng.choice(products["product_id"], size=order_count),
                        "units": rng.integers(1, 9, size=order_count),
                    }).sort_values("date").reset_index(drop=True)
                    return orders, products

                orders, products = make_retail_data(order_count=40, seed=42)
                """
            ),
            markdown_cell("## Step 1: Inspect both tables"),
            code_cell(
                """
                orders
                """
            ),
            code_cell(
                """
                products
                """
            ),
            markdown_cell(
                """
                ## Step 2: Merge orders with product details

                Use a left merge because every order should remain in the analysis.
                If product details are missing, that is a data quality issue to investigate.
                """
            ),
            code_cell(
                """
                sales = orders.merge(products, on="product_id", how="left")
                sales
                """
            ),
            markdown_cell("## Step 3: Create revenue and profit columns"),
            code_cell(
                """
                sales = sales.assign(
                    revenue=lambda data: data["units"] * data["price"],
                    cost=lambda data: data["units"] * data["unit_cost"],
                    profit=lambda data: data["revenue"] - data["cost"],
                )

                sales
                """
            ),
            markdown_cell("## Step 4: Summarize by region"),
            code_cell(
                """
                region_summary = (
                    sales
                    .groupby("region", as_index=False)
                    .agg(
                        orders=("order_id", "count"),
                        units=("units", "sum"),
                        revenue=("revenue", "sum"),
                        profit=("profit", "sum"),
                    )
                    .sort_values("revenue", ascending=False)
                )

                region_summary
                """
            ),
            markdown_cell("## Step 5: Summarize by category"),
            code_cell(
                """
                category_summary = (
                    sales
                    .groupby("category", as_index=False)
                    .agg(
                        units=("units", "sum"),
                        revenue=("revenue", "sum"),
                        profit=("profit", "sum"),
                    )
                    .assign(profit_margin=lambda data: data["profit"] / data["revenue"])
                    .sort_values("profit", ascending=False)
                )

                category_summary
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Best region by revenue:
                - Best category by profit:
                - Category with the highest profit margin:
                - One action you recommend to the retail manager:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `order_count` and `seed`, or add products to the product table inside
                the function. Set `seed=None` for a randomized dataset each run. Then rerun
                the merge and summaries.
                """
            ),
            code_cell(
                """
                my_orders, my_products = make_retail_data(order_count=100, seed=21)
                my_orders.head()
                """
            ),
        ]
    ),
    "04_support_ticket_operations.ipynb": notebook(
        [
            markdown_cell(
                """
                # Support Ticket Operations

                **Level:** Intermediate

                ## Project description

                A support team wants to understand response speed and backlog risk.
                You will clean date columns, calculate response times, and summarize
                tickets by priority and status.

                ## Skills practiced

                - Parsing dates
                - Calculating time differences
                - Pivot tables
                - Filtering operational risk
                """
            ),
            code_cell(
                """
                import pandas as pd
                import numpy as np
                import secrets

                practice_run_name = f"support-tickets-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_ticket_data(row_count=35, seed=42):
                    \"\"\"Create a synthetic support ticket dataset for operations practice.\"\"\"
                    rng = np.random.default_rng(seed)
                    created_at = (
                        pd.Timestamp("2026-04-01 08:00")
                        + pd.to_timedelta(rng.integers(0, 10 * 24 * 60, size=row_count), unit="m")
                    )
                    status = rng.choice(["Closed", "Open"], size=row_count, p=[0.7, 0.3])
                    response_minutes = rng.integers(20, 8 * 60, size=row_count)

                    tickets = pd.DataFrame({
                        "ticket_id": range(2001, 2001 + row_count),
                        "priority": rng.choice(["High", "Medium", "Low"], size=row_count, p=[0.25, 0.45, 0.30]),
                        "status": status,
                        "created_at": created_at,
                    }).sort_values("created_at").reset_index(drop=True)

                    tickets["first_response_at"] = tickets["created_at"] + pd.to_timedelta(response_minutes, unit="m")
                    tickets.loc[tickets["status"] == "Open", "first_response_at"] = pd.NaT
                    return tickets

                tickets = make_ticket_data(row_count=35, seed=42)
                tickets
                """
            ),
            markdown_cell("## Step 1: Convert text dates into datetime columns"),
            code_cell(
                """
                work = tickets.copy()

                work["created_at"] = pd.to_datetime(work["created_at"])
                work["first_response_at"] = pd.to_datetime(work["first_response_at"])

                work.info()
                """
            ),
            markdown_cell("## Step 2: Calculate response time in hours"),
            code_cell(
                """
                work["response_hours"] = (
                    work["first_response_at"] - work["created_at"]
                ).dt.total_seconds() / 3600

                work
                """
            ),
            markdown_cell("## Step 3: Summarize response time by priority"),
            code_cell(
                """
                priority_summary = (
                    work
                    .groupby("priority", as_index=False)
                    .agg(
                        ticket_count=("ticket_id", "count"),
                        open_tickets=("status", lambda status: (status == "Open").sum()),
                        average_response_hours=("response_hours", "mean"),
                    )
                    .sort_values("average_response_hours")
                )

                priority_summary
                """
            ),
            markdown_cell("## Step 4: Create a backlog pivot table"),
            code_cell(
                """
                backlog = pd.pivot_table(
                    work,
                    index="priority",
                    columns="status",
                    values="ticket_id",
                    aggfunc="count",
                    fill_value=0,
                )

                backlog
                """
            ),
            markdown_cell("## Step 5: Identify high-priority open tickets"),
            code_cell(
                """
                high_priority_open = work.loc[
                    (work["priority"] == "High") & (work["status"] == "Open")
                ]

                high_priority_open
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Priority with slowest average response:
                - Number of open high-priority tickets:
                - Biggest operational risk:
                - One staffing or process recommendation:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `row_count` and `seed` to simulate different ticket queues. Set
                `seed=None` for a randomized dataset each run. Try making more rows and
                compare whether the backlog risk changes.
                """
            ),
            code_cell(
                """
                my_tickets = make_ticket_data(row_count=80, seed=99)
                my_tickets.head()
                """
            ),
        ]
    ),
    "05_time_series_feature_builder.ipynb": notebook(
        [
            markdown_cell(
                """
                # Time Series Feature Builder

                **Level:** Advanced

                ## Project description

                You are preparing daily sales data for forecasting. The model team needs
                complete daily records, lag features, and rolling averages.

                ## Skills practiced

                - Date parsing
                - Resampling
                - Filling missing dates
                - Lag and rolling-window features
                """
            ),
            code_cell(
                """
                import pandas as pd
                import numpy as np
                import secrets

                practice_run_name = f"time-series-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_daily_sales_data(day_count=45, missing_days=6, seed=42):
                    \"\"\"Create synthetic daily revenue with trend, weekly seasonality, and missing dates.\"\"\"
                    rng = np.random.default_rng(seed)
                    dates = pd.date_range("2026-05-01", periods=day_count, freq="D")
                    day_number = np.arange(day_count)
                    weekly_pattern = np.where(dates.dayofweek >= 5, 180, 0)
                    revenue = 1100 + (day_number * 18) + weekly_pattern + rng.normal(0, 120, size=day_count)

                    sales = pd.DataFrame({
                        "date": dates,
                        "revenue": revenue.round(0).astype(int),
                    })
                    drop_count = min(missing_days, max(day_count - 1, 0))
                    missing_index = rng.choice(sales.index, size=drop_count, replace=False)
                    return sales.drop(index=missing_index).sort_values("date").reset_index(drop=True)

                sales = make_daily_sales_data(day_count=45, missing_days=6, seed=42)
                sales
                """
            ),
            markdown_cell(
                """
                ## Step 1: Set a daily date index

                Forecasting data usually needs one row per time period. Missing dates can
                confuse models and charts, so we create a complete daily index.
                """
            ),
            code_cell(
                """
                daily = (
                    sales
                    .set_index("date")
                    .asfreq("D")
                )

                daily
                """
            ),
            markdown_cell(
                """
                ## Step 2: Fill missing revenue values

                For this training example, missing dates mean no recorded sales, so we fill
                missing revenue with 0. In real work, always confirm this assumption.
                """
            ),
            code_cell(
                """
                daily["revenue"] = daily["revenue"].fillna(0)
                daily
                """
            ),
            markdown_cell("## Step 3: Create lag features"),
            code_cell(
                """
                daily["revenue_lag_1"] = daily["revenue"].shift(1)
                daily["revenue_lag_7"] = daily["revenue"].shift(7)

                daily
                """
            ),
            markdown_cell("## Step 4: Create rolling averages"),
            code_cell(
                """
                daily["rolling_3_day_revenue"] = daily["revenue"].rolling(window=3).mean()
                daily["rolling_7_day_revenue"] = daily["revenue"].rolling(window=7).mean()

                daily
                """
            ),
            markdown_cell("## Step 5: Export the modeling table"),
            code_cell(
                """
                modeling_table = daily.reset_index()
                modeling_table
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Dates that were missing from the original data:
                - Why filling missing revenue with 0 may or may not be correct:
                - Most useful forecasting feature:
                - One validation check you would add:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `day_count`, `missing_days`, and `seed` to create a new forecasting
                practice dataset. Set `seed=None` for a randomized dataset each run. More
                missing days will make the resampling step easier to see.
                """
            ),
            code_cell(
                """
                my_sales = make_daily_sales_data(day_count=90, missing_days=14, seed=5)
                my_sales.head()
                """
            ),
        ]
    ),
    "06_reusable_cleaning_pipeline.ipynb": notebook(
        [
            markdown_cell(
                """
                # Reusable Cleaning Pipeline

                **Level:** Advanced

                ## Project description

                You receive messy CSV exports every week. Instead of manually cleaning each
                file, build reusable Pandas functions that normalize columns, clean labels,
                validate required fields, and calculate revenue.

                ## Skills practiced

                - Writing reusable cleaning functions
                - Using pipe()
                - Validating data quality
                - Keeping transformations readable
                """
            ),
            code_cell(
                """
                import pandas as pd
                import numpy as np
                import secrets

                practice_run_name = f"cleaning-pipeline-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_messy_sales_export(row_count=20, seed=42):
                    \"\"\"Create a synthetic messy CSV-style export for cleaning practice.\"\"\"
                    rng = np.random.default_rng(seed)
                    raw = pd.DataFrame({
                        " Order ID ": range(1, row_count + 1),
                        "Region ": rng.choice([" west", "EAST", "South ", "north", "WEST "], size=row_count),
                        "Units Sold": rng.integers(1, 12, size=row_count).astype(float),
                        "Unit Price": rng.choice([45, 80, 120, 150, 220], size=row_count),
                    })
                    raw.loc[rng.choice(raw.index, size=max(1, row_count // 8), replace=False), "Units Sold"] = np.nan
                    return raw

                raw = make_messy_sales_export(row_count=20, seed=42)
                raw
                """
            ),
            markdown_cell("## Step 1: Create a function to normalize column names"),
            code_cell(
                """
                def normalize_columns(data: pd.DataFrame) -> pd.DataFrame:
                    \"\"\"Return a copy with clean snake_case column names.\"\"\"
                    cleaned = data.copy()
                    cleaned.columns = (
                        cleaned.columns
                        .str.strip()
                        .str.lower()
                        .str.replace(" ", "_")
                    )
                    return cleaned
                """
            ),
            markdown_cell("## Step 2: Create a function to clean text labels"),
            code_cell(
                """
                def clean_region_labels(data: pd.DataFrame) -> pd.DataFrame:
                    \"\"\"Return a copy with consistent region labels.\"\"\"
                    cleaned = data.copy()
                    cleaned["region"] = cleaned["region"].str.strip().str.title()
                    return cleaned
                """
            ),
            markdown_cell("## Step 3: Create a validation function"),
            code_cell(
                """
                def validate_required_columns(data: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
                    \"\"\"Raise a clear error when required columns are missing.\"\"\"
                    missing_columns = set(required_columns) - set(data.columns)
                    if missing_columns:
                        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
                    return data
                """
            ),
            markdown_cell("## Step 4: Create a function for business metrics"),
            code_cell(
                """
                def add_revenue(data: pd.DataFrame) -> pd.DataFrame:
                    \"\"\"Return a copy with revenue calculated from units and price.\"\"\"
                    cleaned = data.copy()
                    cleaned["units_sold"] = cleaned["units_sold"].fillna(0)
                    cleaned["revenue"] = cleaned["units_sold"] * cleaned["unit_price"]
                    return cleaned
                """
            ),
            markdown_cell("## Step 5: Combine the functions with pipe()"),
            code_cell(
                """
                required = ["order_id", "region", "units_sold", "unit_price"]

                clean = (
                    raw
                    .pipe(normalize_columns)
                    .pipe(validate_required_columns, required_columns=required)
                    .pipe(clean_region_labels)
                    .pipe(add_revenue)
                )

                clean
                """
            ),
            markdown_cell("## Step 6: Create a validation report"),
            code_cell(
                """
                validation_report = pd.DataFrame({
                    "check": [
                        "row_count",
                        "missing_units_sold_after_cleaning",
                        "missing_region_after_cleaning",
                        "total_revenue",
                    ],
                    "value": [
                        len(clean),
                        clean["units_sold"].isna().sum(),
                        clean["region"].isna().sum(),
                        clean["revenue"].sum(),
                    ],
                })

                validation_report
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Which function is most reusable:
                - Which validation check protects the analysis most:
                - One additional function you would add:
                - One reason pipe() improves readability:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `row_count` and `seed` to create a new messy export. Set `seed=None`
                for a randomized dataset each run. You can also add more messy region labels
                inside the function to test your cleaning pipeline.
                """
            ),
            code_cell(
                """
                my_raw = make_messy_sales_export(row_count=50, seed=12)
                my_raw.head()
                """
            ),
        ]
    ),
}


NUMPY_PROJECTS = {
    "07_numpy_student_score_simulator.ipynb": notebook(
        [
            markdown_cell(
                """
                # NumPy Student Score Simulator

                **Level:** Beginner

                ## Project description

                Generate synthetic exam scores, curve them, and summarize pass rates.
                This notebook teaches students how to create their own numeric practice
                datasets with NumPy.

                ## Skills practiced

                - Creating arrays with `np.random.default_rng`
                - Inspecting shape and dtype
                - Vectorized math
                - Boolean masks
                - Summary statistics
                """
            ),
            markdown_cell("## Step 1: Generate synthetic score data"),
            code_cell(
                """
                import numpy as np
                import pandas as pd
                import secrets

                practice_run_name = f"numpy-scores-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_score_data(student_count=40, seed=42):
                    \"\"\"Create synthetic exam scores for practice.\"\"\"
                    rng = np.random.default_rng(seed)
                    scores = rng.normal(loc=76, scale=12, size=student_count)
                    return np.clip(scores, 0, 100).round(1)

                scores = make_score_data(student_count=40, seed=42)
                scores[:10]
                """
            ),
            code_cell(
                """
                scores.shape, scores.dtype, scores.mean().round(1)
                """
            ),
            markdown_cell("## Step 2: Curve scores with vectorized math"),
            code_cell(
                """
                curved_scores = np.minimum(scores + 5, 100)
                curved_scores[:10]
                """
            ),
            markdown_cell("## Step 3: Calculate pass-rate metrics"),
            code_cell(
                """
                passing_mask = curved_scores >= 70

                pass_rate = passing_mask.mean()
                average_score = curved_scores.mean()
                highest_score = curved_scores.max()
                lowest_score = curved_scores.min()

                pd.DataFrame({
                    "metric": ["Pass rate", "Average score", "Highest score", "Lowest score"],
                    "value": [pass_rate, average_score, highest_score, lowest_score],
                })
                """
            ),
            markdown_cell("## Step 4: Find students who need support"),
            code_cell(
                """
                needs_support = curved_scores[curved_scores < 70]
                needs_support
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Average score after curve:
                - Pass rate:
                - Number of students below 70:
                - One teaching action you recommend:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `student_count` and `seed`. Use `seed=None` when you want a fresh
                randomized dataset each run.
                """
            ),
            code_cell(
                """
                my_scores = make_score_data(student_count=100, seed=None)
                my_scores[:10]
                """
            ),
        ]
    ),
    "08_numpy_weather_array_explorer.ipynb": notebook(
        [
            markdown_cell(
                """
                # NumPy Weather Array Explorer

                **Level:** Beginner

                ## Project description

                Simulate daily temperatures and find unusually hot or cold days.

                ## Skills practiced

                - Generating synthetic arrays
                - Boolean masks
                - Min, max, mean, and standard deviation
                - Counting conditions
                """
            ),
            code_cell(
                """
                import numpy as np
                import pandas as pd
                import secrets

                practice_run_name = f"numpy-weather-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_temperature_data(day_count=30, seed=42):
                    \"\"\"Create synthetic daily temperatures.\"\"\"
                    rng = np.random.default_rng(seed)
                    baseline = rng.normal(loc=72, scale=9, size=day_count)
                    trend = np.linspace(-2, 4, day_count)
                    return (baseline + trend).round(1)

                temperatures = make_temperature_data(day_count=30, seed=42)
                temperatures
                """
            ),
            markdown_cell("## Step 1: Summarize the array"),
            code_cell(
                """
                summary = pd.DataFrame({
                    "metric": ["Days", "Average", "Minimum", "Maximum", "Standard deviation"],
                    "value": [
                        temperatures.size,
                        temperatures.mean().round(1),
                        temperatures.min(),
                        temperatures.max(),
                        temperatures.std().round(1),
                    ],
                })

                summary
                """
            ),
            markdown_cell("## Step 2: Build boolean masks"),
            code_cell(
                """
                hot_days = temperatures >= 85
                cold_days = temperatures <= 55

                hot_days.sum(), cold_days.sum()
                """
            ),
            code_cell(
                """
                temperatures[hot_days]
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Average temperature:
                - Number of hot days:
                - Number of cold days:
                - One weather pattern you noticed:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `day_count` and `seed`. Try 365 days to simulate a full year.
                """
            ),
            code_cell(
                """
                my_temperatures = make_temperature_data(day_count=365, seed=None)
                my_temperatures[:10]
                """
            ),
        ]
    ),
    "09_numpy_sales_matrix_analyzer.ipynb": notebook(
        [
            markdown_cell(
                """
                # NumPy Sales Matrix Analyzer

                **Level:** Intermediate

                ## Project description

                Generate a store-by-product sales matrix and summarize by row and column.

                ## Skills practiced

                - Working with 2D arrays
                - Axis-based aggregation
                - Shape reasoning
                - Converting summaries to readable tables
                """
            ),
            code_cell(
                """
                import numpy as np
                import pandas as pd
                import secrets

                practice_run_name = f"numpy-sales-matrix-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_sales_matrix(store_count=6, product_count=4, seed=42):
                    \"\"\"Create a synthetic store-by-product units-sold matrix.\"\"\"
                    rng = np.random.default_rng(seed)
                    return rng.integers(20, 160, size=(store_count, product_count))

                sales_matrix = make_sales_matrix(store_count=6, product_count=4, seed=42)
                sales_matrix
                """
            ),
            markdown_cell("## Step 1: Inspect shape and totals"),
            code_cell(
                """
                sales_matrix.shape, sales_matrix.sum()
                """
            ),
            markdown_cell("## Step 2: Summarize stores and products"),
            code_cell(
                """
                store_totals = sales_matrix.sum(axis=1)
                product_totals = sales_matrix.sum(axis=0)

                store_totals, product_totals
                """
            ),
            code_cell(
                """
                product_summary = pd.DataFrame({
                    "product": [f"Product {i}" for i in range(1, sales_matrix.shape[1] + 1)],
                    "units_sold": product_totals,
                    "average_per_store": sales_matrix.mean(axis=0).round(1),
                })

                product_summary
                """
            ),
            markdown_cell("## Step 3: Find top performers"),
            code_cell(
                """
                top_store_index = store_totals.argmax()
                top_product_index = product_totals.argmax()

                top_store_index, top_product_index
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Top store index:
                - Top product index:
                - Total units sold:
                - One recommendation:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change `store_count`, `product_count`, and `seed`. Use `seed=None` for a
                fresh randomized matrix.
                """
            ),
            code_cell(
                """
                my_sales_matrix = make_sales_matrix(store_count=10, product_count=8, seed=None)
                my_sales_matrix.shape
                """
            ),
        ]
    ),
    "10_numpy_broadcasting_practice_lab.ipynb": notebook(
        [
            markdown_cell(
                """
                # NumPy Broadcasting Practice Lab

                **Level:** Intermediate

                ## Project description

                Apply product prices and discounts across a sales matrix using broadcasting.

                ## Skills practiced

                - Broadcasting row and column vectors
                - Revenue calculations
                - Shape validation
                - Clipping and rounding
                """
            ),
            code_cell(
                """
                import numpy as np
                import pandas as pd
                import secrets

                practice_run_name = f"numpy-broadcasting-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def make_broadcasting_data(store_count=5, product_count=4, seed=42):
                    \"\"\"Create synthetic units, prices, and store discounts.\"\"\"
                    rng = np.random.default_rng(seed)
                    units = rng.integers(10, 100, size=(store_count, product_count))
                    prices = rng.choice([15, 25, 40, 60, 90], size=product_count)
                    discounts = rng.uniform(0, 0.15, size=store_count).round(2)
                    return units, prices, discounts

                units, prices, discounts = make_broadcasting_data(seed=42)
                units, prices, discounts
                """
            ),
            markdown_cell("## Step 1: Validate shapes"),
            code_cell(
                """
                units.shape, prices.shape, discounts.shape
                """
            ),
            markdown_cell("## Step 2: Broadcast prices across product columns"),
            code_cell(
                """
                gross_revenue = units * prices
                gross_revenue
                """
            ),
            markdown_cell("## Step 3: Broadcast store discounts down rows"),
            code_cell(
                """
                net_revenue = gross_revenue * (1 - discounts[:, np.newaxis])
                net_revenue = net_revenue.round(2)
                net_revenue
                """
            ),
            code_cell(
                """
                pd.DataFrame({
                    "store": [f"Store {i}" for i in range(1, units.shape[0] + 1)],
                    "gross_revenue": gross_revenue.sum(axis=1).round(2),
                    "net_revenue": net_revenue.sum(axis=1).round(2),
                    "discount": discounts,
                })
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Shape of units:
                - Shape of prices:
                - Why `discounts[:, np.newaxis]` was needed:
                - Top store by net revenue:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own dataset

                Change store and product counts. Predict the shapes before running the revenue cells.
                """
            ),
            code_cell(
                """
                my_units, my_prices, my_discounts = make_broadcasting_data(
                    store_count=8,
                    product_count=6,
                    seed=None,
                )
                my_units.shape, my_prices.shape, my_discounts.shape
                """
            ),
        ]
    ),
    "11_numpy_monte_carlo_budget_risk.ipynb": notebook(
        [
            markdown_cell(
                """
                # NumPy Monte Carlo Budget Risk

                **Level:** Advanced

                ## Project description

                Simulate thousands of monthly costs and estimate the chance of going over budget.

                ## Skills practiced

                - Monte Carlo simulation
                - Random sampling
                - Vectorized totals
                - Risk estimation
                - Percentiles
                """
            ),
            code_cell(
                """
                import numpy as np
                import pandas as pd
                import secrets

                practice_run_name = f"numpy-budget-risk-{secrets.token_hex(3)}"
                print(f"Practice run: {practice_run_name}")

                def simulate_monthly_costs(simulation_count=5000, seed=42):
                    \"\"\"Create synthetic monthly cost simulations.\"\"\"
                    rng = np.random.default_rng(seed)
                    rent = rng.normal(loc=1400, scale=40, size=simulation_count)
                    food = rng.normal(loc=520, scale=120, size=simulation_count)
                    transport = rng.normal(loc=180, scale=60, size=simulation_count)
                    health = rng.lognormal(mean=4.8, sigma=0.5, size=simulation_count)
                    entertainment = rng.normal(loc=220, scale=80, size=simulation_count)
                    costs = np.column_stack([rent, food, transport, health, entertainment])
                    return np.clip(costs, 0, None).round(2)

                costs = simulate_monthly_costs(simulation_count=5000, seed=42)
                costs[:5]
                """
            ),
            markdown_cell("## Step 1: Calculate total monthly costs"),
            code_cell(
                """
                total_costs = costs.sum(axis=1)
                total_costs[:10]
                """
            ),
            markdown_cell("## Step 2: Estimate budget risk"),
            code_cell(
                """
                budget = 2600
                over_budget = total_costs > budget
                risk = over_budget.mean()

                risk
                """
            ),
            markdown_cell("## Step 3: Summarize scenarios"),
            code_cell(
                """
                scenario_summary = pd.DataFrame({
                    "metric": ["Average total", "Median total", "90th percentile", "Over-budget risk"],
                    "value": [
                        total_costs.mean().round(2),
                        np.median(total_costs).round(2),
                        np.percentile(total_costs, 90).round(2),
                        risk.round(3),
                    ],
                })

                scenario_summary
                """
            ),
            markdown_cell("## Step 4: Find category averages"),
            code_cell(
                """
                categories = ["rent", "food", "transport", "health", "entertainment"]
                category_summary = pd.DataFrame({
                    "category": categories,
                    "average_cost": costs.mean(axis=0).round(2),
                    "p90_cost": np.percentile(costs, 90, axis=0).round(2),
                })

                category_summary
                """
            ),
            markdown_cell(
                """
                ## Final project notes

                - Budget used:
                - Estimated over-budget risk:
                - Highest average cost category:
                - One recommendation:
                """
            ),
            markdown_cell(
                """
                ## Practice extension: Generate your own simulation

                Change `simulation_count`, `seed`, and `budget`. Use `seed=None` for a new
                randomized simulation each run.
                """
            ),
            code_cell(
                """
                my_costs = simulate_monthly_costs(simulation_count=10000, seed=None)
                my_total_costs = my_costs.sum(axis=1)
                (my_total_costs > 2800).mean()
                """
            ),
        ]
    ),
}


def write_index() -> None:
    """Write a README file that lists the generated notebooks."""
    lines = [
        "# Python Data Project Notebooks",
        "",
        "These notebooks turn the app's project ideas into guided Pandas and NumPy projects with synthetic practice datasets.",
        "",
        "## Pandas notebooks",
        "",
    ]

    for index, filename in enumerate(PROJECTS, start=1):
        title = filename.removesuffix(".ipynb").replace("_", " ").title()
        lines.append(f"{index}. [{title}]({filename})")

    lines.extend(["", "## NumPy notebooks", ""])

    for index, filename in enumerate(NUMPY_PROJECTS, start=1):
        title = filename.removesuffix(".ipynb").replace("_", " ").title()
        lines.append(f"{index}. [{title}]({filename})")

    lines.extend(
        [
            "",
            "## How to open",
            "",
            "Use Jupyter Notebook, JupyterLab, VS Code, or any editor that supports `.ipynb` files.",
            "",
            "Each notebook includes synthetic starter data, guided steps, commented code, practice prompts for changing the data, and final reflection prompts.",
        ]
    )

    (NOTEBOOK_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Generate all project notebooks."""
    NOTEBOOK_DIR.mkdir(exist_ok=True)

    for filename, content in (PROJECTS | NUMPY_PROJECTS).items():
        path = NOTEBOOK_DIR / filename
        path.write_text(json.dumps(content, indent=2), encoding="utf-8")

    write_index()
    print(f"Created {len(PROJECTS) + len(NUMPY_PROJECTS)} notebooks in {NOTEBOOK_DIR}")


if __name__ == "__main__":
    main()
