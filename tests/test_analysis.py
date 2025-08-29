# run with python3 -m unittest discover -s tests -p "test_*.py"
import unittest
import os
import pandas as pd

from cfb_dynasty.config.constants import DEV_TRAIT_MULTIPLIERS, RS_DISCOUNT
from cfb_dynasty.analysis.roster_analysis import calculate_player_value
from tests.utils import create_mock_roster, create_mock_recruits, add_player

class TestRosterAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.roster_data = create_mock_roster()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_calculate_player_value(self):
        print('test_analysis.calculate_player_value')
        # Add a few players to the roster for testing purposes
        roster_data = self.roster_data.copy()
        roster_data = add_player(roster_data, 'WR', 'CAMERON', 'THOMAS', 'FR', 80, 82, 'STAR')
        roster_data = add_player(roster_data, 'TE', 'RILEY', 'CHILDERS', 'SO (RS)', 85, 82, 'NORMAL')
        roster_data = add_player(roster_data, 'LE', 'DARIAN', 'CHILDERS', 'JR (RS)', 94, 92, 'ELITE')

        # Apply calculate_player_value to each row
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1)

        # Assert known valuations
        # 1. Riley's value should be 116.85 as a SO (RS) with a base rating of 85 and a normal dev trait
        self.assertEqual(roster_data.loc[(roster_data['FIRST NAME'] == 'RILEY') & (roster_data['LAST NAME'] == 'CHILDERS'), 'VALUE'].values[0], 116.85)

        # 2. All else equal, younger players should have higher valuations due to having more remaining years. If we changed Riley to a FR,
        # his value should be higher than his valuation as a SO (RS)
        roster_data.loc[(roster_data['FIRST NAME'] == 'RILEY') & (roster_data['LAST NAME'] == 'CHILDERS'), 'YEAR'] = 'FR'
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1)
        self.assertGreater(roster_data.loc[(roster_data['FIRST NAME'] == 'RILEY') & (roster_data['LAST NAME'] == 'CHILDERS'), 'VALUE'].values[0], 116.85)

        # 3. Redshirt players should have a 5% discount to their value. If we change Darian to a true JR, his value should be slightly hihger than his
        # value as a redshirt JR (163.88)
        roster_data.loc[(roster_data['FIRST NAME'] == 'DARIAN') & (roster_data['LAST NAME'] == 'CHILDERS'), 'YEAR'] = 'JR'
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1)
        self.assertGreater(roster_data.loc[(roster_data['FIRST NAME'] == 'DARIAN') & (roster_data['LAST NAME'] == 'CHILDERS'), 'VALUE'].values[0], 163.88)

        # 4. Dev trait multipliers should also affect value. If we change Chase to an elite dev trait, his value should be higher than his value as a star
        # (179.38)
        roster_data.loc[(roster_data['FIRST NAME'] == 'CAMERON') & (roster_data['LAST NAME'] == 'THOMAS'), 'DEV TRAIT'] = 'ELITE'
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1)
        self.assertGreater(roster_data.loc[(roster_data['FIRST NAME'] == 'CAMERON') & (roster_data['LAST NAME'] == 'THOMAS'), 'VALUE'].values[0], 179.38)
