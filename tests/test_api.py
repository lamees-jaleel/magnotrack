import os
import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use in-memory SQLite database for unit tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DEVICE_OFFLINE_THRESHOLD_SECONDS"] = "30"

from app.database import Base, get_db
from app.models import SensorReading
from app.main import app

# Create test database engine with StaticPool so all connections share the same in-memory DB
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "database" in data
    assert "server_time" in data


def test_serve_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "MagnoTrack" in response.text
    assert "Total Magnetic Events" in response.text
    assert "Chart.js" in response.text or "chart.umd" in response.text


def test_empty_stats_and_latest(client):
    stats_res = client.get("/api/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_events"] == 0
    assert stats["events_last_60s"] == 0
    assert stats["is_online"] is False
    assert stats["current_sensor_state"] is False
    assert stats["latest_event_timestamp"] is None

    latest_res = client.get("/api/latest")
    assert latest_res.status_code == 200
    latest = latest_res.json()
    assert latest["reading"] is None
    assert latest["is_online"] is False


def test_post_sensor_data_validation(client):
    # Missing required field
    res = client.post("/api/sensor-data", json={"device_id": "magnotrack-01"})
    assert res.status_code == 422

    # Negative event count
    res = client.post("/api/sensor-data", json={
        "device_id": "magnotrack-01",
        "event_count": -1,
        "magnet_detected": True,
        "uptime_ms": 1000
    })
    assert res.status_code == 422

    # Negative uptime
    res = client.post("/api/sensor-data", json={
        "device_id": "magnotrack-01",
        "event_count": 0,
        "magnet_detected": True,
        "uptime_ms": -50
    })
    assert res.status_code == 422


def test_post_and_retrieve_sensor_data(client):
    # Ingest first packet (magnet detected)
    payload1 = {
        "device_id": "magnotrack-01",
        "event_count": 5,
        "magnet_detected": True,
        "uptime_ms": 10000
    }
    post_res1 = client.post("/api/sensor-data", json=payload1)
    assert post_res1.status_code == 201
    res_data1 = post_res1.json()
    assert res_data1["status"] == "success"
    assert res_data1["id"] == 1
    assert res_data1["device_id"] == "magnotrack-01"

    # Ingest second packet (magnet removed)
    payload2 = {
        "device_id": "magnotrack-01",
        "event_count": 8,
        "magnet_detected": False,
        "uptime_ms": 12000
    }
    post_res2 = client.post("/api/sensor-data", json=payload2)
    assert post_res2.status_code == 201
    assert post_res2.json()["id"] == 2

    # Test /api/latest
    latest_res = client.get("/api/latest")
    assert latest_res.status_code == 200
    latest_data = latest_res.json()
    assert latest_data["is_online"] is True
    assert latest_data["reading"]["event_count"] == 8
    assert latest_data["reading"]["magnet_detected"] is False

    # Test /api/stats
    stats_res = client.get("/api/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_events"] == 8
    assert stats["events_last_60s"] == 3  # 8 - 5 = 3
    assert stats["is_online"] is True
    assert stats["current_sensor_state"] is False
    assert stats["total_readings_logged"] == 2
    assert stats["latest_event_timestamp"] is not None

    # Test /api/history pagination
    hist_res = client.get("/api/history?limit=1&offset=0")
    assert hist_res.status_code == 200
    hist = hist_res.json()
    assert hist["total"] == 2
    assert len(hist["readings"]) == 1
    assert hist["readings"][0]["id"] == 2

    hist_offset_res = client.get("/api/history?limit=1&offset=1")
    assert hist_offset_res.status_code == 200
    hist_offset = hist_offset_res.json()
    assert hist_offset["readings"][0]["id"] == 1

    # Test /api/chart-data
    chart_res = client.get("/api/chart-data?limit=10")
    assert chart_res.status_code == 200
    chart = chart_res.json()
    assert len(chart["labels"]) == 2
    assert chart["event_counts"] == [5, 8]
    assert chart["activity_deltas"] == [0, 3]
    assert chart["sensor_states"] == [1, 0]


def test_device_offline_detection():
    """Verify that a reading older than 30s marks the device as OFFLINE."""
    db = TestingSessionLocal()
    try:
        # Insert a reading timestamped 45 seconds ago
        old_time = datetime.now(timezone.utc) - timedelta(seconds=45)
        old_reading = SensorReading(
            device_id="magnotrack-01",
            event_count=10,
            magnet_detected=False,
            uptime_ms=60000,
            created_at=old_time
        )
        db.add(old_reading)
        db.commit()

        client = TestClient(app)

        latest_res = client.get("/api/latest")
        assert latest_res.status_code == 200
        latest = latest_res.json()
        assert latest["is_online"] is False
        assert latest["seconds_since_last_seen"] >= 45.0

        stats_res = client.get("/api/stats")
        assert stats_res.status_code == 200
        stats = stats_res.json()
        assert stats["is_online"] is False
    finally:
        db.close()


def test_multiple_devices_filtering(client):
    """Verify filtering by device_id."""
    client.post("/api/sensor-data", json={
        "device_id": "device-A",
        "event_count": 10,
        "magnet_detected": True,
        "uptime_ms": 5000
    })
    client.post("/api/sensor-data", json={
        "device_id": "device-B",
        "event_count": 25,
        "magnet_detected": False,
        "uptime_ms": 7000
    })

    # Query device-A
    res_a = client.get("/api/latest?device_id=device-A")
    assert res_a.json()["device_id"] == "device-A"
    assert res_a.json()["reading"]["event_count"] == 10

    # Query device-B
    res_b = client.get("/api/latest?device_id=device-B")
    assert res_b.json()["device_id"] == "device-B"
    assert res_b.json()["reading"]["event_count"] == 25

    # Query stats for device-A
    stats_a = client.get("/api/stats?device_id=device-A")
    assert stats_a.json()["total_events"] == 10
