# RestaurantRec

Builds a SQLite catalogue of London restaurants using the Google Places API, then lets you inspect results with pandas queries.

## Prerequisites

- Python 3.10+
- Google Places API key with the **Places API** and **Geocoding API** enabled

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## API Key

A `GOOGLE_API_KEY` environment variable must be set before running any script:

```bash
export GOOGLE_API_KEY="your-key-here"
```

A sample helper (`environment_variables.sh`) is included — update it with your key and source it, or export the variable directly. Do not commit a real key to version control.

## Usage

**1. Fetch data and populate the database:**

```bash
python src/api_request.py
```

Loops over predefined London neighbourhoods and cuisine types, paginates over `next_page_token`, and writes results to `restaurants.db`.

**2. Inspect the data:**

```bash
python src/data.py
```

Prints a pandas view of Soho restaurants sorted by rating and review count.

## Project Layout

| Path | Description |
|---|---|
| `src/api_request.py` | Fetches restaurant data from Google Places and writes to `restaurants.db` |
| `src/data.py` | Quick pandas view of the saved data |
| `src/logger.py` | Logging helper |
| `src/paths.py` | Directory path constants |
| `restaurants.db` | SQLite database created by `api_request.py` |
| `data/` | Scratch directory created by `paths.py` |

## Notes

- The collector is hard-coded for London with a 2–3 km search radius. Adjust the neighbourhood/cuisine lists or radius in `src/api_request.py` to target other areas.
- API calls may incur cost and quota usage; run sparingly and rely on the cached `restaurants.db` for subsequent analysis.
