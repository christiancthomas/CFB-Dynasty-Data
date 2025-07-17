# Running Unit Tests in Python

To run unit tests in this project, follow these steps:

## Setup

1. **Navigate to the project directory:**
    ```bash
    cd /Users/christianthomas/GitHub/CFB-Dynasty-Data
    ```

2. **Activate your virtual environment (if using one):**
    ```bash
    source venv/bin/activate
    ```

3. **Install required dependencies:**
    ```bash
    pip install pandas numpy matplotlib seaborn plotly
    ```

    Or if you have a requirements.txt file:
    ```bash
    pip install -r requirements.txt
    ```

## Running Tests

4. **Run all tests using the built-in unittest module:**
    ```bash
    python3 -m unittest discover -s tests -p "test_*.py"
    ```

    - This command will automatically discover and run all test files named `test*.py` in the tests directory.

5. **Run a specific test file:**
    ```bash
    python3 -m unittest tests.test_analysis
    ```

6. **Run a specific test method:**
    ```bash
    python3 -m unittest tests.test_analysis.TestRosterAnalysis.test_calculate_player_value
    ```

7. **Run tests with verbose output:**
    ```bash
    python3 -m unittest discover -s tests -p "test_*.py" -v
    ```

## Important Notes

- Make sure you're running tests from the project root directory (`/Users/christianthomas/GitHub/CFB-Dynasty-Data`)
- The virtual environment should be activated if you're using one
- Tests use relative imports that require the proper Python path setup

## For more options, see the unittest documentation:
https://docs.python.org/3/library/unittest.html