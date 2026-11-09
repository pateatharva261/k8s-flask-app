# Explanation: Containerization and Deployment Process

## 1. Application
I built a small Flask web app (`app.py`) with two endpoints:
- `/` returns a greeting and the hostname of the machine serving the request.
- `/health` returns `{"status":"ok"}`, used by Kubernetes health probes.

Dependencies are listed in `requirements.txt` (Flask 3.0.3). I first tested it
locally at http://localhost:5000, where the hostname showed my PC name.

## 2. Containerization with Docker
The `Dockerfile` defines how the image is built:
- `FROM python:3.12-slim`: small official Python base image.
- `WORKDIR /app`: working directory inside the container.
- `COPY requirements.txt` then `RUN pip install`: dependencies are installed
  before copying the code, so Docker can cache this layer and rebuild faster.
- `COPY app.py`: adds the application code.
- `EXPOSE 5000` and `CMD ["python", "app.py"]`: documents the port and starts the app.

A `.dockerignore` keeps `venv/` and cache files out of the image.

Commands used:
- `docker build -t k8s-flask-app:v1 .` builds the image.
- `docker run -d --name flask-container -p 5000:5000 k8s-flask-app:v1` runs it.

When running in the container, the page showed the container ID
(`8e791b37c89d`) instead of my PC name, which proves the app runs inside Docker.

## 3. Publishing the image
Kubernetes pulls images from a registry, so I tagged and pushed the image:
- `docker tag k8s-flask-app:v1 pate77/k8s-flask-app:v1`
- `docker push pate77/k8s-flask-app:v1`

## 4. Kubernetes deployment
I used Docker Desktop's built-in single-node Kubernetes cluster and wrote two manifests.

**`k8s/deployment.yaml`**
- Runs 2 replicas of the image `pate77/k8s-flask-app:v1`.
- Uses a readiness probe and a liveness probe on `/health`.
- Sets CPU and memory requests/limits.
- The Deployment creates a ReplicaSet, which keeps 2 pods running and
  recreates any pod that fails (self-healing).

**`k8s/service.yaml`**
- Type `NodePort`, selecting pods with label `app: flask-app`.
- Service port 80 forwards to container port 5000, exposed on node port 30007.
- It load-balances traffic across the pods.

Commands used:
- `kubectl apply -f k8s/deployment.yaml`
- `kubectl apply -f k8s/service.yaml`
- `kubectl get pods`, `kubectl get services`, `kubectl get all`

## 5. Verification
Opening http://localhost:30007 showed the app with a pod name
(`flask-deployment-775899587-4jqnb`). `kubectl get all` showed 2/2 pods running,
the Deployment available, and the Service exposing `80:30007/TCP`.

## 6. Conclusion
The app moved from local code, to a Docker image, to a registry, to a
Kubernetes Deployment exposed through a Service. Docker gives a portable,
reproducible package, and Kubernetes adds scaling, health checks, self-healing
and service exposure.