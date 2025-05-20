import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from io import BytesIO

# Suppress known warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="pytrends.request")

# Streamlit configuration
st.set_page_config(page_title="Google Trends Analyzer", layout="wide")
st.title("📊 Google Trends Analyzer (Malaysia)")

# Input
keyword = st.text_input("Enter a search keyword:", placeholder="e.g. AI, Olympics, Tesla")

if keyword:
    kw_list = [keyword]
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list, cat=13, timeframe='today 5-y', geo='MY', gprop='')

    # Interest Over Time
    interest_over_time = pytrends.interest_over_time()
    if 'isPartial' in interest_over_time.columns:
        interest_over_time = interest_over_time.drop(columns=['isPartial'])

    # Interest by Region
    interest_by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
    top_regions = interest_by_region.sort_values(by=keyword, ascending=False).head(10)

    # Related Topics
    related = pytrends.related_topics()
    top_related = related[keyword]['top']
    rising_related = related[keyword]['rising']

    # Plot: Interest Over Time
    st.subheader(f"📈 Interest Over Time: `{keyword}`")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=interest_over_time, x=interest_over_time.index, y=keyword, ax=ax1, color='blue')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Interest Level")
    ax1.set_title("Search Interest Over Time in Malaysia")
    st.pyplot(fig1)

    # Plot: Top Countries
    st.subheader(f"🌍 Top 10 Countries Searching `{keyword}`")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_regions[keyword], y=top_regions.index, ax=ax2, color='skyblue')
    ax2.set_xlabel("Interest Level")
    ax2.set_ylabel("Country")
    st.pyplot(fig2)

    # Table: Country Data
    st.subheader("📋 Interest by Country")
    st.dataframe(top_regions.reset_index())

    # Related Topics
    st.subheader("🧠 Related Topics")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔝 Top Related Topics")
        if isinstance(top_related, pd.DataFrame) and not top_related.empty:
            st.dataframe(top_related[['topic_title', 'value']].rename(columns={'topic_title': 'Topic', 'value': 'Interest'}))
        else:
            st.write("No data available.")
    with col2:
        st.markdown("#### 📈 Rising Related Topics")
        if isinstance(rising_related, pd.DataFrame) and not rising_related.empty:
            st.dataframe(rising_related[['topic_title', 'value']].rename(columns={'topic_title': 'Topic', 'value': 'Growth'}))
        else:
            st.write("No data available.")

    # CSV Download
    st.subheader("📥 Download Time Series Data")
    csv_buffer = BytesIO()
    interest_over_time.to_csv(csv_buffer)
    st.download_button(
        label="Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"{keyword}_trend_timeseries.csv",
        mime="text/csv"
    )
else:
    st.info("👆 Please enter a keyword to analyze Google Trends data.")
