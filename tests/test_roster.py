# run with python -m unittest discover -s tests -p "test_*.py"
import unittest
import os
import pandas as pd
import shutil
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfb_dynasty.data.roster_generator import generate_roster
from tests.utils import create_mock_roster, create_mock_recruits

DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")
MOCK_ROSTER_FILE = os.path.join(DOWNLOADS_FOLDER, "Test_Roster.csv")
MOCK_RECRUITING_FILE = os.path.join(DOWNLOADS_FOLDER, "Test_Recruiting_Hub.csv")
OUTPUT_DIR = os.path.join(DOWNLOADS_FOLDER, "test_cfb_dynasty_data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Test_New_Roster.csv")

class TestRosterScripts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create mock roster CSV
        roster_data = create_mock_roster()

        # Create mock recruiting CSV
        recruiting_data = create_mock_recruits()

        # Save mock CSV files
        roster_data.to_csv(MOCK_ROSTER_FILE, index=False)
        recruiting_data.to_csv(MOCK_RECRUITING_FILE, index=False)

    @classmethod
    def tearDownClass(cls):
        # Remove mock CSV files
        if os.path.exists(MOCK_ROSTER_FILE):
            os.remove(MOCK_ROSTER_FILE)
        if os.path.exists(MOCK_RECRUITING_FILE):
            os.remove(MOCK_RECRUITING_FILE)
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)

    def test_generate_roster(self):
        """Test that the generate_roster function works correctly with updated column logic"""
        print("test_roster.generate_roster")

        roster_df = pd.read_csv(MOCK_ROSTER_FILE)
        recruiting_df = pd.read_csv(MOCK_RECRUITING_FILE)

        # Test roster generation
        new_roster_df = generate_roster(roster_df, recruiting_df, 'TEXAS TECH')

        # Create output directory if needed
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # Save the result
        new_roster_df.to_csv(OUTPUT_FILE, index=False)

        # Test that output file was created
        self.assertTrue(os.path.exists(OUTPUT_FILE))

        # Test that the DataFrame has the correct column structure
        expected_columns = [
            'REDSHIRT', 'FIRST NAME', 'LAST NAME', 'YEAR', 'POSITION', 'OVERALL',
            'BASE OVERALL', 'CITY', 'STATE', 'ARCHETYPE', 'DEV TRAIT', 'CUT',
            'TRANSFER OUT', 'DRAFTED', 'VALUE', 'STATUS'
        ]

        self.assertEqual(list(new_roster_df.columns), expected_columns)

        # Test that specific columns have been reset to default values
        self.assertTrue(all(new_roster_df['REDSHIRT'] == ""))
        self.assertTrue(all(new_roster_df['CUT'] == False))
        self.assertTrue(all(new_roster_df['OVERALL'] == ""))
        self.assertTrue(all(new_roster_df['BASE OVERALL'] == ""))
        self.assertTrue(all(new_roster_df['DRAFTED'] == ""))
        self.assertTrue(all(new_roster_df['VALUE'] == ""))
        self.assertTrue(all(new_roster_df['STATUS'] == ""))

        # Test that we have some players (roster + recruits - filtered out players)
        self.assertGreater(len(new_roster_df), 0)

    def test_player_filtering(self):
        """Test that players are correctly filtered out based on graduation, cut, drafted, transfer out"""
        print("test_roster.player_filtering")

        # Create a custom roster with players that should be filtered out
        test_roster_data = {
            'FIRST NAME': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
            'LAST NAME': ['Doe', 'Smith', 'Brown', 'Wilson', 'Johnson'],
            'POSITION': ['QB', 'RB', 'WR', 'TE', 'OL'],
            'YEAR': ['FR', 'SO', 'SR', 'JR', 'SO'],
            'OVERALL': ['80', '85', '90', '82', '78'],
            'BASE OVERALL': ['78', '83', '88', '80', '76'],
            'CITY': ['Dallas', 'Houston', 'Austin', 'Tyler', 'Plano'],
            'STATE': ['TX', 'TX', 'TX', 'TX', 'TX'],
            'ARCHETYPE': ['Dual Threat', 'Power Back', 'Speed', 'Possession', 'Pass Pro'],
            'DEV TRAIT': ['Star', 'Normal', 'Impact', 'Elite', 'Normal'],
            'CUT': [False, True, False, False, False],  # Jane should be filtered
            'DRAFTED': ['', '', 'NFL', '', ''],  # Bob should be filtered
            'REDSHIRT': [False, False, False, False, False],
            'VALUE': ['100', '120', '150', '110', '90'],
            'STATUS': ['Active', 'Active', 'Active', 'Active', 'Active'],
            'TEAM': ['TTU', 'TTU', 'TTU', 'TTU', 'TTU'],
            'NATIONAL RANKING': ['100', '200', '50', '150', '300'],
            'STARS': ['4', '3', '5', '4', '3'],
            'GEM STATUS': ['Normal', 'Normal', 'Blue', 'Normal', 'Normal'],
            'COMMITTED TO': ['TTU', 'TTU', 'TTU', 'TTU', 'TTU'],
            'TRANSFER OUT': [False, False, False, True, False]  # Alice should be filtered
        }

        test_roster_df = pd.DataFrame(test_roster_data)

        # Create minimal recruiting data
        recruiting_data = create_mock_recruits()

        # Generate roster
        new_roster_df = generate_roster(test_roster_df, recruiting_data, 'TEXAS TECH')

        # Check that filtered players are not in the result
        player_names = list(new_roster_df['FIRST NAME'] + ' ' + new_roster_df['LAST NAME'])

        self.assertNotIn('Jane Smith', player_names)  # Cut player
        self.assertNotIn('Bob Brown', player_names)   # Drafted player
        self.assertNotIn('Alice Wilson', player_names) # Transfer out player

        # Check that remaining players are present + recruits
        self.assertIn('John Doe', player_names)      # Should remain
        self.assertIn('Charlie Johnson', player_names) # Should remain


    @classmethod
    def tearDownClass(cls):
        # Remove mock CSV files
        os.remove(MOCK_ROSTER_FILE)
        os.remove(MOCK_RECRUITING_FILE)
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)

    def test_generate_roster(self):
        print("test_roster.generate_roster")
        roster_df = pd.read_csv(MOCK_ROSTER_FILE)
        recruiting_df = pd.read_csv(MOCK_RECRUITING_FILE)
        new_roster_df = generate_roster(roster_df, recruiting_df, 'TEXAS TECH')
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        new_roster_df.to_csv(OUTPUT_FILE, index=False)
        self.assertTrue(os.path.exists(OUTPUT_FILE))

    def test_incoming_recruits(self):
        # test that only incoming recruits from school = school_name are included in the new roster
        print("test_roster.test_incoming_recruits")
        roster_df = pd.read_csv(MOCK_ROSTER_FILE)
        recruiting_df = pd.read_csv(MOCK_RECRUITING_FILE)
        school_name = 'TEXAS TECH'
        new_roster_df = generate_roster(roster_df, recruiting_df, school_name)

        # collect a list of the first and last names of all the recruits who committed to school_name in the recruiting_df
        committed_recruits = recruiting_df[recruiting_df['COMMITTED TO'] == school_name.upper()][['FIRST NAME', 'LAST NAME']]
        non_commits = recruiting_df[recruiting_df['COMMITTED TO'] != school_name.upper()][['FIRST NAME', 'LAST NAME']]

        # check that the only recruits from the recruiting_df who are in the new_roster_df are the ones who committed to school_name using first and last names and additionally none of the non_commits made it into the new_roster_df
        for _, recruit in committed_recruits.iterrows():
            self.assertTrue(((new_roster_df['FIRST NAME'] == recruit['FIRST NAME']) & (new_roster_df['LAST NAME'] == recruit['LAST NAME'])).any())

        # Check that no non-committed recruits are in the new roster
        for _, recruit in non_commits.iterrows():
            self.assertFalse(((new_roster_df['FIRST NAME'] == recruit['FIRST NAME']) & (new_roster_df['LAST NAME'] == recruit['LAST NAME'])).any())

    def test_archetype(self):
        # test that the archetype column is correctly populated for returning players and incoming recruits
        print("test_roster.test_archetype")
        roster_df = pd.read_csv(MOCK_ROSTER_FILE)
        recruiting_df = pd.read_csv(MOCK_RECRUITING_FILE)
        school_name = 'TEXAS TECH'
        new_roster_df = generate_roster(roster_df, recruiting_df, school_name)

        # test that orion greenwood is a slot archetype
        orion = new_roster_df[(new_roster_df['FIRST NAME'] == 'ORION') & (new_roster_df['LAST NAME'] == 'GREENWOOD')]
        self.assertEqual(orion['ARCHETYPE'].values[0], 'SLOT')

        # test that christian thomas has a dual threat archetype (from mock data)
        christian = new_roster_df[(new_roster_df['FIRST NAME'] == 'CHRISTIAN') & (new_roster_df['LAST NAME'] == 'THOMAS')]
        self.assertEqual(christian['ARCHETYPE'].values[0], 'DUAL THREAT')
