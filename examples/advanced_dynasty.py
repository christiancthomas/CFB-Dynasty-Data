#!/usr/bin/env python3
"""
Advanced Dynasty Management Example

This script demonstrates advanced dynasty management techniques including
multi-year planning, custom analysis, and automated decision making.
"""

import sys
import os
import glob

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfb_dynasty import *
from cfb_dynasty.config.constants import YEAR_PROGRESSION
import pandas as pd


def analyze_graduation_impact(roster_df):
    """Analyze the impact of upcoming graduations."""
    print("🎓 GRADUATION IMPACT ANALYSIS")
    print("-" * 30)
    
    graduating = roster_df[roster_df['STATUS'] == 'GRADUATING']
    
    if len(graduating) == 0:
        print("✅ No players graduating this season!")
        return
    
    print(f"📊 {len(graduating)} players graduating:")
    
    # Group by position
    grad_by_position = graduating.groupby('POSITION').size().sort_values(ascending=False)
    
    for position, count in grad_by_position.items():
        # Calculate average value of graduating players
        pos_grads = graduating[graduating['POSITION'] == position]
        avg_value = pos_grads['VALUE'].mean() if 'VALUE' in pos_grads.columns else 0
        
        print(f"   • {position}: {count} players (avg value: {avg_value:.1f})")
        
        # Show individual high-value graduates
        high_value_grads = pos_grads[pos_grads['VALUE'] > 150] if 'VALUE' in pos_grads.columns else pd.DataFrame()
        for _, player in high_value_grads.iterrows():
            print(f"     ⭐ {player['FIRST NAME']} {player['LAST NAME']} (Value: {player['VALUE']:.1f})")


def project_future_roster(roster_df, years_ahead=2):
    """Project what the roster will look like in future years."""
    print(f"\n🔮 {years_ahead}-YEAR ROSTER PROJECTION")
    print("-" * 30)
    
    # Create a copy for projections
    future_roster = roster_df.copy()
    
    # Simulate year advancement
    for year in range(years_ahead):
        print(f"\nYear +{year + 1}:")
        
        # Remove graduates
        future_roster = future_roster[future_roster['STATUS'] != 'GRADUATING']
        
        # Advance all players by one year using centralized YEAR_PROGRESSION
        future_roster['YEAR'] = future_roster['YEAR'].map(YEAR_PROGRESSION)
        future_roster.loc[future_roster['YEAR'] == 'GRADUATING', 'STATUS'] = 'GRADUATING'
        
        # Show position counts
        position_counts = future_roster[future_roster['STATUS'] != 'GRADUATING']['POSITION'].value_counts()
        
        critical_positions = position_counts[position_counts < 3]  # Positions with < 3 players
        if len(critical_positions) > 0:
            print(f"   ⚠️  Critical shortages: {dict(critical_positions)}")
        else:
            print("   ✅ No critical position shortages")
        
        graduating_next = len(future_roster[future_roster['STATUS'] == 'GRADUATING'])
        print(f"   📊 Graduating next year: {graduating_next} players")


def identify_position_change_candidates(roster_df):
    """Identify players who might benefit from position changes."""
    print("\n🔄 POSITION CHANGE ANALYSIS")
    print("-" * 30)
    
    # This would require scheme fit data - simplified example
    if 'SCHEME FIT' in roster_df.columns:
        poor_fits = roster_df[roster_df['SCHEME FIT'] < 0.5]
        
        if len(poor_fits) > 0:
            print("Players with poor scheme fit (consider position changes):")
            for _, player in poor_fits.iterrows():
                print(f"   • {player['FIRST NAME']} {player['LAST NAME']} ({player['POSITION']})")
                print(f"     Current fit: {player['SCHEME FIT']:.2f}")
        else:
            print("✅ All players have good scheme fit!")
    else:
        print("ℹ️  Scheme fit data not available. Run scheme_fit analysis first.")


def create_transfer_portal_strategy(roster_df, recruiting_plan):
    """Develop transfer portal strategy based on needs."""
    print("\n🎯 TRANSFER PORTAL STRATEGY")
    print("-" * 30)
    
    # Identify high-priority positions
    high_priority = recruiting_plan[recruiting_plan['Priority'] == 'HIGH']
    
    if len(high_priority) == 0:
        print("✅ No high-priority needs - focus on depth and upgrades")
        return
    
    print("Transfer portal targets by priority:")
    
    for _, pos in high_priority.iterrows():
        shortage = pos['Min Required'] - pos['Current Count']
        print(f"\n📍 {pos['Position']} (Grade: {pos['Grade']})")
        print(f"   Need: {shortage} players minimum")
        print(f"   Target profile: Experienced player (JR/SR) with immediate impact")
        print(f"   Alternative: High-upside underclassman if development time available")


