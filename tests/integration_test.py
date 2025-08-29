#!/usr/bin/env python3
"""
Integration Test - CFB Dynasty Data Package

This script tests all major functionality to ensure the package works correctly
after reorganization and optimization.
"""

import sys
import os
import tempfile
import pandas as pd

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfb_dynasty import *


def test_player_functionality():
    """Test Player class functionality."""
    print("🏃 Testing Player class...")
    
    # Test player creation
    player = Player(
        first_name="Test",
        last_name="Player",
        position="QB", 
        year="FR",
        overall=85,
        base_overall=82,
        dev_trait="STAR"
    )
    
    assert player.first_name == "Test"
    assert player.position == "QB"
    assert player.year == "FR"
    
    # Test year advancement
    new_year = player.advance_year()
    assert new_year == "SO"
    
    # Test dictionary conversion
    player_dict = player.to_dict()
    assert 'first_name' in player_dict
    assert player_dict['position'] == 'QB'
    
    # Test from_dict creation
    new_player = Player.from_dict(player_dict)
    assert new_player.first_name == player.first_name
    
    print("   ✅ Player class tests passed")


def test_analysis_functions():
    """Test analysis functions."""
    print("🔍 Testing analysis functions...")
    
    # Test player value calculation
    test_data = pd.Series({
        'BASE OVERALL': 85,
        'DEV TRAIT': 'STAR',
        'YEAR': 'FR'
    })
    
    value = calculate_player_value(test_data)
    assert isinstance(value, float)
    assert value > 0
    
    # Test position grade calculation
    grade = calculate_position_grade(150)
    assert grade == 'A+'
    
    grade = calculate_position_grade(75)
    assert grade == 'C-'
    
    print("   ✅ Analysis function tests passed")


def test_configuration_access():
    """Test configuration constants."""
    print("⚙️  Testing configuration access...")
    
    # Test constants are accessible
    assert isinstance(DEV_TRAIT_MULTIPLIERS, dict)
    assert 'ELITE' in DEV_TRAIT_MULTIPLIERS
    assert DEV_TRAIT_MULTIPLIERS['ELITE'] == 1.5
    
    assert isinstance(DEFAULT_POSITION_REQUIREMENTS, dict)
    assert 'QB' in DEFAULT_POSITION_REQUIREMENTS
    assert 'min' in DEFAULT_POSITION_REQUIREMENTS['QB']
    
    print("   ✅ Configuration access tests passed")


def test_data_generation():
    """Test roster generation functionality."""
    print("📊 Testing data generation...")
    
    # Create sample data
    roster_data = pd.DataFrame({
        'FIRST NAME': ['John', 'Mike'],
        'LAST NAME': ['Doe', 'Smith'],
        'POSITION': ['QB', 'WR'],
        'YEAR': ['JR', 'SO'],
        'OVERALL': [85, 80],
        'BASE OVERALL': [82, 78],
        'REDSHIRT': [False, False],
        'CUT': [False, False],
        'DRAFTED': ['', ''],
        'STATUS': ['ACTIVE', 'ACTIVE'],
        'TRANSFER OUT': [False, False]
    })
    
    recruits_data = pd.DataFrame({
        'FIRST NAME': ['New'],
        'LAST NAME': ['Recruit'],
        'POSITION': ['HB'],  # Use HB instead of RB to match CFB naming convention
        'YEAR': ['HS'],
        'COMMITTED TO': ['USC']
    })
    
    # Test roster generation
    new_roster = generate_roster(roster_data, recruits_data, 'USC')
    print(f"   DEBUG: Original roster length: {len(roster_data)}")
    print(f"   DEBUG: New roster length: {len(new_roster)}")
    print(f"   DEBUG: Positions in new roster: {new_roster['POSITION'].unique()}")
    print(f"   DEBUG: Recruits data: {recruits_data}")
    
    assert len(new_roster) >= len(roster_data)  # Should include recruits
    # Check that the HB recruit was added
    assert 'HB' in new_roster['POSITION'].values  # Should include recruit
    
    print("   ✅ Data generation tests passed")


def test_utility_functions():
    """Test utility functions."""
    print("🛠️  Testing utility functions...")
    
    # Test validation
    valid_player_data = {
        'first_name': 'John',
        'last_name': 'Doe', 
        'position': 'QB',
        'year': 'FR',
        'redshirt': False
    }
    
    is_valid = validate_player_data(valid_player_data)
    assert is_valid == True
    
    # Test invalid data
    invalid_player_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        # Missing required fields
    }
    
    is_valid = validate_player_data(invalid_player_data)
    assert is_valid == False
    
    print("   ✅ Utility function tests passed")


