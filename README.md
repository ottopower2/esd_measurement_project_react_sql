# ESD Oscilloscope Measurement Project

A small full-stack learning project showing this flow:

`HTML -> FastAPI -> Controller -> Service -> ScopeClient -> RTO6/RTM64 -> Screenshot -> Repository -> Database`

## 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Start in mock mode

Mock mode is enabled by default, so you do not need a real oscilloscope.

```powershell
uvicorn app:app --reload
```

Open:

- Frontend: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

The default database is SQLite and will be created automatically as `esd_measurements.db`.

## 3. Connect a real RTO6 / RTM64

PowerShell example:

```powershell
$env:MOCK_SCOPE="false"
$env:SCOPE_IP="192.168.0.92"
uvicorn app:app --reload
```

Check and adapt the SCPI commands in `hardware/scope_client.py` to the measurement configuration of your instrument.

## 4. PostgreSQL instead of SQLite

Create database `esd_db`, then set:

```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:password@localhost:5432/esd_db"
uvicorn app:app --reload
```

Direct SQL creates the `measurements` table automatically for this learning project.

## Main endpoints

- `POST /esd/measurement` - run measurement and save screenshot + DB record
- `GET /measurements` - list measurement history
- `GET /measurements/{id}` - get one measurement
- `GET /measurements/{id}/screenshot` - return the PNG screenshot

## Important architecture idea

- `app.py`: HTTP/FastAPI routes only
- `controller/`: forwards API actions to business logic
- `service/`: coordinates the measurement workflow
- `hardware/`: VISA/SCPI communication
- `repository/`: database access
- `models/`: Pydantic API models and a database-row dataclass
