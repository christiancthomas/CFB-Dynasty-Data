import unittest
import os
import sys
import pandas as pd
import shutil

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.Player import Player
from utils.player_integration import create_hybrid_roster, sync_dataframe_with_players, dataframe_to_players, players_to_dataframe

class TestPlayerIntegration(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a sample CSV file
        self.csv_file = os.path.join(self.test_dir, "players.csv")
        self.create_sample_csv()

    def tearDown(self):
        # Remove the test directory and its contents
        shutil.rmtree(self.test_dir)

    def create_sample_csv(self):
        data = {
            "first_name": ["John", "Jane"],
            "last_name": ["Doe", "Smith"],
            "position": ["QB", "WR"],
            "year": ["FR", "SO"],
            "overall": [85, 90],
            "base_overall": [80, 85],
            "city": ["Los Angeles", "New York"],
            "state": ["CA", "NY"],
            "archetype": ["Pocket Passer", "Slot Receiver"],
            "dev_trait": ["Star", "Normal"],
            "cut": [False, False],
            "drafted": ["2023", "2024"],
            "redshirt": [False, False],
            "value": [50000, 60000],
            "status": ["Active", "Active"],
            "team": ["Team A", "Team B"],
            "national_rank": ["1", "2"],
            "stars": ["5", "4"],
            "gem_status": ["Blue", "Green"],
            "committed_to": ["College A", "College B"],
            "transfer": [False, False],
            "transferred": [False, False]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_file, index=False)

    def test_create_hybrid_roster(self):
        df, players = create_hybrid_roster(self.csv_file)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(players, list)
        self.assertTrue(all(isinstance(p, Player) for p in players))

    def test_sync_dataframe_with_players(self):
        df, players = create_hybrid_roster(self.csv_file)
        # Modify player data
        players[0].overall = 90
        sync_dataframe_with_players(df, players)
        self.assertEqual(df.iloc[0]["overall"], 90)

    def test_dataframe_to_players(self):
        df, players = create_hybrid_roster(self.csv_file)
        new_players = dataframe_to_players(df)
        self.assertEqual(len(players), len(new_players))
        self.assertTrue(all(p1 == p2 for p1, p2 in zip(players, new_players)))

    def test_players_to_dataframe(self):
        df, players = create_hybrid_roster(self.csv_file)
        new_df = players_to_dataframe(players)
        pd.testing.assert_frame_equal(df, new_df)