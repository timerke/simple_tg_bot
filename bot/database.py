import os
import sqlite3
from typing import Any, Callable, Optional


def connect_and_disconnect_database(func: Callable[..., Any]):
    """
    The decorator connects the database and disconnects it after the execution of the decorated function.
    :param func: decorated function.
    """

    def wrapper(self, *args, **kwargs) -> Any:
        conn = sqlite3.connect(Database.DATABASE_PATH, uri=True)
        result = func(self, conn, *args, **kwargs)
        conn.close()
        return result
    
    return wrapper


class Database:
    """
    Class for working with a database.
    """

    DATABASE_PATH: str = os.path.join("data", "database.db")

    def __init__(self) -> None:
        if not self._check_database_created():
            self._create_tables()

    def _check_database_created(self) -> bool:
        """
        :return: True if the database has been created.
        """

        return os.path.exists(Database.DATABASE_PATH)

    @staticmethod
    def _create_employees_table(cursor) -> None:
        cursor.execute("CREATE TABLE IF NOT EXISTS employees("
                       "id INTEGER PRIMARY KEY,"
                       "username TEXT)")

    @staticmethod
    def _create_history_table(cursor) -> None:
        cursor.execute("CREATE TABLE IF NOT EXISTS history("
                       "employee_id INTEGER,"
                       "last_menu TEXT,"
                       "FOREIGN KEY(employee_id) REFERENCES eployees(id))")

    @connect_and_disconnect_database
    def _create_tables(self, conn) -> None:
        """
        :param conn: database connection.
        """

        cursor = conn.cursor()
        self._create_employees_table(cursor)
        self._create_history_table(cursor)
        conn.commit()

    @connect_and_disconnect_database
    def add_employee(self, conn, employee_id: int, username: str) -> None:
        """
        :param conn: database connection;
        :param employee_id: employee ID in Telegram;
        :param username: employee username in Telegram.
        """

        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees VALUES (?, ?)", (employee_id, username))
        conn.commit()
    
    @connect_and_disconnect_database
    def check_employee(self, conn, employee_id: int) -> bool:
        """
        :param conn: database connection;
        :param employee_id: employee ID in Telegram.
        :return: True if the employee is registered in the database.
        """

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        return bool(cursor.fetchall())
    
    @connect_and_disconnect_database
    def get_last_menu_item_name(self, conn, employee_id: int) -> Optional[str]:
        """
        :param conn: database connection;
        :param employee_id: employee ID in Telegram.
        :return: the name of the menu item where the employee was last.
        """

        cursor = conn.cursor()
        cursor.execute("SELECT last_menu FROM history WHERE employee_id = ?", (employee_id,))
        result = cursor.fetchall()
        return result[0][0] if result else None            

    @connect_and_disconnect_database
    def save_employee_history(self, conn, employee_id: int, menu_item_name: str) -> bool:
        """
        :param conn: database connection;
        :param employee_id: employee ID in Telegram;
        :param menu_item_name: the name of the menu item where the employee was last.
        """

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history WHERE employee_id = ?", (employee_id,))
        if not cursor.fetchall():
            cursor.execute("INSERT INTO history VALUES (?, ?)", (employee_id, menu_item_name))
        else:
            cursor.execute("UPDATE history SET last_menu = ? WHERE employee_id = ?", (menu_item_name, employee_id))
        conn.commit()
