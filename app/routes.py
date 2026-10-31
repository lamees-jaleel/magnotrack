import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db, check_db_connection
from app.models import SensorReading
from app.schemas import (
    SensorDataCreate,
    SensorDataPostResponse,
    SensorDataResponse,
    LatestReadingResponse,
    StatsResponse,
    HistoryResponse,
    ChartDataResponse,
    HealthResponse
)

logger = logging.getLogger("magnotrack.routes")

router = APIRouter(prefix="/api", tags=["MagnoTrack API"])

# Default timeout in seconds after which device is considered OFFLINE
OFFLINE_THRESHOLD_SECONDS = int(os.getenv("DEVICE_OFFLINE_THRESHOLD_SECONDS", "30"))


@router.post(
    "/sensor-data",
    response_model=SensorDataPostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record sensor telemetry from ESP32",
    description="Ingests cumulative event count, digital sensor status, and uptime from ESP32."
)
def record_sensor_data(
    payload: SensorDataCreate,
    db: Session = Depends(get_db)
):
    try:
        now_utc = datetime.now(timezone.utc)
        reading = SensorReading(
            device_id=payload.device_id.strip(),
            event_count=payload.event_count,
            magnet_detected=payload.magnet_detected,
            uptime_ms=payload.uptime_ms,
            created_at=now_utc
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)

        logger.info(
            f"Reading recorded [id={reading.id}] from {reading.device_id}: "
            f"count={reading.event_count}, magnet={reading.magnet_detected}, uptime={reading.uptime_ms}ms"
        )

        return SensorDataPostResponse(
            status="success",
            message="Sensor reading recorded successfully",
            id=reading.id,
            device_id=reading.device_id,
            created_at=reading.created_at
        )
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to record sensor reading: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record sensor telemetry: {str(exc)}"
        )


@router.get(
    "/latest",
    response_model=LatestReadingResponse,
    summary="Get latest reading and connection state"
)
def get_latest_reading(
    device_id: Optional[str] = Query(None, description="Optional device ID filter"),
    db: Session = Depends(get_db)
):
    query = db.query(SensorReading)
    if device_id:
        query = query.filter(SensorReading.device_id == device_id.strip())

    latest = query.order_by(desc(SensorReading.created_at), desc(SensorReading.id)).first()

    if not latest:
        return LatestReadingResponse(
            device_id=device_id or "magnotrack-01",
            is_online=False,
            seconds_since_last_seen=None,
            reading=None
        )

    now_utc = datetime.now(timezone.utc)
    # Ensure timezone awareness for comparison
    reading_time = latest.created_at
    if reading_time.tzinfo is None:
        reading_time = reading_time.replace(tzinfo=timezone.utc)

    diff_seconds = max(0.0, (now_utc - reading_time).total_seconds())
    is_online = diff_seconds <= OFFLINE_THRESHOLD_SECONDS

    return LatestReadingResponse(
        device_id=latest.device_id,
        is_online=is_online,
        seconds_since_last_seen=round(diff_seconds, 1),
        reading=SensorDataResponse.model_validate(latest)
    )


