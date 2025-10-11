import httpx
import pandas as pd
import plotly.express as px
import streamlit as st

API_URL = "http://localhost:8000/builds?week=Y2025m10d05&relevance=top_n&relevance_threshold=100&sort_by=moveset_item_win_rate"

st.title("Pokémon Unite Meta Dashboard")
st.set_page_config(layout="wide")

response = httpx.get(API_URL)
if response.status_code == 200:
    data = pd.DataFrame(response.json())
    data = data.drop(columns=["id", "week"])

    cols = data.columns.tolist()
    cols.insert(0, cols.pop(cols.index("popularity")))
    cols.insert(0, cols.pop(cols.index("rank")))
    data = data[cols]

    # Rename columns for better readability
    data = data.rename(
        columns={
            "popularity": "popularity rank",
            "moveset_item_win_rate": "build win rate",
            "pokemon_win_rate": "pokemon win rate",
            "pokemon_pick_rate": "pokemon pick rate",
            "move_1": "move 1",
            "move_2": "move 2",
            "moveset_win_rate": "moveset win rate",
            "moveset_pick_rate": "moveset pick rate",
            "moveset_true_pick_rate": "moveset true pick rate",
            "moveset_item_pick_rate": "build pick rate",
            "moveset_item_true_pick_rate": "build true pick rate",
        }
    )

    st.dataframe(data, hide_index=True)
else:
    st.error("Failed to load data")

# Interactive visualization
if not data.empty:
    st.subheader("Interactive Visualization")

    # Create two columns for the dropdowns
    col1, col2 = st.columns(2)

    with col1:
        x_axis = st.selectbox(
            "Select X-axis",
            options=data.columns.tolist(),
            index=data.columns.tolist().index("rank"),
        )

    with col2:
        y_axis = st.selectbox(
            "Select Y-axis",
            options=data.columns.tolist(),
            index=data.columns.tolist().index("build win rate"),
        )

    # Create the scatter plot with selected axes
    fig = px.scatter(
        data,
        x=x_axis,
        y=y_axis,
        title=f"{x_axis} vs {y_axis}",
        hover_data=["pokemon", "rank"],
    )

    # Rotate x-axis labels if x-axis is categorical (e.g., pokemon names)
    if x_axis in ("pokemon", "move 1", "move 2", "item"):
        fig.update_xaxes(tickangle=-90)

    st.plotly_chart(fig, use_container_width=True)
