# Smartphone Review Intelligence Dashboard

A fully interactive executive dashboard built with Python Dash and Plotly.

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/smartphone-dashboard.git
cd smartphone-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place your CSV file in the same folder as app.py
#    File must be named: Mobile_Reviews_Sentiment.csv

# 4. Run locally
python app.py
```

Open your browser at **http://localhost:8050**

## Deploy to Render (free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:server`
6. Deploy — your live URL will appear in minutes

## Deploy to Railway (free tier)

1. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
2. Select your repo
3. Set start command: `gunicorn app:server`
4. Done

## Project Structure

```
smartphone-dashboard/
├── app.py                        # Main Dash application
├── requirements.txt              # Python dependencies
├── Mobile_Reviews_Sentiment.csv  # Dataset (add this yourself)
└── README.md
```

## Features

- 12 interactive charts (sentiment, ratings, trends, scatter, radar, and more)
- 6 global filters (brand, country, platform, year, sentiment, verified)
- Dark premium boardroom theme
- Fully reactive — all charts update on every filter change
