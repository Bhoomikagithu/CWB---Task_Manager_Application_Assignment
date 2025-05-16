import json
import os
from datetime import datetime
import task_structures  # Import the C++ extension module

class TaskManager:
    def __init__(self):
        self.tasks = task_structures.LinkedList()  # C++ LinkedList
        self.task_id_counter = 1
        self.deleted_tasks = task_structures.Stack()  # C++ Stack
        self.upcoming_tasks = task_structures.Queue()  # C++ Queue
        self.load_data()
        print(f"TaskManager initialized with {self.tasks.size} tasks")
    
    def add_task(self, title, description, due_date, priority, category=""):
        task = {
            "id": self.task_id_counter,
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        
        # If high priority, add to upcoming tasks queue
        if priority == "High":
            self.upcoming_tasks.enqueue(task)
            
        self.task_id_counter += 1
        self.save_data()
        print(f"Task added: {task}")
        return task
    
    def delete_task(self, task_id):
        print(f"Attempting to delete task with ID: {task_id}")
        
        # Find the task to push to deleted stack
        all_tasks = self.tasks.get_all()
        for task in all_tasks:
            if task["id"] == task_id:
                self.deleted_tasks.push(task)
                print(f"Task pushed to deleted stack: {task}")
                break
            
        result = self.tasks.remove(task_id)
        if result:
            self.save_data()
            print(f"Task with ID {task_id} deleted successfully")
        else:
            print(f"Failed to delete task with ID {task_id}")
        return result
    
    def update_task(self, task_id, new_data):
        print(f"Updating task with ID {task_id}: {new_data}")
        result = self.tasks.update(task_id, new_data)
        if result:
            self.save_data()
            print(f"Task updated successfully")
        else:
            print(f"Failed to update task")
        return result
    
    def complete_task(self, task_id):
        print(f"Marking task {task_id} as complete")
        return self.update_task(task_id, {"completed": True})
    
    def uncomplete_task(self, task_id):
        print(f"Marking task {task_id} as incomplete")
        return self.update_task(task_id, {"completed": False})
    
    def get_all_tasks(self):
        tasks = self.tasks.get_all()
        print(f"Retrieved {len(tasks)} tasks from LinkedList")
        return tasks
    
    def undo_delete(self):
        task = self.deleted_tasks.pop()
        if task and len(task) > 0:  # Check if task is not empty
            print(f"Restoring task from deleted stack: {task}")
            self.tasks.append(task)
            self.save_data()
            return task
        print("No deleted tasks to restore")
        return None
    
    def get_upcoming_task(self):
        return self.upcoming_tasks.dequeue()
    
    def load_data(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    data = json.load(f)
                    
                if "tasks" in data:
                    for task in data["tasks"]:
                        self.tasks.append(task)
                    print(f"Loaded {len(data['tasks'])} tasks from file")
                
                if "task_id_counter" in data:
                    self.task_id_counter = data["task_id_counter"]
                    print(f"Loaded task_id_counter: {self.task_id_counter}")
            except Exception as e:
                print(f"Error loading data: {str(e)}")
    
    def save_data(self):
        data = {
            "tasks": self.tasks.get_all(),
            "task_id_counter": self.task_id_counter
        }
        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data['tasks'])} tasks to file") 