"""
Test utilities for CFB Dynasty Data system.

This module contains tests for utility functions in the package.
"""

import unittest
import os
import sys
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfb_dynasty.utils.validator import (
    validate_player_data,
    validate_roster_columns,
    validate_position,
    validate_year,
)


class TestValidatePlayerData(unittest.TestCase):
    """Tests for validate_player_data function."""

    def test_valid_player_data(self):
        """Test validation passes for valid player data."""
        player_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'position': 'QB',
            'year': 'FR',
            'redshirt': False
        }
        self.assertTrue(validate_player_data(player_data))

    def test_valid_redshirt_player(self):
        """Test validation passes for redshirt player."""
        player_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'position': 'WR',
            'year': 'SO (RS)',
            'redshirt': True
        }
        self.assertTrue(validate_player_data(player_data))

    def test_missing_required_field(self):
        """Test validation fails when required field is missing."""
        player_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'position': 'QB',
            # missing 'year' and 'redshirt'
        }
        self.assertFalse(validate_player_data(player_data))

    def test_invalid_year(self):
        """Test validation fails for invalid year."""
        player_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'position': 'QB',
            'year': 'INVALID',
            'redshirt': False
        }
        self.assertFalse(validate_player_data(player_data))

    def test_invalid_redshirt_type(self):
        """Test validation fails when redshirt is not boolean."""
        player_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'position': 'QB',
            'year': 'FR',
            'redshirt': 'yes'  # Should be bool
        }
        self.assertFalse(validate_player_data(player_data))

    def test_invalid_name_type(self):
        """Test validation fails when name is not a string."""
        player_data = {
            'first_name': 123,  # Should be string
            'last_name': 'Doe',
            'position': 'QB',
            'year': 'FR',
            'redshirt': False
        }
        self.assertFalse(validate_player_data(player_data))


class TestValidateRosterColumns(unittest.TestCase):
    """Tests for validate_roster_columns function."""

    def test_valid_roster_all_columns(self):
        """Test validation passes when all required columns present."""
        df = pd.DataFrame({
            'FIRST NAME': ['John'],
            'LAST NAME': ['Doe'],
            'POSITION': ['QB'],
            'YEAR': ['FR'],
            'REDSHIRT': [False]
        })
        is_valid, missing = validate_roster_columns(df)
        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    def test_missing_columns(self):
        """Test validation fails with missing columns."""
        df = pd.DataFrame({
            'FIRST NAME': ['John'],
            'LAST NAME': ['Doe'],
            # Missing POSITION, YEAR, REDSHIRT
        })
        is_valid, missing = validate_roster_columns(df)
        self.assertFalse(is_valid)
        self.assertIn('POSITION', missing)
        self.assertIn('YEAR', missing)
        self.assertIn('REDSHIRT', missing)

    def test_custom_required_columns(self):
        """Test validation with custom required columns."""
        df = pd.DataFrame({
            'NAME': ['John Doe'],
            'POS': ['QB']
        })
        is_valid, missing = validate_roster_columns(df, ['NAME', 'POS'])
        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

    def test_empty_dataframe(self):
        """Test validation with empty dataframe."""
        df = pd.DataFrame()
        is_valid, missing = validate_roster_columns(df)
        self.assertFalse(is_valid)
        self.assertEqual(len(missing), 5)  # All 5 default columns missing


class TestValidatePosition(unittest.TestCase):
    """Tests for validate_position function."""

    def test_valid_positions(self):
        """Test all valid positions pass validation."""
        valid_positions = [
            'QB', 'HB', 'FB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT',
            'LEDG', 'REDG', 'DT', 'WILL', 'MIKE', 'SAM', 'CB', 'FS', 'SS', 'K', 'P', 'ATH'
        ]
        for pos in valid_positions:
            self.assertTrue(validate_position(pos), f"{pos} should be valid")

    def test_lowercase_position(self):
        """Test lowercase positions are accepted."""
        self.assertTrue(validate_position('qb'))
        self.assertTrue(validate_position('wr'))

    def test_invalid_position(self):
        """Test invalid positions fail validation."""
        self.assertFalse(validate_position('INVALID'))
        self.assertFalse(validate_position('RB'))  # Should be HB
        self.assertFalse(validate_position('OL'))  # Generic, not specific


class TestValidateYear(unittest.TestCase):
    """Tests for validate_year function."""

    def test_valid_years(self):
        """Test all valid years pass validation."""
        valid_years = ['HS', 'FR', 'FR (RS)', 'SO', 'SO (RS)', 'JR', 'JR (RS)', 'SR', 'SR (RS)']
        for year in valid_years:
            self.assertTrue(validate_year(year), f"{year} should be valid")

    def test_invalid_year(self):
        """Test invalid years fail validation."""
        self.assertFalse(validate_year('FRESHMAN'))
        self.assertFalse(validate_year('fr'))  # Must be uppercase
        self.assertFalse(validate_year('GRADUATED'))


if __name__ == '__main__':
    unittest.main()
