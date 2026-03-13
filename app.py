import streamlit as st
import pandas as pd
from src.load import load_data
from src.clean import clean_data
from src.analyse import (
    avg_price_by_retailer,
    own_brand_vs_branded,
    price_by_category,
    price_trends_over_time,
    listings_over_time,
)

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UK Supermarket Price Analysis",
    page_icon="🛒",
    layout="wide"
)

# ── Load data (cached so it only runs once) ────────────────────────────
@st.cache_data
def get_data():
    df = load_data()
    df = clean_data(df)
    return df

df = get_data()

# ── Header ─────────────────────────────────────────────────────────────
st.title("🛒 UK Supermarket Price Analysis")
st.markdown("**Prepared by Eric James** | Data: 5 UK Retailers, 9.5M price observations")
st.divider()

# ── Sidebar filters ────────────────────────────────────────────────────
st.sidebar.header("Filters")
selected_retailers = st.sidebar.multiselect(
    "Select Retailers",
    options=df["retailer"].unique().tolist(),
    default=df["retailer"].unique().tolist()
)
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["category"].unique().tolist(),
    default=df["category"].unique().tolist()
)

# Apply filters
filtered = df[
    df["retailer"].isin(selected_retailers) &
    df["category"].isin(selected_categories)
]

# ── KPI row ────────────────────────────────────────────────────────────
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Observations", f"{len(filtered):,}")
col2.metric("Retailers", filtered["retailer"].nunique())
col3.metric("Categories", filtered["category"].nunique())
col4.metric("Date Range", f"{filtered['date'].min().strftime('%b %Y')} – {filtered['date'].max().strftime('%b %Y')}")

st.divider()

# ── Q1: Average price by retailer ─────────────────────────────────────
st.subheader("1️⃣ Average Price by Retailer")
st.caption("Which supermarket is cheapest overall?")
q1 = avg_price_by_retailer(filtered)
col1, col2 = st.columns([1, 1])
with col1:
    st.bar_chart(q1.set_index("retailer")["avg_price"])
with col2:
    st.dataframe(q1, use_container_width=True)

st.divider()

# ── Q2: Own brand vs branded ───────────────────────────────────────────
st.subheader("2️⃣ Own Brand vs Branded Prices")
st.caption("How much do own-brand products save consumers?")
q2 = own_brand_vs_branded(filtered)
col1, col2 = st.columns([1, 1])
with col1:
    st.bar_chart(q2.set_index("retailer")[["own_brand_avg", "branded_avg"]])
with col2:
    st.dataframe(q2, use_container_width=True)

st.divider()

# ── Q3: Price by category ──────────────────────────────────────────────
st.subheader("3️⃣ Average Price by Category & Retailer")
st.caption("Which categories are most expensive and where?")
q3 = price_by_category(filtered)
selected_cat = st.selectbox("Select a category to explore", q3["category"].unique())
q3_filtered = q3[q3["category"] == selected_cat]
st.bar_chart(q3_filtered.set_index("retailer")["avg_price"])

st.divider()

# ── Q4: Price trends over time ─────────────────────────────────────────
st.subheader("4️⃣ Price Trends Over Time")
st.caption("Is inflation visible across retailers?")
q4 = price_trends_over_time(filtered)
q4_pivot = q4.pivot(index="month", columns="retailer", values="avg_price")
st.line_chart(q4_pivot)

st.divider()

# ── Q5: Listings over time ─────────────────────────────────────────────
st.subheader("5️⃣ Product Listings Over Time")
st.caption("Which retailer stocks the most products and when?")
q5 = listings_over_time(filtered)
q5_pivot = q5.pivot(index="month", columns="retailer", values="num_listings")
st.line_chart(q5_pivot)

st.divider()
st.caption("Analysis by Eric James")
