import pandas as pd
import os
import glob


def advance_year(year, redshirt):
    year_mapping = {
        'HS': 'FR',
        'FR': 'SO',
        'SO': 'JR',
        'JR': 'SR',
        'SR': 'GRADUATED',
        'FR (RS)': 'SO (RS)',
        'SO (RS)': 'JR (RS)',
        'JR (RS)': 'SR (RS)',
        'SR (RS)': 'GRADUATED'
    }
    if redshirt:
        if 'RS' not in year:
            return f"{year} (RS)"
    return year_mapping.get(year, year)

def generate_roster(roster_df, recruits_df, school_name=None):

    # Apply the function to advance the year for each player
    roster_df['YEAR'] = roster_df.apply(lambda row: advance_year(row['YEAR'], row['REDSHIRT']), axis=1)

    # Filter the roster data to include only players who are not graduating or drafted or cut
    filtered_roster_df = roster_df[(roster_df['YEAR'] != 'GRADUATED') & (roster_df['CUT'] != True) & (roster_df['DRAFTED'].isna())].copy()

    # Filter the recruiting data to include only players committed to your school
    if not school_name:
        school_name = input("Enter the name of your school: ")
    recruits_df = recruits_df[recruits_df['COMMITTED TO'] == school_name.upper()].copy()

    # Advance the year for recruits from HS to FR
    recruits_df.loc[:, 'YEAR'] = recruits_df['YEAR'].apply(lambda year: advance_year(year, False))

    # Combine the filtered roster data with the recruits
    new_roster_df = pd.concat([filtered_roster_df, recruits_df], ignore_index=True)

    # Drop the specified columns
    columns_to_drop = ['STARS', 'GEM STATUS', 'COMMITTED TO', 'Unnamed: 8', 'CITY', 'STATE']
    new_roster_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Define the position order
    position_order = ['QB', 'HB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 'LE', 'RE', 'DT', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS', 'K', 'P', 'ATH']

    # Create a categorical type for the position column based on the defined order
    new_roster_df['POSITION'] = pd.Categorical(new_roster_df['POSITION'], categories=position_order, ordered=True)

    # Sort the roster by position and then by rating in descending order
    new_roster_df.sort_values(by=['POSITION', 'RATING'], ascending=[True, False], inplace=True)

    # Ensure the columns exist before setting their values
    for col in ['RATING', 'BASE RATING', 'VALUE', 'STATUS']:
        if col not in new_roster_df.columns:
            new_roster_df[col] = ""

    # Set the values of the specified columns to empty strings
    new_roster_df[['RATING', 'BASE RATING', 'VALUE', 'STATUS']] = ""

    # Ensure the columns exist before setting their values
    for col in ['REDSHIRT', 'CUT']:
        if col not in new_roster_df.columns:
            new_roster_df[col] = False

    # Set all REDSHIRT and CUT values to False
    new_roster_df[['REDSHIRT', 'CUT']] = False

    # Return the new roster
    return new_roster_df

def _to_csv(data_path, data_folder, new_path='New_Roster.csv'):
    roster_file = glob.glob(os.path.join(data_path, '*[Rr]oster.csv'))
    recruiting_file = glob.glob(os.path.join(data_path, '*[Rr]ecruiting*.csv'))
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    for roster_path in roster_file:
        roster_df = pd.read_csv(roster_path)
        recruiting_df = pd.read_csv(recruiting_file[0])
        new_roster_df = generate_roster(roster_df, recruiting_df)
        new_path = os.path.join(data_folder, new_path)
        new_roster_df.to_csv(new_path, index=False)
        print(f"Processed {roster_path}")
        print("New roster is now available in the data folder.")

def main():
    downloads_folder = os.path.expanduser('~/Downloads')
    data_folder = os.path.join(downloads_folder, 'cfb_dynasty_data')
    _to_csv(downloads_folder, data_folder)

if __name__ == "__main__":
    main()
