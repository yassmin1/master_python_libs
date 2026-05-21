const lessons = {
  beginner: {
    title: "Beginner: DataFrames, Series, and selection",
    summary:
      "Build a mental model of rows, columns, indexes, dtypes, and the read-inspect-select loop used in almost every Pandas workflow.",
    modules: [
      {
        title: "Create and inspect data",
        text: "Use read_csv, head, info, describe, shape, columns, and dtypes before transforming anything.",
        code: 'df = pd.read_csv("orders.csv")\ndf.head()\ndf.info()',
      },
      {
        title: "Select columns and rows",
        text: "Choose columns with brackets, rows with loc or iloc, and boolean filters for conditions.",
        code: 'df.loc[df["region"] == "West", ["date", "sales"]]',
      },
      {
        title: "Add and change columns",
        text: "Use assign for readable derived columns and keep transformations chainable.",
        code: 'df = df.assign(revenue=df["units"] * df["price"])',
      },
      {
        title: "Missing values",
        text: "Find nulls, decide whether to fill or drop them, and document the business reason.",
        code: 'df["discount"].fillna(0)\ndf.dropna(subset=["customer_id"])',
      },
    ],
  },
  intermediate: {
    title: "Intermediate: Cleaning, grouping, merging, and reshaping",
    summary:
      "Learn the workhorse skills used in analysis jobs: cleaning messy inputs, summarizing data, joining sources, and reshaping tables.",
    modules: [
      {
        title: "Group and aggregate",
        text: "Use groupby with named aggregations to create readable summary tables.",
        code: 'df.groupby("category", as_index=False).agg(total=("revenue", "sum"))',
      },
      {
        title: "Merge related tables",
        text: "Choose inner, left, right, or outer joins based on which records must be retained.",
        code: 'orders.merge(customers, on="customer_id", how="left")',
      },
      {
        title: "Reshape data",
        text: "Use melt for tidy long data and pivot_table for cross-tab summaries.",
        code: 'df.melt(id_vars="date", var_name="metric", value_name="value")',
      },
      {
        title: "Text and categories",
        text: "Clean strings with str methods and use category dtype for repeated labels.",
        code: 'df["city"] = df["city"].str.strip().str.title()',
      },
    ],
  },
  advanced: {
    title: "Advanced: Time series, windows, performance, and pipelines",
    summary:
      "Practice production-minded Pandas: reliable date handling, rolling metrics, memory use, validation, and maintainable method chains.",
    modules: [
      {
        title: "Time series",
        text: "Parse dates early, set useful indexes when needed, and resample for calendar-based analysis.",
        code: 'df["date"] = pd.to_datetime(df["date"])\ndf.resample("W", on="date")["revenue"].sum()',
      },
      {
        title: "Window calculations",
        text: "Use rolling, expanding, and shift to create trends, lags, and moving averages.",
        code: 'df["ma_7"] = df["revenue"].rolling(7).mean()',
      },
      {
        title: "Performance basics",
        text: "Prefer vectorized operations, avoid row loops, and profile before optimizing.",
        code: 'df.eval("margin = revenue - cost")',
      },
      {
        title: "Reusable pipelines",
        text: "Use pipe and small functions to make analysis repeatable and testable.",
        code: 'clean = (raw.pipe(normalize_columns).pipe(remove_test_rows))',
      },
    ],
  },
};

const questions = [
  {
    question: "Which method gives a concise summary of columns, non-null counts, and dtypes?",
    options: ["df.info()", "df.sample()", "df.rename()"],
    answer: 0,
    explanation: "df.info() is usually one of the first inspection methods to run.",
  },
  {
    question: "Which expression filters rows where revenue is above 500?",
    options: ['df["revenue"] > 500', 'df.loc["revenue"]', "df.revenue(500)"],
    answer: 0,
    explanation: "A boolean Series can be used inside df.loc or brackets to filter rows.",
  },
  {
    question: "What is the safest join when all orders must remain even if customer details are missing?",
    options: ["left merge from orders", "inner merge", "right merge from customers"],
    answer: 0,
    explanation: "A left merge keeps every row from the left table.",
  },
  {
    question: "Which tool summarizes revenue by category?",
    options: ["groupby + agg", "drop_duplicates", "sort_values only"],
    answer: 0,
    explanation: "groupby + agg creates grouped summary statistics.",
  },
  {
    question: "Which method converts wide columns into a tidy long format?",
    options: ["melt", "head", "fillna"],
    answer: 0,
    explanation: "melt turns multiple value columns into variable and value columns.",
  },
  {
    question: "What should you prefer before optimizing a slow Pandas workflow?",
    options: ["Profile the bottleneck", "Rewrite everything", "Add random indexes"],
    answer: 0,
    explanation: "Profiling keeps performance work focused on the real constraint.",
  },
];

