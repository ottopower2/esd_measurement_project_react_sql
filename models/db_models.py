from dataclasses import dataclass
from datetime import datetime
from sqlite3 import Row


@dataclass
class Measurement:
    id: int
    created_at: datetime
    test_point: str
    projekt_name: str
    operator: str
    test_art: str
    hw: str
    esd_voltage_kv: float
    polarity: str
    measured_voltage: float
    scope_name: str
    screenshot_path: str
    status: str

    @classmethod
    def from_row(cls, row: Row) -> "Measurement":
        data = dict(row)
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)