def analyze_scholarship_situation(roster_df):
    """Analyze current scholarship usage and availability."""
    print("\n🎓 SCHOLARSHIP ANALYSIS")
    print("-" * 30)
    
    total_players = len(roster_df)
    graduating = len(roster_df[roster_df['STATUS'] == 'GRADUATING'])
    cuts = len(roster_df[roster_df['STATUS'] == 'CUT'])
    
    # Assume 85 scholarship limit (adjust as needed)
    SCHOLARSHIP_LIMIT = 85
    
    current_scholarships = total_players - cuts  # Cuts don't count against limit
    available_scholarships = SCHOLARSHIP_LIMIT - current_scholarships + graduating
    
    print(f"📊 Current roster: {total_players} players")
    print(f"📊 On scholarship: {current_scholarships} players")
    print(f"📊 Graduating: {graduating} players")
    print(f"📊 Recommended cuts: {cuts} players")
    print(f"📊 Available scholarships: {available_scholarships}")
    
    if available_scholarships < 0:
        print(f"⚠️  OVER LIMIT by {abs(available_scholarships)} scholarships!")
        print("   Need additional cuts or transfers out")
    elif available_scholarships < 5:
        print(f"⚠️  Limited scholarships available ({available_scholarships})")
        print("   Focus on highest-priority positions only")
    else:
        print(f"✅ Good scholarship flexibility ({available_scholarships} available)")


def generate_dynasty_report(roster_df, recruiting_plan):
    """Generate comprehensive dynasty management report."""
    print("\n📋 DYNASTY MANAGEMENT REPORT")
    print("=" * 40)
    
    # Overall team strength
    if 'Grade' in recruiting_plan.columns:
        avg_grade_mapping = {'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 
                            'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0}
        
        numeric_grades = recruiting_plan['Grade'].map(avg_grade_mapping)
        team_gpa = numeric_grades.mean()
        
        print(f"🏆 Team Strength GPA: {team_gpa:.2f}/4.3")
        
        if team_gpa >= 3.5:
            print("   ✅ Championship-caliber roster depth")
        elif team_gpa >= 3.0:
            print("   👍 Competitive roster with some weaknesses")
        elif team_gpa >= 2.5:
            print("   ⚠️  Rebuilding roster - focus on key positions")
        else:
            print("   🚨 Major rebuilding needed across multiple positions")
    
    # Key recommendations
    print("\n🎯 KEY RECOMMENDATIONS:")
    
    # High-priority recruiting
    high_priority = recruiting_plan[recruiting_plan['Priority'] == 'HIGH']
    if len(high_priority) > 0:
        print(f"   🔴 Immediate needs: {', '.join(high_priority['Position'].tolist())}")
    
    # Strongest positions
    strong_positions = recruiting_plan[recruiting_plan['Grade'].isin(['A+', 'A', 'A-'])]
    if len(strong_positions) > 0:
        print(f"   💪 Position strengths: {', '.join(strong_positions['Position'].tolist())}")
    
    # Development opportunities
    if 'VALUE' in roster_df.columns:
        high_value_underclassmen = roster_df[
            (roster_df['VALUE'] > 150) & 
            (roster_df['YEAR'].isin(['FR', 'SO', 'FR (RS)', 'SO (RS)']))
        ]
        if len(high_value_underclassmen) > 0:
            print(f"   ⭐ Future stars to develop: {len(high_value_underclassmen)} high-value underclassmen")


def main():
    """Run advanced dynasty management analysis."""
    print("🏈 CFB Dynasty - Advanced Management Analysis")
    print("=" * 50)
    
    try:
        # Load and analyze roster
        print("📊 Loading roster data...")
        roster_df = load_roster()
        
        if roster_df is None:
            print("❌ No roster data found. Please add a CSV file to ~/Downloads")
            return
        
        print("🔍 Running comprehensive analysis...")
        # Find the roster file in Downloads
        downloads_folder = os.path.expanduser('~/Downloads')
        roster_files = glob.glob(os.path.join(downloads_folder, '*[Rr]oster.csv'))
        if not roster_files:
            print("❌ No roster file found in Downloads")
            return
        analyzed_roster, recruiting_plan = process_roster_and_create_recruiting_plan(
            roster_files[0]  # Use the first roster file found
        )
        
        # Run advanced analyses
        analyze_graduation_impact(analyzed_roster)
        project_future_roster(analyzed_roster, years_ahead=2)
        identify_position_change_candidates(analyzed_roster)
        create_transfer_portal_strategy(analyzed_roster, recruiting_plan)
        analyze_scholarship_situation(analyzed_roster)
        generate_dynasty_report(analyzed_roster, recruiting_plan)
        
        # Export everything
        print("\n💾 Exporting comprehensive analysis...")
        export_files(
            roster_df=analyzed_roster,
            recruiting_plan=recruiting_plan,
            position_requirements=DEFAULT_POSITION_REQUIREMENTS
        )
        
        print("\n🎉 Advanced analysis complete!")
        print("📁 Check ~/Downloads/cfb_dynasty_data/ for detailed reports")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