const sales = [
  { date: "2026-01-04", region: "West", category: "Software", units: 8, price: 120 },
  { date: "2026-01-07", region: "East", category: "Hardware", units: 3, price: 210 },
  { date: "2026-01-09", region: "South", category: "Services", units: 6, price: 90 },
  { date: "2026-01-12", region: "West", category: "Hardware", units: 2, price: 340 },
  { date: "2026-01-15", region: "North", category: "Software", units: 5, price: 150 },
  { date: "2026-01-17", region: "East", category: "Services", units: 9, price: 75 },
  { date: "2026-01-19", region: "South", category: "Software", units: 4, price: 180 },
  { date: "2026-01-22", region: "North", category: "Hardware", units: 1, price: 520 },
];

const projects = [
  {
    level: "Beginner",
    title: "Movie Ratings Explorer",
    tasks: ["Load CSV files", "Clean missing ratings", "Find top genres", "Export a summary CSV"],
  },
  {
    level: "Beginner",
    title: "Personal Budget Tracker",
    tasks: ["Categorize transactions", "Calculate monthly totals", "Plot spending trends", "Flag unusual expenses"],
  },
  {
    level: "Intermediate",
    title: "Retail Sales Dashboard Data",
    tasks: ["Merge orders and products", "Create revenue metrics", "Group by region", "Prepare dashboard tables"],
  },
  {
    level: "Intermediate",
    title: "Support Ticket Analysis",
    tasks: ["Parse dates", "Measure response time", "Pivot by priority", "Find backlog patterns"],
  },
  {
    level: "Advanced",
    title: "Time Series Forecast Prep",
    tasks: ["Resample daily sales", "Create lag features", "Add rolling means", "Validate missing dates"],
  },
  {
    level: "Advanced",
    title: "Reusable Data Cleaning Package",
    tasks: ["Write pipe functions", "Add schema checks", "Benchmark operations", "Document assumptions"],
  },
];

let currentQuestion = 0;
let score = 0;
let grouped = false;

function renderLesson(level) {
  const lesson = lessons[level];
  const panel = document.querySelector("#lesson-panel");
  panel.innerHTML = `
    <h3>${lesson.title}</h3>
    <p class="muted">${lesson.summary}</p>
    <div class="lesson-grid">
      ${lesson.modules
        .map(
          (module) => `
          <div class="mini-card">
            <h4>${module.title}</h4>
            <p>${module.text}</p>
            <code>${module.code}</code>
          </div>
        `
        )
        .join("")}
    </div>
  `;
}

function renderQuiz() {
  const item = questions[currentQuestion];
  document.querySelector("#quiz-progress").textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
  document.querySelector("#quiz-score").textContent = `Score ${score}`;
  document.querySelector("#quiz-question").textContent = item.question;
  document.querySelector("#quiz-feedback").textContent = "";
  document.querySelector("#quiz-options").innerHTML = item.options
    .map((option, index) => `<button type="button" data-answer="${index}">${option}</button>`)
    .join("");
}

function calculateRevenue(row) {
  return row.units * row.price;
}

