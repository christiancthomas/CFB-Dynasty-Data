"""File utilities for CFB Dynasty Data system."""

import os
import glob
import pandas as pd


DEFAULT_FOLDER = os.path.expanduser('~/Downloads')

# Expected column names to help identify the real header row
EXPECTED_HEADERS = {'REDSHIRT', 'FIRST NAME', 'LAST NAME', 'YEAR', 'POSITION', 'OVERALL', 'BASE OVERALL'}


def _is_empty_column(series):
    """Check if a column is entirely empty/unnamed."""
    return series.isna().all() or (series.astype(str).str.strip() == '').all()


def _is_empty_or_unnamed(col_name):
    """Check if a column name indicates an empty/border column."""
    if pd.isna(col_name):
        return True
    col_str = str(col_name).strip()
    return col_str == '' or col_str.startswith('Unnamed')


def _clean_csv_borders(df):
    """
    Clean CSV data exported from spreadsheets with design borders.

    Google Sheets and Excel files with colored borders/design elements
    often export with empty first row(s) and/or empty first column(s).
    This function dynamically detects and removes any number of empty borders.
    """
    if df.empty:
        return df

    rows_removed = 0
    cols_removed = 0

    # Remove empty leading columns (left border)
    while len(df.columns) > 0:
        first_col_name = df.columns[0]
        if _is_empty_or_unnamed(first_col_name) and _is_empty_column(df.iloc[:, 0]):
            df = df.iloc[:, 1:]
            cols_removed += 1
        else:
            break

    # Remove empty trailing columns (right border)
    while len(df.columns) > 0:
        last_col_name = df.columns[-1]
        if _is_empty_or_unnamed(last_col_name) and _is_empty_column(df.iloc[:, -1]):
            df = df.iloc[:, :-1]
            cols_removed += 1
        else:
            break

    # Check if the current column headers are actually empty/unnamed
    # and the real headers are in a data row
    if len(df.columns) > 0 and _is_empty_or_unnamed(df.columns[0]):
        # Search for the real header row (up to first 10 rows)
        for i in range(min(10, len(df))):
            row = df.iloc[i]
            # Check if this row contains expected header names
            row_values = {str(v).strip().upper() for v in row.values if pd.notna(v)}
            if row_values & EXPECTED_HEADERS:
                # Found the header row - promote it and drop rows above
                df.columns = df.iloc[i]
                df = df.iloc[i + 1:].reset_index(drop=True)
                rows_removed = i + 1
                break

    # Remove any remaining empty rows at the start
    while len(df) > 0 and df.iloc[0].isna().all():
        df = df.iloc[1:].reset_index(drop=True)
        rows_removed += 1

    # Remove empty rows at the end
    while len(df) > 0 and df.iloc[-1].isna().all():
        df = df.iloc[:-1]

    # Clean column names - strip whitespace
    df.columns = [str(col).strip() if pd.notna(col) else col for col in df.columns]

    # Report what was cleaned
    if rows_removed > 0 or cols_removed > 0:
        print(f"🔧 Cleaned spreadsheet borders: removed {rows_removed} row(s), {cols_removed} column(s)")

    return df


def load_roster(folder=None):
    """
    Load roster CSV file from specified folder.

    Args:
        folder (str): Folder path to search for roster files (default: ~/Downloads)

    Returns:
        pd.DataFrame or None: Loaded roster DataFrame or None if error
    """
    if folder is None:
        folder = DEFAULT_FOLDER

    # Find roster files
    roster_files = glob.glob(os.path.join(folder, '*[Rr]oster.csv'))

    if not roster_files:
        print("❌ No roster CSV files found in Downloads folder")
        print("📁 Make sure your roster file is in ~/Downloads/ and contains 'roster' in the filename")
        return None
    else:
        print(f"📁 Found {len(roster_files)} roster file(s):")
        for i, file in enumerate(roster_files):
            print(f"  {i+1}. {os.path.basename(file)}")

        # Load the first roster file found
        roster_path = roster_files[0]
        print(f"\n📊 Loading: {os.path.basename(roster_path)}")

        try:
            roster_df = pd.read_csv(roster_path)

            # Handle CSVs exported from Google Sheets with design borders
            # These may have empty first row(s) and/or empty first column(s)
            roster_df = _clean_csv_borders(roster_df)

            # Convert numeric columns to proper types (they may be strings from CSV)
            if 'OVERALL' in roster_df.columns:
                roster_df['OVERALL'] = pd.to_numeric(roster_df['OVERALL'], errors='coerce')
            if 'BASE OVERALL' in roster_df.columns:
                roster_df['BASE OVERALL'] = pd.to_numeric(roster_df['BASE OVERALL'], errors='coerce')

            print(f"✅ Successfully loaded {len(roster_df)} players")
            print(f"📋 Columns: {list(roster_df.columns)}")

            # Display basic info about the roster
            print(f"\n📈 Quick Stats:")
            print(f"  • Total Players: {len(roster_df)}")
            print(f"  • Positions: {roster_df['POSITION'].nunique()}")
            print(f"  • Years: {', '.join(sorted(roster_df['YEAR'].unique()))}")

            return roster_df

        except Exception as e:
            print(f"❌ Error loading roster file: {e}")
            return None


