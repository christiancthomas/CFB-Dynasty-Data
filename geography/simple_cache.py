"""
Simple JSON-based coordinate lookup for CFB Dynasty geography module.

This module provides direct JSON file lookup for city coordinates,
eliminating the need for in-memory caching.
"""

import json
import os
from typing import Dict, Optional, Tuple


def get_coordinates_file_path() -> str:
    """Get the path to the coordinates JSON file."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'city_coordinates.json')


def load_coordinates() -> Dict:
    """
    Load coordinates from JSON file.

    Returns:
        dict: Coordinates dictionary or empty dict if file doesn't exist
    """
    file_path = get_coordinates_file_path()

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error loading coordinates file: {e}")
            return {}
    else:
        return {}


def save_coordinates(coordinates: Dict) -> bool:
    """
    Save coordinates to JSON file.

    Args:
        coordinates (dict): Full coordinates dictionary to save

    Returns:
        bool: True if successful, False otherwise
    """
    file_path = get_coordinates_file_path()

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(coordinates, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"❌ Error saving coordinates file: {e}")
        return False


def get_city_coordinates_from_json(city: str, state: str) -> Optional[Tuple[float, float]]:
    """
    Get coordinates for a city from JSON file.

    Args:
        city (str): City name
        state (str): State name or abbreviation

    Returns:
        tuple: (latitude, longitude) if found, None if not found
    """
    coordinates = load_coordinates()
    state_key = normalize_state_name(state)

    if state_key in coordinates and city in coordinates[state_key]:
        coords = coordinates[state_key][city]
        return (coords['latitude'], coords['longitude'])

    return None


def store_city_coordinates_to_json(city: str, state: str, latitude: float, longitude: float) -> bool:
    """
    Store coordinates for a city in JSON file.

    Args:
        city (str): City name
        state (str): State name or abbreviation
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate

    Returns:
        bool: True if successfully stored, False otherwise
    """
    coordinates = load_coordinates()
    state_key = normalize_state_name(state)

    # Initialize state if not exists
    if state_key not in coordinates:
        coordinates[state_key] = {}

    # Store coordinates
    coordinates[state_key][city] = {
        'latitude': latitude,
        'longitude': longitude
    }

    # Save to file
    success = save_coordinates(coordinates)
    if success:
        print(f"💾 Saved coordinates for {city}, {state}")

    return success


def normalize_state_name(state: str) -> str:
    """
    Normalize state name/abbreviation to full state name.

    Args:
        state (str): State name or abbreviation

    Returns:
        str: Normalized state name
    """
    state_mapping = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }

    state_upper = state.upper()
    if state_upper in state_mapping:
        return state_mapping[state_upper]
    else:
        return state.title()


def get_coordinates_stats() -> Dict[str, int]:
    """
    Get statistics about stored coordinates.

    Returns:
        dict: Statistics including total cities and states
    """
    coordinates = load_coordinates()
    total_cities = sum(len(cities) for cities in coordinates.values())
    total_states = len(coordinates)

    return {
        'total_states': total_states,
        'total_cities': total_cities,
        'file_path': get_coordinates_file_path()
    }


def clear_coordinates() -> bool:
    """
    Clear all stored coordinates.

    Returns:
        bool: True if successfully cleared
    """
    return save_coordinates({})
