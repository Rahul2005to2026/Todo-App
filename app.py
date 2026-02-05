from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/')
def index():
    """Render the main page"""
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task"""
    title = request.form.get('title')
    if title and title.strip():
        tasks = load_tasks()
        new_task = {
            'id': len(tasks) + 1,
            'title': title.strip(),
            'completed': False,
            'created_at': 'Just now'
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task by ID"""
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    
    # Reassign IDs to maintain sequence
    for i, task in enumerate(tasks, 1):
        task['id'] = i
    
    save_tasks(tasks)
    return redirect('/')

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Toggle task completion status"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    save_tasks(tasks)
    return redirect('/')

@app.route('/api/tasks', methods=['GET'])
def get_tasks_api():
    """API endpoint to get all tasks (for potential future use)"""
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/clear-completed', methods=['POST'])
def clear_completed():
    """Clear all completed tasks"""
    tasks = load_tasks()
    tasks = [task for task in tasks if not task['completed']]
    
    # Reassign IDs
    for i, task in enumerate(tasks, 1):
        task['id'] = i
    
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    # Create tasks file if it doesn't exist
    if not os.path.exists(TASKS_FILE):
        save_tasks([])
    
    app.run(debug=True, port=5000)