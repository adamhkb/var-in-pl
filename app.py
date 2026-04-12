"""
EPL VAR Analysis Dashboard
A Streamlit web application for analyzing VAR decisions in the Premier League.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind, pearsonr, spearmanr

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="EPL VAR Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# LOAD DATA
# =============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv('data/var_decisions_all_seasons.csv')
    
    # Standardize team names
    name_mapping = {
        'AFC Bournemouth': 'Bournemouth',
        'Tottenham Hotspur': 'Tottenham',
        'Leicester City': 'Leicester',
        'Norwich City': 'Norwich',
        'Sheffield United': 'Sheffield Utd',
        'Sheff United': 'Sheffield Utd',
        'Nottm Forest': 'Nottingham Forest',
        'West Brom': 'West Bromwich Albion',
        'Brighton & Hove Albion': 'Brighton',
    }
    df['team_name'] = df['team_name'].replace(name_mapping)
    
    # Convert numeric columns
    df['net_score'] = pd.to_numeric(df['net_score'].astype(str).str.replace('+', ''), errors='coerce')
    df['net_goal_score'] = pd.to_numeric(df['net_goal_score'].astype(str).str.replace('+', ''), errors='coerce')
    df['net_subjective_score'] = pd.to_numeric(df['net_subjective_score'].astype(str).str.replace('+', ''), errors='coerce')
    
    # Big 6 classification
    big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester City', 'Manchester United', 'Tottenham']
    df['is_big_6'] = df['team_name'].isin(big_6)
    
    return df

df = load_data()

# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.title("⚽ EPL VAR Analysis")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Overview", "🏆 Team Analysis", "📈 Trends", "🔬 Statistical Tests"]
)

st.sidebar.markdown("---")

seasons = sorted(df['year'].unique())
selected_seasons = st.sidebar.multiselect(
    "Filter Seasons",
    options=seasons,
    default=seasons
)

show_big6_only = st.sidebar.checkbox("Show Big 6 Only", value=False)

filtered_df = df[df['year'].isin(selected_seasons)]
if show_big6_only:
    filtered_df = filtered_df[filtered_df['is_big_6']]

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source**: ESPN VAR Analysis")
st.sidebar.markdown("**Seasons**: 2019/20 - 2024/25")
st.sidebar.markdown("**Author**: [Adam Bahrin](https://github.com/adamhkb)")

# =============================================================================
# OVERVIEW PAGE
# =============================================================================
if page == "📊 Overview":
    st.title("📊 Premier League VAR Analysis Dashboard")
    st.markdown("Analyzing the impact of Video Assistant Referee (VAR) decisions across 6 seasons.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Team-Seasons", len(filtered_df))
    with col2:
        st.metric("Seasons Analyzed", len(selected_seasons))
    with col3:
        avg_overturns = filtered_df['overturns_total'].mean()
        st.metric("Avg Overturns/Team", f"{avg_overturns:.1f}")
    with col4:
        total_overturns = filtered_df['overturns_total'].sum()
        st.metric("Total VAR Overturns", total_overturns)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("VAR Net Score Distribution")
        fig = px.histogram(
            filtered_df, 
            x='net_score', 
            nbins=20,
            color='is_big_6',
            color_discrete_map={True: '#e74c3c', False: '#3498db'},
            labels={'net_score': 'Net VAR Score', 'is_big_6': 'Big 6'},
            title="Distribution of VAR Net Scores"
        )
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Top 10 VAR Beneficiaries (All Time)")
        team_totals = filtered_df.groupby('team_name')['net_score'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=team_totals.values,
            y=team_totals.index,
            orientation='h',
            color=team_totals.values,
            color_continuous_scale='RdYlGn',
            labels={'x': 'Total Net VAR Score', 'y': 'Team'}
        )
        fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("VAR Impact Heatmap by Season")
    pivot = filtered_df.pivot_table(values='net_score', index='team_name', columns='year', aggfunc='sum')
    pivot = pivot.dropna(how='all')
    
    fig = px.imshow(
        pivot,
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        labels=dict(x="Season", y="Team", color="Net Score"),
        aspect="auto"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, width='stretch')

# =============================================================================
# TEAM ANALYSIS PAGE
# =============================================================================
elif page == "🏆 Team Analysis":
    st.title("🏆 Team Analysis")
    
    teams = sorted(filtered_df['team_name'].unique())
    selected_team = st.selectbox("Select a Team", teams)
    
    team_df = filtered_df[filtered_df['team_name'] == selected_team]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_net = team_df['net_score'].sum()
        color = "normal" if total_net >= 0 else "inverse"
        st.metric("Total Net VAR Score", f"{total_net:+d}", delta_color=color)
    with col2:
        total_goals = team_df['net_goal_score'].sum()
        st.metric("Net Goals from VAR", f"{total_goals:+.0f}")
    with col3:
        total_overturns = team_df['overturns_total'].sum()
        st.metric("Total Overturns", total_overturns)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{selected_team} - VAR Score by Season")
        fig = px.bar(
            team_df,
            x='year',
            y='net_score',
            color='net_score',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            labels={'year': 'Season', 'net_score': 'Net VAR Score'}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader(f"{selected_team} - Decision Breakdown")
        decision_data = {
            'Category': ['Goals Awarded', 'Goals Disallowed For', 'Goals Disallowed Against', 'Penalties For', 'Penalties Against'],
            'Count': [
                team_df['leading_to_goals_for'].sum(),
                team_df['disallowed_goals_for'].sum(),
                team_df['disallowed_goals_against'].sum(),
                team_df['penalties_for'].sum(),
                team_df['penalties_against'].sum()
            ]
        }
        fig = px.bar(
            decision_data,
            x='Category',
            y='Count',
            color='Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    st.subheader(f"{selected_team} - Season by Season Data")
    display_cols = ['year', 'net_score', 'net_goal_score', 'overturns_total', 'leading_to_goals_for', 'disallowed_goals_for', 'disallowed_goals_against']
    st.dataframe(team_df[display_cols].sort_values('year'), width='stretch')

# =============================================================================
# TRENDS PAGE
# =============================================================================
elif page == "📈 Trends":
    st.title("📈 VAR Trends Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average VAR Overturns per Season")
        season_avg = filtered_df.groupby('year')['overturns_total'].mean().reset_index()
        fig = px.line(
            season_avg,
            x='year',
            y='overturns_total',
            markers=True,
            labels={'year': 'Season', 'overturns_total': 'Avg Overturns per Team'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Big 6 vs Other Clubs - Net Score")
        big6_avg = filtered_df.groupby(['year', 'is_big_6'])['net_score'].mean().reset_index()
        big6_avg['Group'] = big6_avg['is_big_6'].map({True: 'Big 6', False: 'Other Clubs'})
        fig = px.line(
            big6_avg,
            x='year',
            y='net_score',
            color='Group',
            markers=True,
            color_discrete_map={'Big 6': '#e74c3c', 'Other Clubs': '#3498db'},
            labels={'year': 'Season', 'net_score': 'Avg Net VAR Score'}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("Cumulative VAR Impact by Team")
    
    top_n = st.slider("Number of teams to show", 5, 20, 10)
    
    cumulative = filtered_df.sort_values('year').copy()
    cumulative['cumulative_score'] = cumulative.groupby('team_name')['net_score'].cumsum()
    
    final_scores = cumulative.groupby('team_name')['cumulative_score'].last().abs().nlargest(top_n).index
    cumulative_top = cumulative[cumulative['team_name'].isin(final_scores)]
    
    fig = px.line(
        cumulative_top,
        x='year',
        y='cumulative_score',
        color='team_name',
        markers=True,
        labels={'year': 'Season', 'cumulative_score': 'Cumulative Net Score', 'team_name': 'Team'}
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')

# =============================================================================
# STATISTICAL TESTS PAGE
# =============================================================================
elif page == "🔬 Statistical Tests":
    st.title("🔬 Statistical Analysis")
    
    st.subheader("1. Big 6 Bias Analysis")
    st.markdown("""
    **Research Question**: Do "Big 6" clubs receive favorable VAR treatment compared to other clubs?
    
    **Method**: Welch's t-test comparing mean net VAR scores
    """)
    
    big6_scores = filtered_df[filtered_df['is_big_6']]['net_score']
    other_scores = filtered_df[~filtered_df['is_big_6']]['net_score']
    
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
        x='is_big_6',
        y='net_score',
        color='is_big_6',
        color_discrete_map={True: '#e74c3c', False: '#3498db'},
        labels={'is_big_6': 'Club Type', 'net_score': 'Net VAR Score'}
    )
    fig.update_xaxes(ticktext=['Other Clubs', 'Big 6'], tickvals=[False, True])
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("2. Correlation Analysis")
    st.markdown("""
    **Research Question**: How do different VAR metrics correlate with each other?
    """)
    
    corr_cols = ['net_score', 'net_goal_score', 'overturns_total', 'leading_to_goals_for', 
                 'disallowed_goals_for', 'disallowed_goals_against', 'penalties_for', 'penalties_against']
    
    corr_matrix = filtered_df[corr_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        color_continuous_scale='RdBu_r',
        color_continuous_midpoint=0,
        labels=dict(color="Correlation")
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    st.subheader("3. Key Insights")
    
    most_benefited = filtered_df.groupby('team_name')['net_score'].sum().idxmax()
    most_benefited_score = filtered_df.groupby('team_name')['net_score'].sum().max()
    
    most_disadvantaged = filtered_df.groupby('team_name')['net_score'].sum().idxmin()
    most_disadvantaged_score = filtered_df.groupby('team_name')['net_score'].sum().min()
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**Most Benefited**: {most_benefited} ({most_benefited_score:+.0f})")
    with col2:
        st.error(f"**Most Disadvantaged**: {most_disadvantaged} ({most_disadvantaged_score:+.0f})")
    
    st.markdown("""
    ### Interpretation
    
    - **Net Score > 0**: Team benefited from VAR decisions overall
    - **Net Score < 0**: Team disadvantaged by VAR decisions overall
    - **Statistical significance (p < 0.05)**: Difference unlikely due to chance
    """)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Built with Streamlit | Data from ESPN | 
        <a href='https://github.com/adamhkb' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)
