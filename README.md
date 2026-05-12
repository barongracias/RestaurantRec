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

Export your key before running any script:

```bash
export GOOGLE_API_KEY="your-key-here"
```

`environment_variables.sh` is a convenience template — update it with your key and `source` it. Do not commit a real key to version control.

## Usage

**1. Fetch data and populate the database:**

```bash
python -m src.api_request
```

Loops over predefined London neighbourhoods and cuisine types, paginates results via `next_page_token`, and writes to `restaurants.db` in the project root.

**2. Inspect the data:**

```bash
python -m src.data
```

Prints a pandas view of Soho restaurants sorted by rating and review count. Import `src.data.load_restaurants()` in your own scripts to get the full DataFrame.

## Project Layout

| Path | Description |
|---|---|
| `src/api_request.py` | Fetches restaurant data from Google Places and writes to `restaurants.db` |
| `src/data.py` | Loads the database into a pandas DataFrame; CLI prints Soho results |
| `src/logger.py` | Logging helper |
| `src/paths.py` | Centralised path constants (`DB_PATH`, `DATA_DIR`) |
| `restaurants.db` | SQLite database created by `api_request.py` (git-ignored) |
| `data/` | Scratch directory created on first import of `src.paths` |

## Notes

- Run scripts with `python -m src.<module>` from the project root so that `src` is importable as a package.
- The collector targets London with a 3 km search radius. Adjust `NEIGHBORHOODS`, `CUISINES`, or the radius constant in `src/api_request.py` to target other areas.
- API calls incur cost and quota usage; the cached `restaurants.db` can be reused for subsequent analysis without re-fetching.
- If `GOOGLE_API_KEY` is not set, `api_request.py` exits with a clear error message rather than crashing with a traceback.
- If `restaurants.db` does not exist when running `src.data`, a clear error message is shown instead of a traceback.
