#!/usr/bin/env python3
"""
Player Valuation Example

This script demonstrates advanced player valuation techniques and comparisons.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfb_dynasty import (
    Player, 
    calculate_player_value,
    DEV_TRAIT_MULTIPLIERS,
    REMAINING_YEARS
)
import pandas as pd


def demonstrate_player_creation():
    """Show how to create and manipulate Player objects."""
    print("🏃 PLAYER CREATION EXAMPLES")
    print("-" * 30)
    
    # Create different types of players
    players = [
        Player(
            first_name="Elite", 
            last_name="Quarterback", 
            position="QB", 
            year="FR",
            overall=90,
            base_overall=88,
            dev_trait="ELITE"
        ),
        Player(
            first_name="Star",
            last_name="Linebacker",
            position="WILL",
            year="SO (RS)",  # Redshirt Sophomore
            overall=85,
            base_overall=82,
            dev_trait="STAR",
            redshirt=True
        ),
        Player(
            first_name="Normal",
            last_name="Receiver",
            position="WR",
            year="JR",
            overall=80,
            base_overall=78,
            dev_trait="NORMAL"
        )
    ]
    
    # Display players and their advancement
    for player in players:
        print(f"\n📋 {player}")
        print(f"   Current Year: {player.year}")
        print(f"   Development: {player.dev_trait}")
        print(f"   Next Year: {player.advance_year()}")
        
        # Calculate value
        player_data = pd.Series({
            'BASE OVERALL': player.base_overall,
            'DEV TRAIT': player.dev_trait,
            'YEAR': player.year
        })
        value = calculate_player_value(player_data)
        print(f"   Dynasty Value: {value}")


def demonstrate_value_calculations():
    """Show how different factors affect player value."""
    print("\n💰 VALUE CALCULATION EXAMPLES")
    print("-" * 30)
    
    # Base player for comparison
    base_player = {
        'BASE OVERALL': 85,
        'DEV TRAIT': 'NORMAL',
        'YEAR': 'FR'
    }
    
    print(f"Base Player (85 OVR FR Normal): {calculate_player_value(pd.Series(base_player))}")
    
    # Show impact of development trait
    print("\n🔥 Impact of Development Trait:")
    for trait, multiplier in DEV_TRAIT_MULTIPLIERS.items():
        test_player = base_player.copy()
        test_player['DEV TRAIT'] = trait
        value = calculate_player_value(pd.Series(test_player))
        print(f"   {trait:8} ({multiplier:4.2f}x): {value:6.2f}")
    
    # Show impact of remaining years
    print("\n📅 Impact of Remaining Eligibility:")
    for year, remaining in REMAINING_YEARS.items():
        test_player = base_player.copy()
        test_player['YEAR'] = year
        value = calculate_player_value(pd.Series(test_player))
        print(f"   {year:8} ({remaining} years left): {value:6.2f}")
    
    # Show impact of rating
    print("\n⭐ Impact of Base Rating:")
    for rating in [70, 75, 80, 85, 90, 95]:
        test_player = base_player.copy()
        test_player['BASE OVERALL'] = rating
        value = calculate_player_value(pd.Series(test_player))
        print(f"   {rating} OVR: {value:6.2f}")


def find_hidden_gems():
    """Demonstrate finding undervalued players."""
    print("\n💎 FINDING HIDDEN GEMS")
    print("-" * 30)
    
    # Create sample roster data
    sample_roster = pd.DataFrame({
        'FIRST NAME': ['John', 'Mike', 'Chris', 'David', 'Alex'],
        'LAST NAME': ['Smith', 'Johnson', 'Brown', 'Wilson', 'Davis'],
        'POSITION': ['QB', 'WR', 'RB', 'TE', 'QB'],
        'BASE OVERALL': [78, 82, 75, 80, 73],
        'DEV TRAIT': ['ELITE', 'NORMAL', 'STAR', 'NORMAL', 'STAR'],
        'YEAR': ['FR', 'SO', 'FR', 'JR', 'FR']
    })
    
    # Calculate values
    sample_roster['VALUE'] = sample_roster.apply(calculate_player_value, axis=1)
    
    # Find gems (high value despite lower rating)
    print("Players with high dynasty value despite lower current rating:")
    gems = sample_roster[(sample_roster['BASE OVERALL'] < 80) & (sample_roster['VALUE'] > 130)]
    
    for _, player in gems.iterrows():
        print(f"   🌟 {player['FIRST NAME']} {player['LAST NAME']} ({player['POSITION']})")
        print(f"      Rating: {player['BASE OVERALL']} | Value: {player['VALUE']:.1f}")
        print(f"      Why: {player['DEV TRAIT']} development, {player['YEAR']} eligibility")


def compare_recruiting_targets():
    """Compare potential recruiting targets."""
    print("\n🎯 RECRUITING TARGET COMPARISON")
    print("-" * 30)
    
    # Create sample recruits
    recruits = pd.DataFrame({
        'FIRST NAME': ['Star', 'Elite', 'Normal', 'Impact'],
        'LAST NAME': ['Recruit', 'Prospect', 'Player', 'Freshman'],
        'POSITION': ['QB', 'QB', 'QB', 'QB'],
        'BASE OVERALL': [82, 80, 85, 78],
        'DEV TRAIT': ['STAR', 'ELITE', 'NORMAL', 'IMPACT'],
        'YEAR': ['HS', 'HS', 'HS', 'HS']  # All high school recruits
    })
    
    # Convert HS to FR for value calculation
    recruits['CALC_YEAR'] = 'FR'
    
    # Calculate 4-year dynasty value projection
    recruits['4_YEAR_VALUE'] = recruits.apply(
        lambda row: calculate_player_value(pd.Series({
            'BASE OVERALL': row['BASE OVERALL'],
            'DEV TRAIT': row['DEV TRAIT'],
            'YEAR': row['CALC_YEAR']
        })), axis=1
    )
    
    # Sort by dynasty value
    recruits = recruits.sort_values('4_YEAR_VALUE', ascending=False)
    
    print("QB Recruiting Targets (ranked by 4-year dynasty value):")
    for i, (_, recruit) in enumerate(recruits.iterrows(), 1):
        print(f"   {i}. {recruit['FIRST NAME']} {recruit['LAST NAME']}")
        print(f"      Current: {recruit['BASE OVERALL']} OVR | Development: {recruit['DEV TRAIT']}")
        print(f"      4-Year Value: {recruit['4_YEAR_VALUE']:.1f}")
        print()


def main():
    """Run all player valuation examples."""
    print("🏈 CFB Dynasty - Player Valuation Examples")
    print("=" * 50)
    
    demonstrate_player_creation()
    demonstrate_value_calculations()
    find_hidden_gems()
    compare_recruiting_targets()
    
    print("\n✅ All examples complete!")
    print("\nKey Takeaways:")
    print("• Development trait has huge impact on dynasty value")
    print("• Younger players with good development > older players with high rating")
    print("• Look for 'hidden gems' with high value despite lower current rating")
    print("• Use dynasty value to make recruiting priority decisions")


if __name__ == "__main__":
    main()
