import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Bike Sharing Dashboard (Cleaned Data)",
    layout="wide",
    initial_sidebar_state="expanded",
)


plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})


CUSTOM_CSS = """
<style>
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
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
    max-width: 1400px;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(17, 24, 39, 0.92), rgba(15, 23, 42, 0.92));
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #E5E7EB !important;
}

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
.card {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 14px 14px 6px 14px;
    background: rgba(15, 23, 42, 0.55);
    box-shadow: 0 8px 22px rgba(0,0,0,0.18);
}
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
hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.10);
    margin: 1.1rem 0 1.1rem 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


st.markdown(
    """
    <div class="hero">
        <h1>🚲 Bike Sharing Demand Dashboard (Cleaned Data)</h1>
        <p>Streamlit dashboard built using the cleaned dataset used in Assignment 2 visualizations.</p>
    </div>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    df = pd.read_csv("newtrain.csv")

    # Some safety conversions
    for col in ["year", "month", "day_of_week", "hour_of_day", "holiday", "workingday", "weather"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure strings for these
    if "season" in df.columns:
        df["season"] = df["season"].astype(str).str.lower()
    if "day_period" in df.columns:
        df["day_period"] = df["day_period"].astype(str).str.lower()

    return df

df = load_data()


st.sidebar.markdown("## 🔎 Filters")
st.sidebar.caption("Filters for the cleaned dataset (Assignment 2).")

years = sorted(df["year"].dropna().unique().astype(int).tolist()) if "year" in df.columns else []
months = list(range(1, 13)) if "month" in df.columns else []
hours = (0, 23) if "hour_of_day" in df.columns else (0, 23)

with st.sidebar.expander("🗓️ Time Filters", expanded=True):
    year_sel = st.multiselect("Year", options=years, default=years if years else None)
    month_sel = st.multiselect("Month", options=months, default=months)
    hour_range = st.slider("Hour Range", 0, 23, (0, 23))

with st.sidebar.expander("🌦️ Conditions", expanded=True):
    season_opts = sorted(df["season"].dropna().unique().tolist()) if "season" in df.columns else []
    weather_opts = sorted(df["weather"].dropna().unique().astype(int).tolist()) if "weather" in df.columns else []

    season_sel = st.multiselect("Season", options=season_opts, default=season_opts)
    weather_sel = st.multiselect("Weather Category", options=weather_opts, default=weather_opts)

with st.sidebar.expander("🌡️ Weather Ranges", expanded=True):
    temp_min, temp_max = float(df["temp"].min()), float(df["temp"].max())
    temp_range = st.slider("Temperature Range (°C)", temp_min, temp_max, (temp_min, temp_max))

    hum_min, hum_max = float(df["humidity"].min()), float(df["humidity"].max())
    humidity_range = st.slider("Humidity Range", hum_min, hum_max, (hum_min, hum_max))

with st.sidebar.expander("🏢 Day Type", expanded=True):
    working_sel = st.multiselect("Working Day", options=[0, 1], default=[0, 1])

st.sidebar.markdown("---")
st.sidebar.caption("Tip: Working day = 1, Non-working day = 0")


filtered = df.copy()

if "year" in filtered.columns and year_sel:
    filtered = filtered[filtered["year"].isin(year_sel)]

if "month" in filtered.columns and month_sel:
    filtered = filtered[filtered["month"].isin(month_sel)]

if "hour_of_day" in filtered.columns:
    filtered = filtered[filtered["hour_of_day"].between(hour_range[0], hour_range[1], inclusive="both")]

if "season" in filtered.columns and season_sel:
    filtered = filtered[filtered["season"].isin(season_sel)]

if "weather" in filtered.columns and weather_sel:
    filtered = filtered[filtered["weather"].isin(weather_sel)]

filtered = filtered[
    (filtered["temp"].between(temp_range[0], temp_range[1], inclusive="both")) &
    (filtered["humidity"].between(humidity_range[0], humidity_range[1], inclusive="both"))
]

if "workingday" in filtered.columns and working_sel:
    filtered = filtered[filtered["workingday"].isin(working_sel)]


st.markdown("### 📌 Key Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Rows (filtered)", f"{len(filtered):,}")
k2.metric("Avg Count", f"{filtered['count'].mean():.1f}")
k3.metric("Avg Casual", f"{filtered['casual'].mean():.1f}")
k4.metric("Avg Registered", f"{filtered['registered'].mean():.1f}")

st.markdown("---")


st.markdown("### 📊 Visualizations (Assignment 2)")

col1, col2 = st.columns(2)

# 1: Mean hourly rentals by working vs non-working days 
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("1) Mean Rentals by Hour (Working vs Non-working)")

    mean_hourly = filtered.groupby(["hour_of_day", "workingday"])["count"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 3))
    sns.lineplot(
        data=mean_hourly,
        x="hour_of_day",
        y="count",
        hue="workingday",
        marker="o",
        ax=ax
    )
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Mean Total Rentals")
    ax.legend(title="Working Day", labels=["Non-working (0)", "Working (1)"])
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2: Mean rentals by month 
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("2) Mean Rentals by Month (Both Years Combined)")

    mean_by_month = filtered.groupby("month")["count"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 3))
    sns.barplot(data=mean_by_month, x="month", y="count", ax=ax, palette="viridis")
    ax.set_xlabel("Month")
    ax.set_ylabel("Mean Total Rentals")
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3: Mean + 95% CI by weather 
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("3) Mean Rentals with 95% CI by Weather Category")

fig, ax = plt.subplots(figsize=(8, 3.5))
sns.barplot(x="weather", y="count", data=filtered, ci=95, ax=ax, palette="magma")
ax.set_xlabel("Weather Category")
ax.set_ylabel("Mean Total Rentals")
st.pyplot(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

# 4: Mean rentals vs hour of day 
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("4) Mean Rentals vs Hour of Day")

    mean_rentals_by_hour = filtered.groupby("hour_of_day")["count"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=mean_rentals_by_hour, x="hour_of_day", y="count", marker="o", ax=ax)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Mean Total Rentals")
    st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 5: Correlation heatmap 

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("5) Correlation Heatmap (Numerical Features)")

numeric_df = filtered.select_dtypes(include=["number"])
corr = numeric_df.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
