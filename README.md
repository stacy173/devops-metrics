# devops-metrics

A hands-on DevOps learning project for collecting sample computer performance
measurements and building, deploying, and monitoring the service.


## Project purpose

I’m building this project to refresh my Python and infrastructure skills while
practicing a modern DevOps workflow. The first version will collect CPU and
memory measurements from a test computer, send them to a FastAPI service, and
store them in PostgreSQL.


## Planned architecture

- A Python collector reads CPU and memory measurements from a test computer.
- A FastAPI service receives and stores those measurements in PostgreSQL.
- The service exposes its own operational metrics, such as request counts and
  errors, for Prometheus to scrape.
- Docker Compose runs the service and database locally.
- GitHub Actions runs checks and builds a container image; GHCR stores the image.
- Kubernetes, Helm, and Argo CD will be used later to deploy the service locally.

The service's `/metrics` endpoint will report how the service is operating. It
will not be presented as the source of computer CPU or memory measurements.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Check that the API process is running. |
| `GET` | `/ready` | Check whether the API is ready to serve requests. |
| `POST` | `/measurements` | Submit a CPU and memory measurement. |
| `GET` | `/measurements` | Retrieve submitted measurements. |

## Planned tools

Python, FastAPI, PostgreSQL, Docker Compose, GitHub Actions, GHCR, Kubernetes,
Helm, and Argo CD.

Terraform may be added for a separate infrastructure exercise once its role in
the project is defined.


## Running the project

Setup and run instructions will be added once the first working version exists.


## Learning goals

- Practice Linux, Git, and networking fundamentals.
- Build and containerize a Python service.
- Add automated checks and image publishing.
- Deploy and troubleshoot the service on Kubernetes.
- Document operational decisions and recovery steps.
