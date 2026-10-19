# FastAPI ESD Project Cheat Sheet

This file is a quick reference for adding or changing fields in this project.

## Why this helps

- You do not need to remember every syntax detail from memory.
- You can follow one repeatable pattern.
- It helps you avoid common mistakes like `422`, missing DB columns, or `NOT NULL` errors.

## Add a new field example

Example field: `operator`

### 1. Frontend

Add the input in `templates/index.html`:

```html
<label>
  Operator
  <input id="operator" value="Max" />
</label>
```

Add it to the request body:

```javascript
const body = {
  projekt_name: document.getElementById('projektName').value,
  operator: document.getElementById('operator').value,
  test_art: document.getElementById('testArt').value,
  voltage_kv: Number(document.getElementById('voltage').value),
  polarity: document.getElementById('polarity').value,
  test_point: document.getElementById('testPoint').value,
};
```

### 2. Request model

In `models/api_models.py`:

```python
operator: str = Field(min_length=1, max_length=100, examples=["Max"])
```

### 3. Response model

In `models/api_models.py`:

```python
operator: str
```

### 4. Database model

In `models/db_models.py`:

```python
operator = Column(String(100), nullable=False)
```

### 5. Service layer

In `service/esd_service.py`:

```python
return self.repository.create(
    db,
    projekt_name=request.projekt_name,
    operator=request.operator,
    test_art=request.test_art,
    test_point=request.test_point,
    esd_voltage_kv=request.voltage_kv,
    polarity=request.polarity,
    measured_voltage=measured_voltage,
    scope_name=scope_name,
    screenshot_path=screenshot_path,
    status="COMPLETED",
)
```

### 6. Serializer

In `app.py` inside `serialize_measurement()`:

```python
"operator": item.operator,
```

### 7. Tests

In `tests/test_api.py`:

```python
json={
    "projekt_name": "ESD_Test",
    "operator": "Max",
    "test_art": "ESD",
    "voltage_kv": 1,
    "polarity": "positive",
    "test_point": "KL30",
}
```

### 8. Database file

If the SQLite DB already exists, either:

- delete `esd_measurements.db` and restart the app
- or run a DB migration / `ALTER TABLE`

## Order to remember

When adding a new field, check this flow:

`Frontend -> API Model -> DB Model -> Service -> Serializer -> Tests -> Database`

## Typical errors

### `422 Unprocessable Entity`

- field missing
- wrong field name
- wrong type

### `500 Internal Server Error`

Look at the real traceback. Often it means:

- DB column is missing
- a required field was not passed through the service

### `no column named ...`

- the code knows the field
- the SQLite table does not

### `NOT NULL constraint failed`

- the field exists in the DB
- but your code saved `None`
- often the field was forgotten in `service.py`

## Mini templates

Pydantic field:

```python
name: str = Field(min_length=1, max_length=100)
```

SQLAlchemy column:

```python
name = Column(String(100), nullable=False)
```

Service pass-through:

```python
name=request.name
```

Serializer:

```python
"name": item.name
```
