
import pandas as pd

# Define the development trait multipliers
dev_trait_multipliers = {
    'NORMAL': 1.00,
    'IMPACT': 1.10,
    'STAR': 1.2,
    'ELITE': 1.3
}

# Define the remaining years of development for different player years
remaining_years = {
    'FR': 3,
    'SO': 2,
    'JR': 1,
    'SR': 0,
    'FR (RS)': 3,  # Redshirt Freshman
    'SO (RS)': 2,  # Redshirt Sophomore
    'JR (RS)': 1,  # Redshirt Junior
    'SR (RS)': 0   # Redshirt Senior
}

# Define the redshirt discount
rs_discount = 0.05

# Define function to calculate player value with corrected multiplier logic
def calculate_player_value(row):
    ovr = row['OVR']
    dev_trait = row['DEV TRAIT']
    year = row['YEAR']

    # Get the correct multiplier for dev trait
    dev_multiplier = dev_trait_multipliers.get(dev_trait, 1.0)

    # Get the remaining years of development based on the player's year
    years_remaining = remaining_years.get(year, 0)

    # Apply the redshirt discount if applicable
    redshirted = 'RS' in year
    discount = rs_discount if redshirted else 0

    # Calculate the player value using the corrected dev trait multiplier
    player_value = round(ovr * dev_multiplier * (1 + years_remaining / 4) * (1 - discount), 2)
    return player_value

# Main function to process the roster
def process_roster(roster_path):
    roster_df = pd.read_csv(roster_path)

    # Calculate player values using the corrected function
    roster_df['Value'] = roster_df.apply(calculate_player_value, axis=1)

    # Save the results to a CSV file
    roster_df.to_csv('player_values_corrected.csv', index=False)

    return roster_df

if __name__ == "__main__":
    roster_path = 'UCLA Dynasty - 2030 Roster.csv'
    roster_df = process_roster(roster_path)

    print("Player valuations have been recalculated and saved to CSV.")
