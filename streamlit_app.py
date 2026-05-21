"""
Python Data Pathways
--------------------

This Streamlit app teaches data Python libraries from beginner to advanced
level. It is meant to be more than a syntax demo: it explains concepts, shows
examples, gives practice tasks, and points learners toward project work.

Why Streamlit?
Streamlit lets us build an interactive Python app with very little web-code.
That means the learning app can use real Pandas DataFrames, real filters,
real groupby operations, and real charts instead of JavaScript simulations.

Run this app with:

    python -m streamlit run streamlit_app.py
"""

from __future__ import annotations

import os
from urllib.parse import quote

import numpy as np
import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
# Streamlit reads this once when the app starts. The wide layout gives tables,
# charts, and code examples enough horizontal room.
st.set_page_config(
    page_title="Python Data Pathways",
    page_icon="P",
    layout="wide",
)


# Colab can open notebooks directly from GitHub. After this project is pushed
# to GitHub, set these before running the app:
#   $env:GITHUB_REPO_SLUG="your-github-user-or-org/your-repo"
#   $env:GITHUB_BRANCH="main"
#   $env:GITHUB_PROJECT_PATH="pandas-learning-app"
GITHUB_REPO_SLUG = os.getenv("GITHUB_REPO_SLUG", "").strip()
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main").strip()
GITHUB_PROJECT_PATH = os.getenv("GITHUB_PROJECT_PATH", "pandas-learning-app").strip("/")


def build_colab_url(notebook_path: str) -> str | None:
    """Build a Colab link for a notebook stored in GitHub."""
    if not GITHUB_REPO_SLUG:
        return None

    path_parts = [part for part in [GITHUB_PROJECT_PATH, notebook_path] if part]
    github_path = "/".join(path_parts).replace("\\", "/")
    encoded_path = quote(github_path)
    return (
        "https://colab.research.google.com/github/"
        f"{GITHUB_REPO_SLUG}/blob/{GITHUB_BRANCH}/{encoded_path}"
    )


