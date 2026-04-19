import streamlit as st

from data import ESPN_SOURCES, NOTEBOOK_LINKS


def render_about() -> None:
    st.title("ℹ️ About & Methodology")

    st.subheader("Data Collection (Web Scraping)")
    st.markdown(
        """
        This dashboard is built from ESPN's season-by-season VAR review articles.
        The underlying tables are rendered dynamically in the browser, so the data
        was collected via **web scraping** using **Selenium** (to render the page)
        and **BeautifulSoup** (to parse the HTML into structured rows).

        The cleaned results are stored in `data/var_decisions_all_seasons.csv` and
        loaded by the Streamlit app.
        """
    )

    st.subheader("Definitions")
    st.markdown(
        """
        - `net_score`: overall VAR impact per team-season (positive means net benefit).
        - `net_goal_score`: net goals gained/lost from VAR decisions.
        - `overturns_total`: count of VAR reviews involving the team.
        """
    )

    st.subheader("Caveats")
    st.markdown(
        """
        - Metrics reflect ESPN's published summaries and categorization.
        - Correlation does not imply causation; treat results as descriptive.
        - Season coverage currently spans **2019/20 through 2024/25**.
        """
    )

    st.subheader("Sources (ESPN)")
    for season, url in ESPN_SOURCES:
        st.markdown(f"- [{season} ESPN VAR Review]({url})")

    st.subheader("Project Notebooks")
    st.markdown(
        """
        These notebooks show the end-to-end work behind the dashboard (scraping, cleaning, analysis, and validation):
        """
    )
    for title, url, blurb in NOTEBOOK_LINKS:
        st.markdown(f"- [{title}]({url}): {blurb}")
