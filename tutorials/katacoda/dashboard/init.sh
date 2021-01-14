# Wait for Katacoda to initialize
sleep 1

# Start Kubernetes
launch.sh

# # Install Tekton Pipelines
# kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# # Install Tekton Triggers
# kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml

# # Install Tekton Dashboard
# kubectl apply --filename https://github.com/tektoncd/dashboard/releases/download/v0.3.0/dashboard-latest-release.yaml
# kubectl port-forward -n tekton-pipelines svc/tekton-dashboard 9097:9097 &
