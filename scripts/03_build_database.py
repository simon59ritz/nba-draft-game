"""
Assemble tous les CSV bruts (data/raw/) en une base SQLite unique (data/nba.db).
Écrase les tables existantes à chaque exécution -> relance-le après chaque fetch.

Usage:
    python scripts/03_build_database.py
"""
import sqlite3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import RAW_DIR, DB_PATH

import pandas as pd


def main():
    conn = sqlite3.connect(DB_PATH)

    # --- Stats joueurs par saison ---
    season_files = sorted(RAW_DIR.glob("player_stats_*.csv"))
    if not season_files:
        print("Aucun fichier player_stats_*.csv trouvé. Lance d'abord 02_fetch_season_stats.py")
    else:
        df_all = pd.concat([pd.read_csv(f) for f in season_files], ignore_index=True)
        df_all.to_sql("player_season_stats", conn, if_exists="replace", index=False)
        print(f"player_season_stats -> {len(df_all)} lignes ({len(season_files)} saisons)")

    # --- Historique de la draft ---
    draft_file = RAW_DIR / "draft_history.csv"
    if draft_file.exists():
        df_draft = pd.read_csv(draft_file)
        df_draft.to_sql("draft_history", conn, if_exists="replace", index=False)
        print(f"draft_history -> {len(df_draft)} lignes")
    else:
        print("draft_history.csv introuvable. Lance d'abord 01_fetch_draft_history.py")

    conn.close()
    print(f"Base construite : {DB_PATH}")


if __name__ == "__main__":
    main()
