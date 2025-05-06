# COVID-19 Global Data Tracker Complete Script
# Supports static analysis (--static) and interactive Streamlit dashboard.

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

def load_and_clean(csv_file, countries):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['location'].isin(countries)]
    # Ensure critical columns exist before dropping
    drop_cols = [c for c in ['total_cases', 'total_deaths', 'total_vaccinations', 'population'] if c in df.columns]
    df = df.dropna(subset=drop_cols)
    df.ffill(inplace=True)
    return df

def static_analysis():
    csv_file = 'owid-covid-data.csv'
    countries = ['Kenya', 'United States', 'India']
    df = load_and_clean(csv_file, countries)
    
    # Static plots
    metrics = [
        ('total_cases', 'Total COVID-19 Cases Over Time', 'Total Cases'),
        ('total_deaths', 'Total Deaths Over Time', 'Total Deaths'),
        ('new_cases', 'New Daily Cases', 'New Cases'),
    ]
    for metric, title, ylabel in metrics:
        plt.figure()
        for country in countries:
            temp = df[df['location'] == country]
            plt.plot(temp['date'], temp[metric], label=country)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()
    
    # Death rate
    df['death_rate'] = df['total_deaths'] / df['total_cases']
    plt.figure()
    for country in countries:
        temp = df[df['location'] == country]
        plt.plot(temp['date'], temp['death_rate'], label=country)
    plt.title('Death Rate Over Time')
    plt.xlabel('Date')
    plt.ylabel('Death Rate')
    plt.legend()
    plt.show()
    
    # Vaccinations
    plt.figure()
    for country in countries:
        temp = df[df['location'] == country]
        plt.plot(temp['date'], temp['total_vaccinations'], label=country)
    plt.title('Total Vaccinations Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Vaccinations')
    plt.legend()
    plt.show()
    
    # Percent vaccinated
    if 'population' in df.columns:
        df['perc_vaccinated'] = df['total_vaccinations'] / df['population'] * 100
        plt.figure()
        for country in countries:
            temp = df[df['location'] == country]
            plt.plot(temp['date'], temp['perc_vaccinated'], label=country)
        plt.title('Percentage Vaccinated Over Time')
        plt.xlabel('Date')
        plt.ylabel('% Vaccinated')
        plt.legend()
        plt.show()

    # Insights
    print("\nKey Insights:")
    print("1. The United States had the highest number of both cases and deaths.")
    print("2. India experienced sharp waves of new cases, especially in 2021.")
    print("3. Kenya maintained relatively low total cases but had slower vaccine rollouts.")
    print("4. Death rate declined after vaccine introduction in all three countries.")
    print("5. Vaccination drives directly impacted the stabilization of case numbers.")
    if 'population' in df.columns:
        print("6. Percent vaccinated offers insight into comparative vaccine coverage.")

def run_streamlit():
    import streamlit as st
    import plotly.express as px

    st.title("🌐 COVID-19 Global Data Tracker")
    st.sidebar.header("User Inputs")

    @st.cache_data
    def load_data(csv_file):
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date'])
        return df

    data_file = "owid-covid-data.csv"
    df = load_data(data_file)

    countries = df['location'].unique().tolist()
    selected_countries = st.sidebar.multiselect("Select Countries", countries, default=["Kenya", "United States", "India"])

    min_date, max_date = df['date'].min(), df['date'].max()
    selected_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    start_date, end_date = selected_range if len(selected_range) == 2 else (min_date, max_date)

    mask = (
        df['location'].isin(selected_countries) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    )
    filtered = df.loc[mask].copy()
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered.head())

    hosp_cols = [col for col in filtered.columns if 'hospital' in col.lower() or 'icu' in col.lower()]
    include_hosp = bool(hosp_cols)

    def plot_metric(metric, title, ylabel):
        st.write(f"### {title}")
        fig, ax = plt.subplots()
        for country in selected_countries:
            temp = filtered[filtered['location'] == country]
            ax.plot(temp['date'], temp[metric], label=country)
        ax.set_xlabel("Date")
        ax.set_ylabel(ylabel)
        ax.legend()
        st.pyplot(fig)

    # Plot metrics
    for metric, title, ylabel in [
        ("total_cases", "Total COVID-19 Cases Over Time", "Total Cases"),
        ("total_deaths", "Total Deaths Over Time", "Total Deaths"),
        ("new_cases", "New Daily Cases", "New Cases")
    ]:
        plot_metric(metric, title, ylabel)

    filtered['death_rate'] = filtered['total_deaths'] / filtered['total_cases']
    plot_metric("death_rate", "Death Rate Over Time", "Death Rate")
    plot_metric("total_vaccinations", "Total Vaccinations Over Time", "Total Vaccinations")

    if 'population' in filtered.columns:
        filtered['perc_vaccinated'] = filtered['total_vaccinations'] / filtered['population'] * 100
        plot_metric("perc_vaccinated", "Percentage Vaccinated Over Time", "% Vaccinated")

    if include_hosp:
        for col in hosp_cols:
            plot_metric(col, f"{col.replace('_',' ').title()} Over Time", col.title())

    st.write("### Choropleth Map: Percent Vaccinated (Latest)")
    latest = filtered[filtered['date'] == filtered['date'].max()]
    map_df = latest[['iso_code', 'location', 'perc_vaccinated']].dropna()
    fig = px.choropleth(
        map_df,
        locations="iso_code",
        color="perc_vaccinated",
        hover_name="location",
        title="Percentage Vaccinated by Country (Latest)",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig)

    st.write("## Key Insights")
    st.write("- United States leads in total cases and deaths.")
    st.write("- India shows sharp waves of cases in 2021.")
    st.write("- Kenya has lower case counts and slower vaccination rollouts.")
    st.write("- Death rate declined after vaccine rollout.")
    if include_hosp:
        st.write("- Hospitalization/ICU trends help gauge healthcare burden.")
    if 'population' in df.columns:
        st.write("- Percent vaccinated offers insight into comparative vaccine coverage.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="COVID-19 Tracker")
    parser.add_argument("--static", action="store_true", help="Run static analysis")
    args, _ = parser.parse_known_args()
    if args.static:
        static_analysis()
    else:
        # If Streamlit is installed & script run by streamlit, this will execute UI
        # For normal python run without --static, default to static_analysis
        if 'streamlit' in sys.modules:
            run_streamlit()
        else:
            static_analysis()
