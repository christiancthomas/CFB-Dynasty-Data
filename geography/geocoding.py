"""
Geocoding utilities for city coordinate lookup.

This module provides enhanced geocoding functionality with retry logic,
timeout handling, and simple JSON-based coordinate storage.
"""

import time
from typing import Optional, Tuple
from .simple_cache import get_city_coordinates_from_json, store_city_coordinates_to_json, get_coordinates_stats, clear_coordinates


def get_city_coordinates(city: str, state: str, cache_legacy=None, timeout: int = 10, max_retries: int = 2) -> Optional[Tuple[float, float]]:
    """
    Get coordinates for a city using JSON file lookup first, then geopy if needed.

    Args:
        city (str): City name
        state (str): State abbreviation (e.g., 'TX', 'CA') or full name
        cache_legacy: Deprecated legacy cache parameter (ignored)
        timeout (int): Timeout in seconds for geocoding requests
        max_retries (int): Maximum number of retry attempts

    Returns:
        tuple: (latitude, longitude) if successful, None if failed
    """
    # First, check the JSON file for cached coordinates
    cached_coords = get_city_coordinates_from_json(city, state)
    if cached_coords is not None:
        print(f"📦 Using saved coordinates for {city}, {state}")
        return cached_coords

    # If not in JSON file, make API call to geopy
    print(f"🌐 Geocoding {city}, {state} via API...")

    for attempt in range(max_retries + 1):
        try:
            from geopy.geocoders import Nominatim

            # Exponential backoff for retries
            if attempt > 0:
                delay = 0.5 * (2 ** attempt)  # 0.5s, 1s, 2s delays
                time.sleep(delay)
                print(f"🔄 Retry {attempt} for {city}, {state}")
            else:
                time.sleep(0.1)  # Base rate limiting

            # Configure explicit timeout
            geolocator = Nominatim(
                user_agent="cfb_dynasty_analysis",
                timeout=timeout
            )
            location = geolocator.geocode(f"{city}, {state}, USA")

            if location:
                coords = (location.latitude, location.longitude)

                # Store in JSON file for future use
                store_city_coordinates_to_json(city, state, coords[0], coords[1])

                if attempt > 0:
                    print(f"✅ Successfully geocoded {city}, {state} on retry {attempt}")
                return coords
            else:
                print(f"⚠️  Could not find coordinates for {city}, {state}")
                return None

        except Exception as e:
            error_msg = str(e).lower()
            if ("timed out" in error_msg or "timeout" in error_msg) and attempt < max_retries:
                print(f"⏱️ Timeout for {city}, {state} - retrying in {0.5 * (2 ** (attempt + 1))}s...")
                continue
            elif attempt == max_retries:
                print(f"⚠️  Failed to geocode {city}, {state} after {max_retries + 1} attempts: {e}")
                break
            else:
                print(f"⚠️  Could not geocode {city}, {state}: {e}")
                break

    return None


def clear_coordinate_cache() -> bool:
    """
    Clear all cached coordinates.

    Returns:
        bool: True if successfully cleared, False otherwise
    """
    return clear_coordinates()


def get_cache_statistics() -> dict:
    """
    Get statistics about the coordinate cache.

    Returns:
        dict: Cache statistics including total cities and states
    """
    return get_coordinates_stats()
