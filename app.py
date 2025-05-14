from flask import Flask, render_template, request, send_file
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = None
    time_chart_path = None
    top_countries = None
    csv_path = None

    if request.method == "POST":
        keyword = request.form["keyword"]
        kw_list = [keyword]

        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

        # Interest over time
        interest_over_time = pytrends.interest_over_time()
        if 'isPartial' in interest_over_time.columns:
            interest_over_time = interest_over_time.drop(columns=['isPartial'])

        # Interest by region
        interest_by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
        top_regions = interest_by_region.sort_values(by=keyword, ascending=False).head(10)

        # Save CSV
        csv_path = f"static/{keyword}_data.csv"
        combined_data = pd.concat([interest_over_time, top_regions], axis=1)
        combined_data.to_csv(csv_path)

        # Plotting
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 6))
        plt.plot(interest_over_time.index, interest_over_time[keyword], color='blue')
        plt.title(f"Google Search Interest Over Time: '{keyword}'", fontsize=16)
        plt.xlabel("Year")
        plt.ylabel("Interest Level")
        plt.tight_layout()
        time_chart_path = "static/trends.png"
        plt.savefig(time_chart_path)
        plt.close()

        # Save bar plot for top countries (optional)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_regions[keyword], y=top_regions.index, palette="viridis")
        plt.title(f"Top 10 Countries Searching for '{keyword}'", fontsize=16)
        plt.xlabel("Interest Level")
        plt.ylabel("Country")
        plt.tight_layout()
        plt.savefig("static/top_countries.png")
        plt.close()

        top_countries = top_regions

    return render_template("index.html", keyword=keyword,
                           time_chart=time_chart_path,
                           csv_path=csv_path,
                           top_countries=top_countries)


@app.route("/download/<filename>")
def download(filename):
    return send_file(f"static/{filename}", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
