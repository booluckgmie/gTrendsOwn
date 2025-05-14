# Google-Trends-Analysis
Google Trends Analysis
🌍 Google Trends Analyzer
Unlock the power of data with this simple yet powerful web app that visualizes Google search interest trends for any keyword across time and countries!

<div align="center"> <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" /> <img src="https://img.shields.io/badge/Flask-WebApp-lightgrey?logo=flask" /> <img src="https://img.shields.io/badge/GoogleTrends-Analyzer-brightgreen?logo=google" /> </div>
📊 Overview
Curious about how a topic has trended globally over the past 5 years?

Just enter any keyword, and this app will:

📈 Plot search interest over time

🌐 Show top 10 countries interested in that topic

📄 Allow CSV download of the data

All powered by Google Trends via pytrends.

🔍 Features
✅ Keyword-based Google Trends analysis

📉 Line chart of interest over the last 5 years

🌎 Bar chart of top countries searching for the keyword

📁 CSV file export for further analysis

🖼️ Real-time chart rendering using Seaborn and Matplotlib

🧠 Built with Flask for an interactive UI

🖼️ Demo Preview
✍️ Type a keyword, hit Submit, and watch the data appear.

<p align="center"> <img src="static/trends.png" width="600"><br> <em>Interest Over Time</em> </p> <p align="center"> <img src="static/top_countries.png" width="600"><br> <em>Top Countries by Interest</em> </p>
🧠 How It Works
Takes a keyword input via a simple HTML form

Uses pytrends to fetch:

Interest Over Time (interest_over_time)

Interest by Region (interest_by_region)

Visualizes data using:

Line plot (search trends)

Bar chart (top countries)

Saves the results as a downloadable CSV

Displays the charts and download link on the web page

📦 Requirements
Install dependencies via pip:

bash
Copy code
pip install flask pytrends pandas matplotlib seaborn
Note: Also ensure you have access to Google (some proxies or VPNs might block pytrends).

🚀 Getting Started
Clone this repo

Make sure the static/ directory exists

Run the Flask app:

bash
Copy code
python app.py
Open your browser and go to:

cpp
Copy code
http://127.0.0.1:5000/
📁 Project Structure
php
Copy code
.
├── app.py                      # Main Flask application
├── templates/
│   └── index.html              # HTML frontend
├── static/
│   ├── trends.png              # Line plot saved here
│   ├── top_countries.png       # Bar chart saved here
│   └── <keyword>_data.csv      # Exported CSV file
└── README.md
📌 Sample Output
Keyword	Peak Interest Date	Top Country
AI	2023-09	United States
Python	2022-11	India
Bitcoin	2021-05	Nigeria

📁 And yes, you can download this data as a .csv!

💡 Potential Use Cases
💼 Market research for business trends

🎓 Academic keyword popularity analysis

📰 Tracking interest in world events or tech

📢 SEO & content planning

🙌 Credits
Built using Flask and PyTrends

Inspired by the power of public data 📊

📃 License
MIT License. Free to use, modify, and share.

👨‍💻 Author
[Vedanth] — Turning data into powerful stories.
