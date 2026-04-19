import plotly.express as px
import streamlit as st

from charts import apply_plot_style, render_plot


def render_trends(filtered_df) -> None:
    st.title("📈 VAR Trends Over Time")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average VAR Overturns per Season")
        season_avg = filtered_df.groupby("year")["overturns_total"].mean().reset_index()
        fig = px.line(
            season_avg,
            x="year",
            y="overturns_total",
            markers=True,
            labels={"year": "Season", "overturns_total": "Avg Overturns per Team"},
        )
        apply_plot_style(fig, 400)
        render_plot(fig)

    with col2:
        st.subheader("Big 6 vs Other Clubs - Net Score")
        big6_avg = filtered_df.groupby(["year", "is_big_6"])["net_score"].mean().reset_index()
        big6_avg["Group"] = big6_avg["is_big_6"].map({True: "Big 6", False: "Other Clubs"})
        fig = px.line(
            big6_avg,
            x="year",
            y="net_score",
            color="Group",
            markers=True,
            color_discrete_map={"Big 6": "#e74c3c", "Other Clubs": "#3498db"},
            labels={"year": "Season", "net_score": "Avg Net VAR Score"},
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        apply_plot_style(fig, 400)
        render_plot(fig)

    st.markdown("---")

    st.subheader("Cumulative VAR Impact by Team")
    top_n = st.slider("Number of teams to show", 5, 20, 10)

    cumulative = filtered_df.sort_values("year").copy()
    cumulative["cumulative_score"] = cumulative.groupby("team_name")["net_score"].cumsum()

    final_scores = cumulative.groupby("team_name")["cumulative_score"].last().abs().nlargest(top_n).index
    cumulative_top = cumulative[cumulative["team_name"].isin(final_scores)]

    fig = px.line(
        cumulative_top,
        x="year",
        y="cumulative_score",
        color="team_name",
        markers=True,
        labels={"year": "Season", "cumulative_score": "Cumulative Net Score", "team_name": "Team"},
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    apply_plot_style(fig, 500)
    render_plot(fig)

