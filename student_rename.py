import os

# Add your target names here (copy from your list)
target_names = [
    # Copy your list of names here
    "Suthanya A",
    "Dinesh Pranav K S", 
    # ... add all your names
]

# Directory path for students
directory = os.path.join(os.getcwd(), "photouploads", "Students")

# Get list of files in the directory
files = os.listdir(directory)

def normalize(name):
    """Normalize name for matching - remove dots, dashes, underscores, extra spaces"""
    return name.replace('.', '').replace('_', ' ').replace('-', ' ').replace('  ', ' ').lower().strip()

# Build a mapping from normalized file base name to actual file name
file_map = {}
for filename in files:
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        base = os.path.splitext(filename)[0]
        file_map[normalize(base)] = filename

print(f"Found {len(files)} files in Students directory")
print(f"Looking to rename to {len(target_names)} target names")

# Rename files to match the target names
renamed_count = 0
not_found_count = 0

for target in target_names:
    norm_target = normalize(target)
    if norm_target in file_map:
        old_name = file_map[norm_target]
        ext = os.path.splitext(old_name)[1]
        new_name = f"{target}{ext}"
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        
        if old_path != new_path:
            try:
                # Check if target file already exists
                if os.path.exists(new_path):
                    print(f"Warning: {new_name} already exists, skipping {old_name}")
                    continue
                
                os.rename(old_path, new_path)
                print(f"Renamed: {old_name} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {old_name}: {e}")
        else:
            print(f"File {old_name} already has correct name")
    else:
        print(f"File for '{target}' not found!")
        not_found_count += 1

print(f"\nRenaming process completed!")
print(f"Files renamed: {renamed_count}")
print(f"Files not found: {not_found_count}")
print(f"Total target names: {len(target_names)}") 