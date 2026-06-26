import json
import os

DATA_DIR = ".data"
TASK_FILE = os.path.join(DATA_DIR, "tasks.json")

_tasks = []
_next_id = 1

def _load_tasks():
    global _tasks, _next_id
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            data = json.load(f)
            _tasks = data.get("tasks", [])
            _next_id = data.get("next_id", 1)
            # Ensure _next_id is at least 1 if tasks are empty or max existing ID + 1
            if not _tasks and _next_id < 1:
                _next_id = 1
            elif _tasks:
                max_id = max(task["id"] for task in _tasks)
                _next_id = max(max_id + 1, _next_id)
    else:
        _tasks = []
        _next_id = 1

def _save_tasks():
    os.makedirs(DATA_DIR, exist_ok=True) # Ensure .data directory exists
    with open(TASK_FILE, 'w') as f:
        json.dump({"tasks": _tasks, "next_id": _next_id}, f, indent=4)

def add_task(title: str) -> dict:
    """Adds a new task with the given title."""
    global _next_id
    task = {
        "id": _next_id,
        "title": title,
        "status": "Pending"
    }
    _tasks.append(task)
    _next_id += 1
    _save_tasks() # Save after adding
    return task

def complete_task(task_id: int) -> bool:
    """Marks a task as 'Completed'."""
    found = False
    for task in _tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            found = True
            break
    if found:
        _save_tasks() # Save after completing
    return found

def get_all_tasks() -> list:
    """Returns a list of all tasks."""
    return list(_tasks)

# Load tasks when the module is imported
_load_tasks()
