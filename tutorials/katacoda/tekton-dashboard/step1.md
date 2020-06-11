In this section, we will install and expose the Tekton Dashboard.

## Katacoda Kubernetes Cluster

It might take a minute or two for Katacoda to initialize your Kubernetes
cluster. When your cluster has been initialized, the
`kubectl cluster-info`{{execute}} command will return the cluster info.

Now, let's begin!

## Install the Tekton Dashboard Prerequisites

- [Tekton Pipelines](https://github.com/tektoncd/pipeline/blob/master/docs/install.md)
`kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.10.1/release.yaml`{{execute}}
- [Tekton Triggers](https://github.com/tektoncd/triggers/blob/master/docs/install.md) (optional)
`kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/previous/v0.3.1/release.yaml`{{execute}}

Verify the pods are running:
`kubectl get pods -n tekton-pipelines`{{execute}}

## Install the Tekton Dashboard

For reference, the installation instructions are [here](https://github.com/tektoncd/dashboard#install-dashboard). To install the Tekton Dashboard, run the following
command:
`kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/previous/v0.5.3/tekton-dashboard-release.yaml`{{execute}}

<!-- `kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/release.yaml`{{execute}} -->

Verify the Dashboard pod is running:
`kubectl get pods -n tekton-pipelines`{{execute}}

## Expose the Tekton Dashboard

### Install Ingress controller

Install the nginx ingress controller into the `ingress-nginx` namespace:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud/deploy.yaml
```{{execute}}

Verify the ingress controller pod is running:

```bash
kubectl get pods -n ingress-nginx
```{{execute}}

### Create Ingress for the Tekton Dashboard

View the Tekton Dashboard Service:
`kubectl get svc tekton-dashboard -n tekton-pipelines`{{execute}}

The Tekton Dashboard Service is exposed on port `9097`. So, create an Ingress
for the `tekton-dashboard` Service on port `9097`:

```bash
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: tekton-dashboard
  namespace: tekton-pipelines
spec:
  backend:
    serviceName: tekton-dashboard
    servicePort: 9097
EOF
```{{execute}}

Verify the Ingress was created:
`kubectl get ingress -n tekton-pipelines`{{execute}}

## Open the Tekton Dashboard

Open the `Dashboard` tab in your Katacoda window, or click on the following link:
https://[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com/.

It might take a minute for the ingress and Katacoda to get set up.

![Dashboard homepage screenshot](https://raw.githubusercontent.com/ncskier/katacoda/master/tekton-dashboard/images/dashboard-homepage.png)
