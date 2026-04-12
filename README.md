# EPL VAR Analysis

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end data pipeline and interactive dashboard analyzing VAR (Video Assistant Referee) decisions in the English Premier League across 6 seasons.

**Live Demo**: [Coming Soon]

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technical Architecture](#technical-architecture)
- [Data Pipeline](#data-pipeline)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Statistical Methods](#statistical-methods)
- [Challenges & Solutions](#challenges--solutions)
- [How to Run](#how-to-run)
- [Future Improvements](#future-improvements)

---

## Project Overview

### The Problem

VAR was introduced to the Premier League in 2019/20 to reduce refereeing errors. However, fans and analysts have raised questions about its consistency and potential bias toward certain clubs.

### The Solution

I built a **full-stack data project** that:

1. **Scrapes** VAR decision data from ESPN (120+ team-season records)
2. **Analyzes** patterns using statistical methods
3. **Visualizes** insights through an interactive web dashboard

### Research Questions

| Question | Method | Finding |
|----------|--------|---------|
| Do "Big 6" clubs receive favorable treatment? | Welch's t-test | See dashboard |
| Which teams benefit/suffer most from VAR? | Aggregation & ranking | Brighton historically benefits most |
| Has VAR consistency improved over time? | Time series analysis | Variable by season |

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐     ┌─────────────┐     ┌─────────────┐          │
│   │  ESPN   │────▶│  Selenium   │────▶│   Pandas    │          │
│   │ Website │     │  Scraper    │     │  DataFrame  │          │
│   └─────────┘     └─────────────┘     └──────┬──────┘          │
│                                              │                  │
│                                              ▼                  │
│                                       ┌─────────────┐          │
│                                       │  CSV Files  │          │
│                                       └──────┬──────┘          │
│                                              │                  │
├──────────────────────────────────────────────┼──────────────────┤
│                        ANALYSIS              │                  │
│                                              ▼                  │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│   │   Scipy    │     │   Pandas    │     │   Plotly    │      │
│   │   Stats    │◀───▶│  Analysis   │────▶│   Charts    │      │
│   └─────────────┘     └─────────────┘     └──────┬──────┘      │
│                                                  │              │
├──────────────────────────────────────────────────┼──────────────┤
│                        WEB APP                   │              │
│                                                  ▼              │
│                                           ┌─────────────┐      │
│                                           │  Streamlit  │      │
│                                           │  Dashboard  │      │
│                                           └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Pipeline

### 1. Data Acquisition (`VAR_Analysis_Data_Acquisition.ipynb`)

```python
# Web scraping with Selenium (dynamic JavaScript content)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(espn_url)

# Wait for dynamic content to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Table"))
)

# Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
```

**Why Selenium over Requests?**
- ESPN uses JavaScript to render tables dynamically
- Static HTTP requests only return empty page shells
- Selenium renders the full DOM before scraping

### 2. Data Transformation

```python
# Standardize team names (handle inconsistencies across seasons)
name_mapping = {
    'AFC Bournemouth': 'Bournemouth',
    'Tottenham Hotspur': 'Tottenham',
    'Sheffield United': 'Sheffield Utd',
    'Sheff United': 'Sheffield Utd',
    # ... more mappings
}
df['team_name'] = df['team_name'].replace(name_mapping)
```

### 3. Data Schema

| Column | Type | Description |
|--------|------|-------------|
| `team_name` | string | Standardized club name |
| `net_score` | int | Overall VAR impact (+ve = benefited) |
| `net_goal_score` | int | Net goals gained/lost from VAR |
| `overturns_total` | int | Total VAR reviews involving team |
| `is_big_6` | bool | Arsenal, Chelsea, Liverpool, Man City, Man Utd, Tottenham |
| `year` | string | Season (e.g., "2023/2024") |

---

## Tech Stack

| Layer | Technology | Why I Chose It |
|-------|------------|----------------|
| **Scraping** | Selenium + BeautifulSoup | Dynamic JS content + clean parsing |
| **Data Processing** | Pandas, NumPy | Industry standard, efficient for tabular data |
| **Statistics** | SciPy | Robust statistical tests (t-test, correlation) |
| **Visualization** | Plotly | Interactive charts, animation support |
| **Web App** | Streamlit | Rapid prototyping, Python-native, free hosting |
| **Deployment** | Streamlit Cloud | Zero-config deployment, GitHub integration |

---

## Key Features

### 1. Interactive Dashboard

- **Filters**: Season selection, Big 6 toggle
- **4 Pages**: Overview, Team Analysis, Trends, Statistical Tests
- **Real-time**: All charts update based on filter selections

### 2. Team Deep-Dive

- Select any team to see their VAR history
- Season-by-season breakdown
- Decision type analysis (goals awarded, disallowed, penalties)

### 3. Statistical Analysis

- **Welch's t-test**: Compares Big 6 vs other clubs (handles unequal variances)
- **Correlation matrix**: Relationships between VAR metrics
- **P-value reporting**: Statistical significance clearly indicated

---

## Statistical Methods

### Big 6 Bias Test

```python
from scipy.stats import ttest_ind

# Welch's t-test (unequal variance assumption)
t_stat, p_value = ttest_ind(
    big6_scores, 
    other_scores, 
    equal_var=False  # Welch's correction
)

# Interpretation
if p_value < 0.05:
    print("Statistically significant difference")
```

**Why Welch's t-test?**
- Big 6 (6 teams) vs Others (14+ teams) = unequal sample sizes
- Variance likely differs between groups
- More robust than Student's t-test for this scenario

### Correlation Analysis

```python
from scipy.stats import pearsonr, spearmanr

# Pearson: Linear relationship (assumes normality)
r, p = pearsonr(var_score, league_points)

# Spearman: Monotonic relationship (rank-based, no normality assumption)
rho, p = spearmanr(var_score, league_position)
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| ESPN uses dynamic JavaScript rendering | Used Selenium WebDriver instead of Requests |
| Team names inconsistent across seasons | Created name mapping dictionary for standardization |
| Large dataset causing slow scraping | Implemented parallel scraping with ThreadPoolExecutor |
| Streamlit deprecation warnings | Updated to new API (`width='stretch'` vs `use_container_width`) |

---

## How to Run

### Local Development

```bash
# Clone repository
git clone https://github.com/adamhkb/epl-var-analysis.git
cd epl-var-analysis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → Set `app.py` as main file → Deploy

---

## Project Structure

```
epl-var-analysis/
├── app.py                                # Streamlit web application
├── VAR_Analysis_Data_Acquisition.ipynb   # Data scraping pipeline
├── VAR_Analysis_Team_Impact.ipynb        # Team-level analysis
├── VAR_Analysis_League_Correlation.ipynb # Performance correlation
├── data/
│   └── var_decisions_all_seasons.csv     # Processed dataset
├── images/                               # Generated visualizations
├── requirements.txt                      # Python dependencies
├── LICENSE                               # MIT License
└── README.md                             # This file
```

---

## Future Improvements

- [ ] **Automate data refresh** - GitHub Actions to re-scrape weekly
- [ ] **Add match-level data** - Individual VAR incidents, not just aggregates
- [ ] **ML predictions** - Predict likelihood of VAR overturn based on match context
- [ ] **API endpoint** - FastAPI backend for programmatic access
- [ ] **Expand leagues** - La Liga, Bundesliga, Serie A comparison

---

## Skills Demonstrated

- **Data Engineering**: Web scraping, ETL pipeline, data cleaning
- **Data Analysis**: Statistical testing, correlation analysis
- **Data Visualization**: Interactive dashboards, meaningful charts
- **Software Engineering**: Clean code, modular design, documentation
- **DevOps**: Deployment, dependency management

---

## Author

**Adam Bahrin** - [GitHub](https://github.com/adamhkb)

---

## License

MIT License - see [LICENSE](LICENSE) for details.
