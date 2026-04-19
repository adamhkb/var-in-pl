import plotly.express as px
import streamlit as st
from scipy.stats import ttest_ind

from charts import apply_plot_style, render_plot


def render_statistical_tests(filtered_df) -> None:
    st.title("🔬 Statistical Analysis")

    st.subheader("1. Big 6 Bias Analysis")
    st.markdown(
        """
        **Research Question**: Do "Big 6" clubs receive favorable VAR treatment compared to other clubs?

        **Method**: Welch's t-test comparing mean net VAR scores
        """
    )

    big6_scores = filtered_df[filtered_df["is_big_6"]]["net_score"]
    other_scores = filtered_df[~filtered_df["is_big_6"]]["net_score"]

    t_stat, p_value = ttest_ind(big6_scores, other_scores, equal_var=False)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Big 6 Mean", f"{big6_scores.mean():.2f}")
    with col2:
        st.metric("Other Clubs Mean", f"{other_scores.mean():.2f}")
    with col3:
        significance = "✅ Significant" if p_value < 0.05 else "❌ Not Significant"
        st.metric("P-value", f"{p_value:.4f}", delta=significance)

    fig = px.box(
        filtered_df,
        x="is_big_6",
        y="net_score",
        color="is_big_6",
        color_discrete_map={True: "#e74c3c", False: "#3498db"},
        labels={"is_big_6": "Club Type", "net_score": "Net VAR Score"},
    )
    fig.update_xaxes(ticktext=["Other Clubs", "Big 6"], tickvals=[False, True])
    apply_plot_style(fig, 400)
    fig.update_layout(showlegend=False)
    render_plot(fig)

    st.markdown("---")

    st.subheader("2. Correlation Analysis")
    st.markdown(
        """
        **Research Question**: How do different VAR metrics correlate with each other?
        """
    )

    corr_cols = [
        "net_score",
        "net_goal_score",
        "overturns_total",
        "leading_to_goals_for",
        "disallowed_goals_for",
        "disallowed_goals_against",
        "penalties_for",
        "penalties_against",
    ]
    corr_matrix = filtered_df[corr_cols].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        color_continuous_midpoint=0,
        labels=dict(color="Correlation"),
    )
    apply_plot_style(fig, 600)
    render_plot(fig)

    st.markdown("---")

    st.subheader("3. Key Insights")

    totals = filtered_df.groupby("team_name")["net_score"].sum()
    most_benefited = totals.idxmax()
    most_benefited_score = totals.max()
    most_disadvantaged = totals.idxmin()
    most_disadvantaged_score = totals.min()

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**Most Benefited**: {most_benefited} ({most_benefited_score:+.0f})")
    with col2:
        st.error(f"**Most Disadvantaged**: {most_disadvantaged} ({most_disadvantaged_score:+.0f})")

    st.markdown(
        """
        ### Interpretation

        - **Net Score > 0**: Team benefited from VAR decisions overall
        - **Net Score < 0**: Team disadvantaged by VAR decisions overall
        - **Statistical significance (p < 0.05)**: Difference unlikely due to chance
        """
    )

