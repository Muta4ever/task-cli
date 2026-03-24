import json
import sys
from datetime import datetime

status_list = ["todo", "in-progress", "done"]

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

    if tasks:
        task_id = max(task["id"] for task in tasks) + 1
    else:
        task_id = 1  


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

def update_tasks(id, new_description):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == id:
            t["description"] = new_description
            t["updatedAt"] = str(datetime.now())
            print(f"Task {id} updated")
            save_tasks(tasks)
            return
        
    print(f"Task {id} not found")

def mark(id, statusID):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == id:
            t["status"] = status_list[statusID]
            print(f"Task {id} marked '{status_list[statusID]}'")
            save_tasks(tasks)
            return
        
    print(f"Task {id} not found")

def remove(id):
    tasks  = load_tasks()
    if len(tasks) <= 0:
        print("There are no tasks")
        return
    
    elif id < 0:
        print("No tasks with negative indices")
        return 
    
    for i in range(len(tasks)):
        if tasks[i]["id"] == id:
            tasks.pop(i)
            print(f"Task {id} removed")
            save_tasks(tasks)
            return

    print(f"Task {id} not found")

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

    elif command == "mark-in-progress":
        id = int(args[0])
        mark(id, 1)

    elif command == "mark-done":
        id = int(args[0])
        mark(id, 2)
    
    elif command == "remove":
        id = int(args[0])
        remove(id)

def main():
    process()
    
main()