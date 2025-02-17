# run with python -m unittest discover -s tests -p "test_*.py"
import unittest
import os
import pandas as pd
import shutil
import subprocess

from new_roster import generate_roster, _to_csv

DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")
MOCK_ROSTER_FILE = os.path.join(DOWNLOADS_FOLDER, "Test_Roster.csv")
MOCK_RECRUITING_FILE = os.path.join(DOWNLOADS_FOLDER, "Test_Recruiting_Hub.csv")
OUTPUT_DIR = os.path.join(DOWNLOADS_FOLDER, "test_cfb_dynasty_data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Test_New_Roster.csv")
ROSTER_ANALYSIS_SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "roster_analysis.py")

class TestRosterScripts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create mock roster CSV
        print('creating mock roster\n')
        roster_data = {
            'POSITION': ['QB', 'FS', 'ROLB', 'CB'],
            'FIRST NAME': ['CHRISTIAN', 'KALLUM', 'SAM', 'TYLOR'],
            'LAST NAME': ['THOMAS', 'GRIFFIN', 'VEGA', 'RUSSELL'],
            'YEAR': ['FR', 'SO (RS)', 'SR', 'SO (RS)'],
            'RATING': [91, 90, 92, 72],
            'BASE RATING': [88, 89, 90, 69],
            'DEV TRAIT': ['ELITE', 'STAR', 'IMPACT', 'NORMAL'],
            'VALUE': ['', '', '', ''],
            'STATUS': ['ACTIVE', 'ACTIVE', 'GRADUATING', 'ACTIVE'],
            'CUT': [False, False, False, True],
            'REDSHIRT': [False, True, False, False],
            'DRAFTED': [None, None, None, None]
        }

        # Create mock recruiting CSV
        print('creating mock recruiting board\n')
        recruiting_data = {
            'POSITION': ['QB', 'FS', 'CB'],
            'FIRST NAME': ['JACK', 'JAMES', 'ORION'],
            'LAST NAME': ['SMITH', 'JOHNSON', 'GREENWOOD'],
            'YEAR': ['HS', 'HS', 'HS'],
            'DEV TRAIT': ['NORMAL', 'STAR', 'ELITE'],
            'STARS': [4, 5, 4],
            'GEM STATUS': ['NORMAL', 'BUST', 'GEM'],
            'COMMITTED TO': ['USC', 'TEXAS A&M', 'TEXAS TECH'],
            'CITY': ['LOS ANGELES', 'DALLAS', 'KILLEEN'],
            'STATE': ['CA', 'TX', 'TX']
        }
        pd.DataFrame(roster_data).to_csv(MOCK_ROSTER_FILE, index=False)
        pd.DataFrame(recruiting_data).to_csv(MOCK_RECRUITING_FILE, index=False)


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
        roster_df = pd.read_csv(MOCK_ROSTER_FILE)
        recruiting_df = pd.read_csv(MOCK_RECRUITING_FILE)
        new_roster_df = generate_roster(roster_df, recruiting_df, 'TEXAS TECH')
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        new_roster_df.to_csv(OUTPUT_FILE, index=False)
        self.assertTrue(os.path.exists(OUTPUT_FILE))

    def test_incoming_recruits(self):
        # test that only incoming recruits from school = school_name are included in the new roster
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

    def test_analyze_roster(self):
        # Run the roster_analysis.py script as a subprocess
        result = subprocess.run(["python3", ROSTER_ANALYSIS_SCRIPT, OUTPUT_FILE], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=f"Script failed with output: {result.stdout}\n{result.stderr}")
        # Add assertions to check the expected output files

if __name__ == '__main__':
    unittest.main()