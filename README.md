# English → SQL Generator

A Streamlit web app that turns plain-English data questions into SQL queries, powered by the Google Gemini API.

## What it does
Describe the data you want in plain English (e.g. "show me the top 5 customers by total purchase amount") and the app generates a clean SQL query plus a short explanation.

## Built with
- Python
- Streamlit (web UI)
- Google Gemini API

## Running locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Gemini API key to a `.env` file as `GEMINI_API_KEY=your_key`
4. Run: `streamlit run app.py`