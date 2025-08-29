# CFB Dynasty Data

A comprehensive toolkit for managing college football dynasty rosters, analyzing player data, and creating recruiting plans.

## 📁 Project Structure

```
CFB-Dynasty-Data/
├── cfb_dynasty/                    # Main package
│   ├── __init__.py                 # Package initialization and exports
│   ├── models/                     # Data models
│   │   ├── __init__.py
│   │   └── player.py               # Player class with year advancement
│   ├── data/                       # Data handling modules
│   │   ├── __init__.py
│   │   └── roster_generator.py     # Roster generation logic
│   ├── analysis/                   # Analysis and evaluation modules
│   │   ├── __init__.py
│   │   └── roster_analysis.py      # Player valuation and recruiting plans
│   ├── config/                     # Configuration and constants
│   │   ├── __init__.py
│   │   └── constants.py            # Position requirements, multipliers
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       ├── file_utils.py           # File I/O operations
│       ├── log.py                  # Logging configuration
│       └── validator.py            # Data validation functions
├── scripts/                        # Executable scripts
│   └── dynasty.sh                  # Main execution script
├── notebooks/                      # Jupyter notebooks
│   └── roster_analysis.ipynb       # Interactive analysis notebook
├── docs/                           # Documentation
│   └── README.md                   # This file
├── tests/                          # Test suite
│   ├── test_player.py              # Player class tests
│   ├── test_roster.py              # Roster generation tests
│   ├── test_analysis.py            # Analysis function tests
│   └── test_utils.py               # Utility function tests
├── requirements.txt                # Python dependencies
└── README.md                       # Project overview
```

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/CFB-Dynasty-Data.git
cd CFB-Dynasty-Data
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### Using the Package

```python
from cfb_dynasty import (
    Player, 
    generate_roster, 
    process_roster_and_create_recruiting_plan,
    load_roster
)

# Load a roster from CSV
roster_df = load_roster()

# Create a player
player = Player(
    first_name="John",
    last_name="Doe",
    position="QB",
    year="FR",
    redshirt=False
)

# Advance player's year
new_year = player.advance_year()

# Generate recruiting plan
roster_df, recruiting_plan = process_roster_and_create_recruiting_plan(
    "path/to/roster.csv"
)
```

#### Using the Script

```bash
# Make script executable
chmod +x scripts/dynasty.sh

# Run analysis (looks for CSV files in ~/Downloads)
./scripts/dynasty.sh
```

## 📊 Features

### Player Management
- **Player Class**: Comprehensive player data model with year advancement logic
- **Year Progression**: Automatic handling of eligibility progression and redshirt status
- **Validation**: Input validation for player data integrity

### Roster Analysis
- **Player Valuation**: Calculate player values based on rating, development traits, and remaining years
- **Position Analysis**: Evaluate roster strength by position with grading system
- **Status Classification**: Categorize players as Safe, At Risk, Cut, or Graduating

### Recruiting Intelligence
- **Position Requirements**: Configurable minimum and ideal roster sizes per position
- **Scheme Fit Analysis**: Evaluate player archetypes against position requirements
- **Priority Matrix**: Identify high, medium, and low priority recruiting targets

### Data Processing
- **CSV Integration**: Load roster and recruiting data from CSV files
- **Export Capabilities**: Generate analysis reports and recruiting plans
- **Logging**: Comprehensive logging for debugging and monitoring

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_player.py -v

# Run with coverage report
python -m pytest tests/ --cov=cfb_dynasty --cov-report=html
```

## 📋 Configuration

### Position Requirements

Customize position requirements in `cfb_dynasty/config/constants.py`:

```python
DEFAULT_POSITION_REQUIREMENTS = {
    'QB': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'POCKET PASSER': 1.15,
            'DUAL THREAT': 1.00,
            # ... more archetypes
        }
    },
    # ... more positions
}
```

### Development Traits

Adjust development multipliers:

```python
DEV_TRAIT_MULTIPLIERS = {
    'NORMAL': 1.00,
    'IMPACT': 1.10,
    'STAR': 1.25,
    'ELITE': 1.50
}
```

## 📈 Analysis Features

### Player Valuation Formula

```
Value = Base Rating × Dev Multiplier × (1 + Remaining Years / 4) × (1 - Redshirt Discount)
```

Where:
- **Base Rating**: Player's current overall rating
- **Dev Multiplier**: Based on development trait (Normal: 1.0, Impact: 1.1, Star: 1.25, Elite: 1.5)
- **Remaining Years**: Years of eligibility remaining (0-3)
- **Redshirt Discount**: 5% penalty for redshirt players

### Position Grading Scale

- **A+ (150+)**: Elite position group
- **A (140-149)**: Excellent depth and talent
- **A- (130-139)**: Very strong position
- **B+ (120-129)**: Above average
- **B (110-119)**: Solid contributors
- **B- (100-109)**: Adequate depth
- **C+ (90-99)**: Below average
- **C (80-89)**: Concerning depth
- **C- (70-79)**: Major weakness
- **F (<70)**: Critical need

## 🔧 Development

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Add code to appropriate module in `cfb_dynasty/`
3. Add tests in `tests/`
4. Update documentation
5. Run tests: `python -m pytest tests/`
6. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions
- Maintain test coverage above 80%

## 📄 File Formats

### Roster CSV Format

Required columns:
```
FIRST NAME, LAST NAME, POSITION, YEAR, RATING, BASE RATING, 
ARCHETYPE, DEV TRAIT, REDSHIRT, CUT, DRAFTED, STATUS
```

### Recruiting CSV Format

Required columns:
```
FIRST NAME, LAST NAME, POSITION, COMMITTED TO, YEAR, RATING
```

## 🐛 Known Issues

1. Some player integration utilities are not fully implemented (3/27 tests failing)
2. Position mappings may need updates for CFB 26 compatibility
3. Archetype valuations require validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Run tests to verify setup

---

**Version**: 1.0.0  
**Python**: 3.13+ required  
**Dependencies**: pandas, pytest
