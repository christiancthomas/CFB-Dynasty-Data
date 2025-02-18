import pandas as pd
import glob
import os

# Define minimum and ideal roster sizes per position
default_position_requirements = {
    'QB': {'min': 3, 'ideal': 4, 'archetypes': {'FIELD GENERAL': 1, 'IMPROVISER': 0.75, 'SCRAMBLER': 0.25}},
    'HB': {'min': 4, 'ideal': 6, 'archetypes': {'ELUSIVE BACK': 0.75, 'POWER BACK': 0.75, 'RECEIVING BACK': 0.5}},
    'FB': {'min': 0, 'ideal': 0, 'archetypes': {'UTILITY': 0, 'BLOCKING': 0}},
    'WR': {'min': 6, 'ideal': 8, 'archetypes': {'DEEP THREAT': 0.75, 'PHYSICAL': 0.75, 'ROUTE RUNNER': 0.75}},
    'TE': {'min': 3, 'ideal': 4, 'archetypes': {'VERTICAL THREAT': 1, 'POSSESSION': 0.25, 'BLOCKING': 0.25}},
    'LT': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 1, 'AGILE': 0.8, 'POWER': 0.6}},
    'LG': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.6, 'AGILE': 1, 'POWER': 1}},
    'C':  {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.5, 'AGILE': 1, 'POWER': 1}},
    'RG': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.6, 'AGILE': 1, 'POWER': 1}},
    'RT': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.8, 'AGILE': 0.8, 'POWER': 0.75}},
    'LE': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 0.9, 'SPEED RUSHER': 0.9, 'RUN STOPPER': 1}},
    'RE': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 0.9, 'SPEED RUSHER': 1, 'RUN STOPPER': 1}},
    'DT': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 0.9, 'SPEED RUSHER': 0.8, 'RUN STOPPER': 1}},
    'LOLB': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 1, 'RUN STOPPER': 1, 'PASS COVERAGE': 0.1}},
    'MLB': {'min': 3, 'ideal': 4, 'archetypes': {'FIELD GENERAL': 1, 'RUN STOPPER': 1, 'PASS COVERAGE': 1}},
    'ROLB': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 1, 'RUN STOPPER': 1, 'PASS COVERAGE': 0.1}},
    'CB': {'min': 5, 'ideal': 7, 'archetypes': {'MAN TO MAN': 1, 'ZONE': 0.75, 'SLOT': 0.5}},
    'FS': {'min': 2, 'ideal': 3, 'archetypes': {'ZONE': 1, 'HYBRID': 0.75, 'RUN SUPPORT': 0.5}},
    'SS': {'min': 2, 'ideal': 3, 'archetypes': {'ZONE': 0.25, 'HYBRID': 0.75, 'RUN SUPPORT': 0.75}},
    'K': {'min': 1, 'ideal': 1, 'archetypes': {'ACCURATE': 0.75, 'POWER': 0.75}},
    'P': {'min': 1, 'ideal': 1, 'archetypes': {'ACCURATE': 0.75, 'POWER': 0.75}}
}

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

# Define function to calculate player value with corrected multiplier logic
def calculate_player_value(row, dev_trait_multipliers=dev_trait_multipliers, rs_discount=rs_discount):
    if "(RS)" not in row['YEAR']:
        rs_discount = 0
    dev_multiplier = dev_trait_multipliers.get(row['DEV TRAIT'], 1.00)
    remaining_dev_years = remaining_years.get(row['YEAR'], 0)
    value = round(row['BASE RATING'] * dev_multiplier * (1 + remaining_dev_years / 4) * (1 - rs_discount), 2)
    return value

# Decide if player is safe, at risk, or on the cut list
def player_status(row):
    """Player status determines if a player is safe, at risk, or on the cut list based on their value.
    A few rules determine their status.
    1. If a player's year is 'SR' or 'SR (RS)', they are considered 'GRADUATING'.
    2. If a player's value is between 100 and 125, they are considered 'AT RISK'.
    3. If a player's value is less than 100, they are considered 'CUT'.
    4. If a player is the best at his position based on their ovr, he is always considered 'SAFE'."""

    value = row['VALUE']
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
    starters_num = starters_count.get(position, 1)
    position_df = df[df['POSITION'] == position].sort_values(by='VALUE', ascending=False)
    starters = position_df.head(starters_num)
    backups = position_df.tail(len(position_df) - starters_num)

    if len(starters) > 0:
        starters_avg = starters['VALUE'].mean()
    else:
        starters_avg = 0

    if len(backups) > 0:
        backups_avg = backups['VALUE'].mean()
    else:
        backups_avg = 0

    # Blended measure: 70% starters, 30% backups
    blended_value = round(0.7 * starters_avg + 0.3 * backups_avg, 2)
    return blended_value

