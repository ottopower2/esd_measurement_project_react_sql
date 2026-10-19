import sqlite3
from models.api_models import ESDMeasurementRequest
from service.esd_service import ESDService


class ESDController:
    def __init__(self):
        self.service = ESDService()

    def start_measurement(self, db: sqlite3.Connection, request: ESDMeasurementRequest):
        return self.service.run_measurement(db, request)

    def list_measurements(self, db: sqlite3.Connection):
        return self.service.get_all(db)

    def get_measurement(self, db: sqlite3.Connection, measurement_id: int):
        return self.service.get_by_id(db, measurement_id)

    def delete_measurement(self, db: sqlite3.Connection, measurement_id: int):
        return self.service.delete_by_id(db, measurement_id)

    def get_countNumber_Measurements(self, db: sqlite3.Connection):
        return self.service.get_countNumber_Measurements(db)

    def get_operator_by_measurement_id(self, db: sqlite3.Connection, measurement_id: int):
        return self.service.get_operator_by_measurement_id(db, measurement_id)
