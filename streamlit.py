import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# added the customized css to look it better

CUSTOM_CSS = """
<style>
/* --- App background + typography --- */
.stApp {
    background: radial-gradient(1200px circle at 10% 10%, rgba(99, 102, 241, 0.10), transparent 55%),
                radial-gradient(900px circle at 90% 20%, rgba(16, 185, 129, 0.10), transparent 50%),
                radial-gradient(900px circle at 40% 90%, rgba(236, 72, 153, 0.08), transparent 55%),
                #0b1220;
    color: #E5E7EB;
}
html, body, [class*="css"]  {
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
}

/* --- Make main content a bit narrower on very wide screens (optional) --- */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
    max-width: 1400px;
}

/* --- Hide Streamlit default menu/footer for a cleaner dashboard feel --- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* --- Sidebar styling --- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(17, 24, 39, 0.92), rgba(15, 23, 42, 0.92));
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #E5E7EB !important;
}

/* --- Hero header --- */
.hero {
    padding: 18px 18px 14px 18px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(99,102,241,0.20), rgba(16,185,129,0.14), rgba(236,72,153,0.12));
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
}
.hero h1 {
    margin: 0;
    font-size: 2.05rem;
    letter-spacing: -0.02em;
}
.hero p {
    margin: 6px 0 0 0;
    color: rgba(229,231,235,0.85);
    font-size: 0.98rem;
}

/* --- Section cards (containers around charts) --- */
.card {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 14px 14px 6px 14px;
    background: rgba(15, 23, 42, 0.55);
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
}
.card h3 {
    margin-top: 0.2rem;
    margin-bottom: 0.8rem;
}

/* --- KPI row: make metrics look like cards --- */
div[data-testid="metric-container"] {
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 14px 14px 12px 14px;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.16);
}
div[data-testid="metric-container"] label {
    color: rgba(229,231,235,0.78) !important;
}
div[data-testid="metric-container"] div {
    color: #E5E7EB !important;
}

/* --- Divider line (make it subtle) --- */
hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.10);
    margin: 1.1rem 0 1.1rem 0;
}

/* --- Improve widget spacing --- */
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stDateInput {
    margin-bottom: 0.6rem;
}

/* --- Optional: sticky sidebar (works in many layouts) --- */
section[data-testid="stSidebar"] > div {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    padding-top: 0.2rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


st.markdown(
    """
    <div class="hero">
        <h1>Bike Sharing Demand Dashboard</h1>
        <p>Interactive dashboard summarizing EDA + visualization insights (Assignments 1 & 2).</p>
    </div>
    """,
    unsafe_allow_html=True
)


# Data loading

@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month
    return df

df = load_data()


# Sidebar filters widget as slider

st.sidebar.markdown("## Filters")
st.sidebar.caption("Use the controls below to refine the dashboard.")

min_date = df["date"].min()
max_date = df["date"].max()

with st.sidebar.expander("📅 Date Filter", expanded=True):
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_map = {1: "Clear/Few clouds", 2: "Mist/Cloudy", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow"}

df["season_name"] = df["season"].map(season_map)
df["weather_name"] = df["weather"].map(weather_map)

with st.sidebar.expander("🌦️ Conditions", expanded=True):
    season_sel = st.multiselect(
        "Season",
        options=sorted(df["season_name"].unique()),
        default=sorted(df["season_name"].unique())
    )
    weather_sel = st.multiselect(
        "Weather",
        options=sorted(df["weather_name"].unique()),
        default=sorted(df["weather_name"].unique())
    )

with st.sidebar.expander("Time & Temperature", expanded=True):
    hour_range = st.slider("Hour Range", 0, 23, (0, 23))
    temp_range = st.slider(
        "Temperature Range (°C)",
        float(df["temp"].min()),
        float(df["temp"].max()),
        (float(df["temp"].min()), float(df["temp"].max()))
    )

st.sidebar.markdown("---")
st.sidebar.caption("Tip: Try narrowing to commute hours (7–10, 16–19).")


# Apply filters in the slider

filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[(filtered["date"] >= start_date) & (filtered["date"] <= end_date)]

filtered = filtered[
    (filtered["season_name"].isin(season_sel)) &
    (filtered["weather_name"].isin(weather_sel)) &
    (filtered["hour"].between(hour_range[0], hour_range[1], inclusive="both")) &
    (filtered["temp"].between(temp_range[0], temp_range[1], inclusive="both"))
]



st.markdown("### Key Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Rows (filtered)", f"{len(filtered):,}")
k2.metric("Avg Count", f"{filtered['count'].mean():.1f}")
k3.metric("Avg Casual", f"{filtered['casual'].mean():.1f}")
k4.metric("Avg Registered", f"{filtered['registered'].mean():.1f}")

st.markdown("---")



st.markdown("### 📊 Insights")

col1, col2 = st.columns(2)


with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1) Average Demand by Hour")
    fig, ax = plt.subplots()
    hour_avg = filtered.groupby("hour")["count"].mean().reset_index()
    sns.lineplot(data=hour_avg, x="hour", y="count", ax=ax, color='orange')
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Count")
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2) Average Demand by Season")
    fig, ax = plt.subplots()
    season_avg = filtered.groupby("season_name")["count"].mean().reindex(["Spring", "Summer", "Fall", "Winter"]).reset_index()
    sns.barplot(data=season_avg, x="season_name", y="count", ax=ax)
    ax.set_xlabel("Season")
    ax.set_ylabel("Average Count")
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)



# 3: Count by weather (full width)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("3) Average Demand by Weather")
fig, ax = plt.subplots(figsize=(4,2))
weather_avg = filtered.groupby("weather_name")["count"].mean().sort_values(ascending=False).reset_index()
sns.barplot(data=weather_avg, x="weather_name", y="count", ax=ax, palette='rocket')
ax.set_xlabel("Weather")
ax.set_ylabel("Average Count")
ax.tick_params(axis='both', labelsize=8)
plt.xticks(rotation=20, ha="right")
st.pyplot(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

# 4: Temp vs Count
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("4) Temperature vs Demand")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x="temp", y="count", alpha=0.5, ax=ax, palette='magma')
    ax.set_xlabel("Temp (°C)")
    ax.set_ylabel("Count")
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 5: Correlation heatmap
with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("5) Correlation Heatmap")
    fig, ax = plt.subplots()
    corr_cols = ["temp", "atemp", "humidity", "windspeed", "casual", "registered", "count"]
    corr = filtered[corr_cols].corr(numeric_only=True)
    sns.heatmap(corr, annot=True, fmt=".2f", ax=ax)
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

