from tasks import get_all_tasks
from typing import List, Dict, Any

def calculate_completion_rate(tasks: List[Dict[str, Any]]) -> float:
    """
    Calculates the percentage of completed tasks from a given list of tasks.
    Returns 0.0 if the task list is empty.
    """
    if not tasks:
        return 0.0

    completed_tasks = [task for task in tasks if task["status"] == "Completed"]
    return (len(completed_tasks) / len(tasks)) * 100

def get_completion_percentage() -> float:
    """
    Calculates the percentage of completed tasks by retrieving all tasks.
    Returns 0.0 if there are no tasks.
    """
    all_tasks = get_all_tasks()
    return calculate_completion_rate(all_tasks)
