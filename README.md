# Containerized Flask App on Docker and Kubernetes

A simple Flask web app, containerized with Docker and deployed to Kubernetes
using a Deployment (2 replicas) and a NodePort Service.

## Project structure

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── screenshots/
```

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Build and run with Docker

```bash
docker build -t k8s-flask-app:v1 .
docker run -d --name flask-container -p 5000:5000 k8s-flask-app:v1
```

## Docker Hub image

`pate77/k8s-flask-app:v1`

## Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get all
```

Open http://localhost:30007

## Endpoints

- `/` shows a greeting and the serving hostname (pod name in Kubernetes)
- `/health` returns `{"status":"ok"}` (used by the probes)
