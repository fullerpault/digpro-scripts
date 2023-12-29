import os
import shutil
import re

# Script for separating even and odd numbered files
# Creates two subdirectories named "odd" and "even" in the source directory
# Requires files to end in a 3 digit number

# Source and destination directories
source_dir = input("Enter source directory: ")
destination_dir_odd = os.path.join(source_dir, "odd")
destination_dir_even = os.path.join(source_dir, "even")

# Ensure the destination directories exist or create them
if not os.path.exists(destination_dir_odd):
    os.mkdir(destination_dir_odd)

if not os.path.exists(destination_dir_even):
    os.mkdir(destination_dir_even)

# Function to check if a filename ends with an odd number
def is_odd_number(filename):
    # Split the filename and its extension
    base_filename, file_extension = os.path.splitext(filename)

    # Extract the last 3 digits from the filename using regular expressions
    match = re.search(r'\d{3}$', base_filename)
    if match:
        last_3_digits = int(match.group(0))
        return last_3_digits % 2 == 1
    return False

# Iterate through files in the source directory
for filename in os.listdir(source_dir):
    source_path = os.path.join(source_dir, filename)

    if os.path.isfile(source_path):  # Check if it's a file

        # Check if the file should be moved to the "odd" or "even" folder
        if is_odd_number(filename):
            destination_path_odd = os.path.join(destination_dir_odd, filename)
            
            # Move the file to the "odd" directory
            shutil.move(source_path, destination_path_odd)
            print(f"Moved: {filename} to {destination_path_odd}")

        # Otherwise move the file to the "even" directory
        else:
            destination_path_even = os.path.join(destination_dir_even, filename)
            shutil.move(source_path, destination_path_even)
            print(f"Moved: {filename} to {destination_path_even}")

print("File movement completed.")