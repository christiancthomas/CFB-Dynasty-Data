"""Roster analysis functions for CFB Dynasty Data system."""

import pandas as pd
import glob
import os
from ..config.constants import (
    DEV_TRAIT_MULTIPLIERS,
    REMAINING_YEARS,
    RS_DISCOUNT,
    DEFAULT_POSITION_REQUIREMENTS,
    STARTERS_COUNT
)


def calculate_player_value(row, dev_trait_multipliers=None, rs_discount_rate=None):
    """Calculate player value based on rating, development trait, remaining years, and redshirt status."""
    if dev_trait_multipliers is None:
        dev_trait_multipliers = DEV_TRAIT_MULTIPLIERS
    if rs_discount_rate is None:
        rs_discount_rate = RS_DISCOUNT
    
    # Apply redshirt discount only if player has redshirt designation
    discount = rs_discount_rate if "(RS)" in row['YEAR'] else 0
    
    dev_multiplier = dev_trait_multipliers.get(row['DEV TRAIT'], 1.00)
    remaining_dev_years = REMAINING_YEARS.get(row['YEAR'], 0)
    
    # Handle both 'BASE RATING' and 'BASE OVERALL' column names for backward compatibility
    base_rating = row.get('BASE RATING', row.get('BASE OVERALL', 0))
    
    value = round(
        base_rating * dev_multiplier * (1 + remaining_dev_years / 4) * (1 - discount), 2
    )
    return value


def player_status(row):
    """Determine player status: GRADUATING, SAFE, AT RISK, or CUT."""
    value = row['VALUE']
    year = row['YEAR']
    best_at_position = row['Best at Position']

    if year in ['SR', 'SR (RS)']:
        return 'GRADUATING'
    elif best_at_position:
        return 'SAFE'
    elif value < 100:
        return 'CUT'
    elif 100 <= value <= 125:
        return 'AT RISK'
    else:
        return 'SAFE'


def calculate_position_grade(avg_value):
    """Calculate position strength grade based on average value."""
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


def calculate_blended_measure(df, position):
    """Calculate blended measure of starters and backups (70% starters, 30% backups)."""
    starters_num = STARTERS_COUNT.get(position, 1)
    position_df = df[df['POSITION'] == position].sort_values(by='VALUE', ascending=False)
    
    starters = position_df.head(starters_num)
    backups = position_df.tail(len(position_df) - starters_num)

    starters_avg = starters['VALUE'].mean() if len(starters) > 0 else 0
    backups_avg = backups['VALUE'].mean() if len(backups) > 0 else 0

    # Blended measure: 70% starters, 30% backups
    blended_value = round(0.7 * starters_avg + 0.3 * backups_avg, 2)
    return blended_value


def scheme_fit(roster_df, position_requirements=None):
    """
    Determine the scheme fit for each position group for recruiting purposes.
    
    Returns:
        tuple: (roster_df with scheme fit data, scheme_fit_summary_df)
    """
    if position_requirements is None:
        position_requirements = DEFAULT_POSITION_REQUIREMENTS
    
    scheme_fit_results = []

    for position, requirements in position_requirements.items():
        recommendations = []
        position_df = roster_df[roster_df['POSITION'] == position].copy()
        current_count = len(position_df)
        min_required = requirements['min']
        archetypes = requirements['archetypes']

        # Calculate scheme fit for each player
        position_df.loc[:, 'SCHEME FIT'] = position_df['ARCHETYPE'].apply(
            lambda archetype: archetypes.get(archetype, 0)
        )

        # Identify players with weak or non-scheme fits
        weak_fits = position_df[position_df['SCHEME FIT'] < 0.5]
        non_fits = position_df[position_df['SCHEME FIT'] == 0]

        # Create scheme fit recommendations
        for _, player in weak_fits.iterrows():
            recommended_positions = [
                pos for pos, reqs in position_requirements.items() 
                if reqs['archetypes'].get(player['ARCHETYPE'], 0) > 0.5
            ]
            if recommended_positions:
                recommendations.append(
                    f"{player['FIRST NAME']} {player['LAST NAME']} poor scheme fit "
                    f"(consider moving to {', '.join(recommended_positions)})"
                )

        for _, player in non_fits.iterrows():
            recommendations.append(
                f"{player['FIRST NAME']} {player['LAST NAME']} non-scheme fit (consider for cuts)"
            )

        scheme_fit_results.append({
            'POSITION': position,
            'CURRENT COUNT': current_count,
            'MIN REQUIRED': min_required,
            'BLENDED VALUE': calculate_blended_measure(roster_df, position),
            'GRADE': calculate_position_grade(calculate_blended_measure(roster_df, position)),
            'PRIORITY': 'HIGH' if current_count < min_required else 'LOW',
            'SCHEME FIT': '; '.join(recommendations)
        })

    scheme_fit_df = pd.DataFrame(scheme_fit_results)
    return roster_df, scheme_fit_df


