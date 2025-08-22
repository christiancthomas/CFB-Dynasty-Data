import unittest
import sys
import os
from hashlib import md5
from models.Player import Player


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_player_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'position': 'QB',
            'year': 'FR',
            'overall': '85',
            'base_overall': '82',
            'city': 'Atlanta',
            'state': 'GA',
            'archetype': 'POCKET PASSER',
            'dev_trait': 'STAR',
            'cut': False,
            'drafted': '',
            'redshirt': False,
            'value': 125.5,
            'status': 'SAFE',
            'team': 'Rice',
            'national_rank': '150',
            'stars': '4',
            'gem_status': 'NORMAL',
            'committed_to': 'Rice'
        }

    def test_player_initialization(self):
        """Test that a player can be initialized with all attributes."""
        player = Player(**self.sample_player_data)

        # Test all attributes are set correctly
        self.assertEqual(player.first_name, 'John')
        self.assertEqual(player.last_name, 'Smith')
        self.assertEqual(player.position, 'QB')
        self.assertEqual(player.year, 'FR')
        self.assertEqual(player.overall, '85')
        self.assertEqual(player.base_overall, '82')
        self.assertEqual(player.city, 'Atlanta')
        self.assertEqual(player.state, 'GA')
        self.assertEqual(player.archetype, 'POCKET PASSER')
        self.assertEqual(player.dev_trait, 'STAR')
        self.assertEqual(player.cut, False)
        self.assertEqual(player.drafted, '')
        self.assertEqual(player.redshirt, False)
        self.assertEqual(player.value, 125.5)
        self.assertEqual(player.status, 'SAFE')
        self.assertEqual(player.team, 'Rice')
        self.assertEqual(player.national_rank, '150')
        self.assertEqual(player.stars, '4')
        self.assertEqual(player.gem_status, 'NORMAL')
        self.assertEqual(player.committed_to, 'Rice')

    def test_player_id_generation(self):
        """Test that player ID is generated correctly using MD5 hash."""
        player = Player(**self.sample_player_data)

        # Generate expected ID
        expected_id = md5(f"{player.first_name}{player.last_name}{player.position}{player.city}{player.state}".lower().replace(" ", "").encode()).hexdigest()
        self.assertEqual(player.player_id, expected_id)

    def test_player_id_uniqueness(self):
        """Test that different players have different IDs."""
        player1 = Player(**self.sample_player_data)

        # Create a different player
        different_data = self.sample_player_data.copy()
        different_data['first_name'] = 'Mike'
        player2 = Player(**different_data)

        self.assertNotEqual(player1.player_id, player2.player_id)

    def test_player_str_representation(self):
        """Test the string representation of a player."""
        player = Player(**self.sample_player_data)
        expected_str = "John Smith - QB (FR)"
        self.assertEqual(str(player), expected_str)

    def test_to_dict_method(self):
        """Test converting player to dictionary representation."""
        player = Player(**self.sample_player_data)
        player_dict = player.to_dict()

        # Check that all attributes are present in the dictionary
        expected_keys = [
            'id', 'first_name', 'last_name', 'team', 'position', 'year',
            'overall', 'base_overall', 'city', 'state', 'archetype', 'dev_trait',
            'cut', 'drafted', 'redshirt', 'value', 'status', 'national_rank',
            'stars', 'gem_status', 'committed_to', 'transfer', 'transfer_out'
        ]

        for key in expected_keys:
            self.assertIn(key, player_dict)

        # Verify some specific values
        self.assertEqual(player_dict['first_name'], 'John')
        self.assertEqual(player_dict['last_name'], 'Smith')
        self.assertEqual(player_dict['position'], 'QB')
        self.assertEqual(player_dict['value'], 125.5)

    def test_from_dict_class_method(self):
        """Test creating a player from dictionary data."""
        player = Player.from_dict(self.sample_player_data)

        # Verify the player was created correctly
        self.assertEqual(player.first_name, 'John')
        self.assertEqual(player.last_name, 'Smith')
        self.assertEqual(player.position, 'QB')
        self.assertEqual(player.value, 125.5)

    def test_from_dict_with_missing_optional_fields(self):
        """Test creating a player from dictionary with only required fields."""
        minimal_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'position': 'RB',
            'year': 'SO'
        }

        player = Player.from_dict(minimal_data)

        # Check required fields
        self.assertEqual(player.first_name, 'Jane')
        self.assertEqual(player.last_name, 'Doe')
        self.assertEqual(player.position, 'RB')
        self.assertEqual(player.year, 'SO')

        # Check that optional fields have default values
        self.assertEqual(player.overall, '')
        self.assertEqual(player.city, '')
        self.assertEqual(player.cut, False)
        self.assertEqual(player.redshirt, False)

    def test_advance_year_freshman_to_sophomore(self):
        """Test advancing a freshman to sophomore year."""
        player = Player(**self.sample_player_data)
        player.year = 'FR'
        player.redshirt = False

        new_year = player.advance_year()
        self.assertEqual(new_year, 'SO')
        self.assertEqual(player.year, 'SO')

    def test_advance_year_with_redshirt(self):
        """Test advancing year when player becomes redshirted."""
        player = Player(**self.sample_player_data)
        player.year = 'FR'
        player.redshirt = True

        new_year = player.advance_year()
        self.assertEqual(new_year, 'FR (RS)')
        self.assertEqual(player.year, 'FR (RS)')

    def test_advance_year_redshirt_sophomore(self):
        """Test advancing a redshirt sophomore."""
        player = Player(**self.sample_player_data)
        player.year = 'SO (RS)'
        player.redshirt = True

        new_year = player.advance_year()
        self.assertEqual(new_year, 'JR (RS)')
        self.assertEqual(player.year, 'JR (RS)')

    def test_advance_year_senior_graduation(self):
        """Test that seniors graduate."""
        player = Player(**self.sample_player_data)
        player.year = 'SR'
        player.redshirt = False

        new_year = player.advance_year()
        self.assertEqual(new_year, 'GRADUATED')
        self.assertEqual(player.year, 'GRADUATED')

    def test_advance_year_high_school_to_freshman(self):
        """Test advancing from high school to freshman."""
        player = Player(**self.sample_player_data)
        player.year = 'HS'
        player.redshirt = False

        new_year = player.advance_year()
        self.assertEqual(new_year, 'FR')
        self.assertEqual(player.year, 'FR')

    def test_advance_year_invalid_year(self):
        """Test advance_year with invalid year returns unchanged."""
        player = Player(**self.sample_player_data)
        player.year = 'INVALID'
        player.redshirt = False

        new_year = player.advance_year()
        self.assertEqual(new_year, 'INVALID')
        self.assertEqual(player.year, 'INVALID')

    def test_player_boolean_attributes(self):
        """Test boolean attributes are handled correctly."""
        # Test with cut=True, redshirt=True
        data = self.sample_player_data.copy()
        data['cut'] = True
        data['redshirt'] = True

        player = Player(**data)
        self.assertTrue(player.cut)
        self.assertTrue(player.redshirt)

    def test_player_numeric_attributes(self):
        """Test numeric attributes are handled correctly."""
        data = self.sample_player_data.copy()
        data['value'] = 150.75

        player = Player(**data)
        self.assertEqual(player.value, 150.75)
        self.assertIsInstance(player.value, float)

    def test_round_trip_dict_conversion(self):
        """Test that converting to dict and back preserves all data."""
        original_player = Player(**self.sample_player_data)
        player_dict = original_player.to_dict()
        reconstructed_player = Player.from_dict(player_dict)

        # Compare all attributes
        self.assertEqual(original_player.first_name, reconstructed_player.first_name)
        self.assertEqual(original_player.last_name, reconstructed_player.last_name)
        self.assertEqual(original_player.position, reconstructed_player.position)
        self.assertEqual(original_player.year, reconstructed_player.year)
        self.assertEqual(original_player.value, reconstructed_player.value)
        self.assertEqual(original_player.cut, reconstructed_player.cut)
        self.assertEqual(original_player.redshirt, reconstructed_player.redshirt)

        # IDs should be the same since they're based on the same data
        self.assertEqual(original_player.player_id, reconstructed_player.player_id)

    def test_edge_cases_empty_strings(self):
        """Test handling of empty string values."""
        data = self.sample_player_data.copy()
        data['drafted'] = ''
        data['committed_to'] = ''

        player = Player(**data)
        self.assertEqual(player.drafted, '')
        self.assertEqual(player.committed_to, '')

    def test_edge_cases_special_characters(self):
        """Test handling of special characters in names and locations."""
        data = self.sample_player_data.copy()
        data['first_name'] = "José"
        data['last_name'] = "O'Brien-Smith"
        data['city'] = "San José"

        player = Player(**data)
        self.assertEqual(player.first_name, "José")
        self.assertEqual(player.last_name, "O'Brien-Smith")
        self.assertEqual(player.city, "San José")

        # ID should still be generated properly
        self.assertIsNotNone(player.player_id)
        self.assertIsInstance(player.player_id, str)


if __name__ == '__main__':
    unittest.main()
