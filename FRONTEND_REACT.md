# React-Frontend starten

Das bestehende FastAPI-Backend wurde nicht verändert. Das neue Frontend liegt in `frontend/`.

## 1. Backend starten

```powershell
cd C:\Users\Amo\Desktop\esd_measurement_project_react
.\.venv\Scripts\Activate.ps1
uvicorn app:app --reload
```

## 2. React-Frontend starten

In einem zweiten Terminal:

```powershell
cd C:\Users\Amo\Desktop\esd_measurement_project_react\frontend
npm install
npm run dev
```

Danach `http://localhost:5173` öffnen. Vite leitet die API-Aufrufe an `http://127.0.0.1:8000` weiter.

## Verwendete API-Endpunkte

- `POST /esd/measurement`
- `GET /measurements`
- `GET /measurements/{id}`
- `GET /measurements/{id}/screenshot`
- `DELETE /measurements/{id}`