def scheme_fit(roster_df, position_requirements=default_position_requirements):
    """Determine the scheme fit for each position group for the purposes of recruiting.
    Position groups whose players have a weak affinity for its preferred archetype should be identified as positions and roles of need
    in the recruiting plan.

    This function accepts a roster DataFrame and a dictionary of position requirements. The position requirements dictionary should
    include the minimum and ideal roster sizes per position, as well as the archetypes that are preferred for each position.
    Archetype preferences are rated on a 0 to 1 scale with 0 being least preferred and 1 being most preferred. 0 should be considered
    a non-scheme fit for the position. If a non-scheme fit player's archetype is a strong scheme fit for another position, we should
    note that in the recruiting plan as well as a potential position change during the offseason.

    ## Output
    The output of this function is two DataFrames

    The first with the following columns:
    POSITION, FIRST NAME, LAST NAME, YEAR, RATING, BASE RATING, ARCHETYPE, DEV TRAIT, VALUE, STATUS, CUT, REDSHIRT, DRAFTED, SCHEME FIT
    Where SCHEME FIT is a qualitative recommendation on the player's scheme fit for the position. This column should be used to identify
    positions and roles of need in the recruiting plan.

    The second DataFrame should have the following columns:
    POSITION, CURRENT COUNT, MIN REQUIRED, BLENDED VALUE, GRADE, PRIORITY, SCHEME FIT
    WHERE SCHEME FIT IS A LIST OF RECOMMENDATIONS BASED ON THE POSITION REQUIREMENTS AND PLAYER ARCHETYPES.
    Example output of SCHEME FIT for ROLB: 'need 1 speed rusher, 1 pass coverage poor scheme fit (consider moving to MLB, FS, or SS)'

    Scheme fit values should not be considered supplementary. That is to say, it's not expected that the sum of scheme fit values should = 1.
    A value less than 1 is not necessarily a bad scheme fit.
    ## Scheme Fit Dictionary
    - 1: A perfect scheme fit. We should always have at least one of these players at this position on the roster to be viable and may want more than one.
    - 0.5 to 0.99: A good scheme fit. In some circumstances, these players are project players who we're hoping blossom during development. In other situations,
    these players are essential specialists for situational schemes but won't necessarily be the best fit for every play.
    - 0.01 to 0.49: Weak scheme fits. We likely wouldn't want to have more than one of these players in the position group at a time and should be
    considered for position changes during the offseason or cuts. An ideal position change recommendation would be from their current position where the scheme fit
    is weak to one where it's more preferred or even perfect. For example, pass coverage may be a weak scheme fit for a ROLB but a good fit for MLB. We should
    note these players and recommended changes in the recruiting plan.
    - 0: Non-scheme fit. These players are not a good fit for the position and should be considered for offseason cuts.

    ## Special Considerations
    - LE, RE, and DE: All 3 positions require at least one of ['power rusher' or 'speed rusher'] and at least one 'run stopper' to be a complete unit.
    Speed rusher is slightly preferred over power rusher at RE due to the importance of the RE in pass rushing situations.
    - ROLB & LOLB: Both positions require at least one 'power rusher' and one 'run stopper' to be a complete unit. Pass coverage OLBs are immediate candidates for position changes.
    - MLB: We require at least one of each of the 3 archetypes to be a complete unit.
    """

    scheme_fit_results = []

    for position, requirements in position_requirements.items():
        position_df = roster_df[roster_df['POSITION'] == position].copy()
        current_count = len(position_df)
        min_required = requirements['min']
        archetypes = requirements['archetypes']

        # Calculate scheme fit for each player
        position_df.loc[:, 'SCHEME FIT'] = position_df['ARCHETYPE'].apply(lambda archetype: archetypes.get(archetype, 0))

        # Identify players with weak or non-scheme fits
        weak_fits = position_df[position_df['SCHEME FIT'] < 0.5]
        non_fits = position_df[position_df['SCHEME FIT'] == 0]

        # Create scheme fit recommendations
        recommendations = []
        for _, player in weak_fits.iterrows():
            recommended_positions = [pos for pos, reqs in position_requirements.items() if reqs['archetypes'].get(player['ARCHETYPE'], 0) > 0.5]
            if recommended_positions:
                recommendations.append(f"{player['FIRST NAME']} {player['LAST NAME']} poor scheme fit (consider moving to {', '.join(recommended_positions)})")

        for _, player in non_fits.iterrows():
            recommendations.append(f"{player['FIRST NAME']} {player['LAST NAME']} non-scheme fit (consider for cuts)")

        scheme_fit_results.append({
            'POSITION': position,
            'CURRENT COUNT': current_count,
            'MIN REQUIRED': min_required,
            'BLENDED VALUE': calculate_blended_measure(roster_df, position),
            'GRADE': calculate_position_grade(calculate_blended_measure(roster_df, position)),
            'PRIORITY': 'HIGH' if current_count < min_required else 'LOW',
            'SCHEME FIT': '; '.join(recommendations)
        })
        for _, player in position_df.iterrows():
            print(f"{player['FIRST NAME']} {player['LAST NAME']} ({player['POSITION']} - {player['ARCHETYPE']}): Scheme Fit = {player['SCHEME FIT']}")
        print(f'recommendations:\n {recommendations}')

    scheme_fit_df = pd.DataFrame(scheme_fit_results)

    print(f'scheme_fit_df:\n {scheme_fit_df}')

        # return roster_df, scheme_fit_df


