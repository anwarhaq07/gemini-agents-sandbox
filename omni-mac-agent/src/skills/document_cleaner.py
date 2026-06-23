import os
import datetime
import json
from typing import List, Dict

# Assuming mac_cleanup.py is in the same directory or accessible
from .mac_cleanup import delete_file_or_folder

def get_file_details(path: str) -> Dict:
    """Helper to get file details."""
    try:
        stat_info = os.stat(path)
        access_time = datetime.datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        file_size_bytes = stat_info.st_size

        # Human-readable size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if file_size_bytes < 1024.0:
                file_size = f"{file_size_bytes:.2f} {unit}"
                break
            file_size_bytes /= 1024.0
        else:
            file_size = f"{stat_info.st_size:.2f} B" # Fallback if loop finishes

        return {
            "name": os.path.basename(path),
            "path": path,
            "size": file_size,
            "access_time": access_time,
            "modification_time": modification_time,
            "raw_access_time": stat_info.st_atime
        }
    except OSError:
        return {
            "name": os.path.basename(path),
            "path": path,
            "size": "N/A",
            "access_time": "N/A",
            "modification_time": "N/A",
            "raw_access_time": 0 # For sorting purposes, put unreadable at the beginning (least accessed)
        }

def scan_documents(document_dir: str = os.path.expanduser("~/Documents")) -> List[Dict]:
    """
    Scans the specified document directory and identifies files based on least recent access time.
    Returns a list of dictionaries, each containing file details.
    """
    if not os.path.isdir(document_dir):
        print(f"Warning: Document directory '{document_dir}' not found.")
        return []

    document_files = []
    for root, _, files in os.walk(document_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            document_files.append(get_file_details(file_path))

    # Sort by raw_access_time (least recently accessed first)
    document_files.sort(key=lambda x: x.get('raw_access_time', 0))
    return document_files

def clean_documents_cli(document_dir: str = os.path.expanduser("~/Documents")) -> str:
    """
    Interactively lists documents and allows the user to delete selected files.
    """
    files_to_consider = scan_documents(document_dir)

    if not files_to_consider:
        return "No documents found to clean in the specified directory."

    deletion_queue = list(files_to_consider)
    results = []

    print(f"\n--- Document Cleanup in {document_dir} ---")

    while True:
        if not deletion_queue:
            print("No files remaining in the deletion queue.")
            results.append("No files remaining in the deletion queue.")
            break

        print("\nFiles proposed for deletion (sorted by least recent access time):")
        for i, file_data in enumerate(deletion_queue):
            print(f"{i+1}. Name: {file_data['name']}, Size: {file_data['size']}, Last Accessed: {file_data['access_time']}, Path: {file_data['path']}")

        user_choice = input(
            "\nOptions:\n"
            "  [p]roceed with deletion\n"
            "  [r]emove specific files from deletion queue (enter numbers, e.g., '1 3')\n"
            "  [q]uit without deleting anything\n"
            "> "
        ).lower().strip()

        if user_choice == 'p':
            if not deletion_queue:
                results.append("No files left to delete.")
                break
            
            print(f"\nConfirm deletion of {len(deletion_queue)} files. Type 'yes' to confirm:")
            confirm_delete = input("> ").lower().strip()
            if confirm_delete == 'yes':
                print("\nProceeding with deletion...")
                for file_data in deletion_queue:
                    path_to_delete = file_data['path']
                    delete_result = delete_file_or_folder(path_to_delete, confirm=True)
                    results.append(delete_result)
                    print(f"- {path_to_delete}: {delete_result}")
                break
            else:
                results.append("Deletion cancelled by user.")
                print("Deletion cancelled.")
                break # Exit loop if not confirmed
        elif user_choice == 'r':
            try:
                indices_to_remove_str = input("Enter numbers of files to remove from queue (space-separated): ").strip()
                if not indices_to_remove_str:
                    print("No files specified to remove.")
                    continue
                indices_to_remove = sorted([int(x) - 1 for x in indices_to_remove_str.split()], reverse=True)

                for idx in indices_to_remove:
                    if 0 <= idx < len(deletion_queue):
                        removed_file = deletion_queue.pop(idx)
                        print(f"Removed '{removed_file['name']}' from deletion queue.")
                    else:
                        print(f"Invalid number: {idx+1}. Skipping.")
            except ValueError:
                print("Invalid input. Please enter numbers.")
            except IndexError:
                print("Invalid file number provided.")
        elif user_choice == 'q':
            results.append("Document cleanup aborted by user.")
            print("Document cleanup aborted.")
            break
        else:
            print("Invalid option. Please choose 'p', 'r', or 'q'.")
            
    return "\n".join(results) if results else "Document cleanup completed with no actions taken."

# This is the function that main_agent.py will trigger
def trigger_document_cleanup(directory: str = os.path.expanduser("~/Documents")) -> str:
    """
    Triggers an interactive CLI process to scan, categorize, and offer deletion
    of least-used documents in a specified directory (defaults to ~/Documents).
    The user will be prompted to confirm deletions within the CLI.
    """
    return clean_documents_cli(directory)
