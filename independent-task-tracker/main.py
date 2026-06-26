import argparse
from tasks import add_task, complete_task, get_all_tasks
from analytics import get_completion_percentage

def main():
    parser = argparse.ArgumentParser(description="Simple Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="The title of the task")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="The ID of the task to complete")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show task completion statistics")

    args = parser.parse_args()

    if args.command == "add":
        task = add_task(args.title)
        print(f"Added task: ID {task['id']}, Title: '{task['title']}'")
    elif args.command == "list":
        tasks = get_all_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print("ID    Status     Title")
            print("----  ---------  --------------------")
            for task in tasks:
                print(f"{task['id']:<4}  {task['status']:<9}  {task['title']}")
    elif args.command == "complete":
        if complete_task(args.id):
            print(f"Task {args.id} marked as Completed.")
        else:
            print(f"Task {args.id} not found or already completed.")
    elif args.command == "stats":
        completion_rate = get_completion_percentage()
        print(f"Task Completion Rate: {completion_rate:.2f}%")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
