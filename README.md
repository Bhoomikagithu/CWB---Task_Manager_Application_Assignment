# Task Manager with C++ Data Structures

This project implements a Task Manager application with a Python UI but using C++ data structures for performance optimization.

## Overview

- The data structures (LinkedList, Stack, Queue) are implemented in C++
- The UI and application logic remain in Python
- Python bindings are created using pybind11

## Requirements

- Python 3.6+
- C++ compiler (GCC, MSVC, etc.)
- pybind11 (`pip install pybind11`)
- setuptools (`pip install setuptools`)

## Building the C++ Extension

1. Install pybind11:
   ```
   pip install pybind11
   ```

2. Build the C++ extension:
   ```
   python setup.py build_ext --inplace
   ```

3. Once built, you'll have a `task_structures` module that can be imported in Python.

## Integrating with the Task Manager

To use the C++ data structures with the existing Task Manager app:

1. Replace the TaskManager class in your task.py file with the one from cpp_task_manager.py:
   ```python
   from cpp_task_manager import TaskManager
   ```

2. Make sure to remove the original Python implementation of Node, LinkedList, Stack, and Queue classes as they're now implemented in C++.

## Performance Benefits

The C++ implementation of data structures provides several benefits:

- Faster operations for large datasets (adding, removing, updating tasks)
- More efficient memory usage
- Same functionality as the Python version but with better performance

## Understanding the Code

- `task_structures.cpp`: C++ implementation of LinkedList, Stack, and Queue
- `setup.py`: Build script for creating the Python extension
- `cpp_task_manager.py`: Python wrapper for using the C++ data structures

## Testing

After building the extension, you can test it with:

```python
import task_structures

# Create a linked list
ll = task_structures.LinkedList()

# Add a task
ll.append({"id": 1, "title": "Test Task"})

# Get all tasks
tasks = ll.get_all()
print(tasks)
``` 
