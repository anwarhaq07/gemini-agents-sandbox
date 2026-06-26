import subprocess
import sys
from langchain_core.tools import tool

def _run_task_tracker_command(command_args: list) -> str:
    """Helper function to run commands against the task tracker CLI."""
    try:
        # Assuming langchain_bridge.py is in the same directory as the script calling it,
        # and independent-task-tracker/main.py is one level up and then into independent-task-tracker/
        cli_path = "../independent-task-tracker/main.py"
        result = subprocess.run(
            [sys.executable, cli_path] + command_args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: Python executable or independent-task-tracker/main.py not found. Ensure paths are correct."

@tool
def add_task(task_title: str) -> str:
    """Adds a new task to the task tracker with the given title.

    Args:
        task_title (str): The title of the task to add.

    Returns:
        str: The output from the task tracker CLI indicating the added task.
    """
    return _run_task_tracker_command(["add", task_title])

@tool
def list_tasks() -> str:
    """Lists all tasks currently in the task tracker.

    Returns:
        str: A formatted list of all tasks from the task tracker CLI.
    """
    return _run_task_tracker_command(["list"])

@tool
def complete_task(task_id: int) -> str:
    """Marks a specific task as completed using its ID.

    Args:
        task_id (int): The ID of the task to mark as complete.

    Returns:
        str: The output from the task tracker CLI confirming completion or indicating an error.
    """
    return _run_task_tracker_command(["complete", str(task_id)])

@tool
def view_stats() -> str:
    """Shows the current task completion statistics.

    Returns:
        str: The task completion rate from the task tracker CLI.
    """
    return _run_task_tracker_command(["stats"])
