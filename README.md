# Curbwise

How to get rid of anything, city by city: free and official options first, then recycling and donation, then paid haul-away. It launched with Nashville, Tennessee.

The site is static HTML built by `build.py` into `docs/`, which GitHub Pages serves. Yeha, an AI research agent, adds or re-verifies one useful page each night. Its operating manual is `yeha/YEHA.md`.

## Build locally

```bash
pip install -r requirements.txt
python3 build.py --base-path "" --site-url http://localhost:8001
python3 tools/check.py
python3 -m http.server 8001 -d docs
```

Before you commit, rebuild with the defaults (`python3 build.py`) so the links use the `/curbwise` base path.

## Edit

- A city's official rules (centers, hours, fees, sources, haul-away links): `data/<city>.json`
- Item guides: `content/<city>/<item>.md`
- Site pages: `content/*.md`
- Settings: `config.json`