def apply_app_styles() -> None:
    """Add lightweight visual styling for the Streamlit interface."""
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 1.5rem;
            max-width: 1180px;
        }

        .pathway-hero {
            background:
                radial-gradient(circle at 12% 15%, rgba(255, 184, 77, 0.28), transparent 34%),
                radial-gradient(circle at 92% 12%, rgba(20, 184, 166, 0.22), transparent 30%),
                linear-gradient(135deg, #102033 0%, #17324d 48%, #0f766e 100%);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 18px;
            color: #ffffff;
            padding: 2rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 18px 45px rgba(16, 32, 51, 0.20);
        }

        .pathway-kicker {
            color: #fbbf24;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0;
            margin-bottom: 0.45rem;
            text-transform: uppercase;
        }

        .pathway-hero h1 {
            color: #ffffff;
            font-size: clamp(2.1rem, 4vw, 4.4rem);
            line-height: 1.02;
            margin: 0;
            letter-spacing: 0;
        }

        .pathway-hero p {
            color: #d7f7ef;
            font-size: 1.05rem;
            line-height: 1.55;
            margin: 1rem 0 0;
            max-width: 760px;
        }

        .track-pill {
            align-items: center;
            background: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 999px;
            color: #ffffff;
            display: inline-flex;
            font-size: 0.92rem;
            font-weight: 700;
            gap: 0.45rem;
            margin-top: 1.25rem;
            padding: 0.55rem 0.85rem;
        }

        .track-card-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            margin-bottom: 1.15rem;
        }

        .track-card {
            border-radius: 16px;
            padding: 1.15rem;
            border: 1px solid #d9e4ea;
            background: #ffffff;
            box-shadow: 0 10px 28px rgba(17, 24, 39, 0.08);
        }

        .track-card.active {
            border-color: #14b8a6;
            box-shadow: 0 14px 34px rgba(20, 184, 166, 0.18);
        }

        .track-card.pandas {
            border-top: 6px solid #ef5d50;
        }

        .track-card.numpy {
            border-top: 6px solid #14b8a6;
        }

        .track-card h3 {
            color: #102033;
            font-size: 1.15rem;
            margin: 0 0 0.35rem;
            letter-spacing: 0;
        }

        .track-card p {
            color: #44556a;
            font-size: 0.94rem;
            line-height: 1.45;
            margin: 0;
        }

        .stat-grid {
            display: grid;
            gap: 0.8rem;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin-bottom: 1.4rem;
        }

        .stat-tile {
            background: #ffffff;
            border: 1px solid #d9e4ea;
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 8px 22px rgba(17, 24, 39, 0.06);
        }

        .stat-value {
            color: #0f766e;
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1;
        }

        .stat-label {
            color: #526174;
            font-size: 0.82rem;
            font-weight: 700;
            margin-top: 0.45rem;
        }

        section[data-testid="stSidebar"] {
            background: #f6f9fb;
            border-right: 1px solid #dbe7ee;
        }

        .sidebar-guide {
            background: #ffffff;
            border: 1px solid #dbe7ee;
            border-radius: 12px;
            color: #334155;
            margin-top: 1rem;
            padding: 0.85rem 0.9rem;
        }

        .sidebar-guide-title {
            color: #102033;
            font-size: 0.9rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }

        .sidebar-guide ol {
            margin: 0;
            padding-left: 1.15rem;
        }

        .sidebar-guide li {
            font-size: 0.86rem;
            line-height: 1.55;
            margin: 0;
        }

        div[data-testid="stRadio"] label {
            font-weight: 650;
        }

        @media (max-width: 760px) {
            .pathway-hero {
                border-radius: 14px;
                padding: 1.25rem;
            }

            .track-card-grid,
            .stat-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Course content
# ---------------------------------------------------------------------------
# The lessons are stored as normal Python dictionaries and lists. This keeps the
# app easy to extend: add a module here and the UI renders it automatically.
LESSONS = {
    "Beginner": {
        "goal": "Understand DataFrames, Series, inspection, selection, and basic cleaning.",
        "explanation": (
            "At this level, focus on building the habit every analyst uses: "
            "load data, inspect it, understand the columns, then make small "
            "safe transformations."
        ),
        "modules": [
            {
                "title": "1. Create and inspect a DataFrame",
                "why": "Before cleaning or analyzing data, you need to know its shape, columns, and data types.",
                "code": """import pandas as pd

df = pd.read_csv("orders.csv")

df.head()      # First 5 rows
df.shape       # Number of rows and columns
df.info()      # Column names, non-null counts, and dtypes
df.describe()  # Summary statistics for numeric columns""",
            },
            {
                "title": "2. Select columns and rows",
                "why": "Most Pandas work starts by selecting the exact rows and columns needed for a question.",
                "code": """# Select one column
df["revenue"]

# Select multiple columns
df[["date", "region", "revenue"]]

# Filter rows with a condition
df.loc[df["region"] == "West"]

# Filter rows and choose columns at the same time
df.loc[df["revenue"] > 500, ["date", "customer", "revenue"]]""",
            },
            {
                "title": "3. Add calculated columns",
                "why": "Calculated columns turn raw fields into useful business metrics.",
                "code": """df["revenue"] = df["units"] * df["price"]

# assign() is useful when you want readable method chains
df = df.assign(
    revenue=lambda data: data["units"] * data["price"],
    high_value=lambda data: data["revenue"] >= 500,
)""",
            },
            {
                "title": "4. Handle missing values",
                "why": "Missing values are not just a technical issue. You need to decide what missing means in context.",
                "code": """df.isna().sum()

# Fill missing discounts with 0 when missing means no discount
df["discount"] = df["discount"].fillna(0)

# Drop rows only when the field is required for analysis
df = df.dropna(subset=["customer_id"])""",
            },
        ],
    },
    "Intermediate": {
        "goal": "Clean messy data, group records, merge tables, and reshape datasets.",
        "explanation": (
            "Intermediate Pandas is where you start answering real questions: "
            "Which category performs best? Which customers are missing? How do "
            "separate tables connect?"
        ),
        "modules": [
            {
                "title": "1. Group and aggregate",
                "why": "Grouping turns row-level data into summary tables.",
                "code": """category_summary = (
    df
    .groupby("category", as_index=False)
    .agg(
        total_revenue=("revenue", "sum"),
        total_units=("units", "sum"),
        average_price=("price", "mean"),
    )
    .sort_values("total_revenue", ascending=False)
)""",
            },
            {
                "title": "2. Merge related tables",
                "why": "Real projects often store customers, orders, products, and regions in separate tables.",
                "code": """orders_with_customers = orders.merge(
    customers,
    on="customer_id",
    how="left",  # Keeps all orders, even if customer details are missing
)""",
            },
            {
                "title": "3. Reshape with melt and pivot_table",
                "why": "Many plotting and modeling tasks need tidy long data, while reports often need wide summary tables.",
                "code": """long_data = df.melt(
    id_vars=["date", "region"],
    value_vars=["revenue", "cost"],
    var_name="metric",
    value_name="amount",
)

report = df.pivot_table(
    index="region",
    columns="category",
    values="revenue",
    aggfunc="sum",
    fill_value=0,
)""",
            },
            {
                "title": "4. Clean text columns",
                "why": "Messy text creates duplicate categories like 'west', 'West ', and 'WEST'.",
                "code": """df["region"] = (
    df["region"]
    .str.strip()
    .str.title()
)

df["email_domain"] = df["email"].str.split("@").str[-1]""",
            },
        ],
    },
    "Advanced": {
        "goal": "Work with time series, windows, performance, validation, and reusable pipelines.",
        "explanation": (
            "Advanced Pandas is about reliability. You are no longer only getting "
            "an answer; you are building analysis that other people can trust and repeat."
        ),
        "modules": [
            {
                "title": "1. Time series analysis",
                "why": "Dates need explicit parsing so Pandas can sort, filter, resample, and compare them correctly.",
                "code": """df["date"] = pd.to_datetime(df["date"])

weekly_revenue = (
    df
    .resample("W", on="date")
    .agg(revenue=("revenue", "sum"))
)""",
            },
            {
                "title": "2. Rolling and lag features",
                "why": "Window calculations help you compare current performance against recent history.",
                "code": """df = df.sort_values("date")

df["previous_revenue"] = df["revenue"].shift(1)
df["rolling_7_day_revenue"] = df["revenue"].rolling(7).mean()""",
            },
            {
                "title": "3. Performance habits",
                "why": "Pandas is fastest when you use vectorized operations instead of Python loops over rows.",
                "code": """# Prefer this vectorized expression
df["profit"] = df["revenue"] - df["cost"]

# Avoid this pattern on large data
for index, row in df.iterrows():
    df.loc[index, "profit"] = row["revenue"] - row["cost"]""",
            },
            {
                "title": "4. Reusable pipelines",
                "why": "Small functions make analysis easier to test, review, and reuse.",
                "code": """def normalize_columns(data):
    data = data.copy()
    data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
    return data

def add_revenue(data):
    return data.assign(revenue=data["units"] * data["price"])

clean = (
    raw
    .pipe(normalize_columns)
    .pipe(add_revenue)
)""",
            },
        ],
    },
}


MASTERY_MAP = [
    {
        "Stage": "1. DataFrame mental model",
        "What to master": "Rows, columns, index, Series, DataFrame, dtypes",
        "You can move on when": "You can explain what df['col'], df.loc[], and df.iloc[] return.",
    },
    {
        "Stage": "2. Inspection",
        "What to master": "head, tail, sample, shape, info, describe, value_counts",
        "You can move on when": "You inspect data before transforming it and can spot missing values and wrong dtypes.",
    },
    {
        "Stage": "3. Selection and filtering",
        "What to master": "Column selection, boolean masks, loc, iloc, query",
        "You can move on when": "You can answer row-level questions without guessing syntax.",
    },
    {
        "Stage": "4. Cleaning",
        "What to master": "Missing values, duplicates, strings, dates, categories",
        "You can move on when": "You can explain why you filled, dropped, converted, or preserved a value.",
    },
    {
        "Stage": "5. Transformation",
        "What to master": "assign, where, mask, map, replace, astype, cut, qcut",
        "You can move on when": "You can create analysis-ready columns without row loops.",
    },
    {
        "Stage": "6. Aggregation",
        "What to master": "groupby, agg, transform, pivot_table, crosstab",
        "You can move on when": "You can turn transaction rows into business summaries.",
    },
    {
        "Stage": "7. Combining data",
        "What to master": "merge, concat, join, relationship checks",
        "You can move on when": "You can choose the correct join type and validate row counts.",
    },
    {
        "Stage": "8. Time series",
        "What to master": "to_datetime, dt accessor, resample, rolling, shift",
        "You can move on when": "You can build weekly summaries, lag features, and rolling metrics.",
    },
    {
        "Stage": "9. Reliability",
        "What to master": "method chains, pipe, validation checks, reproducible notebooks",
        "You can move on when": "Your analysis can be rerun from raw data without manual cleanup.",
    },
    {
        "Stage": "10. Performance",
        "What to master": "Vectorization, categorical dtype, memory usage, profiling",
        "You can move on when": "You know when Pandas is enough and when to change tools or file formats.",
    },
]


CONCEPT_LIBRARY = {
    "DataFrame and Series": {
        "meaning": (
            "A DataFrame is a two-dimensional table. A Series is one labeled column "
            "or one labeled row. Most Pandas operations either return a Series, a "
            "DataFrame, or a scalar value."
        ),
        "example": """type(df)              # pandas.DataFrame
type(df["revenue"])  # pandas.Series
df[["revenue"]]      # DataFrame with one column""",
        "mastery_check": "Explain why df['revenue'] and df[['revenue']] are different.",
    },
    "Index": {
        "meaning": (
            "The index labels rows. It can be a default integer index, dates, IDs, "
            "or hierarchical labels. It affects alignment, joins, resampling, and selection."
        ),
        "example": """df = df.set_index("order_id")
df.loc[101]      # Select row with index label 101
df.reset_index() # Move index back into a normal column""",
        "mastery_check": "Know when an ID should remain a column versus become an index.",
    },
    "Dtypes": {
        "meaning": (
            "Dtypes are column data types. Correct dtypes make calculations, date operations, "
            "sorting, and memory usage reliable."
        ),
        "example": """df["date"] = pd.to_datetime(df["date"])
df["region"] = df["region"].astype("category")
df["price"] = pd.to_numeric(df["price"], errors="coerce")""",
        "mastery_check": "Inspect dtypes before analysis and convert object columns intentionally.",
    },
    "Boolean Masks": {
        "meaning": (
            "A boolean mask is a True/False Series used to keep rows that match a condition. "
            "Masks are the foundation of filtering."
        ),
        "example": """high_value = df["revenue"] >= 500
west_orders = df["region"].eq("West")

df.loc[high_value & west_orders]""",
        "mastery_check": "Use &, |, and ~ with parentheses around each condition.",
    },
    "GroupBy": {
        "meaning": (
            "GroupBy splits rows into groups, applies calculations to each group, and combines "
            "the results into a summary."
        ),
        "example": """summary = (
    df.groupby("category", as_index=False)
    .agg(
        orders=("order_id", "count"),
        revenue=("revenue", "sum"),
        avg_revenue=("revenue", "mean"),
    )
)""",
        "mastery_check": "Use named aggregations so the output columns are clear.",
    },
    "Merge": {
        "meaning": (
            "merge combines tables using key columns. The join type controls which rows survive. "
            "Always check row counts and unmatched records."
        ),
        "example": """merged = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
    indicator=True,
)""",
        "mastery_check": "Know when to use left, inner, outer, and many_to_one validation.",
    },
    "Reshaping": {
        "meaning": (
            "Reshaping changes the layout of a dataset. melt usually makes data longer and tidier. "
            "pivot_table usually makes data wider for reports."
        ),
        "example": """long = df.melt(
    id_vars=["date", "region"],
    value_vars=["revenue", "cost"],
    var_name="metric",
    value_name="amount",
)

wide = df.pivot_table(
    index="region",
    columns="category",
    values="revenue",
    aggfunc="sum",
    fill_value=0,
)""",
        "mastery_check": "Use long data for analysis and plotting; use wide data for comparison reports.",
    },
    "Method Chaining": {
        "meaning": (
            "Method chaining keeps transformations readable from top to bottom. It reduces temporary "
            "variables and makes analysis easier to audit."
        ),
        "example": """clean = (
    raw
    .rename(columns=str.lower)
    .assign(revenue=lambda d: d["units"] * d["price"])
    .query("revenue > 0")
    .sort_values("revenue", ascending=False)
)""",
        "mastery_check": "Use one transformation per line and name complex functions with pipe().",
    },
}


CHEAT_SHEETS = {
    "Inspect": [
        ("First rows", "df.head()"),
        ("Random rows", "df.sample(5, random_state=42)"),
        ("Shape", "df.shape"),
        ("Column summary", "df.info()"),
        ("Numeric summary", "df.describe()"),
        ("Missing values", "df.isna().sum()"),
        ("Unique values", "df['region'].value_counts(dropna=False)"),
    ],
    "Select": [
        ("One column as Series", "df['revenue']"),
        ("One column as DataFrame", "df[['revenue']]"),
        ("Multiple columns", "df[['date', 'region', 'revenue']]"),
        ("Rows by label", "df.loc[10:20, ['region', 'revenue']]"),
        ("Rows by position", "df.iloc[:10, :3]"),
        ("Filter rows", "df.loc[df['revenue'] >= 500]"),
    ],
    "Clean": [
        ("Fill missing", "df['discount'] = df['discount'].fillna(0)"),
        ("Drop missing required values", "df.dropna(subset=['customer_id'])"),
        ("Remove duplicates", "df.drop_duplicates(subset=['order_id'])"),
        ("Clean text", "df['city'].str.strip().str.title()"),
        ("Convert dates", "pd.to_datetime(df['date'], errors='coerce')"),
        ("Convert numbers", "pd.to_numeric(df['price'], errors='coerce')"),
    ],
    "Transform": [
        ("New column", "df.assign(revenue=lambda d: d.units * d.price)"),
        ("Conditional column", "df['tier'] = df['revenue'].where(df['revenue'] < 1000, 'High')"),
        ("Map labels", "df['region_name'] = df['region'].map(region_lookup)"),
        ("Bin values", "pd.cut(df['age'], bins=[0, 18, 35, 65, 120])"),
        ("Sort", "df.sort_values(['region', 'revenue'], ascending=[True, False])"),
    ],
    "Summarize": [
        ("Group count", "df.groupby('category').size()"),
        ("Named aggregation", "df.groupby('category').agg(revenue=('revenue', 'sum'))"),
        ("Group transform", "df['category_avg'] = df.groupby('category')['revenue'].transform('mean')"),
        ("Pivot table", "df.pivot_table(index='region', columns='category', values='revenue', aggfunc='sum')"),
        ("Cross tab", "pd.crosstab(df['region'], df['category'])"),
    ],
    "Combine": [
        ("Left merge", "orders.merge(customers, on='customer_id', how='left')"),
        ("Validated merge", "orders.merge(customers, on='customer_id', how='left', validate='many_to_one')"),
        ("Stack rows", "pd.concat([jan, feb], ignore_index=True)"),
        ("Track merge matches", "orders.merge(customers, on='customer_id', how='left', indicator=True)"),
    ],
    "Time Series": [
        ("Parse dates", "df['date'] = pd.to_datetime(df['date'])"),
        ("Date parts", "df['month'] = df['date'].dt.to_period('M')"),
        ("Weekly resample", "df.resample('W', on='date')['revenue'].sum()"),
        ("Previous row", "df['prior_revenue'] = df['revenue'].shift(1)"),
        ("Rolling average", "df['ma_7'] = df['revenue'].rolling(7).mean()"),
    ],
}


COMMON_MISTAKES = [
    {
        "mistake": "Using chained assignment",
        "bad": """df[df["region"] == "West"]["revenue"] = 0""",
        "better": """df.loc[df["region"] == "West", "revenue"] = 0""",
        "why": "The first line may modify a temporary copy instead of the original DataFrame.",
    },
    {
        "mistake": "Forgetting parentheses in boolean filters",
        "bad": """df[df["region"] == "West" & df["revenue"] > 500]""",
        "better": """df[(df["region"] == "West") & (df["revenue"] > 500)]""",
        "why": "Each condition must be wrapped before combining with & or |.",
    },
    {
        "mistake": "Assuming object columns are clean text",
        "bad": """df.groupby("region")["revenue"].sum()""",
        "better": """df["region"] = df["region"].str.strip().str.title()
df.groupby("region")["revenue"].sum()""",
        "why": "Extra spaces and inconsistent capitalization create duplicate groups.",
    },
    {
        "mistake": "Merging without validating relationships",
        "bad": """orders.merge(customers, on="customer_id", how="left")""",
        "better": """orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
)""",
        "why": "Validation catches accidental many-to-many joins that inflate row counts.",
    },
    {
        "mistake": "Replacing missing values without thinking",
        "bad": """df = df.fillna(0)""",
        "better": """df["discount"] = df["discount"].fillna(0)
df = df.dropna(subset=["customer_id"])""",
        "why": "Different columns have different meanings. Missing discount may mean zero; missing customer_id may make a row unusable.",
    },
]


PRACTICE_DRILLS = [
    {
        "skill": "Selection",
        "task": "Return only West region orders with revenue above 500 and show date, category, and revenue.",
        "answer": """df.loc[
    (df["region"] == "West") & (df["revenue"] > 500),
    ["date", "category", "revenue"],
]""",
    },
    {
        "skill": "Cleaning",
        "task": "Clean a city column so values like ' chicago ', 'CHICAGO', and 'Chicago' match.",
        "answer": """df["city"] = df["city"].str.strip().str.title()""",
    },
    {
        "skill": "Aggregation",
        "task": "Summarize total revenue and average price by category.",
        "answer": """df.groupby("category", as_index=False).agg(
    total_revenue=("revenue", "sum"),
    average_price=("price", "mean"),
)""",
    },
    {
        "skill": "Merging",
        "task": "Keep all orders while adding customer details. Catch duplicate customer IDs if they exist.",
        "answer": """orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
)""",
    },
    {
        "skill": "Time series",
        "task": "Create weekly revenue totals from an order table with a date column.",
        "answer": """weekly = df.resample("W", on="date")["revenue"].sum()""",
    },
]


QUIZ_QUESTIONS = [
    {
        "question": "Which method shows column names, non-null counts, and dtypes?",
        "choices": ["df.info()", "df.sample()", "df.rename()"],
        "answer": "df.info()",
        "explanation": "Use df.info() early because it quickly reveals missing values and data types.",
    },
    {
        "question": "Which expression creates a revenue column from units and price?",
        "choices": ['df["revenue"] = df["units"] * df["price"]', "df.revenue(units, price)", "df.groupby('revenue')"],
        "answer": 'df["revenue"] = df["units"] * df["price"]',
        "explanation": "Pandas can multiply whole columns at once. This is called vectorized computation.",
    },
    {
        "question": "Which join keeps every order even when customer details are missing?",
        "choices": ["left merge from orders", "inner merge", "right merge from customers"],
        "answer": "left merge from orders",
        "explanation": "A left merge keeps every row from the left DataFrame.",
    },
    {
        "question": "Which operation summarizes revenue by category?",
        "choices": ["groupby + agg", "drop_duplicates", "head only"],
        "answer": "groupby + agg",
        "explanation": "groupby splits records into groups, and agg calculates summary values for each group.",
    },
    {
        "question": "Which function is commonly used to convert wide data into long tidy data?",
        "choices": ["melt", "tail", "fillna"],
        "answer": "melt",
        "explanation": "melt turns several value columns into two columns: variable and value.",
    },
    {
        "question": "Why is validate='many_to_one' useful in merge()?",
        "choices": [
            "It catches unexpected duplicate keys in the right table",
            "It makes the merge faster",
            "It automatically fills missing values",
        ],
        "answer": "It catches unexpected duplicate keys in the right table",
        "explanation": "Validation protects you from joins that silently multiply rows.",
    },
    {
        "question": "Which accessor is used for vectorized string operations?",
        "choices": ["str", "dt", "cat"],
        "answer": "str",
        "explanation": "Use df['column'].str.strip(), str.contains(), str.split(), and similar methods for text.",
    },
    {
        "question": "Which method creates group-level values while preserving the original row count?",
        "choices": ["transform", "head", "concat"],
        "answer": "transform",
        "explanation": "groupby().transform() returns values aligned to the original rows.",
    },
    {
        "question": "What is usually better than iterrows() for column calculations?",
        "choices": ["Vectorized operations", "Manual row loops", "Printing every row"],
        "answer": "Vectorized operations",
        "explanation": "Vectorized operations use Pandas and NumPy internals and are usually clearer and faster.",
    },
]


PROJECTS = [
    {
        "level": "Beginner",
        "title": "Movie Ratings Explorer",
        "description": "Generate synthetic movie ratings data, then identify top genres, popular years, and missing values.",
        "deliverables": ["Cleaned dataset", "Top 10 genre summary", "Short written findings"],
        "notebook": "notebooks/01_movie_ratings_explorer.ipynb",
    },
    {
        "level": "Beginner",
        "title": "Personal Budget Tracker",
        "description": "Generate synthetic transactions, then summarize spending by month and category.",
        "deliverables": ["Monthly summary table", "Category chart", "Unusual expense list"],
        "notebook": "notebooks/02_personal_budget_tracker.ipynb",
    },
    {
        "level": "Intermediate",
        "title": "Retail Sales Analysis",
        "description": "Generate synthetic order and product tables, then calculate revenue and compare regions.",
        "deliverables": ["Merged dataset", "Regional revenue table", "Product category ranking"],
        "notebook": "notebooks/03_retail_sales_analysis.ipynb",
    },
    {
        "level": "Intermediate",
        "title": "Support Ticket Operations",
        "description": "Generate synthetic support tickets, then measure response time, backlog size, and priority risk.",
        "deliverables": ["Cleaned date columns", "Pivot table", "Response-time insights"],
        "notebook": "notebooks/04_support_ticket_operations.ipynb",
    },
    {
        "level": "Advanced",
        "title": "Time Series Feature Builder",
        "description": "Generate synthetic daily sales data, then create lag and rolling-average forecasting features.",
        "deliverables": ["Daily resampled data", "Lag features", "Rolling metrics"],
        "notebook": "notebooks/05_time_series_feature_builder.ipynb",
    },
    {
        "level": "Advanced",
        "title": "Reusable Cleaning Pipeline",
        "description": "Generate a messy synthetic export, then build reusable cleaning functions with pipe().",
        "deliverables": ["Cleaning functions", "Validation report", "Example notebook"],
        "notebook": "notebooks/06_reusable_cleaning_pipeline.ipynb",
    },
]


NUMPY_MASTERY_MAP = [
    {
        "Stage": "1. Array mental model",
        "What to master": "ndarray, shape, dtype, axes, dimensions",
        "You can move on when": "You can explain the difference between a Python list and a NumPy array.",
    },
    {
        "Stage": "2. Creating arrays",
        "What to master": "array, arange, linspace, zeros, ones, random generators",
        "You can move on when": "You can generate practice arrays without needing external files.",
    },
    {
        "Stage": "3. Indexing and slicing",
        "What to master": "positions, slices, rows, columns, boolean masks",
        "You can move on when": "You can select values from 1D and 2D arrays confidently.",
    },
    {
        "Stage": "4. Vectorized math",
        "What to master": "elementwise operations, ufuncs, broadcasting",
        "You can move on when": "You replace manual loops with array expressions.",
    },
    {
        "Stage": "5. Aggregation",
        "What to master": "sum, mean, min, max, std, axis",
        "You can move on when": "You know how axis changes row-wise and column-wise results.",
    },
    {
        "Stage": "6. Reshaping",
        "What to master": "reshape, ravel, transpose, concatenate, stack",
        "You can move on when": "You can change layout without changing the underlying values.",
    },
    {
        "Stage": "7. Simulation",
        "What to master": "default_rng, normal, integers, choice, reproducible seeds",
        "You can move on when": "You can create synthetic numeric datasets for practice.",
    },
    {
        "Stage": "8. Reliability",
        "What to master": "NaN handling, clipping, dtype checks, shape validation",
        "You can move on when": "Your array calculations handle edge cases intentionally.",
    },
]


NUMPY_LESSONS = {
    "Beginner": {
        "goal": "Understand arrays, shapes, dtypes, indexing, and simple vectorized math.",
        "explanation": (
            "NumPy is the base layer for much of the Python data ecosystem. Start by "
            "thinking in arrays: values with a shape, a dtype, and fast operations."
        ),
        "modules": [
            {
                "title": "1. Create and inspect arrays",
                "why": "Shape and dtype tell you what kind of numeric object you are working with.",
                "code": """import numpy as np

scores = np.array([72, 85, 91, 64, 88])

scores.shape
scores.dtype
scores.mean()""",
            },
            {
                "title": "2. Generate practice data",
                "why": "Synthetic arrays let you practice without waiting for a real dataset.",
                "code": """rng = np.random.default_rng(seed=42)

temperatures = rng.normal(loc=70, scale=8, size=30)
temperatures = temperatures.round(1)
temperatures[:5]""",
            },
            {
                "title": "3. Select values",
                "why": "Indexing and slicing are the foundation for every array workflow.",
                "code": """scores[0]       # first value
scores[-1]      # last value
scores[:3]      # first three values
scores[scores >= 80]  # boolean mask""",
            },
            {
                "title": "4. Use vectorized operations",
                "why": "NumPy applies math to whole arrays, which is clearer and faster than manual loops.",
                "code": """curved_scores = np.minimum(scores + 5, 100)
passed = curved_scores >= 70

curved_scores
passed""",
            },
        ],
    },
    "Intermediate": {
        "goal": "Work with 2D arrays, axis-based summaries, broadcasting, and reshaping.",
        "explanation": (
            "Intermediate NumPy is about controlling array layout. Most mistakes come "
            "from misunderstanding shape, axis, or broadcasting rules."
        ),
        "modules": [
            {
                "title": "1. Build a 2D array",
                "why": "Many numeric datasets are matrices: rows are observations and columns are measurements.",
                "code": """matrix = np.array([
    [72, 85, 91],
    [64, 88, 79],
    [90, 93, 87],
    [58, 71, 69],
])

matrix.shape""",
            },
            {
                "title": "2. Summarize by axis",
                "why": "Axis controls whether you summarize columns, rows, or the whole array.",
                "code": """column_means = matrix.mean(axis=0)
row_means = matrix.mean(axis=1)
overall_mean = matrix.mean()""",
            },
            {
                "title": "3. Broadcast values",
                "why": "Broadcasting lets smaller arrays align with larger arrays for vectorized math.",
                "code": """curve_by_assignment = np.array([3, 5, 2])
curved_matrix = np.minimum(matrix + curve_by_assignment, 100)""",
            },
            {
                "title": "4. Reshape data",
                "why": "Reshaping changes layout while preserving values when the element count matches.",
                "code": """values = np.arange(1, 13)
table = values.reshape(3, 4)
flat = table.ravel()""",
            },
        ],
    },
    "Advanced": {
        "goal": "Build simulations, handle missing values, validate shapes, and prepare arrays for modeling.",
        "explanation": (
            "Advanced NumPy work is about reproducible numeric pipelines: generate data, "
            "transform it, validate it, and summarize results."
        ),
        "modules": [
            {
                "title": "1. Simulate a dataset",
                "why": "Simulation is useful for testing algorithms and creating practice problems.",
                "code": """rng = np.random.default_rng(seed=42)

customer_spend = rng.lognormal(mean=4.2, sigma=0.5, size=1000)
monthly_spend = customer_spend.reshape(100, 10)""",
            },
            {
                "title": "2. Handle missing numeric values",
                "why": "NumPy uses NaN for missing floating-point values.",
                "code": """data = monthly_spend.copy()
data[0, 0] = np.nan

column_means = np.nanmean(data, axis=0)
missing_count = np.isnan(data).sum()""",
            },
            {
                "title": "3. Validate shape before math",
                "why": "Shape checks make errors easier to understand than failed broadcasting later.",
                "code": """weights = np.array([0.2, 0.3, 0.5])

if weights.ndim != 1:
    raise ValueError("weights must be one-dimensional")""",
            },
            {
                "title": "4. Create reusable numeric functions",
                "why": "Reusable functions make array workflows testable and repeatable.",
                "code": """def z_score(values):
    values = np.asarray(values, dtype=float)
    return (values - np.nanmean(values)) / np.nanstd(values)

standardized = z_score(customer_spend)""",
            },
        ],
    },
}


NUMPY_CONCEPT_LIBRARY = {
    "ndarray": {
        "meaning": "The ndarray is NumPy's core object: a typed, multi-dimensional array.",
        "example": """values = np.array([10, 20, 30])
values.shape
values.dtype""",
        "mastery_check": "Explain why one array usually has one dtype.",
    },
    "Shape and Axis": {
        "meaning": "Shape describes array dimensions. Axis tells NumPy which direction to calculate across.",
        "example": """matrix.shape
matrix.mean(axis=0)  # column means
matrix.mean(axis=1)  # row means""",
        "mastery_check": "Predict the output shape before running an axis-based calculation.",
    },
    "Boolean Masks": {
        "meaning": "A boolean mask is an array of True/False values used to filter or update values.",
        "example": """high_scores = scores >= 80
scores[high_scores]""",
        "mastery_check": "Create masks with vectorized comparisons instead of loops.",
    },
    "Broadcasting": {
        "meaning": "Broadcasting lets arrays with compatible shapes work together in arithmetic.",
        "example": """matrix + np.array([1, 2, 3])""",
        "mastery_check": "Know why a column adjustment may need shape `(n, 1)`.",
    },
    "Random Generator": {
        "meaning": "default_rng creates reproducible random numbers for simulations and synthetic datasets.",
        "example": """rng = np.random.default_rng(seed=42)
rng.normal(loc=0, scale=1, size=5)""",
        "mastery_check": "Use seeds for repeatable lessons and `seed=None` for fresh random practice.",
    },
    "NaN": {
        "meaning": "NaN represents missing floating-point values. Use nan-aware functions when needed.",
        "example": """np.isnan(data).sum()
np.nanmean(data)""",
        "mastery_check": "Choose `np.mean` or `np.nanmean` intentionally.",
    },
}


NUMPY_CHEAT_SHEETS = {
    "Create": [
        ("Array from list", "np.array([1, 2, 3])"),
        ("Range", "np.arange(0, 10, 2)"),
        ("Even spacing", "np.linspace(0, 1, 5)"),
        ("Zeros", "np.zeros((3, 4))"),
        ("Random normal", "rng.normal(0, 1, size=100)"),
    ],
    "Inspect": [
        ("Shape", "arr.shape"),
        ("Dimensions", "arr.ndim"),
        ("Data type", "arr.dtype"),
        ("Size", "arr.size"),
        ("Missing count", "np.isnan(arr).sum()"),
    ],
    "Select": [
        ("First value", "arr[0]"),
        ("Last value", "arr[-1]"),
        ("Slice", "arr[:5]"),
        ("Column from matrix", "matrix[:, 0]"),
        ("Boolean filter", "arr[arr > 0]"),
    ],
    "Calculate": [
        ("Elementwise math", "arr * 100"),
        ("Clip values", "np.clip(arr, 0, 1)"),
        ("Mean", "arr.mean()"),
        ("Column means", "matrix.mean(axis=0)"),
        ("NaN-safe mean", "np.nanmean(arr)"),
    ],
    "Reshape": [
        ("Reshape", "arr.reshape(3, 4)"),
        ("Flatten", "matrix.ravel()"),
        ("Transpose", "matrix.T"),
        ("Stack rows", "np.vstack([a, b])"),
        ("Stack columns", "np.column_stack([a, b])"),
    ],
}


NUMPY_COMMON_MISTAKES = [
    {
        "mistake": "Confusing axis 0 and axis 1",
        "bad": """matrix.mean(axis=1)  # expected column means""",
        "better": """matrix.mean(axis=0)  # column means""",
        "why": "Axis 0 moves down rows and summarizes each column. Axis 1 moves across columns and summarizes each row.",
    },
    {
        "mistake": "Using Python lists for numeric math",
        "bad": """[1, 2, 3] * 2  # repeats the list""",
        "better": """np.array([1, 2, 3]) * 2""",
        "why": "NumPy arrays perform elementwise numeric operations.",
    },
    {
        "mistake": "Forgetting NaN-aware functions",
        "bad": """values.mean()""",
        "better": """np.nanmean(values)""",
        "why": "A single NaN can make the regular mean return NaN.",
    },
    {
        "mistake": "Changing shape without checking element count",
        "bad": """np.arange(10).reshape(3, 4)""",
        "better": """np.arange(12).reshape(3, 4)""",
        "why": "Reshape requires the same total number of elements.",
    },
]


NUMPY_PRACTICE_DRILLS = [
    {
        "skill": "Creation",
        "task": "Generate 30 simulated daily temperatures with mean 70 and standard deviation 8.",
        "answer": """rng = np.random.default_rng(seed=42)
temperatures = rng.normal(loc=70, scale=8, size=30)""",
    },
    {
        "skill": "Selection",
        "task": "Return only scores greater than or equal to 80.",
        "answer": """high_scores = scores[scores >= 80]""",
    },
    {
        "skill": "Aggregation",
        "task": "Calculate column means for a 2D matrix.",
        "answer": """column_means = matrix.mean(axis=0)""",
    },
    {
        "skill": "Broadcasting",
        "task": "Add a different curve value to each column in a score matrix.",
        "answer": """curved = matrix + np.array([3, 5, 2])""",
    },
    {
        "skill": "Missing values",
        "task": "Count missing values and calculate a NaN-safe average.",
        "answer": """missing_count = np.isnan(values).sum()
average = np.nanmean(values)""",
    },
]


NUMPY_QUIZ_QUESTIONS = [
    {
        "question": "Which attribute shows the dimensions of an array?",
        "choices": ["arr.shape", "arr.columns", "arr.head()"],
        "answer": "arr.shape",
        "explanation": "shape returns the size of each array dimension.",
    },
    {
        "question": "Which function creates evenly spaced values between two endpoints?",
        "choices": ["np.linspace", "np.value_counts", "np.merge"],
        "answer": "np.linspace",
        "explanation": "linspace is useful for grids, charts, and numeric intervals.",
    },
    {
        "question": "What does axis=0 usually summarize in a 2D array?",
        "choices": ["Columns", "Rows", "Only the first cell"],
        "answer": "Columns",
        "explanation": "axis=0 moves down rows, producing one result per column.",
    },
    {
        "question": "Which expression filters positive values from an array?",
        "choices": ["arr[arr > 0]", "arr.filter('positive')", "arr.loc[arr > 0]"],
        "answer": "arr[arr > 0]",
        "explanation": "The comparison creates a boolean mask, and the mask selects matching values.",
    },
    {
        "question": "Which tool creates reproducible random practice data?",
        "choices": ["np.random.default_rng(seed=42)", "np.read_csv()", "np.groupby()"],
        "answer": "np.random.default_rng(seed=42)",
        "explanation": "A seeded generator gives the same random sequence each time.",
    },
]


NUMPY_PROJECTS = [
    {
        "level": "Beginner",
        "title": "Student Score Simulator",
        "description": "Generate synthetic exam scores, curve them, and summarize pass rates.",
        "deliverables": ["Generated score array", "Pass-rate summary", "Short interpretation"],
        "notebook": "notebooks/07_numpy_student_score_simulator.ipynb",
    },
    {
        "level": "Beginner",
        "title": "Weather Array Explorer",
        "description": "Simulate daily temperatures and find unusually hot or cold days.",
        "deliverables": ["Temperature array", "Boolean masks", "Extreme-day counts"],
        "notebook": "notebooks/08_numpy_weather_array_explorer.ipynb",
    },
    {
        "level": "Intermediate",
        "title": "Sales Matrix Analyzer",
        "description": "Generate a store-by-product sales matrix and summarize by row and column.",
        "deliverables": ["2D sales matrix", "Store totals", "Product averages"],
        "notebook": "notebooks/09_numpy_sales_matrix_analyzer.ipynb",
    },
    {
        "level": "Intermediate",
        "title": "Broadcasting Practice Lab",
        "description": "Apply product prices, discounts, or weights across a matrix using broadcasting.",
        "deliverables": ["Broadcasted calculation", "Shape explanation", "Validation checks"],
        "notebook": "notebooks/10_numpy_broadcasting_practice_lab.ipynb",
    },
    {
        "level": "Advanced",
        "title": "Monte Carlo Budget Risk",
        "description": "Simulate thousands of monthly costs and estimate the chance of going over budget.",
        "deliverables": ["Simulation array", "Risk estimate", "Scenario summary"],
        "notebook": "notebooks/11_numpy_monte_carlo_budget_risk.ipynb",
    },
]


def create_sales_data() -> pd.DataFrame:
    """Create a small DataFrame used by the playground.

    In a real app, you might load this data from a CSV, database, or uploaded
    file. Here we build it directly so the app works immediately after download.
    """
    data = [
        {"date": "2026-01-04", "region": "West", "category": "Software", "units": 8, "price": 120},
        {"date": "2026-01-07", "region": "East", "category": "Hardware", "units": 3, "price": 210},
        {"date": "2026-01-09", "region": "South", "category": "Services", "units": 6, "price": 90},
        {"date": "2026-01-12", "region": "West", "category": "Hardware", "units": 2, "price": 340},
        {"date": "2026-01-15", "region": "North", "category": "Software", "units": 5, "price": 150},
        {"date": "2026-01-17", "region": "East", "category": "Services", "units": 9, "price": 75},
        {"date": "2026-01-19", "region": "South", "category": "Software", "units": 4, "price": 180},
        {"date": "2026-01-22", "region": "North", "category": "Hardware", "units": 1, "price": 520},
    ]

    df = pd.DataFrame(data)

    # Convert strings to real datetime values so Pandas can sort and chart dates.
    df["date"] = pd.to_datetime(df["date"])

    # Create a calculated column exactly like learners would do in Pandas.
    df["revenue"] = df["units"] * df["price"]
    return df


def create_numpy_matrix(rows: int, columns: int, seed: int) -> np.ndarray:
    """Create a synthetic numeric matrix for the NumPy playground."""
    rng = np.random.default_rng(seed=seed)
    base = rng.normal(loc=75, scale=12, size=(rows, columns))
    return np.clip(base, 0, 100).round(1)


def render_header(track: str) -> None:
    """Render the app title and high-level learning promise."""
    if track == "Pandas":
        active_line = "Pandas track selected"
        stats = [
            ("Learning stages", len(MASTERY_MAP)),
            ("Concepts", len(CONCEPT_LIBRARY)),
            ("Cheat sheets", len(CHEAT_SHEETS)),
            ("Projects", len(PROJECTS)),
        ]
    else:
        active_line = "NumPy track selected"
        stats = [
            ("Learning stages", len(NUMPY_MASTERY_MAP)),
            ("Concepts", len(NUMPY_CONCEPT_LIBRARY)),
            ("Cheat sheets", len(NUMPY_CHEAT_SHEETS)),
            ("Projects", len(NUMPY_PROJECTS)),
        ]

    st.markdown(
        f"""
        <section class="pathway-hero">
            <div class="pathway-kicker">Interactive Python library lab</div>
            <h1>Python Data Pathways</h1>
            <p>
                Choose Pandas for table analysis or NumPy for array thinking. Each track
                gives students a roadmap, bite-sized lessons, active drills, quizzes,
                playgrounds, and synthetic-data projects they can open in Colab.
            </p>
            <div class="track-pill">{active_line}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    pandas_active = "active" if track == "Pandas" else ""
    numpy_active = "active" if track == "NumPy" else ""
    st.markdown(
        f"""
        <div class="track-card-grid">
            <div class="track-card pandas {pandas_active}">
                <h3>Pandas Track</h3>
                <p>Practice DataFrames, cleaning, joins, time series, reusable pipelines,
                and business-style analysis notebooks.</p>
            </div>
            <div class="track-card numpy {numpy_active}">
                <h3>NumPy Track</h3>
                <p>Practice arrays, shape, axis, broadcasting, simulations, masks,
                and fast vectorized numeric workflows.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_tiles = "".join(
        f'<div class="stat-tile"><div class="stat-value">{value}</div>'
        f'<div class="stat-label">{label}</div></div>'
        for label, value in stats
    )
    st.markdown(f'<div class="stat-grid">{stat_tiles}</div>', unsafe_allow_html=True)


def render_mastery_map() -> None:
    """Render the complete Pandas mastery roadmap."""
    st.header("Pandas Mastery Map")
    st.write(
        "Use this roadmap as your checklist. Pandas mastery is not memorizing every method; "
        "it is knowing which tool matches the data problem in front of you."
    )

    mastery = pd.DataFrame(MASTERY_MAP)
    st.dataframe(mastery, use_container_width=True, hide_index=True)

    st.subheader("How to study each stage")
    st.write(
        "For every stage: read the concept, run the example, change one part of the code, "
        "explain the result in plain English, then solve a small task without looking."
    )


def render_concepts() -> None:
    """Render a concept library with explanations and examples."""
    st.header("Pandas Concept Library")
    st.write(
        "This section explains the ideas behind the syntax. When you understand these "
        "concepts, Pandas becomes much easier to remember."
    )

    selected_concept = st.selectbox("Choose a concept", list(CONCEPT_LIBRARY.keys()))
    concept = CONCEPT_LIBRARY[selected_concept]

    st.subheader(selected_concept)
    st.write(concept["meaning"])
    st.caption("Example")
    st.code(concept["example"], language="python")
    st.success(f"Mastery check: {concept['mastery_check']}")

    st.subheader("Quick comparison table")
    comparison = pd.DataFrame(
        [
            {"Question": "Need one column?", "Pandas tool": "df['column']", "Returns": "Series"},
            {"Question": "Need rows by condition?", "Pandas tool": "df.loc[condition]", "Returns": "DataFrame"},
            {"Question": "Need summary by group?", "Pandas tool": "groupby().agg()", "Returns": "DataFrame or Series"},
            {"Question": "Need related table columns?", "Pandas tool": "merge()", "Returns": "DataFrame"},
            {"Question": "Need date-based summary?", "Pandas tool": "resample()", "Returns": "DataFrame or Series"},
        ]
    )
    st.dataframe(comparison, use_container_width=True, hide_index=True)


def render_lessons() -> None:
    """Render the selected course level and its lesson modules."""
    st.header("1. Learn Pandas Concepts")

    selected_level = st.selectbox(
        "Choose your level",
        list(LESSONS.keys()),
        help="Start with Beginner if you are new to Pandas. Move up when the examples feel familiar.",
    )

    lesson = LESSONS[selected_level]
    st.info(f"Goal: {lesson['goal']}")
    st.write(lesson["explanation"])

    # Each module is displayed in an expander so the page stays organized.
    for module in lesson["modules"]:
        with st.expander(module["title"], expanded=True):
            st.write(module["why"])
            st.code(module["code"], language="python")

            # These prompts force active learning instead of passive reading.
            st.caption("Practice prompt")
            st.write("Run the example, change one column name or condition, and describe how the output changed.")


def render_cheat_sheets() -> None:
    """Render compact syntax references grouped by task."""
    st.header("Pandas Cheat Sheets")
    st.write(
        "Cheat sheets are for recall after you understand the concept. Use them when "
        "you know what you want to do but need the exact syntax."
    )

    selected_topic = st.selectbox("Choose a topic", list(CHEAT_SHEETS.keys()))
    rows = pd.DataFrame(CHEAT_SHEETS[selected_topic], columns=["Task", "Syntax"])
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("Copy-friendly examples")
    for task, syntax in CHEAT_SHEETS[selected_topic]:
        with st.expander(task):
            st.code(syntax, language="python")


def render_common_mistakes() -> None:
    """Render common Pandas mistakes and safer patterns."""
    st.header("Common Pandas Mistakes")
    st.write(
        "Mastery includes knowing what can silently go wrong. These mistakes cause many "
        "incorrect analyses even when the code runs without crashing."
    )

    for item in COMMON_MISTAKES:
        with st.expander(item["mistake"], expanded=False):
            st.write(item["why"])
            left, right = st.columns(2)
            with left:
                st.caption("Problem pattern")
                st.code(item["bad"], language="python")
            with right:
                st.caption("Better pattern")
                st.code(item["better"], language="python")


def render_drills() -> None:
    """Render short active-recall practice drills."""
    st.header("Mastery Drills")
    st.write(
        "Try to solve each drill before opening the answer. These are intentionally small "
        "because fluency comes from repeated accurate practice."
    )

    selected_skill = st.radio(
        "Filter by skill",
        ["All"] + sorted({drill["skill"] for drill in PRACTICE_DRILLS}),
        horizontal=True,
    )

    visible_drills = [
        drill
        for drill in PRACTICE_DRILLS
        if selected_skill == "All" or drill["skill"] == selected_skill
    ]

    for index, drill in enumerate(visible_drills, start=1):
        with st.expander(f"Drill {index}: {drill['skill']}"):
            st.write(drill["task"])
            st.caption("Answer")
            st.code(drill["answer"], language="python")


def render_playground() -> None:
    """Render a real Pandas playground with filters, grouping, and charts."""
    st.header("2. Practice With a Real DataFrame")
    st.write(
        "This section uses an actual Pandas DataFrame. Change the controls and watch "
        "how the table, chart, and matching Pandas code change."
    )

    df = create_sales_data()

    with st.expander("What this DataFrame represents", expanded=True):
        st.write(
            "Each row is a sales transaction. `region` and `category` are dimensions "
            "used for grouping. `units`, `price`, and `revenue` are measures used for "
            "calculations. A strong Pandas user separates dimensions from measures before analysis."
        )

    st.subheader("Original DataFrame")
    st.dataframe(df, use_container_width=True)

    st.subheader("Interactive Filters")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_region = st.selectbox("Region", ["All"] + sorted(df["region"].unique().tolist()))
    with col2:
        minimum_revenue = st.slider("Minimum revenue", min_value=0, max_value=1000, value=0, step=25)
    with col3:
        sort_column = st.selectbox("Sort by", ["revenue", "units", "price"])

    filtered = df.copy()

    # Apply the region filter only when the user chooses a specific region.
    if selected_region != "All":
        filtered = filtered.loc[filtered["region"] == selected_region]

    # Apply the revenue filter from the slider.
    filtered = filtered.loc[filtered["revenue"] >= minimum_revenue]

    # Sort descending so the largest values are easiest to see.
    filtered = filtered.sort_values(sort_column, ascending=False)

    st.subheader("Filtered Result")
    st.dataframe(filtered, use_container_width=True)

    code_lines = ["result = df.copy()"]
    if selected_region != "All":
        code_lines.append(f'result = result.loc[result["region"] == "{selected_region}"]')
    code_lines.append(f'result = result.loc[result["revenue"] >= {minimum_revenue}]')
    code_lines.append(f'result = result.sort_values("{sort_column}", ascending=False)')

    st.caption("Equivalent Pandas code")
    st.code("\n".join(code_lines), language="python")

    with st.expander("Why this code works"):
        st.write(
            "The filter expressions create boolean Series. Pandas keeps rows where the "
            "condition is True. `sort_values` then reorders the remaining rows without "
            "changing the meaning of the columns."
        )

    st.subheader("GroupBy Practice")
    group_column = st.selectbox("Group rows by", ["category", "region"])

    grouped = (
        filtered.groupby(group_column, as_index=False)
        .agg(
            total_units=("units", "sum"),
            total_revenue=("revenue", "sum"),
            average_price=("price", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    st.dataframe(grouped, use_container_width=True)
    st.bar_chart(grouped, x=group_column, y="total_revenue")

    st.caption("Equivalent groupby code")
    st.code(
        f"""summary = (
    result
    .groupby("{group_column}", as_index=False)
    .agg(
        total_units=("units", "sum"),
        total_revenue=("revenue", "sum"),
        average_price=("price", "mean"),
    )
    .sort_values("total_revenue", ascending=False)
)""",
        language="python",
    )

    with st.expander("GroupBy mental model"):
        st.write(
            "GroupBy has three steps: split rows into groups, apply calculations to each "
            "group, and combine the calculated results into a new table. The original "
            "transaction rows are not the final answer; they are the raw material for the summary."
        )


def render_quiz() -> None:
    """Render a simple quiz and explain each answer immediately."""
    st.header("3. Check Your Understanding")

    # Session state stores values across Streamlit reruns. Without it, the score
    # would reset every time the user clicked a widget.
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    for index, item in enumerate(QUIZ_QUESTIONS, start=1):
        with st.expander(f"Question {index}: {item['question']}"):
            answer = st.radio(
                "Choose one answer",
                item["choices"],
                key=f"question_{index}",
                index=None,
            )

            if answer is not None:
                if answer == item["answer"]:
                    st.success(f"Correct. {item['explanation']}")
                else:
                    st.error(f"Not quite. Correct answer: {item['answer']}")
                    st.write(item["explanation"])


def render_projects() -> None:
    """Render project ideas grouped by difficulty."""
    st.header("4. Build Projects")
    st.write(
        "Projects help you move from recognizing Pandas syntax to solving complete "
        "data problems. Pick one project from your current level before moving up."
    )
    st.write(
        "Each notebook generates synthetic data with a random seed, so students can "
        "change the seed or row count and practice on a new version of the project."
    )

    if not GITHUB_REPO_SLUG:
        st.info(
            "To make the Colab buttons active, push this project to GitHub and set "
            "`GITHUB_REPO_SLUG`, for example `your-name/your-repo`, before running Streamlit."
        )

    selected_project_level = st.radio(
        "Filter projects by level",
        ["All", "Beginner", "Intermediate", "Advanced"],
        horizontal=True,
    )

    visible_projects = [
        project
        for project in PROJECTS
        if selected_project_level == "All" or project["level"] == selected_project_level
    ]

    for project in visible_projects:
        with st.container(border=True):
            st.subheader(f"{project['title']} ({project['level']})")
            st.write(project["description"])
            st.write("Deliverables:")
            for deliverable in project["deliverables"]:
                st.write(f"- {deliverable}")
            st.caption(f"Notebook: {project['notebook']}")
            colab_url = build_colab_url(project["notebook"])
            if colab_url:
                st.link_button("Open in Colab", colab_url)
            else:
                st.button("Open in Colab", disabled=True, key=f"colab-{project['notebook']}")


def render_study_plan() -> None:
    """Render a recommended path through the material."""
    st.header("5. Suggested Study Plan")

    plan = pd.DataFrame(
        [
            {
                "Week": 1,
                "Focus": "DataFrame mental model and inspection",
                "Practice": "Use head, info, describe, dtypes, value_counts, and isna on three datasets",
                "Proof of mastery": "Explain each column's meaning, dtype, and data quality risk",
            },
            {
                "Week": 2,
                "Focus": "Selection, filtering, and new columns",
                "Practice": "Write 20 filters using loc, boolean masks, isin, between, and query",
                "Proof of mastery": "Create correct subsets without trial-and-error syntax",
            },
            {
                "Week": 3,
                "Focus": "Cleaning missing values, text, dates, and duplicates",
                "Practice": "Clean messy labels, parse dates, and document every missing-value decision",
                "Proof of mastery": "Produce a cleaned DataFrame with a written cleaning log",
            },
            {
                "Week": 4,
                "Focus": "Aggregation and reshaping",
                "Practice": "Use groupby, agg, transform, pivot_table, crosstab, melt",
                "Proof of mastery": "Build summaries that answer business questions directly",
            },
            {
                "Week": 5,
                "Focus": "Merging and relational thinking",
                "Practice": "Merge orders, customers, and products with validation and unmatched-row checks",
                "Proof of mastery": "Explain why each join type was chosen and prove row counts are correct",
            },
            {
                "Week": 6,
                "Focus": "Time series and advanced pipelines",
                "Practice": "Create weekly summaries, lag features, rolling averages, and pipe functions",
                "Proof of mastery": "Build a repeatable analysis pipeline from raw data to final table",
            },
            {
                "Week": 7,
                "Focus": "Performance and reliability",
                "Practice": "Replace row loops with vectorized operations and add validation checks",
                "Proof of mastery": "Profile one workflow and explain the bottleneck",
            },
            {
                "Week": 8,
                "Focus": "Portfolio project",
                "Practice": "Complete one guided notebook, then repeat it with your own dataset",
                "Proof of mastery": "Publish a clean notebook with conclusions, assumptions, and next steps",
            },
        ]
    )

    st.dataframe(plan, use_container_width=True, hide_index=True)

    st.subheader("Mastery rule")
    st.write(
        "Do not measure progress by pages read. Measure it by whether you can receive "
        "a messy table, inspect it, clean it, transform it, summarize it, validate it, "
        "and explain the result clearly."
    )


def render_numpy_mastery_map() -> None:
    """Render the complete NumPy mastery roadmap."""
    st.header("NumPy Mastery Map")
    st.write(
        "Use this roadmap as your checklist. NumPy mastery means understanding shape, "
        "dtype, axis, broadcasting, and vectorized numeric thinking."
    )

    mastery = pd.DataFrame(NUMPY_MASTERY_MAP)
    st.dataframe(mastery, use_container_width=True, hide_index=True)

    st.subheader("How to study each stage")
    st.write(
        "For every stage: run the example, change the shape or seed, predict the output "
        "shape, then explain the result without relying on trial and error."
    )


def render_numpy_concepts() -> None:
    """Render NumPy concept explanations."""
    st.header("NumPy Concept Library")
    st.write(
        "This section explains the ideas behind NumPy syntax. Most NumPy errors become "
        "easier to solve when you can reason about shape and dtype."
    )

    selected_concept = st.selectbox("Choose a concept", list(NUMPY_CONCEPT_LIBRARY.keys()))
    concept = NUMPY_CONCEPT_LIBRARY[selected_concept]

    st.subheader(selected_concept)
    st.write(concept["meaning"])
    st.code(concept["example"], language="python")
    st.info(f"Mastery check: {concept['mastery_check']}")


def render_numpy_lessons() -> None:
    """Render NumPy lessons by level."""
    st.header("1. Learn NumPy Concepts")

    selected_level = st.radio(
        "Choose your level",
        list(NUMPY_LESSONS.keys()),
        horizontal=True,
        help="Start with Beginner if arrays, shape, and dtype are new to you.",
    )

    lesson = NUMPY_LESSONS[selected_level]
    st.subheader(lesson["goal"])
    st.write(lesson["explanation"])

    for module in lesson["modules"]:
        with st.expander(module["title"], expanded=True):
            st.write(module["why"])
            st.code(module["code"], language="python")


def render_numpy_cheat_sheets() -> None:
    """Render NumPy syntax cheat sheets."""
    st.header("NumPy Cheat Sheets")
    st.write("Use these as quick references after you understand the concept.")

    selected_topic = st.selectbox("Choose a topic", list(NUMPY_CHEAT_SHEETS.keys()))
    rows = pd.DataFrame(NUMPY_CHEAT_SHEETS[selected_topic], columns=["Task", "Syntax"])
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("Copyable examples")
    for task, syntax in NUMPY_CHEAT_SHEETS[selected_topic]:
        st.code(f"# {task}\n{syntax}", language="python")


def render_numpy_common_mistakes() -> None:
    """Render common NumPy mistakes and safer patterns."""
    st.header("Common NumPy Mistakes")

    for item in NUMPY_COMMON_MISTAKES:
        with st.expander(item["mistake"], expanded=False):
            left, right = st.columns(2)
            with left:
                st.write("Risky pattern")
                st.code(item["bad"], language="python")
            with right:
                st.write("Better pattern")
                st.code(item["better"], language="python")
            st.write(item["why"])


def render_numpy_drills() -> None:
    """Render NumPy practice drills."""
    st.header("2. NumPy Drills")
    st.write(
        "Try writing the answer before opening the solution. The goal is active recall, "
        "not recognizing code after seeing it."
    )

    selected_skill = st.selectbox(
        "Filter by skill",
        ["All"] + sorted({drill["skill"] for drill in NUMPY_PRACTICE_DRILLS}),
    )

    visible_drills = [
        drill
        for drill in NUMPY_PRACTICE_DRILLS
        if selected_skill == "All" or drill["skill"] == selected_skill
    ]

    for index, drill in enumerate(visible_drills, start=1):
        st.subheader(f"Drill {index}: {drill['skill']}")
        st.write(drill["task"])
        with st.expander("Show answer"):
            st.code(drill["answer"], language="python")


def render_numpy_playground() -> None:
    """Render an interactive NumPy array playground."""
    st.header("3. Practice With a NumPy Array")
    st.write(
        "Change the controls and watch how the array, summary statistics, and equivalent "
        "NumPy code change."
    )

    rows = st.slider("Rows", min_value=3, max_value=12, value=6)
    columns = st.slider("Columns", min_value=2, max_value=8, value=4)
    seed = st.number_input("Random seed", min_value=0, max_value=9999, value=42, step=1)
    threshold = st.slider("Highlight values at or above", min_value=0, max_value=100, value=85)

    matrix = create_numpy_matrix(rows=rows, columns=columns, seed=int(seed))
    mask = matrix >= threshold

    st.subheader("Generated array")
    st.dataframe(pd.DataFrame(matrix), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Shape", str(matrix.shape))
    col2.metric("Mean", f"{matrix.mean():.1f}")
    col3.metric("Values above threshold", int(mask.sum()))

    summary = pd.DataFrame(
        {
            "column": [f"Column {index}" for index in range(columns)],
            "mean": matrix.mean(axis=0).round(1),
            "min": matrix.min(axis=0).round(1),
            "max": matrix.max(axis=0).round(1),
        }
    )
    st.subheader("Column summary")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.caption("Equivalent NumPy code")
    st.code(
        f"""rng = np.random.default_rng(seed={int(seed)})
matrix = rng.normal(loc=75, scale=12, size=({rows}, {columns}))
matrix = np.clip(matrix, 0, 100).round(1)

mask = matrix >= {threshold}
column_means = matrix.mean(axis=0)
values_above_threshold = mask.sum()""",
        language="python",
    )


def render_numpy_quiz() -> None:
    """Render a simple NumPy quiz."""
    st.header("4. NumPy Quiz")
    st.write("Choose an answer, then check it immediately.")

    for index, item in enumerate(NUMPY_QUIZ_QUESTIONS, start=1):
        with st.container(border=True):
            st.subheader(f"Question {index}")
            st.write(item["question"])
            answer = st.radio(
                "Answer",
                item["choices"],
                key=f"numpy-quiz-{index}",
                label_visibility="collapsed",
            )
            if st.button("Check answer", key=f"numpy-check-{index}"):
                if answer == item["answer"]:
                    st.success(f"Correct. {item['explanation']}")
                else:
                    st.error(f"Not quite. Correct answer: {item['answer']}")
                    st.write(item["explanation"])


def render_numpy_projects() -> None:
    """Render NumPy project ideas grouped by difficulty."""
    st.header("5. Build NumPy Projects")
    st.write(
        "These projects focus on arrays, random data generation, broadcasting, summary "
        "statistics, and simulation."
    )
    if not GITHUB_REPO_SLUG:
        st.info(
            "To make the Colab buttons active, push this project to GitHub and set "
            "`GITHUB_REPO_SLUG`, for example `your-name/your-repo`, before running Streamlit."
        )

    selected_project_level = st.radio(
        "Filter projects by level",
        ["All", "Beginner", "Intermediate", "Advanced"],
        horizontal=True,
        key="numpy-project-level",
    )

    visible_projects = [
        project
        for project in NUMPY_PROJECTS
        if selected_project_level == "All" or project["level"] == selected_project_level
    ]

    for project in visible_projects:
        with st.container(border=True):
            st.subheader(f"{project['title']} ({project['level']})")
            st.write(project["description"])
            st.write("Deliverables:")
            for deliverable in project["deliverables"]:
                st.write(f"- {deliverable}")
            st.caption(f"Notebook: {project['notebook']}")
            colab_url = build_colab_url(project["notebook"])
            if colab_url:
                st.link_button("Open in Colab", colab_url)
            else:
                st.button("Open in Colab", disabled=True, key=f"numpy-colab-{project['notebook']}")


def render_numpy_study_plan() -> None:
    """Render a recommended NumPy study plan."""
    st.header("6. Suggested NumPy Study Plan")

    plan = pd.DataFrame(
        [
            {
                "Week": 1,
                "Focus": "Array mental model",
                "Practice": "Create arrays, inspect shape and dtype, and explain dimensions",
                "Proof of mastery": "Predict output shapes before running code",
            },
            {
                "Week": 2,
                "Focus": "Indexing and masks",
                "Practice": "Slice 1D and 2D arrays and build boolean filters",
                "Proof of mastery": "Select target values without converting to lists",
            },
            {
                "Week": 3,
                "Focus": "Vectorization and broadcasting",
                "Practice": "Replace loops with array math and column adjustments",
                "Proof of mastery": "Explain why compatible shapes broadcast",
            },
            {
                "Week": 4,
                "Focus": "Simulation project",
                "Practice": "Generate random data, summarize outcomes, and validate assumptions",
                "Proof of mastery": "Build a reproducible simulation with a seed",
            },
        ]
    )

    st.dataframe(plan, use_container_width=True, hide_index=True)


def main() -> None:
    """Main application entry point."""
    apply_app_styles()

    st.sidebar.title("Learning Track")
    track = st.sidebar.radio(
        "What are you learning?",
        ["Pandas", "NumPy"],
        help="Choose one track first, then work through that library's roadmap.",
    )

    render_header(track)

    st.sidebar.title("Navigation")
    if track == "Pandas":
        page = st.sidebar.radio(
            "Go to",
            [
                "Mastery Map",
                "Concept Library",
                "Lessons",
                "Cheat Sheets",
                "Playground",
                "Drills",
                "Quiz",
                "Common Mistakes",
                "Projects",
                "Study Plan",
            ],
        )
    else:
        page = st.sidebar.radio(
            "Go to",
            [
                "Mastery Map",
                "Concept Library",
                "Lessons",
                "Cheat Sheets",
                "Playground",
                "Drills",
                "Quiz",
                "Common Mistakes",
                "Projects",
                "Study Plan",
            ],
            key="numpy-page",
        )

    st.sidebar.markdown(
        """
        <div class="sidebar-guide">
            <div class="sidebar-guide-title">Recommended order</div>
            <ol>
                <li>Mastery Map</li>
                <li>Concept Library</li>
                <li>Lessons</li>
                <li>Playground</li>
                <li>Drills and Quiz</li>
                <li>Projects</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if track == "Pandas":
        if page == "Mastery Map":
            render_mastery_map()
        elif page == "Concept Library":
            render_concepts()
        elif page == "Lessons":
            render_lessons()
        elif page == "Cheat Sheets":
            render_cheat_sheets()
        elif page == "Playground":
            render_playground()
        elif page == "Drills":
            render_drills()
        elif page == "Quiz":
            render_quiz()
        elif page == "Common Mistakes":
            render_common_mistakes()
        elif page == "Projects":
            render_projects()
        elif page == "Study Plan":
            render_study_plan()
    else:
        if page == "Mastery Map":
            render_numpy_mastery_map()
        elif page == "Concept Library":
            render_numpy_concepts()
        elif page == "Lessons":
            render_numpy_lessons()
        elif page == "Cheat Sheets":
            render_numpy_cheat_sheets()
        elif page == "Playground":
            render_numpy_playground()
        elif page == "Drills":
            render_numpy_drills()
        elif page == "Quiz":
            render_numpy_quiz()
        elif page == "Common Mistakes":
            render_numpy_common_mistakes()
        elif page == "Projects":
            render_numpy_projects()
        elif page == "Study Plan":
            render_numpy_study_plan()


if __name__ == "__main__":
    main()
