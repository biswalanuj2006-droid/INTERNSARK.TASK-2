import os
import shutil
import time
from pathlib import Path

# Mapping of folder names to extensions
FILE_TYPES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "PDFs": {".pdf"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv"},
    "Documents": {".doc", ".docx", ".txt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".sql"},
}

# Create a flat map for quick lookup
EXT_MAP = {}
for folder, extensions in FILE_TYPES.items():
    for ext in extensions:
        EXT_MAP[ext] = folder


def organize_folder(target_path: Path):
    if not target_path.exists() or not target_path.is_dir():
        print(f"Error: Invalid directory path: {target_path}")
        return

    script_name = Path(__file__).name
    files = [f for f in target_path.iterdir() if f.is_file() and f.name != script_name]

    if not files:
        print("No files found to organize.")
        return

    print(f"\nProcessing {len(files)} files...")
    count = 0

    for f in files:
        # Determine the target subfolder
        folder_name = EXT_MAP.get(f.suffix.lower(), "Others")
        dest_dir = target_path / folder_name
        dest_dir.mkdir(exist_ok=True)
        
        dest_file = dest_dir / f.name

        # If a file with the same name exists, append a timestamp to prevent overwriting
        if dest_file.exists():
            timestamp = int(time.time())
            dest_file = dest_dir / f"{f.stem}_{timestamp}{f.suffix}"

        try:
            shutil.move(str(f), str(dest_file))
            print(f"Moved: {f.name} -> {folder_name}/")
            count += 1
        except Exception as e:
            print(f"Failed to move {f.name}: {e}")

    print(f"\nSuccessfully organized {count} files.")


def main():
    print("--- FILE ORGANIZER AUTOMATION ---")
    
    while True:
        print("\n1. Organize a Folder")
        print("0. Exit")
        
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            path_input = input("Enter folder path (Leave blank for current folder): ").strip()
            target = Path(path_input) if path_input else Path(".")
            target = target.expanduser().resolve()
            
            print(f"Target directory: {target}")
            confirm = input("Proceed? (y/n): ").strip().lower()
            if confirm == "y":
                organize_folder(target)
            else:
                print("Operation cancelled.")
                
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()