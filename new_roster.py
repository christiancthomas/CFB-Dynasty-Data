import pandas as pd
import os
import glob
import logging
from typing import Optional

# Configure logging
def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Set up logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    handlers = [logging.StreamHandler()]  # Console output
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers,
        force=True  # Override any existing configuration
    )

# Create logger for this module
logger = logging.getLogger(__name__)


def advance_year(year: str, redshirt: bool) -> str:
    """
    Advance a player's year and handle redshirt status.

    Args:
        year (str): Current year (e.g., 'FR', 'SO', 'HS')
        redshirt (bool): Whether the player is being redshirted

    Returns:
        str: Advanced year with redshirt notation if applicable
    """
    logger.debug(f"Advancing year for player: year={year}, redshirt={redshirt}")

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

    if redshirt and 'RS' not in year:
        # Add redshirt designation without advancing year
        new_year = f"{year} (RS)"
        logger.debug(f"Applied redshirt: {year} -> {new_year}")
        return new_year

    # Advance the year normally
    new_year = year_mapping.get(year, year)
    if new_year != year:
        logger.debug(f"Advanced year: {year} -> {new_year}")

    return new_year

def generate_roster(roster_df: pd.DataFrame, recruits_df: pd.DataFrame, school_name: Optional[str] = None) -> pd.DataFrame:
    """
    Generate a new roster by combining existing roster with recruits.

    Args:
        roster_df (pd.DataFrame): Current roster data
        recruits_df (pd.DataFrame): Recruiting data
        school_name (str, optional): School name to filter recruits

    Returns:
        pd.DataFrame: New roster with advanced years and incoming recruits
    """
    logger.info("Starting roster generation process")
    logger.debug(f"Input roster size: {len(roster_df)} players")
    logger.debug(f"Input recruits size: {len(recruits_df)} recruits")

    # Validate inputs
    if roster_df.empty:
        logger.error("Roster DataFrame is empty")
        raise ValueError("Roster DataFrame cannot be empty")
    if recruits_df.empty:
        logger.error("Recruits DataFrame is empty")
        raise ValueError("Recruits DataFrame cannot be empty")

    required_roster_cols = ['YEAR', 'REDSHIRT', 'CUT', 'DRAFTED']
    required_recruit_cols = ['FIRST NAME', 'LAST NAME', 'POSITION','COMMITTED TO', 'YEAR']

    for col in required_roster_cols:
        if col not in roster_df.columns:
            logger.error(f"Missing required column in roster: {col}")
            raise ValueError(f"Missing required column in roster: {col}")

    for col in required_recruit_cols:
        if col not in recruits_df.columns:
            logger.error(f"Missing required column in recruits: {col}")
            raise ValueError(f"Missing required column in recruits: {col}")

    logger.debug("Input validation completed successfully")

    # Work with copies to avoid modifying original data
    roster_copy = roster_df.copy()
    recruits_copy = recruits_df.copy()

    # Apply the function to advance the year for each player
    logger.info("Advancing years for current roster players")
    roster_copy['YEAR'] = roster_copy.apply(
        lambda row: advance_year(row['YEAR'], row['REDSHIRT']), axis=1
    )

    # Filter the roster data to include only players who are not graduating or drafted or cut
    initial_count = len(roster_copy)
    filtered_roster_df = roster_copy[
        (roster_copy['YEAR'] != 'GRADUATED') &
        (roster_copy['CUT'] != True) &
        (roster_copy['DRAFTED'].isna())
    ].copy()

    filtered_count = len(filtered_roster_df)
    removed_count = initial_count - filtered_count
    logger.info(f"Filtered roster: {filtered_count} players remaining, {removed_count} players removed (graduated/cut/drafted)")

    # Filter the recruiting data to include only players committed to your school
    if not school_name:
        school_name = input("Enter the name of your school: ")
        logger.info(f"User entered school name: {school_name}")

    initial_recruit_count = len(recruits_copy)
    recruits_filtered = recruits_copy[
        recruits_copy['COMMITTED TO'] == school_name.upper()
    ].copy()

    commit_count = len(recruits_filtered)
    logger.info(f"Found {commit_count} recruits committed to {school_name} out of {initial_recruit_count} total recruits")

    # Advance the year for recruits from HS to FR
    logger.debug("Advancing years for incoming recruits")
    recruits_filtered.loc[:, 'YEAR'] = recruits_filtered['YEAR'].apply(
        lambda year: advance_year(year, False)
    )

    # Combine the filtered roster data with the recruits
    logger.info("Combining roster with incoming recruits")
    new_roster_df = pd.concat([filtered_roster_df, recruits_filtered], ignore_index=True)

    final_count = len(new_roster_df)
    logger.info(f"Combined roster size: {final_count} players ({filtered_count} returning + {commit_count} recruits)")

    # Drop the specified columns
    columns_to_drop = ['STARS', 'GEM STATUS', 'COMMITTED TO', 'NATIONAL RANKING']
    columns_dropped = [col for col in columns_to_drop if col in new_roster_df.columns]
    new_roster_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    if columns_dropped:
        logger.debug(f"Dropped columns: {columns_dropped}")

    # Define the position order
    position_order = [
        'QB', 'HB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT',
        'LEDG', 'REDG', 'DT', 'WILL', 'MIKE', 'SAM', 'CB', 'FS', 'SS', 'K', 'P', 'ATH'
    ]

    # Create a categorical type for the position column based on the defined order
    logger.debug("Setting up position-based sorting")
    new_roster_df['POSITION'] = pd.Categorical(
        new_roster_df['POSITION'], categories=position_order, ordered=True
    )

    # Sort by position first, then by original rating if it exists
    sort_cols = ['POSITION']
    sort_ascending = [True]

    if 'OVERALL' in new_roster_df.columns and not new_roster_df['OVERALL'].isna().all():
        sort_cols.append('OVERALL')
        sort_ascending.append(False)
        logger.debug("Sorting by position and rating")
    else:
        logger.debug("Sorting by position only (no rating data available)")

    new_roster_df.sort_values(by=sort_cols, ascending=sort_ascending, inplace=True)

    # Helper function to ensure columns exist and set default values
    def ensure_columns_exist(df, column_defaults):
        for col, default_val in column_defaults.items():
            if col not in df.columns:
                df[col] = default_val
                logger.debug(f"Added missing column '{col}' with default value")
            df[col] = default_val

    # Set columns to default values
    logger.debug("Resetting overall and status columns to default values")
    ensure_columns_exist(new_roster_df, {
        'OVERALL': "",
        'BASE OVERALL': "",
        'VALUE': "",
        'STATUS': ""
    })

    logger.debug("Resetting redshirt and cut flags to False")
    ensure_columns_exist(new_roster_df, {
        'REDSHIRT': False,
        'CUT': False
    })

    logger.info(f"Roster generation completed successfully. Final roster: {len(new_roster_df)} players")

    # Log position breakdown
    if logger.isEnabledFor(logging.DEBUG):
        position_counts = new_roster_df['POSITION'].value_counts().sort_index()
        logger.debug("Position breakdown:")
        for pos, count in position_counts.items():
            logger.debug(f"  {pos}: {count} players")

    # Return the new roster
    return new_roster_df

