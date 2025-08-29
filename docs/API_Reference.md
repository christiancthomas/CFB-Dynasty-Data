# CFB Dynasty Data - API Reference

## Core Classes

### Player

The `Player` class represents a college football player with all relevant attributes.

#### Constructor

```python
Player(
    first_name: str,
    last_name: str, 
    position: str,
    year: str,
    redshirt: bool = False,
    overall: int = 0,
    base_overall: int = 0,
    dev_trait: str = "NORMAL",
    archetype: str = "",
    # ... other attributes
)
```

#### Methods

- `advance_year()` - Advance the player's eligibility year
- `to_dict()` - Convert player to dictionary
- `from_dict(data)` - Create player from dictionary (class method)

#### Example

```python
from cfb_dynasty import Player

# Create a player
player = Player(
    first_name="John",
    last_name="Quarterback", 
    position="QB",
    year="FR",
    overall=85,
    base_overall=82,
    dev_trait="STAR"
)

# Advance to next year
new_year = player.advance_year()  # Returns "SO"
print(f"Player advanced to: {new_year}")

# Convert to dictionary
player_data = player.to_dict()
```

## Analysis Functions

### calculate_player_value

Calculate a player's dynasty value based on multiple factors.

**Formula**: `Base Rating × Dev Multiplier × (1 + Remaining Years / 4) × (1 - Redshirt Discount)`

```python
from cfb_dynasty import calculate_player_value
import pandas as pd

player_data = pd.Series({
    'BASE OVERALL': 85,
    'DEV TRAIT': 'STAR',
    'YEAR': 'FR'
})

value = calculate_player_value(player_data)
print(f"Player value: {value}")  # Output: 185.94
```

### process_roster_and_create_recruiting_plan

Comprehensive roster analysis with recruiting recommendations.

```python
from cfb_dynasty import process_roster_and_create_recruiting_plan

# Analyze roster and generate recruiting plan
roster_df, recruiting_plan = process_roster_and_create_recruiting_plan(
    "path/to/roster.csv"
)

print("Top recruiting priorities:")
high_priority = recruiting_plan[recruiting_plan['Priority'] == 'HIGH']
print(high_priority[['Position', 'Current Count', 'Min Required', 'Grade']])
```

### scheme_fit

Analyze how well players fit your scheme and identify position change candidates.

```python
from cfb_dynasty import scheme_fit, DEFAULT_POSITION_REQUIREMENTS

roster_df, scheme_analysis = scheme_fit(
    roster_df, 
    position_requirements=DEFAULT_POSITION_REQUIREMENTS
)

# View scheme fit recommendations
problem_positions = scheme_analysis[scheme_analysis['SCHEME FIT'] != '']
print(problem_positions[['POSITION', 'SCHEME FIT']])
```

## Data Generation

### generate_roster

Create a new season roster by advancing years and adding recruits.

```python
from cfb_dynasty import generate_roster
import pandas as pd

# Load data
roster_df = pd.read_csv("current_roster.csv")
recruits_df = pd.read_csv("recruiting_class.csv")

# Generate new roster
new_roster = generate_roster(
    roster_df, 
    recruits_df, 
    school_name="USC"
)

print(f"New roster size: {len(new_roster)} players")
```

## Utility Functions

### load_roster

Automatically find and load roster CSV files.

```python
from cfb_dynasty import load_roster

# Load from default location (~/Downloads)
roster_df = load_roster()

# Load from specific folder
roster_df = load_roster("path/to/folder")
```

### export_files

Export comprehensive analysis results.

```python
from cfb_dynasty import export_files, DEFAULT_POSITION_REQUIREMENTS

# Export all analysis data
success = export_files(
    roster_df=processed_roster,
    recruiting_plan=recruiting_plan,
    position_requirements=DEFAULT_POSITION_REQUIREMENTS
)
```

### validate_player_data

Validate player data before creating Player objects.

```python
from cfb_dynasty import validate_player_data

player_data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'position': 'QB',
    'year': 'FR',
    'redshirt': False
}

is_valid = validate_player_data(player_data)
print(f"Data is valid: {is_valid}")
```

## Configuration

### Position Requirements

Customize position requirements and archetype preferences:

