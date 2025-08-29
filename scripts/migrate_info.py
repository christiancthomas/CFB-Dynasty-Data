#!/usr/bin/env python3
"""Migration script to help transition from old structure to new package structure."""

import os
import sys

def main():
    """Display migration information for users."""
    print("🔄 CFB Dynasty Data - Migration Guide")
    print("=" * 50)
    print()
    print("✅ Repository has been reorganized into a professional package structure!")
    print()
    print("📁 NEW STRUCTURE:")
    print("   cfb_dynasty/          - Main package")
    print("   ├── models/          - Player class")
    print("   ├── data/            - Roster generation") 
    print("   ├── analysis/        - Player valuation & recruiting")
    print("   ├── config/          - Constants & settings")
    print("   └── utils/           - Helper functions")
    print()
    print("   scripts/             - Executable scripts")
    print("   notebooks/           - Jupyter notebooks")
    print("   docs/                - Documentation")
    print()
    print("🚀 QUICK START:")
    print("   # As package:")
    print("   from cfb_dynasty import load_roster, process_roster_and_create_recruiting_plan")
    print()
    print("   # As script:")
    print("   chmod +x scripts/dynasty.sh")
    print("   ./scripts/dynasty.sh")
    print()
    print("📋 OLD FILES (can be safely removed after testing):")
    old_files = [
        "new_roster.py", 
        "roster_analysis.py",
    ]
    
    for old_file in old_files:
        if os.path.exists(old_file):
            print(f"   • {old_file} → cfb_dynasty/ (migrated)")
        else:
            print(f"   • {old_file} (already removed)")
    
    print()
    print("🧪 VERIFICATION:")
    print("   python -m pytest tests/ -v")
    print("   python -c 'import cfb_dynasty; print(\"✅ Package working!\")'")
    print()
    print("📖 For detailed documentation, see: docs/README.md")
    print()

if __name__ == "__main__":
    main()
