# CFB Dynasty Data

A comprehensive dynasty roster management and valuation tool for College Football 25, featuring automated player analysis, recruiting planning, and roster generation.

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/your-username/CFB-Dynasty-Data.git
cd CFB-Dynasty-Data
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Basic Usage
```bash
# Run automated analysis (looks for CSV files in ~/Downloads)
chmod +x scripts/dynasty.sh
./scripts/dynasty.sh
```

Or use as a Python package:
```python
from cfb_dynasty import load_roster, process_roster_and_create_recruiting_plan

# Load and analyze roster
roster_df = load_roster()
roster_df, recruiting_plan = process_roster_and_create_recruiting_plan("roster.csv")
```

## 📊 Features

- **Player Valuation**: Calculate player worth based on rating, development traits, and remaining eligibility
- **Roster Analysis**: Comprehensive position-by-position strength evaluation  
- **Recruiting Intelligence**: Automated identification of recruiting priorities and scheme fit analysis
- **Dynasty Management**: Year-over-year roster progression with automatic player advancement

## 📁 Project Structure

- `cfb_dynasty/` - Main package with models, analysis, and utilities
- `scripts/` - Executable scripts for automated processing
- `notebooks/` - Interactive Jupyter analysis notebooks  
- `tests/` - Comprehensive test suite (24/27 tests passing)
- `docs/` - Detailed documentation

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

## 📖 Documentation

See `docs/README.md` for comprehensive documentation including:
- Detailed API reference
- Configuration options
- File format specifications
- Development guidelines

## 🔧 Status

**Version 1.0.0** - Repository successfully reorganized into professional package structure with:
- ✅ All critical functionality working
- ✅ Player class with year advancement logic
- ✅ Roster generation and analysis tools
- ✅ Comprehensive test coverage
- ✅ Proper package organization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality  
4. Ensure all tests pass
5. Submit a pull request

---

**Python 3.13+ Required** | **Dependencies**: pandas, pytest
