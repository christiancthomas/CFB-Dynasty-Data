"""
Geocoding utilities for city coordinate lookup.

This module provides enhanced geocoding functionality with retry logic
and timeout handling for reliable city coordinate lookup.
"""

import time


def get_city_coordinates(city, state, cache={}, timeout=10, max_retries=2):
    """
    Get coordinates for a city using geopy with improved timeout handling.

    Args:
        city (str): City name
        state (str): State abbreviation (e.g., 'TX', 'CA')
        cache (dict): Cache dictionary for storing results (persistent across calls)
        timeout (int): Timeout in seconds for geocoding requests
        max_retries (int): Maximum number of retry attempts

    Returns:
        tuple: (latitude, longitude) if successful, None if failed
    """
    key = f"{city}, {state}"

    if key in cache:
        return cache[key]

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
                cache[key] = coords
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

    cache[key] = None
    return None
