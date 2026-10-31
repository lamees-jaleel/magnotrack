from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class SensorDataCreate(BaseModel):
    """
    Schema for incoming sensor telemetry sent by the ESP32 microcontroller.
    """
    device_id: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Unique device identifier (e.g., 'magnotrack-01')",
        examples=["magnotrack-01"]
    )
    event_count: int = Field(
        ...,
        ge=0,
        description="Cumulative count of magnetic detection events recorded by ESP32",
        examples=[12]
    )
    magnet_detected: bool = Field(
        ...,
        description="Instantaneous state of A3144 Hall-effect digital output (True when magnet is detected)",
        examples=[True]
    )
    uptime_ms: int = Field(
        ...,
        ge=0,
        description="Microcontroller uptime in milliseconds since boot",
        examples=[120000]
    )


class SensorDataResponse(BaseModel):
    """
    Schema representing a recorded sensor reading in API responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    event_count: int
    magnet_detected: bool
    uptime_ms: int
    created_at: datetime


class SensorDataPostResponse(BaseModel):
    """
    Response returned to ESP32 upon successful ingest.
    """
    status: str
    message: str
    id: int
    device_id: str
    created_at: datetime


class LatestReadingResponse(BaseModel):
    """
    Status of the most recent reading and device connectivity.
    """
    device_id: str
    is_online: bool
    seconds_since_last_seen: Optional[float] = None
    reading: Optional[SensorDataResponse] = None


class StatsResponse(BaseModel):
    """
    Aggregated operational statistics for dashboard KPI cards.
    """
    device_id: str
    total_events: int
    events_last_60s: int
    latest_event_timestamp: Optional[datetime] = None
    current_sensor_state: bool
    is_online: bool
    uptime_ms: Optional[int] = None
    total_readings_logged: int
    last_seen_timestamp: Optional[datetime] = None


class HistoryResponse(BaseModel):
    """
    Paginated history of sensor readings.
    """
    total: int
    limit: int
    offset: int
    readings: List[SensorDataResponse]


class ChartDataResponse(BaseModel):
    """
    Clean time-series data optimized for Chart.js rendering.
    """
    labels: List[str]
    event_counts: List[int]
    activity_deltas: List[int]
    sensor_states: List[int]  # 1 for detected, 0 for no magnet


class HealthResponse(BaseModel):
    """
    System and database health check payload.
    """
    status: str
    database: str
    server_time: datetime
    version: str = "1.0.0"
