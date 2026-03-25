#!/usr/bin/env python3

import json
import sys
from datetime import datetime

STATUS_LIST = ["todo", "in-progress", "done"]


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted. Starting fresh.")
        return []


def save_tasks(tasks):
    try:
        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError as e:
        print(f"Error saving tasks: {e}")
        sys.exit(1)


def list_tasks(status="all"):
    tasks = load_tasks()
    filtered = tasks if status == "all" else [t for t in tasks if t["status"] == status]

    if not filtered:
        print("No tasks found.")
        return

    for t in filtered:
        print(f"[{t['status'].upper()}] Task {t['id']}: {t['description']}")


def add_task(description):
    description = description.strip()
    if not description:
        print("Error: Task description cannot be empty.")
        return

    tasks = load_tasks()
    task_id = max((task["id"] for task in tasks), default=0) + 1
    now = str(datetime.now())

    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(task_id, new_description):
    new_description = new_description.strip()
    if not new_description:
        print("Error: New description cannot be empty.")
        return

    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["description"] = new_description
            t["updatedAt"] = str(datetime.now())
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return

    print(f"Error: Task {task_id} not found.")


def mark_task(task_id, status):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            t["updatedAt"] = str(datetime.now())
            save_tasks(tasks)
            print(f"Task {task_id} marked '{status}'.")
            return

    print(f"Error: Task {task_id} not found.")


def remove_task(task_id):
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            print(f"Task {task_id} removed.")
            return

    print(f"Error: Task {task_id} not found.")


def parse_id(value):
    """Parse a string into a positive integer ID, or return None on failure."""
    if not value.isdigit() or int(value) <= 0:
        return None
    return int(value)


def print_help():
    print("""
Usage: task-cli <command> [options]

Commands:
  add <description>             Add a new task
  list [status]                 List tasks (status: all, todo, in-progress, done)
  update <id> <description>     Update a task's description
  delete <id>                   Delete a task
  mark-in-progress <id>         Mark a task as in-progress
  mark-done <id>                Mark a task as done
  help                          Show this help message
""")


def process():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "help":
        print_help()

    elif command == "add":
        if not args:
            print("Error: Please provide a task description.")
            print('  Usage: task-cli add "Buy groceries"')
            sys.exit(1)
        add_task(" ".join(args))

    elif command == "list":
        if not args:
            list_tasks("all")
        else:
            status = args[0]
            if status not in STATUS_LIST and status != "all":
                print(f"Error: Invalid status '{status}'. Choose from: all, todo, in-progress, done")
                sys.exit(1)
            list_tasks(status)

    elif command == "update":
        if len(args) < 2:
            print("Error: Please provide an ID and a new description.")
            print("  Usage: task-cli update <id> <description>")
            sys.exit(1)
        task_id = parse_id(args[0])
        if task_id is None:
            print("Error: ID must be a positive integer.")
            sys.exit(1)
        update_task(task_id, " ".join(args[1:]))

    elif command in ("delete", "mark-in-progress", "mark-done"):
        if len(args) != 1:
            print(f"Error: '{command}' requires exactly one argument (task ID).")
            sys.exit(1)
        task_id = parse_id(args[0])
        if task_id is None:
            print("Error: ID must be a positive integer.")
            sys.exit(1)

        if command == "delete":
            remove_task(task_id)
        elif command == "mark-in-progress":
            mark_task(task_id, "in-progress")
        elif command == "mark-done":
            mark_task(task_id, "done")

    else:
        print(f"Error: Unknown command '{command}'.")
        print_help()
        sys.exit(1)


def main():
    process()


if __name__ == "__main__":
    main()