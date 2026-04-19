import streamlit as st

PLOT_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"l": 20, "r": 20, "t": 56, "b": 20},
}


def apply_plot_style(fig, height: int):
    fig.update_layout(height=height, **PLOT_LAYOUT)
    return fig


def render_plot(fig) -> None:
    # Let Streamlit theme Plotly based on the user's selected theme.
    st.plotly_chart(fig, width="stretch")

