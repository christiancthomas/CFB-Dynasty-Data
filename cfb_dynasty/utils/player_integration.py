"""Player integration utilities for CFB Dynasty Data system."""

from typing import List
import pandas as pd
from ..models.player import Player


def create_hybrid_roster(csv_path: str):
    """Load CSV into both DataFrame and Player objects."""
    df = pd.read_csv(csv_path)
    players = [Player.from_dict(row) for _, row in df.iterrows()]
    return df, players


def sync_dataframe_with_players(df: pd.DataFrame, players: List[Player]):
    """Update DataFrame with changes from Player objects."""
    print(f"df columns: {df.columns.tolist()}")
    for i, player in enumerate(players):
        player_dict = player.to_dict()
        for col, value in player_dict.items():
            if col.upper().replace('_', ' ') in df.columns:
                df.iloc[i][col.upper().replace('_', ' ')] = value


def dataframe_to_players(df: pd.DataFrame) -> List[Player]:
    """Convert DataFrame rows to Player objects."""
    players = []
    for _, row in df.iterrows():
        player_data = row.to_dict()
        player = Player.from_dict(player_data)
        players.append(player)
    return players


def players_to_dataframe(players: List[Player]) -> pd.DataFrame:
    """Convert Player objects to a DataFrame."""
    data = [player.to_dict() for player in players]
    return pd.DataFrame(data)
