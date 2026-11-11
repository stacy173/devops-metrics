"""Collect one host CPU and memory sample and POST it to the API."""

from datetime import datetime, timezone
import os
import socket
import sys

import httpx
import psutil

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/measurements",
)


def collect_measurement():
    """Read system-wide CPU and memory use for this computer."""
    return {
        "host_id": socket.gethostname(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    measurement = collect_measurement()

    try:
        response = httpx.post(API_URL, json=measurement, timeout=5.0)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"API rejected the measurement (HTTP {exc.response.status_code}): "
            f"{exc.response.text}",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    except httpx.RequestError as exc:
        print(
            f"Could not connect to the API at {API_URL}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    print("Measurement accepted by the API:")
    print(response.json())


if __name__ == "__main__":
    main()
