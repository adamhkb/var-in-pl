import plotly.express as px
import streamlit as st

from charts import apply_plot_style, render_plot
from data import ESPN_SOURCES


def render_sources() -> None:
    st.markdown("#### Data Sources")
    for season, url in ESPN_SOURCES:
        st.markdown(f"- [{season} ESPN VAR Review]({url})")


def render_overview(filtered_df, selected_seasons) -> None:
    st.title("⚽ Premier League VAR Analysis Dashboard")
    st.caption("Professional analytics view of VAR outcomes across six EPL seasons.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Team-Seasons", len(filtered_df))
    with col2:
        st.metric("Seasons Analyzed", len(selected_seasons))
    with col3:
        avg_overturns = filtered_df["overturns_total"].mean()
        st.metric("Avg Overturns/Team", f"{avg_overturns:.1f}")
    with col4:
        total_overturns = int(filtered_df["overturns_total"].sum())
        st.metric("Total VAR Overturns", total_overturns)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("VAR Net Score Distribution")
        fig = px.histogram(
            filtered_df,
            x="net_score",
            nbins=20,
            color="is_big_6",
            color_discrete_map={True: "#e74c3c", False: "#3498db"},
            labels={"net_score": "Net VAR Score", "is_big_6": "Big 6"},
            title="Distribution of VAR Net Scores",
        )
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        apply_plot_style(fig, 400)
        render_plot(fig)

    with col2:
        st.subheader("Top 10 VAR Beneficiaries (All Time)")
        team_totals = filtered_df.groupby("team_name")["net_score"].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=team_totals.values,
            y=team_totals.index,
            orientation="h",
            color=team_totals.values,
            color_continuous_scale="RdYlGn",
            labels={"x": "Total Net VAR Score", "y": "Team"},
        )
        apply_plot_style(fig, 400)
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        render_plot(fig)

    st.markdown("---")

    st.subheader("VAR Impact Heatmap by Season")
    pivot = filtered_df.pivot_table(values="net_score", index="team_name", columns="year", aggfunc="sum").dropna(how="all")
    fig = px.imshow(
        pivot,
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        labels=dict(x="Season", y="Team", color="Net Score"),
        aspect="auto",
    )
    apply_plot_style(fig, 600)
    render_plot(fig)
    with st.expander("ESPN source links used for this dashboard", expanded=False):
        render_sources()

