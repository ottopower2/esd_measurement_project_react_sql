from datetime import datetime
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ESDMeasurementRequest(BaseModel):
    projekt_name: str = Field(
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "ESD_Test"},
    )
    operator: str = Field(
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "John Doe"},
    )
    test_art: str = Field(
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "ESD"},
    )
    voltage_kv: float = Field(gt=0, json_schema_extra={"example": 1.0})
    polarity: str = Field(
        pattern="^(positive|negative)$",
        json_schema_extra={"example": "positive"},
    )
    test_point: str = Field(
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "KL30"},
    )
    hw: str = Field(
        min_length=1,
        max_length=100,
        validation_alias=AliasChoices("hw", "HW"),
        json_schema_extra={"example": "HW123"},
    )


class ESDMeasurementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    projekt_name: str
    operator: str
    test_art: str
    hw: str
    created_at: datetime
    test_point: str
    esd_voltage_kv: float
    polarity: str
    measured_voltage: float
    scope_name: str
    screenshot_path: str
    screenshot_url: str
    status: str
