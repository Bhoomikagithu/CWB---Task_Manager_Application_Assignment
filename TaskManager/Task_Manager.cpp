#include <bits/stdc++.h>
using namespace std;

// Node class for LinkedList
class Node {
public:
    int id;
    string name;
    string description;
    int priority;
    Node* next;
    Node* prev;

    Node(int id, string name, string description, int priority)
        : id(id), name(name), description(description), priority(priority), next(nullptr), prev(nullptr) {}
};

// LinkedList class for tasks
class LinkedList {
private:
    Node* head;
    Node* tail;
    int size;

public:
    LinkedList() : head(nullptr), tail(nullptr), size(0) {}
    ~LinkedList() {
        clear();
    }

    void clear() {
        Node* current = head;
        while (current) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
        head = nullptr;
        tail = nullptr;
        size = 0;
    }

    void append(int id, string name, string description, int priority) {
        Node* new_node = new Node(id, name, description, priority);
        if (!head) {
            head = new_node;
            tail = new_node;
        } else {
            new_node->prev = tail;
            tail->next = new_node;
            tail = new_node;
        }
        size++;
    }

    bool remove(int task_id) {
        Node* current = head;
        while (current) {
            if (current->id == task_id) {
                if (current->prev) {
                    current->prev->next = current->next;
                } else {
                    head = current->next;
                }

                if (current->next) {
                    current->next->prev = current->prev;
                } else {
                    tail = current->prev;
                }

                delete current;
                size--;
                return true;
            }
            current = current->next;
        }
        return false;
    }

    vector<Node*> get_all() {
        vector<Node*> tasks;
        Node* current = head;
        while (current) {
            tasks.push_back(current);
            current = current->next;
        }
        return tasks;
    }

    bool update(int task_id, string new_name, string new_description, int new_priority) {
        Node* current = head;
        while (current) {
            if (current->id == task_id) {
                current->name = new_name;
                current->description = new_description;
                current->priority = new_priority;
                return true;
            }
            current = current->next;
        }
        return false;
    }

    int get_size() const {
        return size;
    }

    vector<Node*> get_by_priority(int priority) {
        vector<Node*> tasks;
        Node* current = head;
        while (current) {
            if (current->priority == priority) {
                tasks.push_back(current);
            }
            current = current->next;
        }
        return tasks;
    }
};

// Stack for undo functionality
class TaskStack {
private:
    stack<Node*> items;

public:
    void push(Node* item) {
        items.push(item);
    }

    Node* pop() {
        if (items.empty()) return nullptr;
        Node* item = items.top();
        items.pop();
        return item;
    }

    Node* peek() {
        if (items.empty()) return nullptr;
        return items.top();
    }

    bool is_empty() const {
        return items.empty();
    }

    int size() const {
        return items.size();
    }
};

// Queue for task handling order
class TaskQueue {
private:
    queue<Node*> items;

public:
    void enqueue(Node* item) {
        items.push(item);
    }

    Node* dequeue() {
        if (items.empty()) return nullptr;
        Node* item = items.front();
        items.pop();
        return item;
    }

    bool is_empty() const {
        return items.empty();
    }

    int size() const {
        return items.size();
    }
};

int main() {
    LinkedList taskList;
    TaskStack undoStack;
    TaskQueue taskQueue;

    int choice;

    while (true) {
        cout << "\n=== Task Manager Menu ===\n";
        cout << "1. Add Task" << endl;
        cout << "2. Delete Task" << endl;
        cout << "3. Update Task" << endl;
        cout << "4. View All Tasks" << endl;
        cout << "6. View Tasks by Priority" << endl;
        cout << "7. Exit" << endl;
        cout << "Enter choice: ";
        cin >> choice;

        if (choice == 1) {
            int id, priority;
            string name, description;
            cout << "Enter Task ID: ";
            cin >> id;
            cout << "Enter Task Name: ";
            cin >> ws;
            getline(cin, name);
            cout << "Enter Task Description: ";
            getline(cin, description);
            cout << "Enter Task Priority (1: Low, 10: Medium, 11: High): ";
            cin >> priority;

            taskList.append(id, name, description, priority);
            Node* task = new Node(id, name, description, priority); 
            taskQueue.enqueue(task);

            cout << "Task added successfully." << endl;
        } 
        else if (choice == 2) {
            int id;
            cout << "Enter Task ID to Delete: ";
            cin >> id;

            vector<Node*> tasks = taskList.get_all();
            for (auto& task : tasks) {
                if (task->id == id) {
                    undoStack.push(task); // backup before delete
                }
            }

            if (taskList.remove(id)) {
                cout << "Task deleted successfully." << endl;
            } else {
                cout << "Task with ID " << id << " not found." << endl;
            }
        } 
        else if (choice == 3) {
            int id, priority;
            string name, description;
            cout << "Enter Task ID to Update: ";
            cin >> id;
            cout << "Enter New Task Name: ";
            cin >> ws;
            getline(cin, name);
            cout << "Enter New Task Description: ";
            getline(cin, description);
            cout << "Enter New Task Priority (1: Low, 10: Medium, 11: High): ";
            cin >> priority;

            vector<Node*> tasks = taskList.get_all();
            for (auto& task : tasks) {
                if (task->id == id) {
                    undoStack.push(task);
                }
            }

            if (taskList.update(id, name, description, priority)) {
                cout << "Task updated successfully." << endl;
            } else {
                cout << "Task with ID " << id << " not found." << endl;
            }
        } 
        else if (choice == 4) {
            vector<Node*> allTasks = taskList.get_all();
            for (auto& task : allTasks) {
                cout << "Task ID: " << task->id
                     << ", Name: " << task->name
                     << ", Description: " << task->description
                     << ", Priority: " << task->priority << endl;
            }
        } 
        else if (choice == 6) {
            int priority;
            cout << "Enter Priority to View (1: Low, 10: Medium, 11: High): ";
            cin >> priority;

            vector<Node*> priorityTasks = taskList.get_by_priority(priority);
            if (priorityTasks.empty()) {
                cout << "No tasks with this priority." << endl;
            } else {
                for (auto& task : priorityTasks) {
                    cout << "Task ID: " << task->id
                         << ", Name: " << task->name
                         << ", Description: " << task->description
                         << ", Priority: " << task->priority << endl;
                }
            }
        } 
        else if (choice == 7) {
            break;
        } 
        else {
            cout << "Invalid choice! Please try again." << endl;
        }
    }

    return 0;
}
