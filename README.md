pip install -r requirements.txt

## Running the `dynasty.sh` Script Globally

To run the `dynasty.sh` script from anywhere in your terminal without having to navigate to its directory, you can add the script to your `PATH`. Follow these steps:

### Steps to Add the Script to Your PATH

1. **Move the Script to a Directory in Your PATH**:
   Move the script to a directory that is already in your `PATH`, such as `/usr/local/bin`. This typically requires `sudo` permissions:
   ```
   sudo mv /Users/christianthomas/Developer/CFB-Dynasty-Data/dynasty.sh /usr/local/bin/dynasty
   ```
2. **Make the Script Executable:** Ensure the script has execute permissions:
    ```
    sudo chmod +x /usr/local/bin/dynasty
    ```
3. **Verify the Script Location:** Ensure that the script is now located in bin:
    ```
    ls -l /usr/local/bin/dynasty
    ```
4. **Run the Script:** You can now run the script from anywhere in your terminal by simply typing:
    ```
    dynasty
    ```