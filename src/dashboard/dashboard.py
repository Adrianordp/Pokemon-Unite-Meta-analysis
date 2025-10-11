import httpx
import pandas as pd
import plotly.express as px
import streamlit as st

# API Base URL
API_BASE = "http://localhost:8000"

# Role color mapping (similar to CLI but using hex colors for CSS)
ROLE_COLORS = {
    "Support": "#ff9800",  # Orange (ANSI 214)
    "Attacker": "#d32f2f",  # Red (ANSI 1)
    "Speedster": "#1976d2",  # Blue (ANSI 4)
    "Defender": "#388e3c",  # Green (ANSI 2)
    "All-Rounder": "#7b1fa2",  # Purple (ANSI 93)
}

st.set_page_config(layout="wide", page_title="Pokémon Unite Meta Dashboard")
st.title("Pokémon Unite Meta Dashboard")


def colorize_by_role(row):
    """
    Apply role-based coloring to DataFrame rows.
    Returns a list of CSS styles for each cell in the row.
    """
    role = row.get("role", "")
    color = ROLE_COLORS.get(
        role, "#000000"
    )  # Default to black if role not found
    return [f"color: {color}" for _ in row]


# Fetch metadata from API
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_metadata():
    """Fetch all metadata from the API"""
    try:
        weeks = httpx.get(f"{API_BASE}/weeks").json()
        pokemon = httpx.get(f"{API_BASE}/pokemon").json()
        roles = httpx.get(f"{API_BASE}/roles").json()
        items = httpx.get(f"{API_BASE}/items").json()
        relevance = httpx.get(f"{API_BASE}/relevance").json()
        sort_by = httpx.get(f"{API_BASE}/sort_by").json()
        return {
            "weeks": weeks,
            "pokemon": pokemon,
            "roles": roles,
            "items": items,
            "relevance": relevance,
            "sort_by": sort_by,
        }
    except Exception as e:
        st.error(f"Failed to fetch metadata from API: {e}")
        return None


metadata = fetch_metadata()

if metadata is None:
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Week selection
selected_week = st.sidebar.selectbox(
    "Week",
    options=metadata["weeks"],
    index=0 if metadata["weeks"] else None,
    help="Select the week to analyze",
)

# Relevance strategy
relevance_options = {r["name"]: r["description"] for r in metadata["relevance"]}
selected_relevance = st.sidebar.selectbox(
    "Relevance Strategy",
    options=list(relevance_options.keys()),
    index=list(relevance_options.keys()).index("top_n")
    if "top_n" in relevance_options
    else 0,
    help="Strategy for filtering relevant builds",
)

# Relevance threshold
relevance_threshold = st.sidebar.number_input(
    "Relevance Threshold",
    min_value=0.0,
    max_value=1000.0,
    value=100.0,
    step=1.0,
    help="Threshold value for the selected relevance strategy",
)

# Sort by
sort_options = {s["name"]: s["description"] for s in metadata["sort_by"]}
selected_sort_by = st.sidebar.selectbox(
    "Sort By",
    options=list(sort_options.keys()),
    index=list(sort_options.keys()).index("moveset_item_win_rate")
    if "moveset_item_win_rate" in sort_options
    else 0,
    help="Field to sort builds by",
)

# Sort order
selected_sort_order = st.sidebar.radio(
    "Sort Order",
    options=["desc", "asc"],
    index=0,
    help="Ascending or descending order",
)

# Pokemon filter
st.sidebar.subheader("Pokémon Filter")
pokemon_filter_type = st.sidebar.radio(
    "Filter Type",
    options=["None", "Include", "Exclude"],
    index=0,
    key="pokemon_filter_type",
)

selected_pokemon = None
ignore_pokemon = None

if pokemon_filter_type == "Include":
    selected_pokemon = st.sidebar.multiselect(
        "Select Pokémon to include",
        options=metadata["pokemon"],
        help="Include only these Pokémon",
    )
elif pokemon_filter_type == "Exclude":
    ignore_pokemon = st.sidebar.multiselect(
        "Select Pokémon to exclude",
        options=metadata["pokemon"],
        help="Exclude these Pokémon",
    )

# Role filter
st.sidebar.subheader("Role Filter")
role_filter_type = st.sidebar.radio(
    "Filter Type",
    options=["None", "Include", "Exclude"],
    index=0,
    key="role_filter_type",
)

selected_role = None
ignore_role = None

if role_filter_type == "Include":
    selected_role = st.sidebar.multiselect(
        "Select Roles to include",
        options=metadata["roles"],
        help="Include only these roles",
    )
elif role_filter_type == "Exclude":
    ignore_role = st.sidebar.multiselect(
        "Select Roles to exclude",
        options=metadata["roles"],
        help="Exclude these roles",
    )

# Item filter
st.sidebar.subheader("Item Filter")
item_filter_type = st.sidebar.radio(
    "Filter Type",
    options=["None", "Include", "Exclude"],
    index=0,
    key="item_filter_type",
)

selected_item = None
ignore_item = None

if item_filter_type == "Include":
    selected_item = st.sidebar.multiselect(
        "Select Items to include",
        options=metadata["items"],
        help="Include only these items",
    )
elif item_filter_type == "Exclude":
    ignore_item = st.sidebar.multiselect(
        "Select Items to exclude",
        options=metadata["items"],
        help="Exclude these items",
    )

# Build API URL dynamically
params = {
    "week": selected_week,
    "relevance": selected_relevance,
    "relevance_threshold": relevance_threshold,
    "sort_by": selected_sort_by,
    "sort_order": selected_sort_order,
}

# Add filters if selected
if selected_pokemon:
    params["pokemon"] = ",".join(selected_pokemon)
elif ignore_pokemon:
    params["ignore_pokemon"] = ",".join(ignore_pokemon)

if selected_role:
    params["role"] = ",".join(selected_role)
elif ignore_role:
    params["ignore_role"] = ",".join(ignore_role)

if selected_item:
    params["item"] = ",".join(selected_item)
elif ignore_item:
    params["ignore_item"] = ",".join(ignore_item)

# Build query string
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
API_URL = f"{API_BASE}/builds?{query_string}"

# Display the API URL for debugging
with st.expander("API Request URL"):
    st.code(API_URL)

# Fetch data
response = httpx.get(API_URL)
if response.status_code == 200:
    data = pd.DataFrame(response.json())

    if data.empty:
        st.warning("No builds found matching the selected filters.")
        st.stop()

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

    st.subheader(f"Builds ({len(data)} results)")

    # Apply role-based coloring to the dataframe
    styled_data = data.style.apply(colorize_by_role, axis=1)

    st.dataframe(styled_data, hide_index=True)
else:
    st.error(f"Failed to load data: {response.status_code} - {response.text}")
    st.stop()

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
