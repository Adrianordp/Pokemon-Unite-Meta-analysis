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

# Example: visualize two columns
if not data.empty:
    # X-axis: rank
    fig = px.scatter(
        data,
        x="rank",
        y="pokemon win rate",
        title="Rank vs Pokémon Win Rate",
    )
    st.plotly_chart(fig, config={"scrollable": False})

    fig = px.scatter(
        data,
        x="rank",
        y="pokemon pick rate",
        title="Rank vs Pokémon Pick Rate",
    )
    st.plotly_chart(fig, config={"scrollable": False})

    fig = px.scatter(
        data,
        x="rank",
        y="build win rate",
        title="Rank vs Build Win Rate",
    )
    st.plotly_chart(fig, config={"scrollable": False})

    fig = px.scatter(
        data,
        x="rank",
        y="build pick rate",
        title="Rank vs Build Pick Rate",
    )
    st.plotly_chart(fig, config={"scrollable": False})

    # X-axis: pokemon

    fig = px.scatter(
        data,
        x="pokemon",
        y="pokemon win rate",
        title="Pokémon vs Pokémon Win Rate",
    )
    st.plotly_chart(fig, config={"scrollable": False})

    fig = px.scatter(
        data,
        x="pokemon",
        y="pokemon pick rate",
        title="Pokémon vs Pokémon Pick Rate",
    )
    fig.update_xaxes(tickangle=-90)
    st.plotly_chart(fig, config={"scrollable": False})

    fig = px.scatter(
        data,
        x="pokemon",
        y="build win rate",
        title="Pokémon vs Build Win Rate",
    )
    st.plotly_chart(fig, config={"scrollable": False})

    fig = px.scatter(
        data,
        x="pokemon",
        y="build pick rate",
        title="Pokémon vs Build Pick Rate",
    )
    fig.update_xaxes(tickangle=-90)
    st.plotly_chart(fig, config={"scrollable": False})
