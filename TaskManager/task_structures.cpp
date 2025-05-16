#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include<bits/stdc++.h>
using namespace std;
namespace py = pybind11;
// Linked list for tasks, stack for undo functionality, queue for upcoming tasks


// Node class for LinkedList
class Node {
public:
    py::dict task;
    Node* next;
    Node* prev;

    Node(py::dict t) : task(t), next(nullptr), prev(nullptr) {}
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

    void append(py::dict task) {
        Node* new_node = new Node(task);
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
            if (py::cast<int>(current->task["id"]) == task_id) {
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

    vector<py::dict> get_all() {
        vector<py::dict> tasks;
        Node* current = head;
        while (current) {
            tasks.push_back(current->task);
            current = current->next;
        }
        return tasks;
    }

    bool update(int task_id, py::dict new_data) {
        Node* current = head;
        while (current) {
            if (py::cast<int>(current->task["id"]) == task_id) {
                // Update task with new_data values
                for (auto item : new_data) {
                    std::string key = py::cast<std::string>(item.first);
                    current->task[key.c_str()] = item.second;
                }
                return true;
            }
            current = current->next;
        }
        return false;
    }
    
    int get_size() const {
        return size;
    }
};

// Stack for undo functionality
class TaskStack {
private:
    stack<py::dict> items;

public:
    void push(py::dict item) {
        items.push(item);
    }

    py::dict pop() {
        if (items.empty()) {
            return py::dict();
        }
        py::dict item = items.top();
        items.pop();
        return item;
    }

    py::dict peek() {
        if (items.empty()) {
            return py::dict();
        }
        return items.top();
    }

    bool is_empty() const {
        return items.empty();
    }

    int size() const {
        return items.size();
    }
};

// Queue for upcoming tasks
class TaskQueue {
private:
    queue<py::dict> items;

public:
    void enqueue(py::dict item) {
        items.push(item);
    }

    py::dict dequeue() {
        if (items.empty()) {
            return py::dict();
        }
        py::dict item = items.front();
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

// Python module definition
PYBIND11_MODULE(task_structures, m) {
    m.doc() = "C++ implementation of data structures for Task Manager";

    py::class_<LinkedList>(m, "LinkedList")
        .def(py::init<>())
        .def("append", &LinkedList::append)
        .def("remove", &LinkedList::remove)
        .def("get_all", &LinkedList::get_all)
        .def("update", &LinkedList::update)
        .def_property_readonly("size", &LinkedList::get_size);

    py::class_<TaskStack>(m, "Stack")
        .def(py::init<>())
        .def("push", &TaskStack::push)
        .def("pop", &TaskStack::pop)
        .def("peek", &TaskStack::peek)
        .def("is_empty", &TaskStack::is_empty)
        .def("size", &TaskStack::size);

    py::class_<TaskQueue>(m, "Queue")
        .def(py::init<>())
        .def("enqueue", &TaskQueue::enqueue)
        .def("dequeue", &TaskQueue::dequeue)
        .def("is_empty", &TaskQueue::is_empty)
        .def("size", &TaskQueue::size);
} 