# devops-metrics

A hands-on DevOps learning project for collecting computer performance measurements and practicing how to build, package, deploy, and monitor a Python service.

**Status:** Early API prototype. The FastAPI endpoints are implemented; measurements are currently held in memory. The collector, PostgreSQL persistence, and deployment pipeline are planned.

## Project purpose

This project is a practical way to refresh Python and infrastructure skills while learning a modern DevOps workflow. A Python collector will read CPU and memory measurements from the computer where it runs and send them to the API. The API will validate and store those readings so they can be retrieved later.

## Current API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check that the API process is running. |
| `GET` | `/ready` | Report whether the API is ready. This is currently a placeholder and does not check a database yet. |
| `POST` | `/measurements` | Submit a CPU and memory measurement. |
| `GET` | `/measurements` | List measurements received since the API started. |

The API documentation is available at `/docs` while the service is running.

Example request body for `POST /measurements`:

```json
{
  "host_id": "my-pc",
  "cpu_percent": 23.5,
  "memory_percent": 61.2
}
```

`collected_at` is optional; when omitted, the API records the current UTC time.

## Run locally

Requirements: Python and pip.

From the repository root, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On Linux or macOS, activate it with:

```sh
source .venv/bin/activate
```

Start the API from the repository root:

```sh
python -m uvicorn app.main:app --reload
```

Open <http://localhost:8000/docs> to try the endpoints. Measurements are currently stored in memory and are lost when the API process stops or restarts.

## Planned architecture

- A Python collector reads CPU and memory measurements from its host and submits them to the FastAPI service.
- The API will store submitted measurements in PostgreSQL.
- A separate `/metrics` endpoint will later expose API telemetry, such as request counts and errors, for Prometheus to scrape. It is not implemented yet and will not be the source of host CPU or memory readings.
- Docker Compose will run the API and database locally.
- GitHub Actions will run checks and build a container image; GHCR will store the image.
- Kubernetes, Helm, and Argo CD will be used later to deploy the service locally.
- Terraform may be added for a separate infrastructure exercise once its role is defined.

## Learning goals

- Practice Linux, Git, and networking fundamentals.
- Build and containerize a Python service.
- Add automated checks and image publishing.
- Deploy and troubleshoot the service on Kubernetes.
- Document operational decisions and recovery steps.
