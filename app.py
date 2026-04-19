import streamlit as st

from data import ESPN_SOURCES, load_data
from pages.about import render_about
from pages.overview import render_overview
from pages.statistical_tests import render_statistical_tests
from pages.team_analysis import render_team_analysis
from pages.trends import render_trends
from ui.theme import inject_theme_css


st.set_page_config(
    page_title="EPL VAR Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme_css()

df = load_data()

st.sidebar.title("⚽ EPL VAR Analysis")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "🏆 Team Analysis", "📈 Trends", "🔬 Statistical Tests", "ℹ️ About"],
)

st.sidebar.markdown("---")

seasons = sorted(df["year"].unique())
selected_seasons = st.sidebar.multiselect("Filter Seasons", options=seasons, default=seasons)
show_big6_only = st.sidebar.checkbox("Show Big 6 Only", value=False)

filtered_df = df[df["year"].isin(selected_seasons)]
if show_big6_only:
    filtered_df = filtered_df[filtered_df["is_big_6"]]

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source**: ESPN VAR Analysis")
st.sidebar.markdown("**Seasons**: 2019/20 - 2024/25")
st.sidebar.markdown("**Author**: [Adam Bahrin](https://github.com/adamhkb)")
with st.sidebar.expander("View ESPN source links", expanded=False):
    for season, url in ESPN_SOURCES:
        st.markdown(f"- [{season}]({url})")


if page == "📊 Overview":
    render_overview(filtered_df, selected_seasons)
elif page == "🏆 Team Analysis":
    render_team_analysis(filtered_df)
elif page == "📈 Trends":
    render_trends(filtered_df)
elif page == "🔬 Statistical Tests":
    render_statistical_tests(filtered_df)
elif page == "ℹ️ About":
    render_about()

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Built with Streamlit | Data from ESPN |
        <a href='https://github.com/adamhkb' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)

