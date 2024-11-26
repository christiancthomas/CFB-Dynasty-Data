#!/bin/zsh

# Define the path to the roster_analysis.py file
SCRIPT_PATH="/Users/christianthomas/Documents/GitHub/CFB-Dynasty-Data/roster_analysis.py"

# Define the Downloads folder path
DOWNLOADS_FOLDER="$HOME/Downloads"

# Search for the appropriate CSV file in the Downloads folder
CSV_FILE=$(find "$DOWNLOADS_FOLDER" -name "*Roster.csv" | head -n 1)

# Check if a CSV file was found
if [ -z "$CSV_FILE" ]; then
  echo "No CSV file found in the Downloads folder."
  exit 1
fi

# Run the roster_analysis.py script with the found CSV file as input
# and output the resulting CSVs to the Downloads folder
python3 "$SCRIPT_PATH" "$CSV_FILE" "$DOWNLOADS_FOLDER"

echo "Roster analysis completed. Output files are in the Downloads folder."