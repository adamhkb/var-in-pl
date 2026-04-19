import plotly.express as px
import streamlit as st

from charts import apply_plot_style, render_plot


def render_team_analysis(filtered_df) -> None:
    st.title("🏆 Team Analysis")

    teams = sorted(filtered_df["team_name"].unique())
    selected_team = st.selectbox("Select a Team", teams)

    team_df = filtered_df[filtered_df["team_name"] == selected_team]

    col1, col2, col3 = st.columns(3)
    with col1:
        total_net = int(team_df["net_score"].sum())
        color = "normal" if total_net >= 0 else "inverse"
        st.metric("Total Net VAR Score", f"{total_net:+d}", delta_color=color)
    with col2:
        total_goals = team_df["net_goal_score"].sum()
        st.metric("Net Goals from VAR", f"{total_goals:+.0f}")
    with col3:
        total_overturns = int(team_df["overturns_total"].sum())
        st.metric("Total Overturns", total_overturns)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{selected_team} - VAR Score by Season")
        fig = px.bar(
            team_df,
            x="year",
            y="net_score",
            color="net_score",
            color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
            labels={"year": "Season", "net_score": "Net VAR Score"},
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        apply_plot_style(fig, 400)
        fig.update_layout(showlegend=False)
        render_plot(fig)

    with col2:
        st.subheader(f"{selected_team} - Decision Breakdown")
        decision_data = {
            "Category": [
                "Goals Awarded",
                "Goals Disallowed For",
                "Goals Disallowed Against",
                "Penalties For",
                "Penalties Against",
            ],
            "Count": [
                team_df["leading_to_goals_for"].sum(),
                team_df["disallowed_goals_for"].sum(),
                team_df["disallowed_goals_against"].sum(),
                team_df["penalties_for"].sum(),
                team_df["penalties_against"].sum(),
            ],
        }
        fig = px.bar(decision_data, x="Category", y="Count", color="Count", color_continuous_scale="Blues")
        apply_plot_style(fig, 400)
        fig.update_layout(showlegend=False)
        render_plot(fig)

    st.subheader(f"{selected_team} - Season by Season Data")
    display_cols = [
        "year",
        "net_score",
        "net_goal_score",
        "overturns_total",
        "leading_to_goals_for",
        "disallowed_goals_for",
        "disallowed_goals_against",
    ]
    st.dataframe(team_df[display_cols].sort_values("year"), width="stretch")

