# Campus Lost and Found Portal — DevOps Case Study

A simple Flask app for reporting lost/found campus items. Includes Docker, Kubernetes manifests and a Jenkins pipeline.

## Run locally (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. Health check: http://127.0.0.1:5000/health

## Build and run Docker
Change `srivigna115` in `deployment.yaml` and `Jenkinsfile` if your Docker Hub username differs.
```powershell
docker build -t srivigna115/campus-lost-found:latest .
docker run --name campus-lost-found -p 5000:5000 -v campus-lost-found-data:/app/data srivigna115/campus-lost-found:latest
```
Open http://localhost:5000.

## Push to GitHub
Create an empty GitHub repository and run:
```powershell
git init
git add .
git commit -m "Add Campus Lost and Found DevOps case study"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
Replace the remote URL with your actual repository URL.

## Push Docker image
Build the image first, then:
```powershell
docker login
docker push srivigna115/campus-lost-found:latest
```
Make sure the repository exists on Docker Hub and replace username if needed.

## Kubernetes (Docker Desktop)
Ensure Docker Desktop is running and Kubernetes is enabled:
```powershell
kubectl get nodes
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
```
Open http://localhost:30080.

## Jenkins
Jenkins must be able to run `git`, `docker`, and `kubectl`, access the Docker daemon, and access the Kubernetes cluster.
1. In Jenkins > Manage Jenkins > Credentials, add Username with password credentials with ID `dockerhub-creds`; use a Docker Hub access token as the password.
2. Create a Pipeline job. Choose Pipeline script from SCM, SCM Git, enter your repository URL, branch `*/main`, script path `Jenkinsfile`.
3. Run Build Now.
4. For automatic builds on every push, enable GitHub hook trigger in the job and configure a webhook to `https://YOUR-REACHABLE-JENKINS-URL/github-webhook/`. GitHub cannot reach a localhost-only Jenkins instance; for a classroom demo, manual Build Now is acceptable if webhook networking is not ready.

The pipeline checks out code, builds and pushes an image tagged with the Jenkins build number and `latest`, applies Kubernetes manifests and waits for rollout.

## Demo limitations
This beginner demo uses SQLite in the container. Kubernetes pod replacement can lose records because persistent storage is not configured. Do not store real personal contact details in a public demo.
