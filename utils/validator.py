"""
Validator functions for various data inputs in the CFB Dynasty Data system.
"""

def validate_player_data(player_data: dict) -> bool:
    """
    Validates the player data dictionary to ensure all required fields are present and correctly formatted.
    
    Args:
        player_data (dict): Dictionary containing player attributes.
        
    Returns:
        bool: True if validation passes, False otherwise.
    """
    required_fields = ['first_name', 'last_name', 'position', 'year', 'redshirt']
    
    for field in required_fields:
        if field not in player_data:
            print(f"Missing required field: {field}")
            return False
    
    if not isinstance(player_data['first_name'], str) or not isinstance(player_data['last_name'], str):
        print("First name and last name must be strings.")
        return False
    
    if not isinstance(player_data['position'], str):
        print("Position must be a string.")
        return False
    
    if player_data['year'] not in ['HS', 'FR', 'FR (RS)', 'SO', 'SO (RS)', 'JR', 'JR (RS)', 'SR', 'SR (RS)']:
        print("Year must be one of: HS, FR, FR (RS), SO, SO (RS), JR, JR (RS), SR, SR (RS).")
        return False
    
    if not isinstance(player_data['redshirt'], bool):
        print("Redshirt status must be a boolean.")
        return False
    
    return True