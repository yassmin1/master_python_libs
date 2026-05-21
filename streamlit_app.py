"""
Pandas Pathway
--------------

This Streamlit app teaches Pandas from beginner to advanced level. It is meant
to be more than a syntax demo: it explains concepts, shows examples, gives
practice tasks, and points learners toward full project notebooks.

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

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
# Streamlit reads this once when the app starts. The wide layout gives tables,
# charts, and code examples enough horizontal room.
st.set_page_config(
    page_title="Pandas Pathway",
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


def render_header() -> None:
    """Render the app title and high-level learning promise."""
    st.title("Pandas Pathway")
    st.subheader("A complete Pandas learning path from first DataFrame to advanced analysis.")
    st.write(
        "The goal is mastery: understand the mental model, practice the syntax, avoid "
        "common mistakes, and complete real projects that look like workplace analysis."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Learning stages", len(MASTERY_MAP))
    col2.metric("Concepts", len(CONCEPT_LIBRARY))
    col3.metric("Cheat sheet topics", len(CHEAT_SHEETS))
    col4.metric("Projects", len(PROJECTS))


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


def main() -> None:
    """Main application entry point."""
    render_header()

    st.sidebar.title("Navigation")
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

    st.sidebar.markdown("---")
    st.sidebar.write("Recommended order:")
    st.sidebar.write("1. Mastery Map")
    st.sidebar.write("2. Concept Library")
    st.sidebar.write("3. Lessons")
    st.sidebar.write("4. Playground")
    st.sidebar.write("5. Drills and Quiz")
    st.sidebar.write("6. Projects")

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


if __name__ == "__main__":
    main()