def process_roster_and_create_recruiting_plan(roster_path, position_requirements=None):
    """
    Main function to process the roster and create recruiting plan.
    
    Args:
        roster_path (str): Path to roster CSV file
        position_requirements (dict): Position requirements dictionary
        
    Returns:
        tuple: (processed_roster_df, recruiting_plan_df)
    """
    if position_requirements is None:
        position_requirements = DEFAULT_POSITION_REQUIREMENTS
    
    roster_df = pd.read_csv(roster_path)

    # Ensure the required columns are present
    required_columns = [
        'POSITION', 'FIRST NAME', 'LAST NAME', 'YEAR', 'RATING', 
        'ARCHETYPE', 'DEV TRAIT', 'VALUE', 'STATUS', 'CUT', 'REDSHIRT', 'DRAFTED'
    ]
    # Check for either BASE RATING or BASE OVERALL
    has_base_rating = 'BASE RATING' in roster_df.columns or 'BASE OVERALL' in roster_df.columns
    if not has_base_rating:
        required_columns.append('BASE RATING')  # Will trigger missing column error
    
    missing_columns = [col for col in required_columns if col not in roster_df.columns]
    if missing_columns:
        raise ValueError(f"CSV file is missing required columns: {missing_columns}")

    # Calculate player values
    roster_df['VALUE'] = roster_df.apply(calculate_player_value, axis=1)

    # Fill missing archetype values
    roster_df['ARCHETYPE'] = roster_df['ARCHETYPE'].fillna('')

    # Scheme fit analysis
    roster_df, scheme_fit_df = scheme_fit(roster_df, position_requirements)

    # Determine the best player at each position
    roster_df['Best at Position'] = roster_df.groupby('POSITION')['RATING'].transform(
        lambda x: x == x.max()
    )

    # Apply player status function
    roster_df['STATUS'] = roster_df.apply(player_status, axis=1)

    # Drop the temporary 'Best at Position' column
    roster_df.drop(columns=['Best at Position'], inplace=True)

    # Calculate the number of players at each position for the next season
    next_season_counts = roster_df[roster_df['STATUS'] != 'GRADUATING'].groupby('POSITION').size()

    # Calculate the blended measure for each position
    blended_values = {
        position: calculate_blended_measure(roster_df, position) 
        for position in position_requirements.keys()
    }

    # Sort roster by position order and rating descending
    position_order = [
        'QB', 'HB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 
        'LEDG', 'REDG', 'DT', 'WILL', 'MIKE', 'SAM', 
        'CB', 'FS', 'SS', 'K', 'P', 'ATH'
    ]
    roster_df['POSITION'] = pd.Categorical(
        roster_df['POSITION'], categories=position_order, ordered=True
    )
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


def main():
    """Main function for command-line execution."""
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


if __name__ == "__main__":
    main()
