from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import User, Task
from database import engine

Session = sessionmaker(bind=engine)
session = Session()


def create_user(name, email):
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        raise ValueError(f"A user with email {email} already exists.")
    
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    return new_user

def create_task(user_id, title, description, category, deadline):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")
    
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD for the deadline.")
    
    new_task = Task(
        title=title,
        description=description,
        category=category,
        deadline=deadline_date,
        user=user
    )
    
    session.add(new_task)
    session.commit()
    return new_task

def get_all_tasks():
    tasks = session.query(Task).all()
    return tasks

def get_tasks_by_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")
    
    tasks = session.query(Task).filter_by(user_id=user_id).all()
    return tasks

def get_task_by_id(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")
    return task

def update_task(task_id, title=None, description=None, category=None, completed=None, deadline=None):
    task = session.query(Task).filter_by(id=task_id).first()
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")
    
    if title:
        task.title = title
    if description:
        task.description = description
    if category:
        task.category = category
    if completed is not None:
        task.completed = completed
    if deadline:
        try:
            task.deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD for the deadline.")
    
    session.commit()
    return task

def delete_task(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if not task:
        raise ValueError(f"Task with ID {task_id} not found.")
    
    session.delete(task)
    session.commit()
    return task

def close_session():
    session.close()
