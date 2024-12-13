import pandas as pd

# Load the current roster data
roster_df = pd.read_csv('/Users/christianthomas/Developer/CFB-Dynasty-Data/USC Dynasty - Sheet11-2.csv')

# Filter out players who are graduating or cut
filtered_roster_df = roster_df[(roster_df['STATUS'] != 'GRADUATING') & (roster_df['CUT'] != True)]

# Define a function to advance the year
def advance_year(year, redshirt):
    year_mapping = {
        'HS': 'FR',
        'FR': 'SO',
        'FR (RS)': 'SO (RS)',
        'SO': 'JR',
        'SO (RS)': 'JR (RS)',
        'JR': 'SR',
        'JR (RS)': 'SR (RS)'
    }
    if redshirt:
        if 'RS' not in year:
            return f"{year} (RS)"
    return year_mapping.get(year, year)

# Apply the function to advance the year for each player
filtered_roster_df['YEAR'] = filtered_roster_df.apply(lambda row: advance_year(row['YEAR'], row['REDSHIRT']), axis=1)

# # Set all REDSHIRT values to False
# filtered_roster_df['REDSHIRT'] = False

# Print the first few rows to verify the changes
print(filtered_roster_df.head())

# Load the recruiting data
recruiting_df = pd.read_csv('/Users/christianthomas/Developer/CFB-Dynasty-Data/USC Dynasty - 2026 Recruiting Hub.csv')

# Filter the recruiting data to include only players committed to USC
usc_recruits_df = recruiting_df[recruiting_df['COMMITTED TO'] == 'USC'].copy()

# Advance the year for recruits from HS to FR
usc_recruits_df.loc[:, 'YEAR'] = usc_recruits_df['YEAR'].apply(lambda year: advance_year(year, False))

# Combine the filtered roster data with the USC recruits
new_roster_df = pd.concat([filtered_roster_df, usc_recruits_df], ignore_index=True)

# Drop the specified columns
columns_to_drop = ['STARS', 'GEM STATUS', 'COMMITTED TO', 'Unnamed: 8', 'CITY', 'STATE']
new_roster_df.drop(columns=columns_to_drop, inplace=True)

# Define the position order
position_order = ['QB', 'HB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 'LE', 'RE', 'DT', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS', 'K', 'P']

# Create a categorical type for the position column based on the defined order
new_roster_df['POSITION'] = pd.Categorical(new_roster_df['POSITION'], categories=position_order, ordered=True)

# Sort the roster by position and then by rating in descending order
new_roster_df.sort_values(by=['POSITION', 'RATING'], ascending=[True, False], inplace=True)

# Set the values of the specified columns to empty strings
new_roster_df[['RATING', 'BASE RATING', 'VALUE', 'STATUS']] = ""

# Set all REDSHIRT and CUT values to False
new_roster_df[['REDSHIRT', 'CUT']] = False

# Save the new roster to a CSV file
new_roster_df.to_csv('/Users/christianthomas/Developer/CFB-Dynasty-Data/2026 Roster Raw.csv', index=False)