from datetime import datetime
from pathlib import Path
import sqlite3

from config import SCREENSHOT_DIR
from hardware.scope_client import ScopeClient
from models.api_models import ESDMeasurementRequest
from repository.measurement_repository import MeasurementRepository


class ESDService:
    def __init__(self):
        self.scope = ScopeClient()
        self.repository = MeasurementRepository()

    def run_measurement(self, db: sqlite3.Connection, request: ESDMeasurementRequest):
        scope_name = self.scope.get_identity()
        measured_voltage = self.scope.get_voltage()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = (
            f"ESD_{request.voltage_kv:g}kV_"
            f"{request.polarity}_{request.test_point}_{timestamp}.png"
        )
        local_path = str(Path(SCREENSHOT_DIR) / filename)
        screenshot_path = self.scope.save_screenshot(local_path)

        return self.repository.create(
            db,
            projekt_name=request.projekt_name,
            test_art=request.test_art,
            test_point=request.test_point,
            esd_voltage_kv=request.voltage_kv,
            polarity=request.polarity,
            operator=request.operator,
            measured_voltage=measured_voltage,
            hw=request.hw,
            scope_name=scope_name,
            screenshot_path=screenshot_path,
            status="COMPLETED",
        )

    def get_all(self, db: sqlite3.Connection):
        return self.repository.get_all(db)

    def get_by_id(self, db: sqlite3.Connection, measurement_id: int):
        return self.repository.get_by_id(db, measurement_id)

    def delete_by_id(self, db: sqlite3.Connection, measurement_id: int):
        return self.repository.delete_by_id(db, measurement_id)


    def get_countNumber_Measurements(self, db: sqlite3.Connection):
        return self.repository.get_countNumber_Measurements(db)


    def get_operator_by_measurement_id(self, db: sqlite3.Connection, measurement_id: int):
        return self.repository.get_operator_by_measurement_id(db, measurement_id)

