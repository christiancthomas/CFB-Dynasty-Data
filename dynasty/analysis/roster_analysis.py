# Core Analysis Functions
from ..config.constants import STARTERS_COUNT

def player_status(row):
    """Determine if player is safe, at risk, or on the cut list."""
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

def calculate_position_grade(avg_value):
    """Calculate letter grade based on average position value."""
    if avg_value >= 150: return 'A+'
    elif avg_value >= 140: return 'A'
    elif avg_value >= 130: return 'A-'
    elif avg_value >= 120: return 'B+'
    elif avg_value >= 110: return 'B'
    elif avg_value >= 100: return 'B-'
    elif avg_value >= 90: return 'C+'
    elif avg_value >= 80: return 'C'
    elif avg_value >= 70: return 'C-'
    else: return 'F'

def calculate_blended_measure(df, position):
    """Calculate blended measure of starters and backups (70% starters, 30% backups)."""
    starters_num = STARTERS_COUNT.get(position, 1)
    position_df = df[df['POSITION'] == position].sort_values(by='VALUE', ascending=False)

    starters = position_df.head(starters_num)
    backups = position_df.tail(len(position_df) - starters_num)

    starters_avg = starters['VALUE'].mean() if len(starters) > 0 else 0
    backups_avg = backups['VALUE'].mean() if len(backups) > 0 else 0

    blended_value = round(0.7 * starters_avg + 0.3 * backups_avg, 2)
    return blended_value