@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Get paginated history of sensor readings"
)
def get_history(
    limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    device_id: Optional[str] = Query(None, description="Optional device ID filter"),
    db: Session = Depends(get_db)
):
    query = db.query(SensorReading)
    if device_id:
        query = query.filter(SensorReading.device_id == device_id.strip())

    total = query.count()
    readings = (
        query.order_by(desc(SensorReading.created_at), desc(SensorReading.id))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return HistoryResponse(
        total=total,
        limit=limit,
        offset=offset,
        readings=[SensorDataResponse.model_validate(r) for r in readings]
    )


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Get aggregated statistics for dashboard KPIs"
)
def get_stats(
    device_id: Optional[str] = Query(None, description="Optional device ID filter"),
    db: Session = Depends(get_db)
):
    query = db.query(SensorReading)
    if device_id:
        query = query.filter(SensorReading.device_id == device_id.strip())

    total_readings = query.count()
    latest = query.order_by(desc(SensorReading.created_at), desc(SensorReading.id)).first()

    target_device = device_id or (latest.device_id if latest else "magnotrack-01")

    if not latest:
        return StatsResponse(
            device_id=target_device,
            total_events=0,
            events_last_60s=0,
            latest_event_timestamp=None,
            current_sensor_state=False,
            is_online=False,
            uptime_ms=None,
            total_readings_logged=0,
            last_seen_timestamp=None
        )

    now_utc = datetime.now(timezone.utc)
    reading_time = latest.created_at
    if reading_time.tzinfo is None:
        reading_time = reading_time.replace(tzinfo=timezone.utc)

    seconds_since_last_seen = (now_utc - reading_time).total_seconds()
    is_online = seconds_since_last_seen <= OFFLINE_THRESHOLD_SECONDS

    # 1. Total events: cumulative count reported by device
    total_events = latest.event_count

    # 2. Events in last 60 seconds:
    # Look back 60 seconds from now
    sixty_seconds_ago = now_utc - timedelta(seconds=60)
    readings_60s = (
        query.filter(SensorReading.created_at >= sixty_seconds_ago)
        .order_by(SensorReading.created_at.asc())
        .all()
    )

    events_last_60s = 0
    if len(readings_60s) >= 2:
        # Change in cumulative event count across the 60-second window
        earliest_in_window = readings_60s[0].event_count
        latest_in_window = readings_60s[-1].event_count
        events_last_60s = max(0, latest_in_window - earliest_in_window)
    elif len(readings_60s) == 1:
        # Check against reading immediately prior to the 60-second window
        prior_reading = (
            query.filter(SensorReading.created_at < sixty_seconds_ago)
            .order_by(desc(SensorReading.created_at))
            .first()
        )
        if prior_reading:
            events_last_60s = max(0, readings_60s[0].event_count - prior_reading.event_count)
        else:
            events_last_60s = readings_60s[0].event_count

    # 3. Latest event timestamp:
    # Most recent reading where magnet was detected OR event count was > 0
    latest_event_record = (
        query.filter(SensorReading.magnet_detected == True)
        .order_by(desc(SensorReading.created_at), desc(SensorReading.id))
        .first()
    )
    latest_event_timestamp = latest_event_record.created_at if latest_event_record else None

    # Fallback: if no active magnet detected record yet, but event_count > 0, use latest reading
    if latest_event_timestamp is None and latest.event_count > 0:
        latest_event_timestamp = latest.created_at

    return StatsResponse(
        device_id=latest.device_id,
        total_events=total_events,
        events_last_60s=events_last_60s,
        latest_event_timestamp=latest_event_timestamp,
        current_sensor_state=latest.magnet_detected,
        is_online=is_online,
        uptime_ms=latest.uptime_ms,
        total_readings_logged=total_readings,
        last_seen_timestamp=latest.created_at
    )


@router.get(
    "/chart-data",
    response_model=ChartDataResponse,
    summary="Get chronological time-series data for Chart.js charts"
)
def get_chart_data(
    limit: int = Query(30, ge=5, le=100, description="Number of recent points to plot"),
    device_id: Optional[str] = Query(None, description="Optional device ID filter"),
    db: Session = Depends(get_db)
):
    query = db.query(SensorReading)
    if device_id:
        query = query.filter(SensorReading.device_id == device_id.strip())

    # Get recent readings ordered by created_at DESC then reverse to chronological
    recent_readings = (
        query.order_by(desc(SensorReading.created_at), desc(SensorReading.id))
        .limit(limit)
        .all()
    )
    recent_readings.reverse()

    labels = []
    event_counts = []
    activity_deltas = []
    sensor_states = []

    prev_count = None
    for r in recent_readings:
        # Format time for chart axis: HH:MM:SS
        r_time = r.created_at
        if r_time.tzinfo is None:
            r_time = r_time.replace(tzinfo=timezone.utc)
        labels.append(r_time.strftime("%H:%M:%S"))

        event_counts.append(r.event_count)
        sensor_states.append(1 if r.magnet_detected else 0)

        # Delta calculation between consecutive readings
        if prev_count is None:
            activity_deltas.append(0)
        else:
            activity_deltas.append(max(0, r.event_count - prev_count))
        prev_count = r.event_count

    return ChartDataResponse(
        labels=labels,
        event_counts=event_counts,
        activity_deltas=activity_deltas,
        sensor_states=sensor_states
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check for API and Database"
)
def health_check():
    db_ok, db_msg = check_db_connection()
    status_str = "healthy" if db_ok else "degraded"
    return HealthResponse(
        status=status_str,
        database=db_msg,
        server_time=datetime.now(timezone.utc),
        version="1.0.0"
    )
