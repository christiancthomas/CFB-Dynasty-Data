"""
CFB Dynasty Data Package

Contains data processing, I/O, and validation utilities.
"""

from .roster_generator import (
    generate_roster,
    save_roster_to_csv,
)

__all__ = [
    'generate_roster',
    'save_roster_to_csv',
]
