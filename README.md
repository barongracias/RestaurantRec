# RestaurantRec

Builds a SQLite catalogue of London restaurants using the Google Places API, then lets you query and inspect results with pandas.

## Prerequisites

- Python 3.10+
- A Google Cloud project with the **Places API** and **Geocoding API** enabled
- A valid Google API key

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Yes (for data fetch) | Google API key with Places and Geocoding APIs enabled |

Set it before running any script:

```bash
export GOOGLE_API_KEY="your-key-here"
```

`environment_variables.sh` is a convenience template — fill in your key and `source` it. **Do not commit a real key to version control.**

## Usage

**Step 1 — Fetch data and populate the database:**

```bash
python -m src.api_request
```

Iterates over predefined London neighbourhoods and cuisine types, paginates all results via `next_page_token`, and writes to `restaurants.db` in the project root. Requires `GOOGLE_API_KEY` to be set; exits with a clear error message if it is not.

**Step 2 — Inspect the data:**

```bash
python -m src.data
```

Prints a pandas view of Soho restaurants sorted by rating and review count. You can also import `load_restaurants()` directly in your own scripts:

```python
from src.data import load_restaurants

df = load_restaurants()
print(df[df['neighbourhood'] == 'Shoreditch'].sort_values('rating', ascending=False))
```

## Project Layout

| Path | Description |
|---|---|
| `src/api_request.py` | Fetches restaurant data from Google Places and writes to `restaurants.db` |
| `src/data.py` | Loads the database into a pandas DataFrame; CLI prints Soho results |
| `src/logger.py` | Shared logging helper (`get_console_logger`) |
| `src/paths.py` | Centralised path constants: `DB_PATH`, `DATA_DIR` |
| `environment_variables.sh` | Template for exporting `GOOGLE_API_KEY` (git-ignored) |
| `restaurants.db` | SQLite database (created by `api_request.py`, git-ignored) |
| `data/` | Scratch directory created on first import of `src.paths` (git-ignored) |

## Notes

- Always run with `python -m src.<module>` from the project root so that `src` is importable as a package.
- The data collector targets London with a 3 km search radius. Adjust `NEIGHBORHOODS`, `CUISINES`, or the `radius` argument in `src/api_request.py` to cover other areas.
- API calls incur cost and quota usage. Once `restaurants.db` is populated, `src.data` can be used for analysis without re-fetching.
- If `restaurants.db` does not exist when running `src.data`, a clear error message is logged instead of raising an exception.
