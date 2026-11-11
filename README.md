# devops-metrics

A hands-on DevOps learning project for collecting computer performance measurements and practicing how to build, package, deploy, and monitor a Python service.

**Status:** Early prototype. The FastAPI API and a one-shot host metrics collector are implemented. Measurements are currently held in API memory and are lost when the API restarts. PostgreSQL persistence and the deployment pipeline are planned.

## Project purpose

This project is a practical way to refresh Python and infrastructure skills while learning a modern DevOps workflow. The collector reads CPU and memory usage from the computer where it runs and submits a measurement to the FastAPI service. The API validates the reading and temporarily stores it so it can be retrieved.

## Current API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check that the API process is running. |
| `GET` | `/ready` | Report whether the API is ready. This is currently a placeholder and does not check a database yet. |
| `POST` | `/measurements` | Submit a CPU and memory measurement. |
| `GET` | `/measurements` | List measurements received since the API started. |

The API documentation is available at `/docs` while the service is running.

## Run locally

Requirements: Python and pip.

From the repository root, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On Linux or macOS, activate the environment with:

```sh
source .venv/bin/activate
```

Start the API in one terminal:

```sh
python -m uvicorn app.main:app --reload
```

In a second terminal, activate the same virtual environment and run the collector once:

```sh
python -m collector.main
```

The collector measures the operating system where it runs. For this local setup, run both processes on the same computer so the default API URL, `http://127.0.0.1:8000/measurements`, works. If the API is listening at another address, set `API_URL` before running the collector.

For PowerShell:

```powershell
$env:API_URL = "http://127.0.0.1:8000/measurements"
python -m collector.main
```

For Linux or macOS:

```sh
export API_URL="http://127.0.0.1:8000/measurements"
python -m collector.main
```

A successful run prints the API response, including the generated measurement ID. Open <http://localhost:8000/docs>, run `GET /measurements`, and confirm the new measurement appears. The in-memory list clears when the API process restarts.

## Planned architecture

- The API will store submitted measurements in PostgreSQL instead of process memory.
- A separate `/metrics` endpoint will expose API telemetry, such as request counts and errors, for Prometheus to scrape. It is not implemented yet and will not be the source of host CPU or memory readings.
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
