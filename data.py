import pandas as pd
import streamlit as st


ESPN_SOURCES = [
    ("2019/2020", "https://www.espn.com/soccer/story/_/id/37575919/how-var-decisions-affected-every-premier-league-club"),
    ("2020/2021", "https://www.espn.co.uk/football/story/_/id/37587139/how-var-decisions-affected-every-premier-league-club-2020-21"),
    ("2021/2022", "https://www.espn.co.uk/football/story/_/id/37619801/how-var-decisions-affected-every-premier-league-club-2021-22"),
    ("2022/2023", "https://www.espn.co.uk/football/story/_/id/37631044/how-var-decisions-affected-every-premier-league-club-2022-23"),
    ("2023/2024", "https://www.espn.com/soccer/story/_/id/38196464/how-var-decisions-affect-premier-league-club-2023-24"),
    ("2024/2025", "https://www.espn.co.uk/football/story/_/id/40894476/how-var-decisions-affect-premier-league-club-2024-25"),
]

NOTEBOOK_LINKS = [
    (
        "Data Acquisition (Scraping + Cleaning)",
        "https://github.com/adamhkb/var-in-pl/blob/main/VAR_Analysis_Data_Acquisition.ipynb",
        "Selenium scraping, parsing, normalization, and CSV export.",
    ),
    (
        "Team Impact Analysis",
        "https://github.com/adamhkb/var-in-pl/blob/main/VAR_Analysis_Team_Impact.ipynb",
        "Team-level VAR impact summaries and comparative analysis.",
    ),
    (
        "League Correlation Analysis",
        "https://github.com/adamhkb/var-in-pl/blob/main/VAR_Analysis_League_Correlation.ipynb",
        "Correlation work exploring relationships between VAR metrics and performance.",
    ),
]


@st.cache_data
def load_data(csv_path: str = "data/var_decisions_all_seasons.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Standardize team names
    name_mapping = {
        "AFC Bournemouth": "Bournemouth",
        "Tottenham Hotspur": "Tottenham",
        "Leicester City": "Leicester",
        "Norwich City": "Norwich",
        "Sheffield United": "Sheffield Utd",
        "Sheff United": "Sheffield Utd",
        "Nottm Forest": "Nottingham Forest",
        "West Brom": "West Bromwich Albion",
        "Brighton & Hove Albion": "Brighton",
    }
    df["team_name"] = df["team_name"].replace(name_mapping)

    # Convert numeric columns
    df["net_score"] = pd.to_numeric(df["net_score"].astype(str).str.replace("+", ""), errors="coerce")
    df["net_goal_score"] = pd.to_numeric(df["net_goal_score"].astype(str).str.replace("+", ""), errors="coerce")
    df["net_subjective_score"] = pd.to_numeric(df["net_subjective_score"].astype(str).str.replace("+", ""), errors="coerce")

    # Big 6 classification
    big_6 = ["Arsenal", "Chelsea", "Liverpool", "Manchester City", "Manchester United", "Tottenham"]
    df["is_big_6"] = df["team_name"].isin(big_6)

    return df
