#!/usr/bin/env python3
"""
Basic CFB Dynasty Analysis Example

This script demonstrates the basic workflow for analyzing a CFB dynasty roster.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfb_dynasty import (
    load_roster,
    process_roster_and_create_recruiting_plan,
    export_files,
    DEFAULT_POSITION_REQUIREMENTS
)


def main():
    """Run basic dynasty analysis workflow."""
    print("🏈 CFB Dynasty Basic Analysis")
    print("=" * 40)
    
    try:
        # Step 1: Load roster data
        print("📊 Step 1: Loading roster data...")
        roster_df = load_roster()
        
        if roster_df is None:
            print("❌ No roster data found. Please add a CSV file to ~/Downloads")
            return
        
        # Step 2: Run comprehensive analysis
        print("🔍 Step 2: Analyzing roster and creating recruiting plan...")
        analyzed_roster, recruiting_plan = process_roster_and_create_recruiting_plan(
            # Use the first CSV file found in Downloads
            "roster.csv"  # This will be auto-detected by load_roster
        )
        
        # Step 3: Display key insights
        print("\n📋 ANALYSIS RESULTS")
        print("-" * 20)
        
        # Show roster summary
        total_players = len(analyzed_roster)
        graduating = len(analyzed_roster[analyzed_roster['STATUS'] == 'GRADUATING'])
        cuts = len(analyzed_roster[analyzed_roster['STATUS'] == 'CUT'])
        
        print(f"Total Players: {total_players}")
        print(f"Graduating: {graduating}")
        print(f"Recommended Cuts: {cuts}")
        print(f"Returning Players: {total_players - graduating - cuts}")
        
        # Show high priority recruiting needs
        print("\n🎯 HIGH PRIORITY RECRUITING NEEDS:")
        high_priority = recruiting_plan[recruiting_plan['Priority'] == 'HIGH']
        
        if len(high_priority) > 0:
            for _, pos in high_priority.iterrows():
                print(f"  • {pos['Position']}: {pos['Current Count']}/{pos['Min Required']} players (Grade: {pos['Grade']})")
        else:
            print("  ✅ No critical recruiting needs!")
        
        # Show strongest positions
        print("\n💪 STRONGEST POSITIONS:")
        strong_positions = recruiting_plan[recruiting_plan['Grade'].isin(['A+', 'A', 'A-', 'B+'])]
        strong_positions = strong_positions.sort_values('Grade').head(3)
        
        for _, pos in strong_positions.iterrows():
            print(f"  • {pos['Position']}: Grade {pos['Grade']} ({pos['Current Count']} players)")
        
        # Step 4: Export detailed results
        print("\n💾 Step 3: Exporting detailed analysis...")
        success = export_files(
            roster_df=analyzed_roster,
            recruiting_plan=recruiting_plan,
            position_requirements=DEFAULT_POSITION_REQUIREMENTS
        )
        
        if success:
            print("\n🎉 Analysis complete! Check ~/Downloads/cfb_dynasty_data/ for detailed results.")
        else:
            print("\n⚠️  Analysis complete but export had issues. Check console for details.")
            
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Please check that your CSV file is properly formatted and contains required columns.")


if __name__ == "__main__":
    main()
