# RestaurantRec

Prototype data puller that builds a SQLite catalogue of London restaurants using the Google Places API, then inspects the results with lightweight pandas queries.

## What lives here
- `src/api_request.py` — fetches restaurants for a list of neighbourhoods and cuisines, paginates over `next_page_token`, and writes the results into `restaurants.db`.
- `src/data.py` — quick pandas view of the saved data (currently prints Soho rankings).
- `src/logger.py` / `src/paths.py` — simple logging and directory helpers.
- `data/` — scratch space created by `paths.py` (not used yet).
- `restaurants.db` — SQLite database created by `api_request.py`.
- `environment_variables.sh` — sample helper to export `GOOGLE_API_KEY` (replace with your own; the checked-in key should be rotated).

## Prerequisites
- Python 3.10+
- Google Places API key with Places/Geocoding enabled

Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install googlemaps pandas
```

## Usage
1. Export your API key (or source `environment_variables.sh` after updating it):
   ```bash
   export GOOGLE_API_KEY="your-key-here"
   ```
2. Pull data and populate the database:
   ```bash
   python src/api_request.py
   ```
   This will loop over predefined London neighbourhoods and cuisine types, then write the combined results to `restaurants.db` (with `id`, `name`, `price_level`, `rating`, `num_reviews`, `neighbourhood`).
3. Inspect the data (example Soho query):
   ```bash
   python src/data.py
   ```

## Notes
- The collector is hard-coded for London and uses a 2–3 km radius; adjust the neighbourhood/cuisine lists or radius in `src/api_request.py` to target other areas.
- API calls may incur cost/quotas; run sparingly and cache results in `restaurants.db`.
- Extend `src/data.py` with richer analyses or export scripts as needed.