def export_files(folder=None, roster_df=None, recruiting_plan=None, position_requirements=None):
    """
    Export comprehensive analysis results to CSV files.

    Args:
        folder (str): Base folder for exports (default: ~/Downloads)
        roster_df (pd.DataFrame): Processed roster DataFrame with player values and status
        recruiting_plan (pd.DataFrame): DataFrame with recruiting priorities
        position_requirements (dict): Dictionary with position requirements for detailed analysis

    Returns:
        bool: True if export successful, False otherwise
    """
    if folder is None:
        folder = DEFAULT_FOLDER

    if roster_df is None:
        print("❌ Cannot export - no roster data provided.")
        return False

    # Create output directory
    data_folder = os.path.join(folder, 'cfb_dynasty_data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    try:
        # Export processed roster with player values
        roster_export = roster_df.drop('Best at Position', axis=1, errors='ignore')
        player_values_path = os.path.join(data_folder, 'player_values_analysis.csv')
        roster_export.to_csv(player_values_path, index=False)

        # Export recruiting plan if provided
        if recruiting_plan is not None:
            recruiting_plan_path = os.path.join(data_folder, 'recruiting_plan_analysis.csv')
            recruiting_plan.to_csv(recruiting_plan_path, index=False)

        # Export detailed position analysis if position requirements provided
        if position_requirements is not None:
            position_analysis = []
            for pos in position_requirements.keys():
                pos_data = roster_df[roster_df['POSITION'] == pos]
                if len(pos_data) > 0:
                    analysis = {
                        'Position': pos,
                        'Total_Players': len(pos_data),
                        'Avg_Rating': pos_data['BASE OVERALL'].mean(),
                        'Avg_Value': pos_data['VALUE'].mean(),
                        'Top_Player_Value': pos_data['VALUE'].max(),
                        'Top_Player_Name': f"{pos_data.loc[pos_data['VALUE'].idxmax(), 'FIRST NAME']} {pos_data.loc[pos_data['VALUE'].idxmax(), 'LAST NAME']}",
                        'Elite_Dev_Count': len(pos_data[pos_data['DEV TRAIT'] == 'ELITE']),
                        'Star_Dev_Count': len(pos_data[pos_data['DEV TRAIT'] == 'STAR']),
                        'Graduating_Count': len(pos_data[pos_data['STATUS'] == 'GRADUATING']),
                        'Cut_Candidates': len(pos_data[pos_data['STATUS'] == 'CUT']),
                        'At_Risk_Count': len(pos_data[pos_data['STATUS'] == 'AT RISK'])
                    }
                    position_analysis.append(analysis)

            if position_analysis:
                position_analysis_df = pd.DataFrame(position_analysis)
                position_analysis_path = os.path.join(data_folder, 'position_analysis_detailed.csv')
                position_analysis_df.to_csv(position_analysis_path, index=False)

        print("💾 Export completed successfully!")
        print(f"📁 Files saved to: {data_folder}")
        print(f"  📊 Player Values: {os.path.basename(player_values_path)}")

        if recruiting_plan is not None:
            print(f"  🎯 Recruiting Plan: {os.path.basename(recruiting_plan_path)}")

        if position_requirements is not None and position_analysis:
            print(f"  📋 Position Analysis: {os.path.basename(position_analysis_path)}")

        # Show summary of what was exported
        print(f"\n📈 Export Summary:")
        print(f"  • {len(roster_export)} player records with values and status")

        if recruiting_plan is not None:
            print(f"  • {len(recruiting_plan)} position recruiting priorities")

        if position_requirements is not None and position_analysis:
            print(f"  • {len(position_analysis_df)} detailed position breakdowns")

        return True

    except Exception as e:
        print(f"❌ Error during export: {e}")
        return False
