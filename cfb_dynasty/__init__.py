"""
CFB Dynasty Data - College Football Dynasty Management System

A comprehensive toolkit for managing college football dynasty rosters,
analyzing player data, and creating recruiting plans.
"""

__version__ = "1.0.0"
__author__ = "Christian Thomas"

# Import key classes and functions for easy access
from .models.player import Player
from .data.roster_generator import generate_roster, save_roster_to_csv
from .analysis.roster_analysis import (
    process_roster_and_create_recruiting_plan,
    calculate_player_value,
    calculate_position_grade,
    scheme_fit
)
from .config.constants import (
    DEV_TRAIT_MULTIPLIERS,
    REMAINING_YEARS,
    DEFAULT_POSITION_REQUIREMENTS
)
from .utils.file_utils import load_roster, export_files
from .utils.validator import validate_player_data, validate_roster_columns

__all__ = [
    'Player',
    'generate_roster',
    'save_roster_to_csv',
    'process_roster_and_create_recruiting_plan',
    'calculate_player_value',
    'calculate_position_grade',
    'scheme_fit',
    'DEV_TRAIT_MULTIPLIERS',
    'REMAINING_YEARS',
    'DEFAULT_POSITION_REQUIREMENTS',
    'load_roster',
    'export_files',
    'validate_player_data',
    'validate_roster_columns',
]