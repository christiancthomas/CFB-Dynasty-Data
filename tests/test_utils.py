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
from cfb_dynasty.utils.file_utils import _clean_csv_borders


class TestValidatePlayerData(unittest.TestCase):

    def test_valid_player_data(self):
        """Test validation passes for valid player data"""
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


class TestCleanCsvBorders(unittest.TestCase):
    """Tests for _clean_csv_borders functionality for non-standard CSV borders"""

    def test_clean_csv_no_borders(self):
        """Test that clean CSVs are returned unchanged."""
        df = pd.DataFrame({
            'FIRST NAME': ['Arch', 'Jeremiah'],
            'LAST NAME': ['Manning', 'Smith'],
            'POSITION': ['QB', 'WR'],
            'YEAR': ['FR', 'SO'],
            'OVERALL': [85, 94]
        })
        result = _clean_csv_borders(df.copy())
        self.assertEqual(list(result.columns), list(df.columns))
        self.assertEqual(len(result), len(df))

    def test_clean_csv_single_empty_column_left(self):
        """Test removal of single empty column on the left (Google Sheets border)."""
        df = pd.DataFrame({
            '': [None, None, None],
            'FIRST NAME': ['Arch', 'Jeremiah', 'Jeremiyah'],
            'LAST NAME': ['Manning', 'Smith', 'Love'],
            'POSITION': ['QB', 'WR', 'HB']
        })
        result = _clean_csv_borders(df)
        self.assertEqual(result.columns[0], 'FIRST NAME')
        self.assertEqual(len(result.columns), 3)

    def test_clean_csv_multiple_empty_columns_left(self):
        """Test removal of multiple empty columns on the left."""
        df = pd.DataFrame({
            'Unnamed: 0': [None, None],
            'Unnamed: 1': [None, None],
            'Unnamed: 2': [None, None],
            'FIRST NAME': ['Arch', 'Jeremiah'],
            'POSITION': ['QB', 'WR']
        })
        result = _clean_csv_borders(df)
        self.assertEqual(result.columns[0], 'FIRST NAME')
        self.assertEqual(len(result.columns), 2)

    def test_clean_csv_empty_columns_both_sides(self):
        """Test removal of empty columns on both left and right."""
        df = pd.DataFrame({
            'Unnamed: 0': [None, None],
            'FIRST NAME': ['Arch', 'Jeremiah'],
            'POSITION': ['QB', 'WR'],
            'Unnamed: 3': [None, None],
            '': [None, None]
        })
        result = _clean_csv_borders(df)
        self.assertEqual(result.columns[0], 'FIRST NAME')
        self.assertEqual(result.columns[-1], 'POSITION')
        self.assertEqual(len(result.columns), 2)

    def test_clean_csv_header_row_offset(self):
        """Test detection and promotion of header row when offset by empty rows."""
        # Simulate CSV where pandas reads empty first row as headers
        # and real headers are in row 0 of data
        df = pd.DataFrame({
            'Unnamed: 0': ['FIRST NAME', 'Arch', 'Jeremiah'],
            'Unnamed: 1': ['LAST NAME', 'Manning', 'Smith'],
            'Unnamed: 2': ['POSITION', 'QB', 'WR'],
            'Unnamed: 3': ['YEAR', 'FR', 'SO']
        })
        result = _clean_csv_borders(df)
        self.assertIn('FIRST NAME', result.columns)
        self.assertIn('POSITION', result.columns)
        self.assertEqual(len(result), 2)  # Should have 2 data rows
        self.assertEqual(result.iloc[0]['FIRST NAME'], 'Arch')

    def test_clean_csv_header_offset_with_border_column(self):
        """Test combined border column and header row offset (real-world scenario)."""
        # This simulates: empty first column + header in row 0
        df = pd.DataFrame({
            'Unnamed: 0': [None, None, None],
            'Unnamed: 1': ['REDSHIRT', None, 'RS'],
            'Unnamed: 2': ['FIRST NAME', 'Arch', 'Jeremiah'],
            'Unnamed: 3': ['LAST NAME', 'Manning', 'Smith'],
            'Unnamed: 4': ['POSITION', 'QB', 'WR']
        })
        result = _clean_csv_borders(df)
        self.assertIn('FIRST NAME', result.columns)
        self.assertEqual(len(result), 2)

    def test_clean_csv_multiple_header_row_offset(self):
        """Test header detection when multiple empty rows precede the headers."""
        # Headers are in row index 2 (3rd row of data)
        df = pd.DataFrame({
            'Unnamed: 0': [None, None, 'FIRST NAME', 'Arch'],
            'Unnamed: 1': [None, None, 'LAST NAME', 'Manning'],
            'Unnamed: 2': [None, None, 'POSITION', 'QB'],
            'Unnamed: 3': [None, None, 'OVERALL', '85']
        })
        result = _clean_csv_borders(df)
        self.assertIn('FIRST NAME', result.columns)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['FIRST NAME'], 'Arch')

    def test_clean_csv_empty_rows_at_end(self):
        """Test removal of empty rows at the end of data."""
        df = pd.DataFrame({
            'FIRST NAME': ['Arch', 'Jeremiah', None, None],
            'LAST NAME': ['Manning', 'Smith', None, None],
            'POSITION': ['QB', 'WR', None, None]
        })
        result = _clean_csv_borders(df)
        self.assertEqual(len(result), 2)

    def test_clean_csv_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame()
        result = _clean_csv_borders(df)
        self.assertTrue(result.empty)

    def test_clean_csv_preserves_data_integrity(self):
        """Test that actual data values are preserved after cleaning."""
        df = pd.DataFrame({
            'Unnamed: 0': [None, None, None],
            'Unnamed: 1': ['FIRST NAME', 'Christian', 'Kallum'],
            'Unnamed: 2': ['POSITION', 'QB', 'FS'],
            'Unnamed: 3': ['OVERALL', '91', '90']
        })
        result = _clean_csv_borders(df)
        self.assertEqual(result.iloc[0]['FIRST NAME'], 'Christian')
        self.assertEqual(result.iloc[1]['POSITION'], 'FS')
        self.assertEqual(result.iloc[0]['OVERALL'], '91')


if __name__ == '__main__':
    unittest.main()
