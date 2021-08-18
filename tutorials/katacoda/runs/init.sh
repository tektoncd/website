# Starts Kubernetes
launch.sh
# Installs Tekton in the Kubernetes cluster
## Tekton pipelines
# kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
# Pin to v0.26 since that's the last supported release on Kubernetes 1.18 (environment provided by Katacoda)
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.26.0/release.yaml

# Sets up persistent volumes
mkdir /mnt/data && kubectl apply -f https://k8s.io/examples/pods/storage/pv-volume.yaml
kubectl delete configmap/config-artifact-pvc -n tekton-pipelines
kubectl create configmap config-artifact-pvc --from-literal=storageClassName=manual -n tekton-pipelines