# Main function to process the roster and create recruiting plan
def process_roster_and_create_recruiting_plan(roster_path, position_requirements=default_position_requirements):
    roster_df = pd.read_csv(roster_path)

    # Ensure the required columns are present
    required_columns = [
        'POSITION', 'FIRST NAME', 'LAST NAME', 'YEAR', 'RATING', 'BASE RATING',
        'ARCHETYPE', 'DEV TRAIT', 'VALUE', 'STATUS', 'CUT', 'REDSHIRT', 'DRAFTED'
    ]
    if not all(column in roster_df.columns for column in required_columns):
        raise ValueError("CSV file is missing one or more required columns.")

    # Calculate player values
    roster_df['VALUE'] = roster_df.apply(calculate_player_value, axis=1)

    # Pull archetype values through
    roster_df['ARCHETYPE'] = roster_df['ARCHETYPE'].fillna('')

    # Scheme fit analysis
    scheme_fit(roster_df, position_requirements)

    # Determine the best player at each position
    roster_df['Best at Position'] = roster_df.groupby('POSITION')['RATING'].transform(lambda x: x == x.max())

    # Apply player status function
    roster_df['STATUS'] = roster_df.apply(player_status, axis=1)

    # Drop the 'Best at Position' column
    roster_df.drop(columns=['Best at Position'], inplace=True)

    # Calculate the number of players at each position for the next season
    next_season_counts = roster_df[roster_df['STATUS'] != 'GRADUATING'].groupby('POSITION').size()

    # Calculate the blended measure for each position
    blended_values = {position: calculate_blended_measure(roster_df, position) for position in position_requirements.keys()}

    # Sort roster by position order and rating descending
    position_order = ['QB', 'HB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 'LE', 'RE', 'DT', 'LOLB', 'MLB', 'ROLB', 'CB', 'FS', 'SS', 'K', 'P', 'ATH']
    roster_df['POSITION'] = pd.Categorical(roster_df['POSITION'], categories=position_order, ordered=True)
    roster_df.sort_values(by=['POSITION', 'RATING'], ascending=[True, False], inplace=True)

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

    return roster_df, recruiting_plan

if __name__ == "__main__":
    downloads_folder = os.path.expanduser('~/Downloads')
    data_folder = os.path.join(downloads_folder, 'cfb_dynasty_data')
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    roster_files = glob.glob(os.path.join(downloads_folder, '*[Rr]oster.csv'))
    for roster_path in roster_files:
        roster_df, recruiting_plan = process_roster_and_create_recruiting_plan(roster_path)
        player_values_path = os.path.join(data_folder, 'player_values_corrected.csv')
        recruiting_plan_path = os.path.join(data_folder, 'recruiting_plan.csv')
        roster_df.to_csv(player_values_path, index=False)
        recruiting_plan.to_csv(recruiting_plan_path, index=False)
        print(f"Processed {roster_path}")
        print("Player valuations and statuses have been recalculated and saved to CSV.")
        print("Recruiting plan has been created and saved to CSV.")
