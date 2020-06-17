sleep 1
# Starts Kubernetes
launch.sh
# Installs Tekton in the Kubernetes cluster
## Tekton pipelines
#kubectl apply --filename https://storage.googleapis.com/tekton-releases/latest/release.yaml
# Sets up persistent volumes
#mkdir /mnt/data && kubectl apply -f https://k8s.io/examples/pods/storage/pv-volume.yaml && \
#kubectl delete configmap/config-artifact-pvc -n tekton-pipelines && \
#kubectl create configmap config-artifact-pvc --from-literal=storageClassName=manual -n tekton-pipelines
