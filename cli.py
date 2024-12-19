import sys
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import engine, initialize_db
from models import User, Task

initialize_db()

Session = sessionmaker(bind=engine)
session = Session()

def print_menu():
    print("\nTask Management CLI")
    print("-------------------")
    print("1. Add a User")
    print("2. Add a Task")
    print("3. View All Tasks")
    print("4. Update a Task")
    print("5. Delete a Task")
    print("6. View Tasks by User")
    print("7. Exit")

def add_user():
    name = input("Enter user name: ")
    email = input("Enter user email: ")

    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        print(f"A user with email {email} already exists.")
        return

    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    print(f"User '{name}' added successfully!")

def add_task():
    print("Assign a task to a user:")
    users = session.query(User).all()
    if not users:
        print("No users found. Please add a user first.")
        return

    for user in users:
        print(f"{user.id}. {user.name} ({user.email})")

    try:
        user_id = int(input("Enter User ID: "))
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print("Invalid User ID!")
            return
    except ValueError:
        print("Invalid input. Please enter a valid User ID.")
        return

    title = input("Enter task title: ")
    description = input("Enter task description: ")
    category = input("Enter task category: ")
    deadline = input("Enter deadline (YYYY-MM-DD): ")

    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return

    new_task = Task(
        title=title,
        description=description,
        category=category,
        deadline=deadline_date,
        user=user
    )

    session.add(new_task)
    session.commit()
    print(f"Task '{title}' added successfully!")

def view_all_tasks():
    tasks = session.query(Task).all()
    if not tasks:
        print("No tasks available.")
        return

    for task in tasks:
        print(f"\nTask ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Category: {task.category}")
        print(f"Deadline: {task.deadline}")
        print(f"Completed: {'Yes' if task.completed else 'No'}")
        print(f"Assigned to: {task.user.name} ({task.user.email})")

def update_task():
    try:
        task_id = int(input("Enter the Task ID to update: "))
        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            print("Task not found.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid Task ID.")
        return

    print("Leave input blank to keep current value.")
    title = input(f"Enter new title (current: {task.title}): ") or task.title
    description = input(f"Enter new description (current: {task.description}): ") or task.description
    category = input(f"Enter new category (current: {task.category}): ") or task.category
    completed = input(f"Is the task completed? (yes/no, current: {'Yes' if task.completed else 'No'}): ").lower()
    deadline = input(f"Enter new deadline (YYYY-MM-DD, current: {task.deadline}): ")

    task.title = title
    task.description = description
    task.category = category
    task.completed = completed == "yes"

    if deadline:
        try:
            task.deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format! Task not updated.")
            return

    session.commit()
    print("Task updated successfully!")

def delete_task():
    try:
        task_id = int(input("Enter the Task ID to delete: "))
        task = session.query(Task).filter_by(id=task_id).first()
        if not task:
            print("Task not found.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid Task ID.")
        return

    session.delete(task)
    session.commit()
    print("Task deleted successfully!")

def view_tasks_by_user():
    users = session.query(User).all()
    if not users:
        print("No users found.")
        return

    for user in users:
        print(f"{user.id}. {user.name} ({user.email})")

    try:
        user_id = int(input("Enter User ID: "))
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print("User not found.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid User ID.")
        return

    tasks = session.query(Task).filter_by(user_id=user_id).all()
    if not tasks:
        print(f"No tasks found for {user.name}.")
        return

    print(f"Tasks for {user.name}:")
    for task in tasks:
        print(f"\nTask ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Category: {task.category}")
        print(f"Deadline: {task.deadline}")
        print(f"Completed: {'Yes' if task.completed else 'No'}")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            add_task()
        elif choice == "3":
            view_all_tasks()
        elif choice == "4":
            update_task()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            view_tasks_by_user()
        elif choice == "7":
            print("Exiting... Goodbye!")
            session.close()
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
