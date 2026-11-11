from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="devops-metrics API",
    description="Collect and retrieve computer performance measurements.",
    version="0.1.0",
)

# Data Schema
class MeasurementCreate(BaseModel):
    """A CPU and memory reading submitted by a collector."""

    host_id: str = Field(min_length=1, examples=["my-pc"])
    cpu_percent: float = Field(ge=0, le=100, examples=[23.5])
    memory_percent: float = Field(ge=0, le=100, examples=[61.2])
    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the measurement was collected.",
    )


class Measurement(MeasurementCreate):
    """A submitted measurement with an API-generated ID."""

    id: UUID


# Temporary storage for Day 2. Postgres will replace this on Day 4.
_measurements: list[Measurement] = []


@app.get("/health", tags=["health"], summary="Check that the API is running")
def health_check() -> dict[str, str]:
    """Return success when the API process is running."""
    return {"status": "ok"}


@app.get("/ready", tags=["health"], summary="Check whether the API is ready")
def readiness_check() -> dict[str, str]:
    """For now, report ready; update this to check Postgres on Day 4."""
    return {"status": "ready"}


@app.post(
    "/measurements",
    response_model=Measurement,
    status_code=status.HTTP_201_CREATED,
    tags=["measurements"],
    summary="Submit a computer performance measurement",
)
def create_measurement(payload: MeasurementCreate) -> Measurement:
    """Validate and temporarily store one measurement."""
    measurement = Measurement(id=uuid4(), **payload.model_dump())
    _measurements.append(measurement)
    return measurement


@app.get(
    "/measurements",
    response_model=list[Measurement],
    tags=["measurements"],
    summary="List submitted measurements",
)
def list_measurements() -> list[Measurement]:
    """Return measurements received since the API started."""
    return _measurements