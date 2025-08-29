#!/bin/zsh

# Get the directory of the current script
SCRIPT_DIR=$(dirname "$0")

# Define the path to the roster_analysis.py file relative to the script directory
SCRIPT_PATH="$SCRIPT_DIR/../cfb_dynasty/analysis/roster_analysis.py"

# Define the Downloads folder path
DOWNLOADS_FOLDER="$HOME/Downloads"

# Search for the appropriate CSV file in the Downloads folder
CSV_FILE=$(find "$DOWNLOADS_FOLDER" -name "*Roster.csv" | head -n 1)

# Check if a CSV file was found
if [ -z "$CSV_FILE" ]; then
  echo "No CSV file found in the Downloads folder."
  exit 1
fi

# Print the paths for debugging
echo "Found CSV file: $CSV_FILE"
echo "Using script: $SCRIPT_PATH"
echo "Output folder: $DOWNLOADS_FOLDER"

# Activate the virtual environment
source "$SCRIPT_DIR/../.venv/bin/activate"

# Run the roster_analysis.py script with the found CSV file as input
# and output the resulting CSVs to the Downloads folder
python3.12 "$SCRIPT_PATH" "$CSV_FILE" "$DOWNLOADS_FOLDER"

# Deactivate the virtual environment
deactivate

# Check if the script ran successfully
if [ $? -eq 0 ]; then
  echo "Roster analysis completed successfully."
else
  echo "Roster analysis failed."
  exit 1
fi
