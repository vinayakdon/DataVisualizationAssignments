# 🚲 Bike Sharing Demand Dashboard

Interactive analysis and dashboard for the Washington D.C. bike sharing dataset (2011–2012), completed as part of Assignments 1, 2, and 3.

---

## 📌 Project Objective
Analyze how **weather and temporal factors** affect bike rental demand and summarize insights using an **interactive Streamlit dashboard**.

Dataset source: Kaggle (Bike Sharing Demand – `train.csv`)
Used this after cleaning in streamlit to show visualizations - `newtrain`

---

## 📂 Assignments Overview

### 🧪 Assignment 1: Exploratory Data Analysis (EDA)
- Loaded and cleaned the dataset
- Converted `datetime` to pandas datetime format
- Created new features:
  - year, month, date, hour
- Mapped season and weather codes to readable labels
- Analyzed:
  - Casual vs registered users
  - Working vs non-working days
  - Seasonal and monthly demand trends
- Created a `day_period` feature (night, morning, afternoon, evening)
- Computed correlations with total rental count

---

### 📊 Assignment 2: Data Visualization
- Histograms and box plots for numerical variables
- Mean hourly rentals by:
  - Working vs non-working days
  - Month (combined and separate years)
  - Weather conditions (with 95% confidence intervals)
- Hourly demand trends:
  - By time of day
  - By weekday
  - By season (multi-panel)
- Correlation heatmap for numerical features

---

### 🖥️ Assignment 3: Interactive Dashboard (Streamlit)
- Built an interactive dashboard using Streamlit
- Added filters for:
  - Date range
  - Season
  - Weather
  - Hour range
  - Temperature range
- Displayed:
  - Key metrics (KPIs)
  - 4–6 visualizations summarizing insights
- Enhanced UI using custom CSS
- Deployed on Streamlit Community Cloud

---

## 🚀 Live Demo & Repository

- **GitHub Repository:**  
  [https://github.com/username/bike-sharing-dashboard](https://github.com/vinayakdon/DataVisualizationAssignments)

- **Streamlit App:**  
  [https://bike-sharing-dashboard.streamlit.app](https://datavisualizationassignment.streamlit.app)

---

## 🛠️ Tech Stack
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit

---

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
