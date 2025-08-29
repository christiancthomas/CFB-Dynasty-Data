# CFB Dynasty Data - User Guide

## Getting Started

Welcome to CFB Dynasty Data! This guide will help you get up and running quickly.

### What is CFB Dynasty Data?

CFB Dynasty Data is a comprehensive toolkit for managing college football dynasty mode in video games. It helps you:

- **Evaluate Players**: Calculate dynasty value based on ratings, development traits, and eligibility
- **Plan Recruiting**: Identify position needs and scheme fit issues  
- **Manage Rosters**: Track player progression year-over-year
- **Analyze Performance**: Generate detailed reports and visualizations

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/CFB-Dynasty-Data.git
   cd CFB-Dynasty-Data
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -c "import cfb_dynasty; print('✅ Installation successful!')"
   ```

## Basic Workflow

### Step 1: Export Your Roster

1. In your CFB game, go to the Dynasty menu
2. Export your roster data to CSV format
3. Save the file to your `~/Downloads` folder with "Roster" in the filename (e.g., `USC_Roster.csv`)

### Step 2: Run Analysis

**Option A: Use the Script (Easiest)**
```bash
chmod +x scripts/dynasty.sh
./scripts/dynasty.sh
```

**Option B: Use Python Code**
```python
from cfb_dynasty import load_roster, process_roster_and_create_recruiting_plan

# Load and analyze roster
roster_df = load_roster()
analyzed_roster, recruiting_plan = process_roster_and_create_recruiting_plan("USC_Roster.csv")

print("Analysis complete!")
```

### Step 3: Review Results

The analysis generates several CSV files in `~/Downloads/cfb_dynasty_data/`:

- **`player_values_analysis.csv`**: Complete roster with calculated values and status
- **`recruiting_plan_analysis.csv`**: Position-by-position recruiting priorities  
- **`position_analysis_detailed.csv`**: Detailed breakdowns by position

## Understanding Player Values

### Value Calculation

Player values help you make dynasty decisions by considering:

- **Current Rating**: Player's overall rating
- **Development Potential**: Based on development trait
- **Remaining Eligibility**: More years = higher value
- **Redshirt Status**: Slight penalty for redshirted players

**Example**: A 85 OVR Freshman QB with Star development = 185.94 value

### Player Status Categories

- **🟢 SAFE**: High-value players to keep
- **🟡 AT RISK**: Moderate value, consider for development  
- **🔴 CUT**: Low value, candidates for cutting
- **🎓 GRADUATING**: Will leave after this season

### Grade Scale

Positions are graded on team strength:
- **A+/A/A-**: Elite to very strong position groups
- **B+/B/B-**: Above average to adequate
- **C+/C/C-**: Below average to concerning
- **F**: Critical need area

## Recruiting Strategy

### Position Priorities

The system identifies three priority levels:

1. **🚨 HIGH PRIORITY**: 
   - Below minimum roster requirements
   - Graded D or F in strength
   - Critical scheme fit issues

2. **🔶 MEDIUM PRIORITY**:
   - At minimum but below ideal numbers
   - Graded C in strength
   - Some scheme concerns

3. **🟢 LOW PRIORITY**:
   - Above minimum requirements  
   - Graded B+ or better
   - Good scheme fit

### Scheme Fit Analysis

The system evaluates how well your players fit your preferred scheme:

- **Perfect Fit (1.0)**: Essential archetype for your system
- **Good Fit (0.5-0.99)**: Useful but not critical
- **Weak Fit (0.01-0.49)**: Consider position changes
- **Non-Fit (0.0)**: Strong candidate for cuts

## Advanced Features

### Custom Position Requirements

You can modify position requirements in `cfb_dynasty/config/constants.py`:

```python
# Increase QB requirements
DEFAULT_POSITION_REQUIREMENTS['QB']['min'] = 4
DEFAULT_POSITION_REQUIREMENTS['QB']['ideal'] = 5

# Adjust archetype preferences
DEFAULT_POSITION_REQUIREMENTS['QB']['archetypes']['DUAL THREAT'] = 1.2
```

### Jupyter Notebook Analysis

For interactive analysis, use the included notebook:

```bash
jupyter notebook notebooks/roster_analysis.ipynb
```

This provides:
- Visual charts and graphs
- Interactive data exploration
- Custom analysis workflows
- Export capabilities

### Custom Analysis Scripts

Create your own analysis scripts:

```python
from cfb_dynasty import *

def find_transfer_targets(roster_df, max_value=100):
    """Find players who might transfer out."""
    at_risk = roster_df[
        (roster_df['VALUE'] < max_value) & 
        (roster_df['STATUS'] != 'GRADUATING')
    ]
    return at_risk[['FIRST NAME', 'LAST NAME', 'POSITION', 'VALUE']]

