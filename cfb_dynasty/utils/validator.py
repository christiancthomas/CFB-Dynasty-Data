"""Validator functions for various data inputs in the CFB Dynasty Data system."""

from ..config.constants import POSITION_ORDER

# Valid year designations for player eligibility
VALID_YEARS = ['HS', 'FR', 'FR (RS)', 'SO', 'SO (RS)', 'JR', 'JR (RS)', 'SR', 'SR (RS)']


def validate_player_data(player_data: dict) -> bool:
    """
    Validates the player data dictionary to ensure all required fields are present and correctly formatted.

    Args:
        player_data (dict): Dictionary containing player attributes.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    required_fields = ['first_name', 'last_name', 'position', 'year', 'redshirt']

    for field in required_fields:
        if field not in player_data:
            print(f"Missing required field: {field}")
            return False

    if not isinstance(player_data['first_name'], str) or not isinstance(player_data['last_name'], str):
        print("First name and last name must be strings.")
        return False

    if not isinstance(player_data['position'], str):
        print("Position must be a string.")
        return False

    if player_data['year'] not in VALID_YEARS:
        print(f"Year must be one of: {', '.join(VALID_YEARS)}.")
        return False

    if not isinstance(player_data['redshirt'], bool):
        print("Redshirt status must be a boolean.")
        return False

    return True


def validate_roster_columns(roster_df, required_columns=None):
    """
    Validate that roster DataFrame has required columns.

    Args:
        roster_df (pd.DataFrame): Roster DataFrame to validate
        required_columns (list): List of required column names

    Returns:
        tuple: (bool, list) - (is_valid, missing_columns)
    """
    if required_columns is None:
        required_columns = [
            'FIRST NAME', 'LAST NAME', 'POSITION', 'YEAR', 'REDSHIRT'
        ]

    missing_columns = [col for col in required_columns if col not in roster_df.columns]

    return len(missing_columns) == 0, missing_columns


def validate_position(position: str) -> bool:
    """
    Validate that position is a recognized football position.

    Args:
        position (str): Position abbreviation

    Returns:
        bool: True if valid position, False otherwise
    """
    return position.upper() in POSITION_ORDER


def validate_year(year: str) -> bool:
    """
    Validate that year is a recognized eligibility year.

    Args:
        year (str): Year designation

    Returns:
        bool: True if valid year, False otherwise
    """
    return year in VALID_YEARS
