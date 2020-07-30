#!/bin/bash

# Start Kubernetes
echo "Starting cluster"
launch.sh
echo "done" >> /opt/.clusterstarted

echo "Installing Tekton Pipelines"
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.14.3/release.yaml

mkdir /mnt/data

kubectl apply -f - << EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
EOF

kubectl delete configmap/config-artifact-pvc -n tekton-pipelines
kubectl create configmap config-artifact-pvc --from-literal=storageClassName=manual -n tekton-pipelines

echo "done" >> /opt/.pipelinesinstalled

echo "Installing Tekton Dashboard"
kubectl apply --filename https://github.com/tektoncd/dashboard/releases/download/v0.8.2/tekton-dashboard-release.yaml
echo "done" >> /opt/.dashboardinstalled

echo "Installing Tekton CLI"
curl -LO https://github.com/tektoncd/cli/releases/download/v0.11.0/tkn_0.11.0_Linux_x86_64.tar.gz
tar xvzf tkn_0.11.0_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn
echo "done" >> /opt/.tkninstalled

echo "Waiting for Tekton pods to be ready"
# Need to wait for pods to be scheduled first otherwise `kubectl wait` exits immediately with error
while [[ $(kubectl get pods -n tekton-pipelines --no-headers | wc -l) != 3 ]]; do echo "waiting" && sleep 1; done
kubectl wait pod -n tekton-pipelines --all --for=condition=Ready --timeout=180s
echo "done" >> /opt/.podsready

echo "Configure ingress"
kubectl --namespace tekton-pipelines port-forward --address=0.0.0.0 service/tekton-dashboard 9097:9097 &
echo "done" >> /opt/.ingressconfigured

echo "done" >> /opt/.backgroundfinished
