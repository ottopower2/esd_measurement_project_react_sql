import sqlite3
from pathlib import Path

from config import DATABASE_URL


def database_path_from_url(database_url: str) -> Path:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError(
            "Diese SQL-Version unterstuetzt DATABASE_URL derzeit nur mit sqlite:///"
        )
    return Path(database_url.removeprefix(prefix))


def connect(database_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(database_path) if database_path else database_path_from_url(DATABASE_URL)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables(connection: sqlite3.Connection | None = None) -> None:
    owns_connection = connection is None
    db = connection or connect()
    try:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                test_point TEXT NOT NULL,
                projekt_name TEXT NOT NULL,
                operator TEXT NOT NULL,
                test_art TEXT NOT NULL,
                hw TEXT NOT NULL,
                esd_voltage_kv REAL NOT NULL,
                polarity TEXT NOT NULL,
                measured_voltage REAL NOT NULL,
                scope_name TEXT NOT NULL,
                screenshot_path TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'COMPLETED'
            )
            """
        )
        db.commit()
    finally:
        if owns_connection:
            db.close()


def get_db():
    db = connect()
    try:
        yield db
    finally:
        db.close()
