pip install -r requirements.txt

## Running the `dynasty.sh` Script Globally

To run the `dynasty.sh` script from anywhere in your terminal without having to navigate to its directory, you can create a symbolic link to the script in your `PATH`. Follow these steps:

### Steps to Create a Symbolic Link

1. **Create the Symbolic Link**:
    Create a symbolic link to the script in a directory that is in your `PATH`, such as `/usr/local/bin`:
   ```
   sudo ln -s /Users/christianthomas/Developer/CFB-Dynasty-Data/dynasty.sh /usr/local/bin/dynasty
   ```
2. **Make the Script Executable:**
    Ensure the script has execute permissions:
   ```
   chmod +x /Users/christianthomas/Developer/CFB-Dynasty-Data/dynasty.sh
   ```
3. **Verify the Symbolic Link:**
    Ensure that the symbolic link is created correctly:
    ```
    ls -l /usr/local/bin/dynasty
    ```
4. **Run the Script:**
    You can now run the script from anywhere in your terminal by simply typing:
    ```
    dynasty
    ```

## Updating the Script
To update the dynasty.sh script, simply edit the script in your project directory (/Users/christianthomas/Developer/CFB-Dynasty-Data/dynasty.sh). The symbolic link will always point to the latest version of the script, so there is no need to recreate the link.