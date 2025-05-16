import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from cpp_task_manager import TaskManager  # Import from local file instead of the module path

# GUI Application
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.task_manager = TaskManager()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Task Manager")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)
        
        # Set dark theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Define colors - Dark Pink Theme
        self.bg_color = "#1A1A1A"  # Very dark gray/black
        self.fg_color = "#F0F0F0"  # Off-white
        self.accent_color = "#FF1493"  # Dark Pink (DeepPink)
        self.secondary_bg = "#252526"  # Slightly lighter dark
        self.hover_color = "#3E3E3E"  # Dark gray for hover states
        self.sidebar_bg = "#201020"  # Very dark pink-tinted background
        self.card_bg = "#2D2D30"  # Card background
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        self.style.configure("Sidebar.TFrame", background=self.sidebar_bg)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("Card.TLabel", background=self.card_bg, foreground=self.fg_color)
        self.style.configure("Title.TLabel", background=self.bg_color, foreground=self.fg_color, font=('Segoe UI', 14, 'bold'))
        self.style.configure("Sidebar.TLabel", background=self.sidebar_bg, foreground=self.fg_color)
        
        # Button styles
        self.style.configure("TButton", background=self.accent_color, foreground=self.fg_color, font=('Segoe UI', 9))
        self.style.configure("Accent.TButton", background=self.accent_color, foreground="white")
        self.style.map('TButton', background=[('active', self.accent_color)])
        
        self.style.configure("Sidebar.TButton", 
                           background=self.sidebar_bg, 
                           foreground=self.fg_color,
                           borderwidth=0,
                           font=('Segoe UI', 10),
                           padding=10)
        self.style.map('Sidebar.TButton', 
                     background=[('active', self.accent_color)],
                     foreground=[('active', 'white')])
        
        # Entry fields
        self.style.configure("TEntry", fieldbackground=self.secondary_bg, foreground=self.fg_color)
        self.style.configure("TCombobox", fieldbackground=self.secondary_bg, foreground=self.fg_color)
        self.style.map('TCombobox', fieldbackground=[('readonly', self.secondary_bg)])
        self.style.map('TCombobox', selectbackground=[('readonly', self.accent_color)])
        
        # Treeview style
        self.style.configure("Treeview", 
                           background=self.secondary_bg, 
                           foreground=self.fg_color, 
                           fieldbackground=self.secondary_bg,
                           font=('Segoe UI', 9))
        self.style.map('Treeview', background=[('selected', self.accent_color)])
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar
        self.sidebar = ttk.Frame(main_container, style="Sidebar.TFrame", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Prevent sidebar from shrinking
        
        # App title in sidebar
        title_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        title_frame.pack(fill=tk.X, pady=(15, 25))
        
        ttk.Label(title_frame, text="Task Manager", 
                font=('Segoe UI', 14, 'bold'), 
                style="Sidebar.TLabel").pack(pady=10)
        
        # Sidebar options
        options_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Sidebar buttons - Add Task and View options
        ttk.Button(
            options_frame, 
            text="➕ Add New Task", 
            style="Sidebar.TButton",
            command=self.show_add_task_view
        ).pack(fill=tk.X, padx=5, pady=5)
        
        # Task status filter buttons
        ttk.Button(
            options_frame, 
            text="📋 All Tasks", 
            style="Sidebar.TButton",
            command=lambda: self.show_tasks_view("All")
        ).pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            options_frame, 
            text="⏳ Pending Tasks", 
            style="Sidebar.TButton",
            command=lambda: self.show_tasks_view("Uncompleted")
        ).pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            options_frame, 
            text="✅ Completed Tasks", 
            style="Sidebar.TButton",
            command=lambda: self.show_tasks_view("Completed")
        ).pack(fill=tk.X, padx=5, pady=5)
        
        # Priority filter buttons in same frame
        ttk.Button(
            options_frame, 
            text="🔴 High Priority", 
            style="Sidebar.TButton",
            command=lambda: self.filter_by_priority("High")
        ).pack(fill=tk.X, padx=5, pady=(15, 2))
        
        ttk.Button(
            options_frame, 
            text="🟠 Medium Priority", 
            style="Sidebar.TButton",
            command=lambda: self.filter_by_priority("Medium")
        ).pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(
            options_frame, 
            text="🟢 Low Priority", 
            style="Sidebar.TButton",
            command=lambda: self.filter_by_priority("Low")
        ).pack(fill=tk.X, padx=5, pady=2)
        
        # Main content area - will switch between task list view and add/edit task view
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Task list view
        self.list_view = ttk.Frame(self.content_frame)
        
        # Task form view
        self.form_view = ttk.Frame(self.content_frame)
        
        # Set up task list view components
        list_header = ttk.Frame(self.list_view)
        list_header.pack(fill=tk.X, pady=(0, 15))
        
        self.view_title = ttk.Label(
            list_header, 
            text="All Tasks", 
            font=('Segoe UI', 16, 'bold'), 
            style="Title.TLabel"
        )
        self.view_title.pack(side=tk.LEFT)
        
        # Task cards container
        self.tasks_container = ttk.Frame(self.list_view)
        self.tasks_container.pack(fill=tk.BOTH, expand=True)
        
        # Task form components
        form_header = ttk.Frame(self.form_view)
        form_header.pack(fill=tk.X, pady=(0, 20))
        
        self.form_title = ttk.Label(
            form_header, 
            text="Add New Task", 
            font=('Segoe UI', 16, 'bold'), 
            style="Title.TLabel"
        )
        self.form_title.pack(side=tk.LEFT)
        
        form_container = ttk.Frame(self.form_view)
        form_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Task title
        ttk.Label(form_container, text="Task Title:").pack(anchor="w", pady=(0, 5))
        self.title_entry = ttk.Entry(form_container, width=40)
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Due date
        ttk.Label(form_container, text="Due Date (YYYY-MM-DD):").pack(anchor="w", pady=(0, 5))
        self.due_date_entry = ttk.Entry(form_container, width=40)
        self.due_date_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Priority
        ttk.Label(form_container, text="Priority:").pack(anchor="w", pady=(0, 5))
        self.priority_combo = ttk.Combobox(form_container, values=["Low", "Medium", "High"], state="readonly")
        self.priority_combo.current(1)  # Default to Medium
        self.priority_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Description
        ttk.Label(form_container, text="Description:").pack(anchor="w", pady=(0, 5))
        self.desc_text = tk.Text(form_container, height=8, bg=self.secondary_bg, fg=self.fg_color, wrap=tk.WORD)
        self.desc_text.pack(fill=tk.X, pady=(0, 15))
        
        # Action buttons
        action_frame = ttk.Frame(form_container)
        action_frame.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Button(
            action_frame, 
            text="Cancel", 
            command=lambda: self.show_tasks_view("All")
        ).pack(side=tk.RIGHT, padx=5)
        
        self.save_button = ttk.Button(
            action_frame, 
            text="Add Task", 
            command=self.add_task,
            style="Accent.TButton"
        )
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Current filter state
        self.current_status_filter = "All"
        self.current_priority_filter = "All"
        
        # Show task list view by default
        self.show_tasks_view("All")
        
        # Load initial tasks
        self.load_tasks()

    def show_add_task_view(self):
        # Hide task list view
        self.list_view.pack_forget()
        
        # Show form view
        self.form_view.pack(fill=tk.BOTH, expand=True)
        
        # Set form to add mode
        self.form_title.config(text="Add New Task")
        self.save_button.config(text="Add Task", command=self.add_task)
        
        # Clear form inputs
        self.clear_inputs()
    
    def show_tasks_view(self, filter_type):
        print(f"=== show_tasks_view called with filter: {filter_type} ===")
        # Update the filter
        self.current_status_filter = filter_type
        
        # Refresh the tasks with this filter
        self.load_tasks()
        
        # Show the task list view
        self.form_view.pack_forget()
        self.list_view.pack(fill=tk.BOTH, expand=True)
        
        # Update the title
        self.update_view_title()
        print("=== show_tasks_view completed ===")
    
    def filter_by_priority(self, priority):
        # Update the priority filter
        self.current_priority_filter = priority
        
        # Always set status filter to Uncompleted when filtering by priority
        self.current_status_filter = "Uncompleted"
        
        # Refresh tasks with this filter
        self.load_tasks()
        
        # Make sure we're showing the task list view
        self.form_view.pack_forget()
        self.list_view.pack(fill=tk.BOTH, expand=True)
        
        # Update the title
        self.update_view_title()
    
    def update_view_title(self):
        status = self.current_status_filter
        priority = self.current_priority_filter
        
        if status == "All" and priority == "All":
            self.view_title.config(text="All Tasks")
        elif status == "All" and priority != "All":
            self.view_title.config(text=f"{priority} Priority Tasks")
        elif status == "Uncompleted" and priority == "All":
            self.view_title.config(text="Pending Tasks")
        elif status == "Completed" and priority == "All":
            self.view_title.config(text="Completed Tasks")
        elif status == "Uncompleted" and priority != "All":
            # For priority filters, just show the priority without "Pending"
            self.view_title.config(text=f"{priority} Priority Tasks")
        elif status == "Completed" and priority != "All":
            self.view_title.config(text=f"Completed {priority} Priority Tasks")
    
    def load_tasks(self):
        print("=== load_tasks called ===")
        # Clear existing items
        for widget in self.tasks_container.winfo_children():
            widget.destroy()
        
        # Get all tasks
        tasks = self.task_manager.get_all_tasks()
        print(f"Total tasks available: {len(tasks)}")
        for task in tasks:
            print(f"Task ID: {task['id']}, Title: {task['title']}")
        
        # Apply filter
        status_filter = self.current_status_filter
        priority_filter = self.current_priority_filter
        print(f"Current filters - Status: {status_filter}, Priority: {priority_filter}")
        
        filtered_tasks = []
        for task in tasks:
            # Apply status filter
            if status_filter == "Completed" and not task["completed"]:
                continue
            elif status_filter == "Uncompleted" and task["completed"]:
                continue
                
            # Apply priority filter
            if priority_filter != "All" and task["priority"] != priority_filter:
                continue
                
            filtered_tasks.append(task)
        
        print(f"Filtered tasks count: {len(filtered_tasks)}")
        
        if not filtered_tasks:
            # Show empty state
            empty_frame = ttk.Frame(self.tasks_container, style="TFrame")
            empty_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
            
            ttk.Label(
                empty_frame, 
                text="No tasks found", 
                font=('Segoe UI', 12),
                foreground="#888888"
            ).pack(pady=20)
            
            return
        
        # SIMPLER APPROACH: Just create cards directly in container
        # Add task cards directly to container without canvas+scrollbar
        for task in filtered_tasks:
            self.create_task_card(self.tasks_container, task)
        
        print("=== load_tasks completed ===")
    
    def create_task_card(self, parent, task):
        # Create card frame
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill=tk.X, padx=10, pady=5, ipady=5)
        
        # Add highlight frame to left side based on priority
        priority_colors = {
            "Low": "#4CAF50",    # Green
            "Medium": "#FFC107", # Amber
            "High": "#F44336"    # Red
        }
        
        priority_color = priority_colors.get(task["priority"], "#888888")
        
        # Create highlight bar
        highlight = tk.Frame(card, width=5, bg=priority_color)
        highlight.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Content container
        content = ttk.Frame(card, style="Card.TFrame")
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Header with title and status
        header = ttk.Frame(content, style="Card.TFrame")
        header.pack(fill=tk.X, pady=(5, 8))
        
        # Task title
        title_text = task["title"]
        if len(title_text) > 40:
            title_text = title_text[:37] + "..."
            
        title = ttk.Label(
            header, 
            text=title_text, 
            font=('Segoe UI', 11, 'bold'),
            style="Card.TLabel"
        )
        title.pack(side=tk.LEFT)
        
        # Task status
        status_text = "✓ Completed" if task["completed"] else "◯ Pending"
        status_color = "#4CAF50" if task["completed"] else "#888888"
        
        status = ttk.Label(
            header, 
            text=status_text,
            foreground=status_color,
            style="Card.TLabel"
        )
        status.pack(side=tk.RIGHT)
        
        # Task details
        details = ttk.Frame(content, style="Card.TFrame")
        details.pack(fill=tk.X, pady=(0, 5))
        
        # Due date
        if task["due_date"]:
            date_frame = ttk.Frame(details, style="Card.TFrame")
            date_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(
                date_frame, 
                text="Due:", 
                width=8,
                style="Card.TLabel"
            ).pack(side=tk.LEFT)
            
            ttk.Label(
                date_frame, 
                text=task["due_date"],
                style="Card.TLabel"
            ).pack(side=tk.LEFT)
        
        # Priority
        priority_frame = ttk.Frame(details, style="Card.TFrame")
        priority_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(
            priority_frame, 
            text="Priority:", 
            width=8,
            style="Card.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            priority_frame, 
            text=task["priority"],
            foreground=priority_color,
            style="Card.TLabel"
        ).pack(side=tk.LEFT)
        
        # Description (if exists)
        if task["description"]:
            desc_frame = ttk.Frame(details, style="Card.TFrame")
            desc_frame.pack(fill=tk.X, pady=2)
            
            desc_text = task["description"]
            if len(desc_text) > 80:
                desc_text = desc_text[:77] + "..."
                
            ttk.Label(
                desc_frame, 
                text=desc_text,
                wraplength=400,
                style="Card.TLabel"
            ).pack(anchor="w")
        
        # Actions frame
        actions = ttk.Frame(content, style="Card.TFrame")
        actions.pack(fill=tk.X, pady=(8, 5))
        
        # Buttons
        if task["completed"]:
            ttk.Button(
                actions, 
                text="Mark Incomplete",
                command=lambda t=task["id"]: self.uncomplete_task(t)
            ).pack(side=tk.LEFT, padx=(0, 5))
        else:
            ttk.Button(
                actions, 
                text="Mark Complete",
                command=lambda t=task["id"]: self.complete_task(t)
            ).pack(side=tk.LEFT, padx=(0, 5))
            
        ttk.Button(
            actions, 
            text="Edit",
            command=lambda t=task: self.edit_task(t)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions, 
            text="Delete",
            command=lambda t=task["id"]: self.delete_task(t)
        ).pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.due_date_entry.get().strip()
        priority = self.priority_combo.get()
        category = ""  # No longer using category
        
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return
            
        # Add task
        task = self.task_manager.add_task(title, description, due_date, priority, category)
        
        # Clear input fields
        self.clear_inputs()
        
        # Debug print
        print(f"Added new task: {task}")
        print(f"Current tasks after adding: {self.task_manager.get_all_tasks()}")
        
        # Reset filters to see all tasks
        self.current_status_filter = "All"
        self.current_priority_filter = "All"
        
        # Update the view with the new task
        self.show_tasks_view("All")
        
        # Update status
        self.status_label.config(text=f"Task '{title}' added successfully!")
    
    def edit_task(self, task):
        # Set up form for editing
        self.clear_inputs()
        self.title_entry.insert(0, task["title"])
        self.due_date_entry.insert(0, task["due_date"])
        
        if task["description"]:
            self.desc_text.insert("1.0", task["description"])
            
        if task["priority"] in ["Low", "Medium", "High"]:
            self.priority_combo.set(task["priority"])
        
        # Set form to edit mode
        self.form_title.config(text="Edit Task")
        self.save_button.config(text="Save Changes", 
                               command=lambda: self.update_task_data(task["id"]))
        
        # Show form view
        self.list_view.pack_forget()
        self.form_view.pack(fill=tk.BOTH, expand=True)
    
    def update_task_data(self, task_id):
        # Get form data
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.due_date_entry.get().strip()
        priority = self.priority_combo.get()
        
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return
            
        # Update task
        new_data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority
        }
        
        self.task_manager.update_task(task_id, new_data)
        
        # Return to task list
        self.show_tasks_view("All")
        
        # Refresh tasks
        self.load_tasks()
        
        # Update status
        self.status_label.config(text="Task updated successfully!")
    
    def delete_task(self, task_id=None):
        if task_id is None:
            # If no task_id provided, show error
            messagebox.showerror("Error", "No task selected")
            return
            
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            self.task_manager.delete_task(task_id)
            self.load_tasks()
            self.status_label.config(text="Task deleted successfully!")
    
    def complete_task(self, task_id=None):
        if task_id is None:
            # If no task_id provided, show error
            messagebox.showerror("Error", "No task selected")
            return
            
        self.task_manager.complete_task(task_id)
        self.load_tasks()
        self.status_label.config(text="Task marked as complete!")
    
    def uncomplete_task(self, task_id=None):
        if task_id is None:
            # If no task_id provided, show error  
            messagebox.showerror("Error", "No task selected")
            return
            
        self.task_manager.uncomplete_task(task_id)
        self.load_tasks()
        self.status_label.config(text="Task marked as incomplete!")
    
    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_combo.current(1)  # Default to Medium

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop() 