import streamlit as st


def inject_theme_css() -> None:
    st.markdown(
        """
        <style>
        html[data-theme="light"] .stApp {
            background: radial-gradient(circle at top left, #eef6ff 0%, #f7fafc 40%, #ffffff 100%);
        }
        html[data-theme="dark"] .stApp {
            background: radial-gradient(circle at top left, #111827 0%, #0f172a 45%, #020617 100%);
        }

        html[data-theme="light"] [data-testid="stAppViewContainer"] { color: #0f172a !important; }
        html[data-theme="dark"] [data-testid="stAppViewContainer"] { color: #e2e8f0 !important; }

        [data-testid="stAppViewContainer"] .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container p,
        [data-testid="stAppViewContainer"] .main .block-container span,
        [data-testid="stAppViewContainer"] .main .block-container li,
        [data-testid="stAppViewContainer"] .main .block-container label,
        [data-testid="stAppViewContainer"] .main .block-container h1,
        [data-testid="stAppViewContainer"] .main .block-container h2,
        [data-testid="stAppViewContainer"] .main .block-container h3,
        [data-testid="stAppViewContainer"] .main .block-container h4 {
            color: inherit !important;
        }
        html[data-theme="light"] div[data-testid="stMetricValue"] { color: #0a2540; font-weight: 700; }
        html[data-theme="dark"] div[data-testid="stMetricValue"] { color: #f8fafc; font-weight: 700; }
        html[data-theme="light"] div[data-testid="stMetricLabel"] { color: #334155 !important; }
        html[data-theme="dark"] div[data-testid="stMetricLabel"] { color: #94a3b8 !important; }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

