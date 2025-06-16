# Task Manager Application

This is a simple Task Manager built with Streamlit that manages tasks based on their priority using Stack, Queue and Linked List data structures:

- **High Priority** tasks are managed using a **Stack**
- **Medium Priority** tasks are managed using a **Queue** 
- **Low Priority** tasks are managed using a **Linked List**.

## Features

- Add tasks with title, description, and priority.
- View tasks by priority or all tasks together.
- Delete tasks from each priority category.
- Uses Streamlit session state to maintain tasks during the session.

## How it Works

- **Stack** for high priority tasks allows the most recent high priority task to be addressed first.
- **Queue** for medium priority tasks allows tasks to be handled in the order they were added.
- **Linked List** for low priority tasks stores tasks in the order added and deletes from the front.
 
 ## Requirements

- Python 
- Streamlit

Run the app using the following command in your terminal:

```bash
streamlit run Task_manager.py
