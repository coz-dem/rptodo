"""This module provides the RP To-Do model-controller."""
# rptodo/rptodo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from rptodo import DB_READ_ERROR, ID_ERROR
from rptodo.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:
        """Add a new to-do to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list

    def set_status(self, todo_id: int, status: bool = False) -> CurrentTodo:
        """Set the status of a to-do."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        if status:
            todo["Done"] = True
        else:
            todo["Done"] = False
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

