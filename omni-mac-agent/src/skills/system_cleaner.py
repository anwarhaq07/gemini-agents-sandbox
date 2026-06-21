import datetime
import json
import os
from typing import List, Dict, Any

from .mac_cleanup import list_mac_applications, get_last_used_date, delete_mac_application

def evaluate_unnecessary_applications(
    unused_threshold_days: int = 180
) -> List[Dict[str, Any]]:
    """
    Evaluates installed macOS applications and identifies those that haven't been
    used recently based on a specified threshold.

    Args:
        unused_threshold_days: Number of days defining the threshold for an application
                               to be considered 'unused'.

    Returns:
        A list of dictionaries, where each dictionary represents an unnecessary
        application with its path, name, and last used date.
    """
    applications_str = list_mac_applications()
    applications = json.loads(applications_str)
    unnecessary_apps = []
    current_date = datetime.datetime.now()

    for app in applications:
        try:
            last_used_date_obj = datetime.datetime.strptime(
                app["last_used"],
                "%Y-%m-%d %H:%M:%S"
            )

            if (current_date - last_used_date_obj).days > unused_threshold_days:
                unnecessary_apps.append({
                    "path": app["path"],
                    "name": app["name"],
                    "last_used": last_used_date_obj.strftime("%Y-%m-%d")
                })

        except KeyError as e:
            print(f"Missing field {e} in app data: {app}")
        except ValueError as e:
            print(f"Invalid date for {app.get('name', 'Unknown')}: {e}")
    # Assuming list_mac_applications returns paths separated by newlines
    # app_paths = [app.strip() for app in applications_str.split('\n') if app.strip()]
    # unnecessary_apps = []
    # current_date = datetime.datetime.now()

    # for app_path in app_paths:
    #     try:
    #         # Assuming get_last_used_date returns a string like "YYYY-MM-DD HH:MM:SS"
    #         last_used_str = get_last_used_date(app_path)
    #         last_used_date_obj = datetime.datetime.strptime(last_used_str, "%Y-%m-%d %H:%M:%S")

    #         if (current_date - last_used_date_obj).days > unused_threshold_days:
    #             unnecessary_apps.append({
    #                 "path": app_path,
    #                 "name": os.path.basename(app_path).replace(".app", ""),
    #                 "last_used": last_used_date_obj.strftime("%Y-%m-%d")
    #             })
    #     except ValueError:
    #         # Handle cases where get_last_used_date output format is unexpected
    #         print(f"Warning: Could not parse last used date for {app_path}. Skipping.")
    #         continue
    #     except Exception as e:
    #         # Catch other potential issues, e.g., if path doesn't exist or permission errors
    #         print(f"Could not fully evaluate {app_path}: {e}")
    #         continue
    return unnecessary_apps

def interact_and_cleanup_system(
    items_to_clean: List[Dict[str, Any]],
    item_type: str = "item"
) -> str:
    """
    Interactively presents a list of items to the user, allows them to deselect items,
    and then proceeds with deletion for the remaining confirmed items.

    Args:
        items_to_clean: A list of dictionaries, each representing an item to potentially clean.
                        Each dictionary should have at least 'name' and 'path' keys.
        item_type: A string describing the type of items being cleaned (e.g., "application").

    Returns:
        A summary string of actions taken.
    """
    if not items_to_clean:
        return f"No unnecessary {item_type}s found to clean."

    print(f"\n--- Unnecessary {item_type.capitalize()}s Found ---")
    for i, item in enumerate(items_to_clean):
        print(f"{i + 1}. {item['name']} (Last used: {item.get('last_used', 'N/A')})")

    to_delete_indices = set(range(len(items_to_clean)))
    while True:
        print("\nEnter numbers of items to KEEP (remove from deletion list), or 'd' to proceed with deletion:")
        user_input = input(f"Your choice (e.g., '1 3' to keep {item_type} 1 and 3): ").strip().lower()

        if user_input == 'd':
            break

        try:
            keep_indices = [int(x) - 1 for x in user_input.split()]
            for idx in keep_indices:
                if 0 <= idx < len(items_to_clean):
                    if idx in to_delete_indices:
                        to_delete_indices.remove(idx)
                        print(f"Removed '{items_to_clean[idx]['name']}' from deletion list.")
                    else:
                        print(f"'{items_to_clean[idx]['name']}' was already marked to be kept.")
                else:
                    print(f"Invalid number: {idx + 1}. Please enter numbers between 1 and {len(items_to_clean)}.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces, or 'd'.")

        # Re-list current deletion candidates
        if to_delete_indices:
            print(f"\nItems currently marked for deletion ({len(to_delete_indices)}):")
            for idx in sorted(list(to_delete_indices)):
                item = items_to_clean[idx]
                print(f"- {item['name']} (Last used: {item.get('last_used', 'N/A')})")
        else:
            print(f"\nNo {item_type}s currently marked for deletion.")

    if not to_delete_indices:
        return f"No {item_type}s selected for deletion. Cleanup cancelled."

    print("\n--- Confirm Deletion ---")
    print(f"The following {item_type}s will be deleted:")
    for idx in sorted(list(to_delete_indices)):
        item = items_to_clean[idx]
        print(f"- {item['name']} ({item['path']})")

    confirm_final = input("Are you sure you want to delete these items? (yes/no): ").strip().lower()

    if confirm_final == 'yes':
        deleted_count = 0
        failed_deletions = []
        for idx in sorted(list(to_delete_indices)):
            item = items_to_clean[idx]
            print(f"Attempting to delete: {item['name']}...")
            try:
                # The interact_and_cleanup_system function handles user confirmation.
                # Therefore, we pass confirm=False to delete_mac_application to avoid a double prompt.
                result = delete_mac_application(item['path'], confirm=False)
                print(f"Result for {item['name']}: {result}")
                if "successfully deleted" in result.lower():
                    deleted_count += 1
                else:
                    failed_deletions.append(item['name'])
            except Exception as e:
                failed_deletions.append(item['name'])
                print(f"Error deleting {item['name']}: {e}")

        summary_msg = f"Cleanup complete. Deleted {deleted_count} {item_type}(s)."
        if failed_deletions:
            summary_msg += f" Failed to delete: {', '.join(failed_deletions)}."
        return summary_msg
    else:
        return "Deletion cancelled by user."

if __name__ == "__main__":
    print("Starting system evaluation for unused applications...")
    unnecessary_apps = evaluate_unnecessary_applications(unused_threshold_days=180)

    if unnecessary_apps:
        print(f"Found {len(unnecessary_apps)} potentially unnecessary applications.")
        cleanup_result = interact_and_cleanup_system(unnecessary_apps, item_type="application")
        print(cleanup_result)
    else:
        print("No potentially unnecessary applications found based on the criteria.")
