import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
st.set_page_config(page_title="Google Trends Analyzer", layout="wide")
st.title("📈 Google Trends Insights - Malaysia")
st.markdown("Enter a keyword to explore interest over time and regional popularity.")

# Form input
with st.form(key="trend_form"):
    keyword = st.text_input("🔍 Enter a keyword", "")
    submit = st.form_submit_button("Analyze")

if submit and keyword.strip():
    try:
        kw_list = [keyword.strip()]
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list, cat=13, timeframe='today 5-y', geo='MY', gprop='')

        # Interest over time
        interest_over_time = pytrends.interest_over_time()
        if 'isPartial' in interest_over_time.columns:
            interest_over_time = interest_over_time.drop(columns=['isPartial'])

        st.subheader("📊 Interest Over Time")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=interest_over_time, x=interest_over_time.index, y=keyword, ax=ax)
        ax.set_title(f"Search Interest Over Time: '{keyword}'")
        ax.set_xlabel("Date")
        ax.set_ylabel("Interest Level")
        st.pyplot(fig)

        # Interest by region
        st.subheader("🌍 Top Countries")
        interest_by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
        top_regions = interest_by_region.sort_values(by=keyword, ascending=False).head(10)

        st.dataframe(top_regions)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.barplot(x=top_regions[keyword], y=top_regions.index, palette="viridis", ax=ax2)
        ax2.set_title(f"Top 10 Countries for '{keyword}'")
        ax2.set_xlabel("Interest")
        ax2.set_ylabel("Country")
        st.pyplot(fig2)

        # Save CSV for download
        csv_data = pd.concat([
            interest_over_time.reset_index().rename(columns={'date': 'Date'}),
            top_regions.reset_index().rename(columns={'geoName': 'Country'})
        ], axis=1)

        csv_file = f"{keyword}_trends.csv"
        csv_data.to_csv(csv_file, index=False)

        st.download_button(
            label="📥 Download Data as CSV",
            data=open(csv_file, "rb"),
            file_name=csv_file,
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
