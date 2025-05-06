# python-project
# COVID-19 Global Data Tracker

A comprehensive project that loads, cleans, analyzes, and visualizes global COVID-19 data, allowing both static report generation and an interactive dashboard for exploration.

## 🚀 Objectives

* **Data Collection & Cleaning:** Load and preprocess data from Our World in Data to ensure accuracy and consistency.
* **Exploratory Data Analysis (EDA):** Identify trends in cases, deaths, new infections, death rates, and vaccination coverage across countries.
* **Visualization:** Create static Matplotlib charts and an interactive Streamlit dashboard with time-series plots and a choropleth map.
* **User Interaction:** Allow users to select countries, date ranges, and view optional metrics like hospitalization/ICU data.
* **Insights & Reporting:** Summarize key findings with narrative insights.

## 🛠️ Tools & Libraries

* **Python 3.7+**
* **pandas** for data loading and manipulation
* **matplotlib** & **seaborn** for static visualizations
* **plotly.express** for interactive choropleth maps
* **streamlit** for building the interactive dashboard

## 📦 Project Files

* `COVID19_Global_Tracker_Complete.py` — Single script supporting both static analysis (--static flag) and Streamlit dashboard modes.
* `owid-covid-data.csv` — COVID-19 dataset from [Our World in Data](https://covid.ourworldindata.org/data/owid-covid-data.csv) (download separately).
* `README.md` — This file.

## ▶️ How to Run

1. **Clone the repository** or download the files into a folder.

2. **Download the dataset:**

   ```bash
   wget https://covid.ourworldindata.org/data/owid-covid-data.csv -O owid-covid-data.csv
   ```

3. **Install dependencies:**

   ```bash
   pip install pandas matplotlib seaborn plotly streamlit
   ```

4. **Static Analysis Mode:**

   ```bash
   python COVID19_Global_Tracker_Complete.py --static
   ```

   This generates Matplotlib plots and prints insights in the console.

5. **Interactive Dashboard Mode:**

   ```bash
   streamlit run COVID19_Global_Tracker_Complete.py
   ```

   Use the sidebar to select countries, date ranges, and view metrics.

## 💡 Key Insights & Reflections

* **Global Trends:** The United States consistently leads in total cases and deaths; India shows pronounced waves, notably during variant surges; Kenya’s counts remain lower with delayed vaccination rollouts.
* **Death Rate Dynamics:** Introduction of vaccines greatly reduced death rates across all countries.
* **Vaccination Coverage:** Percent vaccinated highlights disparities in rollout speed and saturation.
* **Interactive Value:** Allowing user-driven country/date selection enriches exploratory analysis and reveals nuanced patterns.
* **Future Extensions:** Incorporating hospitalization/ICU data and enabling exportable reports would further strengthen the tool.

---

*This project offers both reproducible static reporting and an engaging dashboard to explore COVID-19 trends globally.*
