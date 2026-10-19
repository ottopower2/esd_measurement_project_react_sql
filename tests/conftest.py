import sys
import sqlite3
from pathlib import Path
from uuid import uuid4

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from database.database import create_tables, get_db
import service.esd_service as esd_service


@pytest.fixture(autouse=True)
def use_test_database():
    temp_root = PROJECT_ROOT / ".pytest_tmp" / uuid4().hex
    db_path = temp_root / "test_esd_measurements.db"
    screenshot_dir = temp_root / "screenshots"
    temp_root.mkdir(parents=True, exist_ok=True)
    setup_connection = sqlite3.connect(db_path, check_same_thread=False)
    setup_connection.row_factory = sqlite3.Row
    create_tables(setup_connection)
    setup_connection.close()

    def override_get_db():
        db = sqlite3.connect(db_path, check_same_thread=False)
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    original_screenshot_dir = esd_service.SCREENSHOT_DIR
    esd_service.SCREENSHOT_DIR = str(screenshot_dir)

    try:
        yield
    finally:
        app.dependency_overrides.clear()
        esd_service.SCREENSHOT_DIR = original_screenshot_dir
