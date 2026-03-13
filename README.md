# UK Supermarket Price Analysis

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add raw CSV files to `data/raw/`
4. Run the dashboard: `python -m streamlit run app.py`

## Project Structure
- `src/load.py` — loads raw CSVs
- `src/clean.py` — cleans and standardises data
- `src/analyse.py` — 5 CMA-relevant analysis functions
- `app.py` — Streamlit dashboard
- `tests/` — CI pipeline tests

## Data
5 UK retailers, 9.5M price observations (2024)
Retailers: Aldi, ASDA, Morrisons, Sainsbury's, Tesco