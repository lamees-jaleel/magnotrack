from datetime import datetime, timezone
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, func, Index
from app.database import Base


class SensorReading(Base):
    """
    Sensor reading record model.
    Stores telemetry emitted by ESP32 microcontrollers monitoring A3144 Hall-effect sensors.
    """
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String(64), nullable=False, index=True)
    event_count = Column(Integer, nullable=False, default=0)
    magnet_detected = Column(Boolean, nullable=False, default=False)
    uptime_ms = Column(BigInteger, nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        index=True
    )

    # Composite index for fast querying by device and chronological order
    __table_args__ = (
        Index("idx_device_created_at", "device_id", "created_at"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "event_count": self.event_count,
            "magnet_detected": self.magnet_detected,
            "uptime_ms": self.uptime_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<SensorReading id={self.id} device='{self.device_id}' "
            f"count={self.event_count} detected={self.magnet_detected} "
            f"uptime={self.uptime_ms}ms at={self.created_at}>"
        )
