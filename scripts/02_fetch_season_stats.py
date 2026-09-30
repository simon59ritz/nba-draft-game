"""
Télécharge les stats par joueur pour chaque saison (moyennes + stats avancées),
et sauvegarde un CSV par saison dans data/raw/.

Relance-le n'importe quand : il saute automatiquement les saisons déjà téléchargées.
Pour forcer un re-téléchargement (ex: saison en cours), supprime le CSV correspondant.

Usage:
    python scripts/02_fetch_season_stats.py
"""
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import RAW_DIR, season_list

import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

# Colonnes avancées qu'on garde (le reste est redondant avec les stats de base)
ADVANCED_COLS_TO_KEEP = [
    "PLAYER_ID", "PIE", "NET_RATING", "OFF_RATING", "DEF_RATING",
    "TS_PCT", "USG_PCT", "AST_PCT", "REB_PCT",
]


def fetch_one_season(season: str) -> pd.DataFrame:
    base = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star="Regular Season",
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Base",
    ).get_data_frames()[0]

    time.sleep(0.6) 

    advanced = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star="Regular Season",
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Advanced",
    ).get_data_frames()[0]

    advanced = advanced[[c for c in ADVANCED_COLS_TO_KEEP if c in advanced.columns]]

    merged = base.merge(advanced, on="PLAYER_ID", how="left")
    merged.insert(0, "SEASON", season)
    return merged


def main():
    seasons = season_list()
    print(f"{len(seasons)} saisons à traiter : {seasons[0]} -> {seasons[-1]}")

    for season in seasons:
        out_path = RAW_DIR / f"player_stats_{season}.csv"
        if out_path.exists():
            print(f"[skip] {season} déjà téléchargée")
            continue

        print(f"[fetch] {season} ...")
        try:
            df = fetch_one_season(season)
            df.to_csv(out_path, index=False)
            print(f"  -> OK ({len(df)} joueurs)")
        except Exception as e:
            print(f"  -> ERREUR sur {season}: {e}")

        time.sleep(0.6)

    print("Terminé.")


if __name__ == "__main__":
    main()