function getFilteredData() {
  const region = document.querySelector("#region-filter").value;
  const minimumRevenue = Number(document.querySelector("#revenue-filter").value);
  const sortField = document.querySelector("#sort-field").value;

  let rows = sales
    .map((row) => ({ ...row, revenue: calculateRevenue(row) }))
    .filter((row) => region === "all" || row.region === region)
    .filter((row) => row.revenue >= minimumRevenue)
    .sort((a, b) => b[sortField] - a[sortField]);

  if (grouped) {
    const totals = rows.reduce((acc, row) => {
      acc[row.category] ||= { category: row.category, units: 0, revenue: 0 };
      acc[row.category].units += row.units;
      acc[row.category].revenue += row.revenue;
      return acc;
    }, {});
    rows = Object.values(totals).sort((a, b) => b.revenue - a.revenue);
  }

  return rows;
}

function renderData() {
  const rows = getFilteredData();
  const headers = grouped ? ["category", "units", "revenue"] : ["date", "region", "category", "units", "price", "revenue"];
  const region = document.querySelector("#region-filter").value;
  const minimumRevenue = document.querySelector("#revenue-filter").value;
  const sortField = document.querySelector("#sort-field").value;

  document.querySelector("#revenue-value").textContent = `$${minimumRevenue}`;
  document.querySelector("#pandas-code").textContent = grouped
    ? `df.query("revenue >= ${minimumRevenue}").groupby("category").agg({"units": "sum", "revenue": "sum"})`
    : `df${region === "all" ? "" : `.query("region == '${region}'")`}.query("revenue >= ${minimumRevenue}").sort_values("${sortField}", ascending=False)`;

  document.querySelector("#data-head").innerHTML = `<tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr>`;
  document.querySelector("#data-body").innerHTML = rows
    .map(
      (row) => `
      <tr>
        ${headers
          .map((header) => {
            const value = row[header];
            return `<td>${header === "price" || header === "revenue" ? `$${value}` : value}</td>`;
          })
          .join("")}
      </tr>
    `
    )
    .join("");
}

function renderProjects() {
  document.querySelector("#project-grid").innerHTML = projects
    .map(
      (project) => `
      <article class="project-card">
        <span class="badge">${project.level}</span>
        <h3>${project.title}</h3>
        <ul>${project.tasks.map((task) => `<li>${task}</li>`).join("")}</ul>
      </article>
    `
    )
    .join("");
}

document.querySelectorAll(".lesson-tab").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".lesson-tab").forEach((tab) => tab.classList.remove("active"));
    button.classList.add("active");
    renderLesson(button.dataset.level);
  });
});

document.querySelector("#quiz-options").addEventListener("click", (event) => {
  if (event.target.tagName !== "BUTTON") return;
  const selected = Number(event.target.dataset.answer);
  const item = questions[currentQuestion];
  document.querySelectorAll("#quiz-options button").forEach((button, index) => {
    button.disabled = true;
    button.classList.toggle("correct", index === item.answer);
  });
  if (selected === item.answer) {
    score += 1;
    document.querySelector("#quiz-score").textContent = `Score ${score}`;
    document.querySelector("#quiz-feedback").textContent = item.explanation;
  } else {
    event.target.classList.add("wrong");
    document.querySelector("#quiz-feedback").textContent = `Not quite. ${item.explanation}`;
  }
});

document.querySelector("#next-question").addEventListener("click", () => {
  currentQuestion = (currentQuestion + 1) % questions.length;
  renderQuiz();
});

document.querySelector("#group-category").addEventListener("click", () => {
  grouped = !grouped;
  document.querySelector("#group-category").textContent = grouped ? "Show rows" : "Group by category";
  renderData();
});

document.querySelector("#reset-data").addEventListener("click", () => {
  grouped = false;
  document.querySelector("#region-filter").value = "all";
  document.querySelector("#revenue-filter").value = "0";
  document.querySelector("#sort-field").value = "revenue";
  document.querySelector("#group-category").textContent = "Group by category";
  renderData();
});

["region-filter", "revenue-filter", "sort-field"].forEach((id) => {
  document.querySelector(`#${id}`).addEventListener("input", renderData);
});

const regionFilter = document.querySelector("#region-filter");
[...new Set(sales.map((row) => row.region))].sort().forEach((region) => {
  const option = document.createElement("option");
  option.value = region;
  option.textContent = region;
  regionFilter.appendChild(option);
});

renderLesson("beginner");
renderQuiz();
renderData();
renderProjects();
