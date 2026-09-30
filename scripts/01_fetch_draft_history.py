"""
Télécharge l'historique complet de la draft NBA (une seule requête couvre toutes les années,
y compris la plus récente dès qu'elle est publiée officiellement).

Usage:
    python scripts/01_fetch_draft_history.py
"""
import sys
from pathlib import Path

from config import RAW_DIR

from nba_api.stats.endpoints import drafthistory


def main():
    print("Téléchargement de l'historique de la draft...")
    dh = drafthistory.DraftHistory()
    df = dh.get_data_frames()[0]

    out_path = RAW_DIR / "draft_history.csv"
    df.to_csv(out_path, index=False)
    print(f"OK -> {out_path} ({len(df)} lignes, jusqu'à la saison {df['SEASON'].max()})")


if __name__ == "__main__":
    main()
