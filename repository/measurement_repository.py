import sqlite3
from datetime import UTC, datetime

from models.db_models import Measurement


SELECT_COLUMNS = """
    id, created_at, test_point, projekt_name, operator, test_art, hw,
    esd_voltage_kv, polarity, measured_voltage, scope_name,
    screenshot_path, status
"""


class MeasurementRepository:
    def create(self, db: sqlite3.Connection, **data) -> Measurement:
        created_at = datetime.now(UTC).isoformat()
        cursor = db.execute(
            """
            INSERT INTO measurements (
                created_at, test_point, projekt_name, operator, test_art, hw,
                esd_voltage_kv, polarity, measured_voltage, scope_name,
                screenshot_path, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                data["test_point"],
                data["projekt_name"],
                data["operator"],
                data["test_art"],
                data["hw"],
                data["esd_voltage_kv"],
                data["polarity"],
                data["measured_voltage"],
                data["scope_name"],
                data["screenshot_path"],
                data.get("status", "COMPLETED"),
            ),
        )
        db.commit()
        return self.get_by_id(db, cursor.lastrowid)

    def get_all(self, db: sqlite3.Connection) -> list[Measurement]:
        rows = db.execute(
            f"SELECT {SELECT_COLUMNS} FROM measurements ORDER BY id DESC"
        ).fetchall()
        return [Measurement.from_row(row) for row in rows]

    def get_by_id(
        self, db: sqlite3.Connection, measurement_id: int
    ) -> Measurement | None:
        row = db.execute(
            f"SELECT {SELECT_COLUMNS} FROM measurements WHERE id = ?",
            (measurement_id,),
        ).fetchone()
        return Measurement.from_row(row) if row else None

    def delete_by_id(
        self, db: sqlite3.Connection, measurement_id: int
    ) -> Measurement | None:
        measurement = self.get_by_id(db, measurement_id)
        if measurement:
            db.execute("DELETE FROM measurements WHERE id = ?", (measurement_id,))
            db.commit()
        return measurement

    def get_countNumber_Measurements(self, db: sqlite3.Connection) -> int:
        row = db.execute(
            "SELECT COUNT(*) FROM measurements"
        ).fetchone()
        return row[0] if row else 0

    def get_operator_by_measurement_id(self, db: sqlite3.Connection, measurement_id: int) -> str | None:
        row = db.execute(
            "SELECT operator FROM measurements WHERE id = ?",
            (measurement_id,),
        ).fetchone()
        return row[0] if row else None
