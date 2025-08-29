# CFB Dynasty Data - Examples

This directory contains example scripts demonstrating various use cases for the CFB Dynasty Data package.

## Available Examples

### 1. `basic_analysis.py` - Getting Started
**What it does**: Demonstrates the core workflow for dynasty analysis
**Best for**: First-time users, basic dynasty management
**Features**:
- Load roster data automatically
- Run comprehensive analysis
- Display key insights and priorities
- Export detailed results

**Run it**:
```bash
python examples/basic_analysis.py
```

### 2. `player_valuation.py` - Understanding Player Values
**What it does**: Deep dive into player valuation mechanics
**Best for**: Understanding how dynasty values are calculated
**Features**:
- Player creation and manipulation examples
- Value calculation demonstrations
- Finding "hidden gems" with high potential
- Comparing recruiting targets

**Run it**:
```bash
python examples/player_valuation.py
```

### 3. `advanced_dynasty.py` - Multi-Year Planning
**What it does**: Advanced dynasty management strategies
**Best for**: Experienced users, long-term planning
**Features**:
- Graduation impact analysis
- Multi-year roster projections
- Transfer portal strategy
- Scholarship management
- Comprehensive dynasty reports

**Run it**:
```bash
python examples/advanced_dynasty.py
```

## Prerequisites

Before running examples:

1. **Install the package**: Follow installation instructions in main README
2. **Prepare data**: Place a roster CSV file in your `~/Downloads` folder
3. **Activate environment**: Make sure your Python virtual environment is activated

```bash
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

## Expected Output

Each example will generate:
- Console output with analysis results
- CSV files in `~/Downloads/cfb_dynasty_data/` with detailed data
- Actionable insights and recommendations

## Customization

All examples can be modified for your specific needs:

- **Change file paths**: Modify file locations to match your setup
- **Adjust thresholds**: Customize value calculations and grade boundaries  
- **Add custom analysis**: Extend scripts with your own dynasty management logic
- **Export formats**: Add JSON, Excel, or other export formats

## Common Use Cases

### Preseason Planning
Use `basic_analysis.py` to:
- Identify roster strengths and weaknesses
- Plan recruiting priorities
- Make scholarship management decisions

### In-Season Monitoring
Use `player_valuation.py` to:
- Track player development
- Identify breakout candidates
- Make playing time decisions

### Offseason Strategy
Use `advanced_dynasty.py` to:
- Plan for graduations and transfers
- Develop long-term roster strategy
- Optimize scholarship allocation

## Troubleshooting

**"No CSV files found"**
- Ensure your roster file is in `~/Downloads`
- Filename should contain "roster" (case insensitive)
- File must be in CSV format

**"Missing required columns"**
- Export roster data from the correct game menu
- Don't modify CSV files after export
- Check error message for specific missing columns

**Import errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.11+ required)

## Next Steps

After trying the examples:

1. **Create your own scripts** based on these templates
2. **Explore the Jupyter notebook** in `notebooks/` for interactive analysis
3. **Check the API reference** in `docs/` for detailed function documentation
4. **Contribute improvements** by submitting pull requests

---

**Need help?** Check the main documentation or open an issue on GitHub!
