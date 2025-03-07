import os
import shutil

def copy_and_rename_jpgs(source_dir, destination_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    primary_key = 1  # starting primary key
    
    # Walk through the source directory recursively
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Check if the file extension is .jpg (case-insensitive)
            if file.lower().endswith(".jpg"):
                source_file = os.path.join(root, file)
                # Generate a new file name with the primary key and preserve .jpg extension
                new_filename = f"{primary_key}.jpg"
                destination_file = os.path.join(destination_dir, new_filename)
                
                # Copy the file from the source to the destination directory
                shutil.copy2(source_file, destination_file)
                print(f"Copied {source_file} to {destination_file}")
                
                primary_key += 1

if __name__ == "__main__":
    # Define the source and destination directories
    source_directory = "cats"
    destination_directory = "main_dir"
    
    copy_and_rename_jpgs(source_directory, destination_directory)