def _to_csv(data_path: str, data_folder: str, new_path: str = 'New_Roster.csv') -> None:
    """
    Process roster and recruiting CSV files and generate new roster.

    Args:
        data_path (str): Path to search for input CSV files
        data_folder (str): Output directory for new roster
        new_path (str): Output filename
    """
    logger.info(f"Starting CSV processing: searching in {data_path}")

    try:
        roster_files = glob.glob(os.path.join(data_path, '*[Rr]oster.csv'))
        recruiting_files = glob.glob(os.path.join(data_path, '*[Rr]ecruiting*.csv'))

        logger.debug(f"Found {len(roster_files)} roster files: {roster_files}")
        logger.debug(f"Found {len(recruiting_files)} recruiting files: {recruiting_files}")

        if not roster_files:
            logger.error(f"No roster CSV files found in {data_path}")
            raise FileNotFoundError("No roster CSV files found in the specified path")
        if not recruiting_files:
            logger.error(f"No recruiting CSV files found in {data_path}")
            raise FileNotFoundError("No recruiting CSV files found in the specified path")

        if not os.path.exists(data_folder):
            logger.info(f"Creating output directory: {data_folder}")
            os.makedirs(data_folder)

        processed_count = 0
        error_count = 0

        for roster_path in roster_files:
            try:
                logger.info(f"Processing roster file: {os.path.basename(roster_path)}")

                roster_df = pd.read_csv(roster_path)
                recruiting_df = pd.read_csv(recruiting_files[0])

                logger.debug(f"Loaded roster with {len(roster_df)} rows")
                logger.debug(f"Loaded recruiting data with {len(recruiting_df)} rows")

                new_roster_df = generate_roster(roster_df, recruiting_df)
                output_path = os.path.join(data_folder, new_path)
                new_roster_df.to_csv(output_path, index=False)

                logger.info(f"Successfully processed {os.path.basename(roster_path)}")
                logger.info(f"New roster saved to: {output_path}")
                logger.debug(f"Output file contains {len(new_roster_df)} players")

                processed_count += 1

            except Exception as e:
                error_count += 1
                logger.error(f"Error processing {os.path.basename(roster_path)}: {str(e)}")
                logger.debug(f"Full error details for {roster_path}:", exc_info=True)
                continue

        logger.info(f"Processing complete: {processed_count} files processed successfully, {error_count} errors")

    except Exception as e:
        logger.error(f"Fatal error in _to_csv: {str(e)}")
        logger.debug("Full error details:", exc_info=True)
        raise

def main():
    """Main function to process CFB dynasty roster data."""
    # Set up logging
    downloads_folder = os.path.expanduser('~/Downloads')
    log_file = os.path.join(downloads_folder, 'cfb_dynasty_data', 'roster_processing.log')

    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    setup_logging(log_level=logging.INFO, log_file=log_file)

    logger.info("=" * 50)
    logger.info("CFB Dynasty Roster Processing Started")
    logger.info("=" * 50)

    try:
        data_folder = os.path.join(downloads_folder, 'cfb_dynasty_data')
        _to_csv(downloads_folder, data_folder)
        logger.info("All processing completed successfully!")

    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        logger.debug("Full application error:", exc_info=True)
        raise

    finally:
        logger.info("=" * 50)
        logger.info("CFB Dynasty Roster Processing Finished")
        logger.info("=" * 50)

if __name__ == "__main__":
    main()
