"""
Config centrale du projet.
"""
from pathlib import Path

# 30 dernières saisons -> commence en 1996-97 (première saison avec stats avancées)
START_YEAR = 1996
END_YEAR = 2025  # saison 2025-26 = la plus récente à ce jour

def season_list():
    """Retourne la liste des saisons au format nba_api, ex: '1996-97', '1997-98', ..."""
    seasons = []
    for y in range(START_YEAR, END_YEAR + 1):
        seasons.append(f"{y}-{str(y + 1)[-2:]}")
    return seasons

ROOT = Path(__file__).parent
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "nba.db"

RAW_DIR.mkdir(parents=True, exist_ok=True)