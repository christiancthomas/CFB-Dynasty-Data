import os
import glob
import pandas as pd


default_folder = os.path.expanduser('~/Downloads')

def load_roster(folder=default_folder):

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

def export_files(folder=default_folder, roster_df=None, recruiting_plan=None, position_requirements=None):
    """
    Export comprehensive analysis results to CSV files.

    Args:
        folder: Base folder for exports (default: ~/Downloads)
        roster_df: Processed roster DataFrame with player values and status
        recruiting_plan: DataFrame with recruiting priorities
        position_requirements: Dictionary with position requirements for detailed analysis
    """
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
