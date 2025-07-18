from ..config.constants import REMAINING_YEARS, RS_DISCOUNT, DEV_TRAIT_MULTIPLIERS

def calculate_player_value(row):
    """Calculate player value based on base overall, development trait, and remaining years."""
    remaining_dev_years = REMAINING_YEARS.get(row['YEAR'], 0)

    # Calculate discounts and multipliers for redshirts and dev traits
    redshirt_discount = RS_DISCOUNT if "(RS)" in row['YEAR'] else 0
    dev_multiplier = DEV_TRAIT_MULTIPLIERS.get(row['DEV TRAIT'], 1.00)

    # Valuation calculation
    value = round(row['BASE OVERALL'] * dev_multiplier * (1 + remaining_dev_years / 4) * (1 - redshirt_discount), 2)
    return value