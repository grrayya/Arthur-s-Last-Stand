# Arthur's Last Stand

Same fight, four different ways. Arthur (Knight) vs Smaug (Dragon) — attack, heal, retaliate, repeat — written first as a plain script, then rebuilt as classes, then run headless a few thousand times to see who actually wins more, then in an API with a browser front end.

## Files
- `procedural.py` — the original version, no classes, just globals and functions
- `oop.py` — same fight, refactored into `Entity` / `Knight` / `Dragon`
- `monte_carlo.py` — runs the OOP version 10,000 times headless and prints Arthur's win rate
- `api.py` — FastAPI wrapper around the OOP battle, drives `index.html`
- `index.html` — browser UI, hits the API endpoints to render the fight live

Each has a matching `test_*.py`.

## Running it

Procedural / OOP versions just run directly:

```
python procedural.py
python oop.py
```

Monte Carlo sim:

```
python monte_carlo.py
```

API + front end:

```
pip install fastapi uvicorn
uvicorn api:app --reload
```

Then open `index.html` in a browser (CORS is wide open in `api.py`, so no local server needed).

## Tests

```
pip install pytest fastapi httpx
pytest
```

Combat is randomized — crit chance, damage ranges — so most tests monkeypatch `random` for deterministic outcomes instead of asserting on ranges everywhere.

## Fight numbers

Arthur: 120 HP, 18–28 dmg, 25% crit, 2 healing flasks (+50 HP each)
Smaug: 350 HP, 15–25 dmg, 6 flat damage reduction (scales)

The Monte Carlo win rate roughly reflects how those numbers play out over a long run — worth rerunning if you tweak the stats.
