from typing import List
import pandas as pd
from models.Player import Player

def create_hybrid_roster(csv_path: str):
    """Load CSV into both DataFrame and Player objects"""
    df = pd.read_csv(csv_path)
    players = [Player.from_dict(row) for _, row in df.iterrows()]
    return df, players

def sync_dataframe_with_players(df: pd.DataFrame, players: List[Player]):
    """Update DataFrame with changes from Player objects"""
    for i, player in enumerate(players):
        player_dict = player.to_dict()
        for col, value in player_dict.items():
            if col.upper().replace('_', ' ') in df.columns:
                df.iloc[i][col.upper().replace('_', ' ')] = value