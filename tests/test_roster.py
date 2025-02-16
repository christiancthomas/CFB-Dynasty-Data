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
        # roster_df = pd.DataFrame(roster_data)
        # roster_df.to_csv(MOCK_ROSTER_FILE, index=False)

        # Create mock recruiting CSV
        recruiting_data = {
            'POSITION': ['QB', 'FS'],
            'FIRST NAME': ['JACK', 'JAMES'], 
            'LAST NAME': ['SMITH', 'JOHNSON'], 
            'YEAR': ['HS', 'HS'], 
            'RATING': [85, 87], 
            'BASE RATING': [83, 85],
            'DEV TRAIT': ['NORMAL', 'STAR'], 
            'VALUE': ['', ''],
            'STATUS': ['ACTIVE', 'ACTIVE'],
            'CUT': [False, False],
            'REDSHIRT': [False, False],
            'DRAFTED': [None, None],
            'COMMITTED TO': ['USC', 'USC']
        }
        # recruiting_df = pd.DataFrame(recruiting_data)
        # recruiting_df.to_csv(MOCK_RECRUITING_FILE, index=False)
        pd.DataFrame(roster_data).to_csv(MOCK_ROSTER_FILE, index=False)
        pd.DataFrame(recruiting_data).to_csv(MOCK_RECRUITING_FILE, index=False)

    # @classmethod
    # def tearDownClass(cls):
    #     # Remove mock CSV files
    #     os.remove(MOCK_ROSTER_FILE)
    #     print(f"Removed {MOCK_ROSTER_FILE}")
    #     os.remove(MOCK_RECRUITING_FILE)
    #     print(f"Removed {MOCK_RECRUITING_FILE}")
    #     if os.path.exists(OUTPUT_FILE):
    #         os.remove(OUTPUT_FILE)
    #         print(f"Removed {OUTPUT_FILE}")
    #     if os.path.exists(OUTPUT_DIR):
    #         shutil.rmtree(OUTPUT_DIR)
    #         print(f"Removed {OUTPUT_DIR}")

    def test_generate_roster(self):
        roster_df = pd.read_csv(MOCK_ROSTER_FILE)
        recruiting_df = pd.read_csv(MOCK_RECRUITING_FILE)
        new_roster_df = generate_roster(roster_df, recruiting_df)
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        new_roster_df.to_csv(OUTPUT_FILE, index=False)
        print("generated roster")
        print(f"Output file: {OUTPUT_FILE}")
        print(os.path.exists(OUTPUT_FILE))
        self.assertTrue(os.path.exists(OUTPUT_FILE))

    def test_analyze_roster(self):
        # Run the roster_analysis.py script as a subprocess
        result = subprocess.run(["python3", ROSTER_ANALYSIS_SCRIPT, OUTPUT_FILE], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=f"Script failed with output: {result.stdout}\n{result.stderr}")
        # Add assertions to check the expected output files

if __name__ == '__main__':
    unittest.main()