import streamlit as st
# Stack for high priority tasks, queue for medium priority tasks, and linked list for low priority tasks

# Node for Linked List
class Node:
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc
        self.next = None

# Linked List for Low Priority
class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, title, desc):
        new_node = Node(title, desc)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def view_tasks(self):
        tasks = []
        temp = self.head
        while temp:
            tasks.append((temp.title, temp.desc))
            temp = temp.next
        return tasks

    def delete_task(self):
        if self.head:
            deleted = self.head
            self.head = self.head.next
            return deleted.title
        return None

# Stack for High Priority
class Stack:
    def __init__(self):
        self.stack = []

    def add_task(self, title, desc):
        self.stack.append((title, desc))

    def view_tasks(self):
        return list(reversed(self.stack))

    def delete_task(self):
        if self.stack:
            return self.stack.pop()[0]
        return None

# Queue for Medium Priority
class Queue:
    def __init__(self):
        self.queue = []

    def add_task(self, title, desc):
        self.queue.append((title, desc))

    def view_tasks(self):
        return list(self.queue)

    def delete_task(self):
        if self.queue:
            return self.queue.pop(0)[0]
        return None

# Initialize session state for tasks


if "high" not in st.session_state:
    st.session_state.high = Stack()
if "medium" not in st.session_state:
    st.session_state.medium = Queue()
if "low" not in st.session_state:
    st.session_state.low = LinkedList()

# UI for Task Manager



st.title("Task Manager Application")

# Add Task
st.subheader("➕ Add a Task")

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title")
with col2:
    desc = st.text_input("Description")

priority = st.selectbox("Priority", ["High", "Medium", "Low"])

if st.button("Add Task"):
    if title and desc:
        if priority == "High":
            st.session_state.high.add_task(title, desc)
        elif priority == "Medium":
            st.session_state.medium.add_task(title, desc)
        elif priority == "Low":
            st.session_state.low.add_task(title, desc)
        st.success(f"Task '{title}' added!")
    else:
        st.warning("Please enter both title and description.")



# View Tasks based on priority
st.subheader("📋 View Tasks")
view = st.selectbox("Choose View:", ["All Tasks", "High Priority Tasks", "Medium Priority Tasks", "Low Priority Tasks"])



# Show Tasks with delete button
def show_tasks(task_list, delete_method, key_prefix):
    for i, (t, d) in enumerate(task_list):
        st.markdown(f"**{t}**  \n_{d}_  \n`Priority: {key_prefix}`")
        if st.button(f"❌ Delete '{t}'", key=f"{key_prefix}-del-{i}"):
            delete_method()
            st.rerun()

if view == "All Tasks" or view == "High Priority Tasks":
    high_tasks = st.session_state.high.view_tasks()
    if high_tasks:
        show_tasks(high_tasks, st.session_state.high.delete_task, "High")

if view == "All Tasks" or view == "Medium Priority Tasks":
    medium_tasks = st.session_state.medium.view_tasks()
    if medium_tasks:
        show_tasks(medium_tasks, st.session_state.medium.delete_task, "Medium")

if view == "All Tasks" or view == "Low Priority Tasks":
    low_tasks = st.session_state.low.view_tasks()
    if low_tasks:
        show_tasks(low_tasks, st.session_state.low.delete_task, "Low")