def test_performance_optimizations():
    """Test performance optimization features."""
    print("⚡ Testing performance optimizations...")
    
    try:
        from cfb_dynasty.utils.performance import (
            DataFrameOptimizer, 
            optimize_for_large_datasets,
            analysis_cache
        )
        
        # Create test DataFrame
        test_df = pd.DataFrame({
            'POSITION': ['QB'] * 100,
            'YEAR': ['FR'] * 100,
            'VALUE': list(range(100))
        })
        
        # Test optimization
        optimized_df = optimize_for_large_datasets(test_df, threshold=50)
        assert len(optimized_df) == len(test_df)
        
        # Test cache functionality
        analysis_cache.set('test_key', 'test_value')
        cached_value = analysis_cache.get('test_key')
        assert cached_value == 'test_value'
        
        print("   ✅ Performance optimization tests passed")
    
    except ImportError:
        print("   ⚠️  Performance optimizations not available (optional)")


def test_comprehensive_workflow():
    """Test the complete analysis workflow."""
    print("🔄 Testing comprehensive workflow...")
    
    # Create comprehensive test data
    test_roster = pd.DataFrame({
        'REDSHIRT': [False, False, True, False],
        'FIRST NAME': ['John', 'Mike', 'Chris', 'David'],
        'LAST NAME': ['Smith', 'Johnson', 'Brown', 'Wilson'],
        'YEAR': ['FR', 'SO', 'JR (RS)', 'SR'],
        'POSITION': ['QB', 'WR', 'HB', 'TE'],  # Use HB instead of RB
        'OVERALL': [85, 80, 88, 90],
        'BASE OVERALL': [82, 78, 85, 87],
        'RATING': [85, 80, 88, 90],  # Add RATING column for roster analysis
        'CITY': ['Dallas', 'Houston', 'Austin', 'San Antonio'],
        'STATE': ['TX', 'TX', 'TX', 'TX'],
        'ARCHETYPE': ['DUAL THREAT', 'SPEEDSTER', 'ELUSIVE BRUISER', 'VERTICAL THREAT'],
        'DEV TRAIT': ['STAR', 'NORMAL', 'ELITE', 'IMPACT'],
        'CUT': [False, False, False, False],
        'TRANSFER OUT': [False, False, False, False],
        'DRAFTED': ['', '', '', ''],
        'VALUE': ['', '', '', ''],
        'STATUS': ['', '', '', '']
    })
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        test_roster.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        # Test complete analysis pipeline
        processed_roster, recruiting_plan = process_roster_and_create_recruiting_plan(temp_file)
        
        assert len(processed_roster) == len(test_roster)
        assert 'VALUE' in processed_roster.columns
        assert not processed_roster['VALUE'].isna().all()  # Values should be calculated
        
        assert len(recruiting_plan) > 0
        assert 'Position' in recruiting_plan.columns
        assert 'Priority' in recruiting_plan.columns
        
        print("   ✅ Comprehensive workflow tests passed")
        
    finally:
        # Clean up temporary file
        os.unlink(temp_file)


def run_integration_tests():
    """Run all integration tests."""
    print("🧪 CFB Dynasty Data - Integration Tests")
    print("=" * 50)
    
    try:
        test_player_functionality()
        test_analysis_functions()
        test_configuration_access()
        test_data_generation()
        test_utility_functions()
        test_performance_optimizations()
        test_comprehensive_workflow()
        
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ Package is working correctly")
        return True
        
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def benchmark_performance():
    """Run basic performance benchmarks."""
    print("\n⚡ PERFORMANCE BENCHMARKS")
    print("=" * 30)
    
    import time
    
    # Benchmark player creation
    start_time = time.time()
    players = []
    for i in range(1000):
        player = Player(
            first_name=f"Player{i}",
            last_name="Test",
            position="QB",
            year="FR"
        )
        players.append(player)
    
    creation_time = time.time() - start_time
    print(f"🏃 Created 1,000 players in {creation_time:.3f}s ({creation_time*1000:.1f}ms per player)")
    
    # Benchmark value calculation
    test_data = pd.DataFrame({
        'BASE OVERALL': [85] * 1000,
        'DEV TRAIT': ['STAR'] * 1000,
        'YEAR': ['FR'] * 1000
    })
    
    start_time = time.time()
    values = test_data.apply(calculate_player_value, axis=1)
    calc_time = time.time() - start_time
    print(f"💰 Calculated 1,000 player values in {calc_time:.3f}s ({calc_time*1000:.1f}ms per calculation)")
    
    print(f"📊 Total benchmark time: {creation_time + calc_time:.3f}s")


if __name__ == "__main__":
    # Run integration tests
    success = run_integration_tests()
    
    if success:
        # Run performance benchmarks
        benchmark_performance()
        
        print("\n🚀 Package is ready for use!")
        print("📖 Check examples/ directory for usage examples")
        print("📚 Check docs/ directory for detailed documentation")
    else:
        print("\n⚠️  Please fix failing tests before using the package")
        sys.exit(1)
