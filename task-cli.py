import json
import sys
from datetime import datetime

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


def add_tasks(description):

    tasks = load_tasks()                
    task_id = len(tasks) + 1             
    new_task = {
        "id": task_id, 
        "description": description, 
        "status" : "todo",
        "createdAt" : str(datetime.now()),
        "updatedAt": str(datetime.now())
        }  
    
    tasks.append(new_task)                
    save_tasks(tasks)                     

    print(f"Task added successfully (ID: {new_task['id']})")

def remove_tasks():
    pass

def update_tasks(id, description):

    tasks = load_tasks()
    id_pos = id - 1

    tasks[id_pos]["description"] = description
    tasks[id_pos]["updatedAt"] = str(datetime.now())

    save_tasks(tasks)

def list_tasks():
    pass

def list_done_taks():
    pass

def list_not_done_tasks():
    pass

def list_in_progress_tasks():
    pass


def print_help():
    print("""
Usage: task-cli <command> [options]

Commands:
  add "description"             Add a new task
  list [status]                 List tasks (optional status: todo, in-progress, done)
  update <id> "description"     Update a task description
  delete <id>                   Delete a task
  mark-in-progress <id>         Mark task as in-progress
  mark-done <id>                Mark task as done
""")
    
def process():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]    

    if command == "add":
        add_tasks("".join(args))

    elif command == "update":
        id = int(args[0])
        description = args[1]
        update_tasks(id,description)

def main():
    process()
    
main()