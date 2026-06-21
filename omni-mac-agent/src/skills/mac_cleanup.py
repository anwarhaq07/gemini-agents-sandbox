import os
import subprocess
import json
from datetime import datetime
import shutil

def get_folder_size(path):
    """
    Helper function to get the human-readable size of a folder.
    """
    try:
        output = subprocess.check_output(['du', '-sh', path], stderr=subprocess.PIPE).decode('utf-8').split('\t')[0]
        return output.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "N/A"

def get_last_used_date(path):
    """
    Helper function to get the last used date of an application,
    falling back to modification time if spotlight metadata is unavailable.
    """
    try:
        # Try to get kMDItemLastUsedDate using mdls
        mdls_output = subprocess.check_output(
            ['mdls', '-name', 'kMDItemLastUsedDate', '-raw', path],
            stderr=subprocess.PIPE
        ).decode('utf-8').strip()

        if mdls_output and mdls_output != '(null)':
            # Example format: 2024-06-21 10:30:00 +0000
            try:
                dt_obj = datetime.strptime(mdls_output.split(' +')[0], '%Y-%m-%d %H:%M:%S')
                return dt_obj.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass # Fallback to os.stat if parsing fails

    except (subprocess.CalledProcessError, FileNotFoundError):
        pass # Fallback to os.stat if mdls fails

    # Fallback to os.stat if mdls doesn't work or fails to parse
    try:
        stat_info = os.stat(path)
        return datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    except OSError:
        return "N/A"

def list_mac_applications() -> str:
    """
    Reads /Applications and returns a JSON string showing application name,
    full paths, folder size using `du`, and approximation of last used date
    using spotlight metadata `kMDItemLastUsedDate` with an `os.stat` fallback.
    Filters out any path starting with `/System/`.
    """
    applications_dir = "/Applications"
    applications_data = []

    if not os.path.isdir(applications_dir):
        return json.dumps({"error": f"Directory not found: {applications_dir}"})

    for app_name in os.listdir(applications_dir):
        app_path = os.path.join(applications_dir, app_name)

        # Filter out system applications and ensure it's an application bundle directory
        if not app_path.startswith('/System/') and app_name.endswith('.app') and os.path.isdir(app_path):
            size = get_folder_size(app_path)
            last_used = get_last_used_date(app_path)
            applications_data.append({
                "name": app_name.replace('.app', ''),
                "path": app_path,
                "size": size,
                "last_used": last_used
            })

    return json.dumps(applications_data, indent=2)

def delete_mac_application(app_path: str, confirm: bool) -> str:
    """
    Requires an explicit `confirm=True` flag to remove an application folder safely.
    Deletes a specified macOS application folder.
    Returns a success or failure message.
    """
    if not app_path.endswith('.app'):
        return f"Error: '{app_path}' does not appear to be a macOS application bundle (.app). Deletion aborted."

    if not os.path.isdir(app_path):
        return f"Error: Application path '{app_path}' does not exist or is not a directory. Deletion aborted."

    if app_path.startswith('/System/'):
        return f"Error: Cannot delete system application at '{app_path}'. Deletion aborted."

    if not confirm:
        return "Deletion aborted: 'confirm' flag must be explicitly set to True to proceed with deletion."

    try:
        shutil.rmtree(app_path)
        return f"Successfully deleted application: {app_path}"
    except Exception as e:
        return f"Error deleting application {app_path}: {e}"
