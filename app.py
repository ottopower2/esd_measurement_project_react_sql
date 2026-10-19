from pathlib import Path
import sqlite3
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from controller.esd_controller import ESDController
from database.database import create_tables, get_db
from models.api_models import ESDMeasurementRequest

create_tables()

app = FastAPI(title="ESD Oscilloscope Measurement API", version="1.0.0")
controller = ESDController()

app.mount("/static", StaticFiles(directory="static"), name="static")


def serialize_measurement(item):
    return {
        "id": item.id,
        "created_at": item.created_at,
        "projekt_name": item.projekt_name,
        "operator": item.operator,
        "test_art": item.test_art,
        "test_point": item.test_point,
        "esd_voltage_kv": item.esd_voltage_kv,
        "hw": item.hw,
        "polarity": item.polarity,
        "measured_voltage": item.measured_voltage,
        "scope_name": item.scope_name,
        "screenshot_path": item.screenshot_path,
        "screenshot_url": f"/measurements/{item.id}/screenshot",
        "status": item.status,
    }


@app.get("/")
def frontend():
    return FileResponse("templates/index.html")


@app.post("/esd/measurement")
def start_measurement(request: ESDMeasurementRequest, db: sqlite3.Connection = Depends(get_db)):
    item = controller.start_measurement(db, request)
    return serialize_measurement(item)


@app.get("/measurements")
def list_measurements(db: sqlite3.Connection = Depends(get_db)):
    return [serialize_measurement(item) for item in controller.list_measurements(db)]


@app.get("/measurements/count")
def get_measurements_count(db: sqlite3.Connection = Depends(get_db)):
    count = controller.get_countNumber_Measurements(db)
    return {"count": count}


@app.get("/measurements/{measurement_id}")
def get_measurement(measurement_id: int, db: sqlite3.Connection = Depends(get_db)):
    item = controller.get_measurement(db, measurement_id)
    if not item:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return serialize_measurement(item)


@app.get("/measurements/{measurement_id}/screenshot")
def get_screenshot(measurement_id: int, db: sqlite3.Connection = Depends(get_db)):
    item = controller.get_measurement(db, measurement_id)
    if not item:
        raise HTTPException(status_code=404, detail="Measurement not found")

    path = Path(item.screenshot_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Screenshot file not found")

    return FileResponse(path, media_type="image/png", filename=path.name)



@app.delete("/measurements/{measurement_id}")
def delete_measurement(measurement_id: int, db: sqlite3.Connection = Depends(get_db)):
    item = controller.get_measurement(db, measurement_id)
    if not item:
        raise HTTPException(status_code=404, detail="Measurement not found")

    # Delete the screenshot file if it exists
    path = Path(item.screenshot_path)
    if path.exists():
        path.unlink()

    # Delete the measurement record from the database
    controller.delete_measurement(db, measurement_id)

    return {"detail": "Measurement deleted successfully"}


@app.get("/measurements/{measurement_id}/operator")
def get_operator_by_measurement_id(measurement_id: int, db: sqlite3.Connection = Depends(get_db)):
    operator = controller.get_operator_by_measurement_id(db, measurement_id)
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return {"operator": operator}
