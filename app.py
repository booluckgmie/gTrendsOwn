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
st.set_page_config(page_title="Google Trends Analyzer (Malaysia)", layout="wide")
st.title("📊 Google Trends Analyzer (Malaysia)")

# Input
keyword = st.text_input("Enter a search keyword:", placeholder="e.g. AI, Olympics, Tesla")

if keyword:
    kw_list = [keyword]
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        # Added error handling for the build_payload
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='MY', gprop='')
        
        # Interest Over Time
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            if 'isPartial' in interest_over_time.columns:
                interest_over_time = interest_over_time.drop(columns=['isPartial'])
                
            # Row 1: Interest Over Time Plot
            st.subheader(f"📈 Interest Over Time: `{keyword}`")
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=interest_over_time, x=interest_over_time.index, y=keyword, ax=ax1, color='blue')
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Interest Level")
            ax1.set_title("Search Interest Over Time in Malaysia")
            st.pyplot(fig1)
            
            # Row 4: CSV Download
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
            st.warning(f"No interest over time data found for '{keyword}'.")

        # Interest by Region - with error handling
        try:
            interest_by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
            if not interest_by_region.empty and keyword in interest_by_region.columns:
                top_regions = interest_by_region.sort_values(by=keyword, ascending=False).head(10)
                
                # Row 2: Top Countries Plot and Country Data Table
                col_plot, col_table = st.columns([0.6, 0.4])  # Adjust width ratio as needed

                with col_plot:
                    st.subheader(f"🌍 Top 10 Countries Searching `{keyword}`")
                    fig2, ax2 = plt.subplots(figsize=(8, 4))
                    sns.barplot(x=top_regions[keyword], y=top_regions.index, ax=ax2, color='skyblue')
                    ax2.set_xlabel("Interest Level")
                    ax2.set_ylabel("Country")
                    st.pyplot(fig2)

                with col_table:
                    st.subheader("📋 Interest by Country (Top 10)")
                    st.dataframe(top_regions.reset_index())
            else:
                st.warning(f"No regional interest data found for '{keyword}'.")
        except Exception as e:
            st.warning(f"Couldn't fetch regional data: {e}")

        # Related Topics - with comprehensive error handling
        try:
            related = pytrends.related_topics()
            
            if keyword in related and related[keyword] is not None:
                st.subheader("🧠 Related Topics")
                col_top_related, col_rising_related = st.columns(2)
                
                # Top Related Topics
                with col_top_related:
                    st.markdown("#### 🔝 Top Related Topics")
                    if 'top' in related[keyword] and isinstance(related[keyword]['top'], pd.DataFrame) and not related[keyword]['top'].empty:
                        top_related = related[keyword]['top']
                        if 'topic_title' in top_related.columns and 'value' in top_related.columns:
                            st.dataframe(top_related[['topic_title', 'value']].rename(columns={'topic_title': 'Topic', 'value': 'Interest'}))
                        else:
                            st.write("Top related topics data has unexpected format.")
                    else:
                        st.write("No top related topics available.")
                
                # Rising Related Topics
                with col_rising_related:
                    st.markdown("#### 📈 Rising Related Topics")
                    if 'rising' in related[keyword] and isinstance(related[keyword]['rising'], pd.DataFrame) and not related[keyword]['rising'].empty:
                        rising_related = related[keyword]['rising']
                        if 'topic_title' in rising_related.columns and 'value' in rising_related.columns:
                            st.dataframe(rising_related[['topic_title', 'value']].rename(columns={'topic_title': 'Topic', 'value': 'Growth'}))
                        else:
                            st.write("Rising related topics data has unexpected format.")
                    else:
                        st.write("No rising related topics available.")
            else:
                st.warning(f"No related topics found for '{keyword}'.")
        except Exception as e:
            st.warning(f"Couldn't fetch related topics: {e}")

    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
else:
    st.info("👆 Please enter a keyword to analyze Google Trends data.")