# Use custom analysis
transfer_risks = find_transfer_targets(roster_df)
print(f"Found {len(transfer_risks)} potential transfer candidates")
```

## Common Use Cases

### Dynasty Season Planning

1. **Preseason Analysis**: Identify roster strengths and weaknesses
2. **Recruiting Planning**: Focus on high-priority positions
3. **Season Management**: Track player development
4. **Offseason Decisions**: Cut low-value players, plan transfers

### Player Development

1. **Redshirt Decisions**: Balance immediate needs vs long-term value
2. **Position Changes**: Move players to better scheme fits
3. **Playing Time**: Prioritize high-value players
4. **Transfer Portal**: Identify incoming/outgoing candidates

### Recruiting Strategy

1. **Position Targeting**: Focus limited resources effectively  
2. **Scheme Fit**: Recruit players who match your system
3. **Development vs Ready**: Balance immediate impact vs potential
4. **Depth Management**: Maintain adequate numbers without over-recruiting

## Tips & Best Practices

### Data Management
- **Consistent Naming**: Use consistent file naming (e.g., "USC_Roster_2024.csv")
- **Regular Backups**: Keep copies of your analysis files
- **Version Control**: Track changes season-to-season

### Analysis Workflow
- **Regular Updates**: Run analysis monthly during season
- **Compare Trends**: Track how player values change over time
- **Validate Results**: Cross-check with in-game performance

### Dynasty Strategy
- **Long-term Thinking**: Value young players with high potential
- **Scheme Consistency**: Build around your preferred style
- **Depth Balance**: Maintain adequate but not excessive depth
- **Development Investment**: Focus resources on high-potential players

## Troubleshooting

### Common Issues

**"No CSV files found"**
- Ensure files are in `~/Downloads` 
- Check filename contains "roster" (case insensitive)
- Verify file is actually CSV format

**"Missing required columns"**
- Export data from correct game menu
- Don't modify CSV after export
- Check for required columns listed in error

**"Import errors"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.11+ required)

### Getting Help

1. **Check Documentation**: Review this guide and API reference
2. **Run Tests**: Use `python -m pytest tests/ -v` to verify setup
3. **Check Issues**: Look at GitHub issues for similar problems
4. **Debugging**: Use verbose logging for detailed error info

### Performance Issues

**Large Rosters (100+ players)**:
```python
# Process in chunks
import pandas as pd

def process_large_roster(file_path, chunk_size=50):
    results = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk_result = process_roster_and_create_recruiting_plan(chunk)
        results.append(chunk_result)
    return pd.concat(results)
```

**Memory Usage**:
- Close unused DataFrames with `del dataframe`
- Use `pd.read_csv(usecols=['needed', 'columns'])` for large files
- Process analysis in batches for multiple teams

## Next Steps

Once you're comfortable with basic analysis, try:

1. **Custom Metrics**: Create your own player evaluation formulas
2. **Visualization**: Build charts and graphs of your data
3. **Automation**: Set up automated analysis pipelines  
4. **Integration**: Connect with other dynasty management tools
5. **Sharing**: Export results to share with online dynasty communities

## Example Workflows

### New Dynasty Setup
```python
# 1. Set up initial analysis
roster_df = load_roster()
_, recruiting_plan = process_roster_and_create_recruiting_plan("roster.csv")

# 2. Identify immediate needs
critical_needs = recruiting_plan[recruiting_plan['Priority'] == 'HIGH']
print("Critical recruiting needs:")
print(critical_needs[['Position', 'Current Count', 'Min Required']])

# 3. Plan cuts to free scholarships
cuts = roster_df[roster_df['STATUS'] == 'CUT']
print(f"Recommended cuts: {len(cuts)} players, freeing {len(cuts)} scholarships")
```

### Mid-Season Check
```python
# 1. Update player values based on performance
# (manually update CSV with new ratings)

# 2. Re-run analysis
updated_roster, _ = process_roster_and_create_recruiting_plan("updated_roster.csv")

# 3. Compare to preseason
# (compare with saved preseason analysis)

# 4. Adjust recruiting strategy
print("Recruiting adjustments needed based on season performance...")
```

### Offseason Planning  
```python
# 1. Handle graduations and departures
returning_players = roster_df[roster_df['STATUS'] != 'GRADUATING']

# 2. Generate next season roster with recruits
recruits_df = pd.read_csv("incoming_recruits.csv")
next_season = generate_roster(returning_players, recruits_df, "USC")

# 3. Plan for next season
next_analysis = process_roster_and_create_recruiting_plan(next_season)
print("Next season outlook complete!")
```

---

**Need more help?** Check out the API Reference for detailed function documentation, or explore the included Jupyter notebook for interactive examples!