```python
from cfb_dynasty import DEFAULT_POSITION_REQUIREMENTS

# View current requirements
qb_requirements = DEFAULT_POSITION_REQUIREMENTS['QB']
print(f"QB minimum: {qb_requirements['min']}")
print(f"QB ideal: {qb_requirements['ideal']}")
print(f"Archetype preferences: {qb_requirements['archetypes']}")

# Create custom requirements
custom_requirements = DEFAULT_POSITION_REQUIREMENTS.copy()
custom_requirements['QB']['min'] = 4  # Require 4 QBs minimum
```

### Development Multipliers

Adjust how development traits affect player value:

```python
from cfb_dynasty import DEV_TRAIT_MULTIPLIERS

print("Development multipliers:", DEV_TRAIT_MULTIPLIERS)
# Output: {'NORMAL': 1.0, 'IMPACT': 1.1, 'STAR': 1.25, 'ELITE': 1.5}

# Use custom multipliers
custom_multipliers = {
    'NORMAL': 1.0,
    'IMPACT': 1.15,  # Increased from 1.1
    'STAR': 1.3,     # Increased from 1.25
    'ELITE': 1.6     # Increased from 1.5
}
```

## Complete Workflow Example

```python
from cfb_dynasty import *
import pandas as pd

# Step 1: Load current roster
print("Loading roster...")
roster_df = load_roster()

# Step 2: Analyze current roster
print("Analyzing roster and creating recruiting plan...")
roster_df, recruiting_plan = process_roster_and_create_recruiting_plan(
    "USC_Roster.csv"
)

# Step 3: Review high priority positions
print("\nHigh priority recruiting needs:")
high_priority = recruiting_plan[recruiting_plan['Priority'] == 'HIGH']
for _, pos in high_priority.iterrows():
    print(f"- {pos['Position']}: {pos['Current Count']}/{pos['Min Required']} (Grade: {pos['Grade']})")

# Step 4: Check scheme fit issues
print("\nScheme fit analysis...")
roster_df, scheme_analysis = scheme_fit(roster_df)
problem_positions = scheme_analysis[scheme_analysis['SCHEME FIT'] != '']
for _, pos in problem_positions.iterrows():
    print(f"- {pos['POSITION']}: {pos['SCHEME FIT']}")

# Step 5: Export comprehensive analysis
print("\nExporting analysis files...")
export_files(
    roster_df=roster_df,
    recruiting_plan=recruiting_plan,
    position_requirements=DEFAULT_POSITION_REQUIREMENTS
)

print("✅ Analysis complete! Check ~/Downloads/cfb_dynasty_data/ for results.")
```

## Error Handling

The package includes comprehensive error handling:

```python
try:
    from cfb_dynasty import process_roster_and_create_recruiting_plan
    
    roster_df, plan = process_roster_and_create_recruiting_plan("roster.csv")
    
except FileNotFoundError:
    print("Roster file not found. Check the path.")
except ValueError as e:
    print(f"Data validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tips

1. **Large Datasets**: For rosters with 100+ players, consider processing in chunks
2. **Memory Usage**: Use `pandas.read_csv(chunksize=50)` for very large files  
3. **Caching**: Store processed results to avoid recalculation
4. **Validation**: Always validate data before processing to avoid errors

## Advanced Usage

### Custom Analysis Pipeline

```python
from cfb_dynasty import *

def analyze_team_depth(roster_df):
    """Custom function to analyze team depth."""
    depth_analysis = {}
    
    for position in roster_df['POSITION'].unique():
        pos_players = roster_df[roster_df['POSITION'] == position]
        
        # Calculate depth metrics
        total_players = len(pos_players)
        avg_value = pos_players['VALUE'].mean()
        top_player = pos_players['VALUE'].max()
        
        depth_analysis[position] = {
            'total': total_players,
            'avg_value': avg_value,
            'top_value': top_player,
            'depth_score': min(total_players * avg_value / 100, 10)
        }
    
    return depth_analysis

# Use custom analysis
depth_results = analyze_team_depth(roster_df)
print("Team depth analysis:")
for pos, metrics in depth_results.items():
    print(f"{pos}: Depth Score = {metrics['depth_score']:.1f}")
```
