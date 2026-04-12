# EPL VAR Analysis

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Analyzing the impact of VAR (Video Assistant Referee) decisions in the English Premier League across 6 seasons (2019/20 - 2024/25).

## Overview

This project scrapes VAR decision data from ESPN and performs statistical analysis to answer questions like:

- Do "Big 6" clubs receive favorable VAR treatment?
- How does VAR impact correlate with league performance?
- Which teams benefit or suffer most from VAR decisions?

## Project Structure

```
epl-var-analysis/
├── VAR_Analysis_Data_Acquisition.ipynb   # Data scraping
├── VAR_Analysis_Team_Impact.ipynb        # Team-level analysis
├── VAR_Analysis_League_Correlation.ipynb # Performance correlation
├── data/                                 # Generated datasets
├── images/                               # Visualizations
├── requirements.txt
└── README.md
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/adamhkb/epl-var-analysis.git
cd epl-var-analysis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run notebooks in VS Code or Jupyter
```

## Notebooks

| Notebook | Description |
|----------|-------------|
| `VAR_Analysis_Data_Acquisition` | Scrapes VAR data from ESPN using Selenium |
| `VAR_Analysis_Team_Impact` | Statistical analysis of VAR impact by team |
| `VAR_Analysis_League_Correlation` | Correlation between VAR and league standings |

## Key Findings

- Analysis of 120+ team-seasons of VAR data
- Statistical tests for Big 6 bias (Welch's t-test)
- Correlation analysis between VAR net score and final points

## Data Sources

- **VAR Statistics**: [ESPN Premier League VAR Analysis](https://www.espn.com/soccer/story/_/id/29699702/premier-league-var-check-every-call-made-season)
- **League Standings**: Official Premier League records

## Requirements

- Python 3.11+
- Chrome browser (for Selenium scraping)
- See `requirements.txt` for full dependencies

