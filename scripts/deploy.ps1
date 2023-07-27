# Ensure Docker is using the Minikube Docker daemon
minikube -p minikube docker-env | Invoke-Expression

# Build Docker image for the Flask app
docker build -t flask-app:0.0.1 ..\flask-app\

# Apply the Kubernetes configurations
kubectl apply -f ../configs/env-configmap.yml

kubectl apply -f ../elasticsearch-app/elasticsearch-deployment.yml
kubectl apply -f ../elasticsearch-app/elasticsearch-pvc.yml
kubectl apply -f ../elasticsearch-app/elasticsearch-service.yml

kubectl apply -f ../flask-app/flask-deployment.yml
kubectl apply -f ../flask-app/flask-service.yml

kubectl apply -f ../mongodb-app/mongodb-deployment.yml
kubectl apply -f ../mongodb-app/mongodb-pvc.yml
kubectl apply -f ../mongodb-app/mongodb-service.yml

# Wait until the flask-app pod is ready
$flask_app_label = "app=flask-app"
do {
    $status = kubectl get pods -l $flask_app_label -o jsonpath="{.items[0].status.phase}"
    if($status -eq "Running") {
        Write-Output "Flask App is ready."
        break
    } else {
        Write-Output "Waiting for Flask App to be ready..."
        Start-Sleep -Seconds 1
    }
} while ($true)

# Forward port for Flask service to be accessible from localhost
kubectl port-forward service/flask-service 5000:5000


