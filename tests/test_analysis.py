# run with python3 -m unittest discover -s tests -p "test_*.py"
import unittest
import os
import pandas as pd

import tempfile
from cfb_dynasty.config.constants import DEV_TRAIT_MULTIPLIERS, RS_DISCOUNT
from cfb_dynasty.analysis.roster_analysis import calculate_player_value, process_roster_and_create_recruiting_plan
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


class TestProcessRosterRawCsv(unittest.TestCase):
    """Tests for process_roster_and_create_recruiting_plan with raw CSV data."""

    def test_process_raw_csv_with_overall_columns(self):
        """Test that raw CSV with OVERALL/BASE OVERALL columns is processed correctly."""
        # Create raw CSV data like what comes from Google Sheets
        raw_data = pd.DataFrame({
            'REDSHIRT': ['', '', 'RS'],
            'FIRST NAME': ['Arch', 'Jeremiah', 'Quinn'],
            'LAST NAME': ['Manning', 'Smith', 'Ewers'],
            'YEAR': ['FR', 'SO', 'JR (RS)'],
            'POSITION': ['QB', 'WR', 'QB'],
            'OVERALL': [78, 85, 92],
            'BASE OVERALL': [76, 83, 90],
            'CITY': ['New Orleans', 'Dallas', 'Austin'],
            'STATE': ['LA', 'TX', 'TX'],
            'ARCHETYPE': ['Field General', 'Deep Threat', 'Improviser'],
            'DEV TRAIT': ['ELITE', 'STAR', 'STAR']
        })

        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            raw_data.to_csv(f, index=False)
            temp_path = f.name

        try:
            # Process the raw CSV
            processed_roster, recruiting_plan = process_roster_and_create_recruiting_plan(temp_path)

            # Verify data was processed
            self.assertEqual(len(processed_roster), 3)
            self.assertIn('VALUE', processed_roster.columns)
            self.assertIn('STATUS', processed_roster.columns)

            # Verify VALUE was computed (should be numeric, not None)
            self.assertTrue(all(processed_roster['VALUE'].notna()))
            self.assertTrue(all(processed_roster['VALUE'] > 0))

            # Verify extra columns were preserved
            self.assertIn('CITY', processed_roster.columns)
            self.assertIn('STATE', processed_roster.columns)

            # Verify recruiting plan was created
            self.assertGreater(len(recruiting_plan), 0)
            self.assertIn('Position', recruiting_plan.columns)
            self.assertIn('Priority', recruiting_plan.columns)

        finally:
            os.unlink(temp_path)

    def test_process_raw_csv_without_optional_columns(self):
        """Test that raw CSV without CUT/DRAFTED/REDSHIRT columns still works."""
        # Minimal CSV with only required columns
        raw_data = pd.DataFrame({
            'FIRST NAME': ['Test', 'Player'],
            'LAST NAME': ['One', 'Two'],
            'YEAR': ['FR', 'SO (RS)'],
            'POSITION': ['QB', 'WR'],
            'OVERALL': [80, 85],
            'BASE OVERALL': [78, 83],
            'ARCHETYPE': ['Pocket Passer', 'Route Runner'],
            'DEV TRAIT': ['STAR', 'NORMAL']
        })

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            raw_data.to_csv(f, index=False)
            temp_path = f.name

        try:
            processed_roster, recruiting_plan = process_roster_and_create_recruiting_plan(temp_path)

            # Verify optional columns were added with defaults
            self.assertIn('CUT', processed_roster.columns)
            self.assertIn('DRAFTED', processed_roster.columns)
            self.assertIn('REDSHIRT', processed_roster.columns)

            # Verify REDSHIRT was inferred from YEAR
            # Player Two has "SO (RS)" so should have REDSHIRT=True
            player_two = processed_roster[processed_roster['FIRST NAME'] == 'Player']
            self.assertTrue(player_two['REDSHIRT'].values[0])

            # Player One has "FR" so should have REDSHIRT=False
            player_one = processed_roster[processed_roster['FIRST NAME'] == 'Test']
            self.assertFalse(player_one['REDSHIRT'].values[0])

        finally:
            os.unlink(temp_path)

    def test_process_csv_missing_required_columns_raises_error(self):
        """Test that CSV missing required columns raises ValueError."""
        # CSV missing OVERALL column
        raw_data = pd.DataFrame({
            'FIRST NAME': ['Test'],
            'LAST NAME': ['Player'],
            'YEAR': ['FR'],
            'POSITION': ['QB'],
            # Missing: OVERALL, BASE OVERALL, ARCHETYPE, DEV TRAIT
        })

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            raw_data.to_csv(f, index=False)
            temp_path = f.name

        try:
            with self.assertRaises(ValueError) as context:
                process_roster_and_create_recruiting_plan(temp_path)

            self.assertIn('missing required columns', str(context.exception))

        finally:
            os.unlink(temp_path)
