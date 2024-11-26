
import pandas as pd

# Define the development trait multipliers
dev_trait_multipliers = {
    'NORMAL': 1.00,
    'IMPACT': 1.10,
    'STAR': 1.25,
    'ELITE': 1.50
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

# Define minimum and ideal roster sizes per position
position_requirements = {
    'QB': {'min': 3, 'ideal': 4},
    'HB': {'min': 4, 'ideal': 6},
    'FB': {'min': 0, 'ideal': 0},
    'WR': {'min': 6, 'ideal': 8},
    'TE': {'min': 3, 'ideal': 4},
    'LT': {'min': 3, 'ideal': 4},
    'LG': {'min': 3, 'ideal': 4},
    'C':  {'min': 3, 'ideal': 4},
    'RG': {'min': 3, 'ideal': 4},
    'RT': {'min': 3, 'ideal': 4},
    'LE': {'min': 3, 'ideal': 4},
    'RE': {'min': 3, 'ideal': 4},
    'DT': {'min': 3, 'ideal': 4},
    'LOLB': {'min': 3, 'ideal': 4},
    'MLB': {'min': 3, 'ideal': 4},
    'ROLB': {'min': 3, 'ideal': 4},
    'CB': {'min': 5, 'ideal': 7},
    'FS': {'min': 2, 'ideal': 3},
    'SS': {'min': 2, 'ideal': 3},
    'K': {'min': 1, 'ideal': 1},
    'P': {'min': 1, 'ideal': 1}
}

# Define the number of starters for each position
starters_count = {
    'QB': 1,
    'HB': 2,
    'FB': 1,
    'WR': 3,
    'TE': 1,
    'LT': 1,
    'LG': 1,
    'C': 1,
    'RG': 1,
    'RT': 1,
    'LE': 1,
    'RE': 1,
    'DT': 2,
    'LOLB': 1,
    'MLB': 1,
    'ROLB': 1,
    'CB': 2,
    'FS': 1,
    'SS': 1,
    'K': 1,
    'P': 1
}

# Define function to calculate player value with corrected multiplier logic
def calculate_player_value(row):
    dev_multiplier = dev_trait_multipliers.get(row['DEV TRAIT'], 1.00)
    remaining_dev_years = remaining_years.get(row['YEAR'], 0)
    value = round(row['RATING'] * dev_multiplier * (1 + remaining_dev_years / 4) * (1 - rs_discount), 2)
    return value

# Decide if player is safe, at risk, or on the cut list
def player_status(row):
    """Player status determines if a player is safe, at risk, or on the cut list based on their value.
    A few rules determine their status.
    1. If a player's year is 'SR' or 'SR (RS)', they are considered 'GRADUATING'.
    2. If a player's value is between 100 and 125, they are considered 'AT RISK'.
    3. If a player's value is less than 100, they are considered 'CUT'.
    4. If a player is the best at his position based on their ovr, he is always considered 'SAFE'."""

    value = row['Value']
    year = row['YEAR']
    best_at_position = row['Best at Position']

    if year in ['SR', 'SR (RS)']:
        return 'GRADUATING'
    elif best_at_position:
        return 'SAFE'
    elif value < 100:
        return 'CUT'
    elif value >= 100 and value <= 125:
        return 'AT RISK'
    else:
        return 'SAFE'

# Function to calculate position strength grade
def calculate_position_grade(avg_value):
    if avg_value >= 150:
        return 'A+'
    elif avg_value >= 140:
        return 'A'
    elif avg_value >= 130:
        return 'A-'
    elif avg_value >= 120:
        return 'B+'
    elif avg_value >= 110:
        return 'B'
    elif avg_value >= 100:
        return 'B-'
    elif avg_value >= 90:
        return 'C+'
    elif avg_value >= 80:
        return 'C'
    elif avg_value >= 70:
        return 'C-'
    else:
        return 'F'

# Function to calculate blended measure of starters and backups
def calculate_blended_measure(df, position):
    starters_num = starters_count.get(position, 1)
    position_df = df[df['POSITION'] == position].sort_values(by='Value', ascending=False)
    starters = position_df.head(starters_num)
    backups = position_df.tail(len(position_df) - starters_num)

    if len(starters) > 0:
        starters_avg = starters['Value'].mean()
    else:
        starters_avg = 0

    if len(backups) > 0:
        backups_avg = backups['Value'].mean()
    else:
        backups_avg = 0

    # Blended measure: 70% starters, 30% backups
    blended_value = round(0.7 * starters_avg + 0.3 * backups_avg, 2)
    return blended_value

# Main function to process the roster and create recruiting plan
def process_roster_and_create_recruiting_plan(roster_path):
    roster_df = pd.read_csv(roster_path)

    # Calculate player values
    roster_df['Value'] = roster_df.apply(calculate_player_value, axis=1)

    # Determine the best player at each position
    roster_df['Best at Position'] = roster_df.groupby('POSITION')['RATING'].transform(lambda x: x == x.max())

    # Apply player status function
    roster_df['Status'] = roster_df.apply(player_status, axis=1)

    # Drop the 'Best at Position' column
    roster_df.drop(columns=['Best at Position'], inplace=True)

    # Save the player values to a CSV file
    roster_df.to_csv('player_values_corrected.csv', index=False)

    # Calculate the number of players at each position for the next season
    next_season_counts = roster_df[roster_df['Status'] != 'GRADUATING'].groupby('POSITION').size()

    # Calculate the blended measure for each position
    blended_values = {position: calculate_blended_measure(roster_df, position) for position in position_requirements.keys()}

    # Debugging: Print lengths of arrays
    print(f"Positions: {len(position_requirements.keys())}")
    print(f"Next Season Counts: {len(next_season_counts)}")
    print(f"Blended Values: {len(blended_values)}")

    # Create the recruiting plan DataFrame
    recruiting_plan = pd.DataFrame({
        'Position': position_requirements.keys(),
        'Current Count': [next_season_counts.get(pos, 0) for pos in position_requirements.keys()],
        'Min Required': [position_requirements[pos]['min'] for pos in position_requirements.keys()],
        'Blended Value': [blended_values[pos] for pos in position_requirements.keys()],
        'Grade': [calculate_position_grade(blended_values[pos]) for pos in position_requirements.keys()]
    }).fillna(0)

    # Determine the priority level for recruiting at each position
    def determine_priority(row):
        if row['Current Count'] < row['Min Required']:
            return 'HIGH'
        elif row['Grade'] in ['D', 'F']:
            return 'HIGH'
        elif row['Grade'] in ['C']:
            return 'MEDIUM'
        else:
            return 'LOW'

    recruiting_plan['Priority'] = recruiting_plan.apply(determine_priority, axis=1)

    # Save the recruiting plan to a CSV file
    recruiting_plan.to_csv('recruiting_plan.csv', index=False)

    return roster_df, recruiting_plan

if __name__ == "__main__":
    roster_path = 'Texas Dynasty - 2034 Roster.csv'
    roster_df, recruiting_plan = process_roster_and_create_recruiting_plan(roster_path)

    print("Player valuations and statuses have been recalculated and saved to CSV.")
    print("Recruiting plan has been created and saved to CSV.")
