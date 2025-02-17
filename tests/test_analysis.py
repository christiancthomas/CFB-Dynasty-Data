# run with python -m unittest discover -s tests -p "test_*.py"
import unittest
import os
import pandas as pd
import shutil

from roster_analysis import calculate_player_value, player_status, calculate_position_grade, process_roster_and_create_recruiting_plan, calculate_blended_measure
import utils as u

class TestRosterAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.roster_data = u.create_mock_roster()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_calculate_player_value(self):
        print('test_analysis.calculate_player_value')
        # Define default base values for testing -- useful in case we ever update the values in the functional code
        dev_trait_multipliers = {
            'NORMAL': 1.00,
            'IMPACT': 1.10,
            'STAR': 1.25,
            'ELITE': 1.50
        }
        rs_discount = 0.05
        # roster calculation is ['BASE RATING'] * dev_multiplier * (1 + remaining_dev_years / 4) * (1 - rs_discount) to two decimal places

        # Add a few players to the roster for testing purposes
        roster_data = self.roster_data.copy()
        roster_data = u.add_player(roster_data, 'WR', 'CHASE', 'THOMAS', 'FR', 80, 82, 'STAR')
        roster_data = u.add_player(roster_data, 'TE', 'RILEY', 'CHILDERS', 'SO (RS)', 85, 82, 'NORMAL')
        roster_data = u.add_player(roster_data, 'LE', 'DARIAN', 'CHILDERS', 'JR (RS)', 94, 92, 'ELITE')

        # Apply calculate_player_value to each row
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1, dev_trait_multipliers=dev_trait_multipliers, rs_discount = rs_discount)

        # Assert known valuations
        # 1. Riley's value should be 116.85 as a SO (RS) with a base rating of 85 and a normal dev trait
        self.assertEqual(roster_data.loc[(roster_data['FIRST NAME'] == 'RILEY') & (roster_data['LAST NAME'] == 'CHILDERS'), 'VALUE'].values[0], 116.85)

        # 2. All else equal, younger players should have higher valuations due to having more remaining years. If we changed Riley to a FR,
        # his value should be higher than his valuation as a SO (RS)
        roster_data.loc[(roster_data['FIRST NAME'] == 'RILEY') & (roster_data['LAST NAME'] == 'CHILDERS'), 'YEAR'] = 'FR'
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1, dev_trait_multipliers=dev_trait_multipliers, rs_discount = rs_discount)
        self.assertGreater(roster_data.loc[(roster_data['FIRST NAME'] == 'RILEY') & (roster_data['LAST NAME'] == 'CHILDERS'), 'VALUE'].values[0], 116.85)

        # 3. Redshirt players should have a 5% discount to their value. If we change Darian to a true JR, his value should be slightly hihger than his
        # value as a redshirt JR (163.88)
        roster_data.loc[(roster_data['FIRST NAME'] == 'DARIAN') & (roster_data['LAST NAME'] == 'CHILDERS'), 'YEAR'] = 'JR'
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1, dev_trait_multipliers=dev_trait_multipliers, rs_discount = rs_discount)
        self.assertGreater(roster_data.loc[(roster_data['FIRST NAME'] == 'DARIAN') & (roster_data['LAST NAME'] == 'CHILDERS'), 'VALUE'].values[0], 163.88)

        # 4. Dev trait multipliers should also affect value. If we change Chase to an elite dev trait, his value should be higher than his value as a star
        # (179.38)
        roster_data.loc[(roster_data['FIRST NAME'] == 'CHASE') & (roster_data['LAST NAME'] == 'THOMAS'), 'DEV TRAIT'] = 'ELITE'
        roster_data['VALUE'] = roster_data.apply(calculate_player_value, axis=1, dev_trait_multipliers=dev_trait_multipliers, rs_discount = rs_discount)
        self.assertGreater(roster_data.loc[(roster_data['FIRST NAME'] == 'CHASE') & (roster_data['LAST NAME'] == 'THOMAS'), 'VALUE'].values[0], 179.38)
