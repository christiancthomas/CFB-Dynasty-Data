"""holds utility scripts to setup tests"""

import pandas as pd

def create_mock_roster():
    "returns a pandas DataFrame of mock roster data"
    roster_data = {
            'POSITION': ['QB', 'FS', 'ROLB', 'CB'],
            'FIRST NAME': ['CHRISTIAN', 'KALLUM', 'SAM', 'CHASE'],
            'LAST NAME': ['THOMAS', 'GRIFFIN', 'VEGA', 'THOMAS'],
            'YEAR': ['JR', 'SO (RS)', 'SR', 'FR'],
            'OVERALL': [91, 90, 92, 75],
            'BASE OVERALL': [88, 89, 90, 72],
            'CITY': ['ROUND ROCK', 'DALLAS', 'COPPERAS COVE', 'SAN ANTONIO'],
            'STATE': ['TX', 'TX', 'TX', 'TX'],
            'ARCHETYPE': ['DUAL THREAT', 'HYBRID', 'POWER RUSHER', 'BUMP AND RUN'],
            'DEV TRAIT': ['ELITE', 'STAR', 'IMPACT', 'NORMAL'],
            'VALUE': ['', '', '', ''],
            'STATUS': ['ACTIVE', 'ACTIVE', 'GRADUATING', 'ACTIVE'],
            'CUT': [False, False, False, True],
            'REDSHIRT': [False, False, False, True],
            'DRAFTED': [None, None, None, None]
        }
    return pd.DataFrame(roster_data)

def create_mock_recruits():
    "returns a pandas DataFrame of mock recruiting data"
    recruiting_data = {
            'POSITION': ['QB', 'FS', 'CB'],
            'FIRST NAME': ['JACK', 'JAMES', 'ORION'],
            'LAST NAME': ['SMITH', 'JOHNSON', 'GREENWOOD'],
            'ARCHETYPE': ['FIELD GENERAL', 'ZONE', 'SLOT'],
            'YEAR': ['HS', 'HS', 'HS'],
            'DEV TRAIT': ['NORMAL', 'STAR', 'ELITE'],
            'STARS': [4, 5, 4],
            'GEM STATUS': ['NORMAL', 'BUST', 'GEM'],
            'COMMITTED TO': ['USC', 'TEXAS A&M', 'TEXAS TECH'],
            'CITY': ['LOS ANGELES', 'DALLAS', 'KILLEEN'],
            'STATE': ['CA', 'TX', 'TX']
        }
    return pd.DataFrame(recruiting_data)

def add_player(roster_df, position=None, first_name=None, last_name=None,
               year=None, overall=None, base_overall=None, dev_trait=None,
               value=None, status=None, cut=False, redshirt=False, drafted=None):
    "adds a player to the roster DataFrame"
    player = pd.DataFrame({
        'POSITION': [position],
        'FIRST NAME': [first_name],
        'LAST NAME': [last_name],
        'YEAR': [year],
        'OVERALL': [overall],
        'BASE OVERALL': [base_overall],
        'DEV TRAIT': [dev_trait],
        'VALUE': [value],
        'STATUS': [status],
        'CUT': [cut],
        'REDSHIRT': [redshirt],
        'DRAFTED': [drafted]
    })
    return pd.concat([roster_df, player], ignore_index=True)