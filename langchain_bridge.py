import subprocess
import sys
from langchain_core.tools import tool

def _run_task_tracker_command(command_args: list) -> str:
    """
    Executes a command against the `independent-task-tracker/main.py` CLI utility.

    This is an internal helper function designed to abstract away the details of
    calling the external task tracker command-line interface. It constructs the
    full command using the Python executable and the specified CLI path, then
    captures its standard output or error.

    Args:
        command_args (list): A list of strings representing the arguments to pass
                             to the `independent-task-tracker/main.py` script.
                             For example, `["add", "My New Task"]` or `["list"]`.

    Returns:
        str: The stripped standard output of the command if successful.
             If the command fails (returns a non-zero exit code) or the CLI script
             cannot be found, an informative error message prefixed with "Error executing command:"
             or "Error: Python executable or independent-task-tracker/main.py not found." is returned.
    """
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
    """
    Adds a new task to the task tracking system with a specified title.

    This tool is suitable for creating new, pending tasks that need to be
    completed. Provide a clear and concise title for the task.

    Args:
        task_title (str): The descriptive title of the task to be added.
                          For example: "Buy groceries", "Finish report", "Call plumber".

    Returns:
        str: A message indicating the successful addition of the task, including
             its assigned ID and title, or an error message if the operation fails.
             Example successful output: "Added task: ID 1, Title: 'Buy groceries'".
    """
    return _run_task_tracker_command(["add", task_title])

@tool
def list_tasks() -> str:
    """
    Retrieves and displays a list of all tasks currently managed by the task tracker.

    This tool is useful for reviewing all existing tasks, their statuses, and IDs.
    It provides a complete overview of pending and completed tasks.

    Args:
        None

    Returns:
        str: A multi-line string representing the formatted list of tasks.
             Each line typically includes the task ID, its completion status (e.g., "Pending", "Completed"),
             and the task's title. If no tasks are found, it returns "No tasks found."
             Example output:
             "ID    Status     Title
             ----  ---------  --------------------
             1     Pending    Buy groceries
             2     Completed  Finish report"
    """
    return _run_task_tracker_command(["list"])

@tool
def complete_task(task_id: int) -> str:
    """
    Marks an existing task as completed using its unique identifier.

    This tool should be used when a specific task has been finished and its status
    needs to be updated in the task tracker. Ensure you provide the correct
    numerical ID for the task.

    Args:
        task_id (int): The unique integer ID of the task to be marked as completed.
                       This ID can be obtained by using the `list_tasks` tool.

    Returns:
        str: A confirmation message indicating that the task has been marked
             as completed (e.g., "Task 1 marked as Completed."), or an error
             message if the task ID is invalid or the task is already completed.
             Example error output: "Task 99 not found or already completed."
    """
    return _run_task_tracker_command(["complete", str(task_id)])

@tool
def view_stats() -> str:
    """
    Retrieves and displays the overall task completion rate.

    This tool provides a high-level summary of productivity by showing
    what percentage of all recorded tasks have been marked as complete.
    It is useful for quick performance checks.

    Args:
        None

    Returns:
        str: A string indicating the task completion rate as a percentage.
             Example output: "Task Completion Rate: 75.00%".
             If there are no tasks, the rate will likely be 0.00%.
    """
    return _run_task_tracker_command(["stats"])
