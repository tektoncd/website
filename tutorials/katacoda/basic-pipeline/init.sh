# Wait for Katacoda to initialize
sleep 1

# Start Kubernetes
launch.sh

# Install Tekton Pipelines
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# Install the Tekton CLI
curl -LO https://github.com/tektoncd/cli/releases/download/v0.10.0/tkn_0.10.0_Linux_x86_64.tar.gz
sudo tar xvzf tkn_0.10.0_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn

