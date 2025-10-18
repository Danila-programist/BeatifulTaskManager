from sqlalchemy.orm import DeclarativeBase

from .task import Task
from .users import User

Base = DeclarativeBase

__all__ = ["Base", 'User', "Task"]
