---
title: "Install Tekton Operator"
linkTitle: "Tekton Operator"
weight: 4
description: >
  Install and manage Tekton components using the Tekton Operator
---

The [Tekton Operator](https://github.com/tektoncd/operator) provides a
Kubernetes-native way to install, upgrade, and manage Tekton components on your
cluster. It uses a `TektonConfig` custom resource to manage the lifecycle of
Tekton Pipelines, Triggers, Dashboard, and Chains.

## Install the Operator

Install the latest release of Tekton Operator:

```bash
kubectl apply -f https://storage.googleapis.com/tekton-releases/operator/latest/release.yaml
```

Monitor the installation:

```bash
kubectl get deploy -n tekton-operator --watch
```

## Create a TektonConfig

Once the Operator is running, create a `TektonConfig` to install all Tekton
components:

```yaml
apiVersion: operator.tekton.dev/v1alpha1
kind: TektonConfig
metadata:
  name: config
spec:
  profile: all
  targetNamespace: tekton-pipelines
```

Apply it:

```bash
kubectl apply -f tektonconfig.yaml
```

The `profile` field controls which components are installed:

| Profile | Components |
|---------|-----------|
| `all`   | Pipelines, Triggers, Dashboard, Chains |
| `basic` | Pipelines, Triggers |
| `lite`  | Pipelines only |

## Verify the installation

```bash
kubectl get tektonconfig config
kubectl get pods -n tekton-pipelines
```

## Upgrade

To upgrade Tekton components, update the Operator:

```bash
kubectl apply -f https://storage.googleapis.com/tekton-releases/operator/latest/release.yaml
```

The Operator automatically upgrades the managed components.

## Learn more

- [Tekton Operator repository](https://github.com/tektoncd/operator)
- [TektonConfig API reference](https://github.com/tektoncd/operator/blob/main/docs/TektonConfig.md)
- [OpenShift Pipelines](https://docs.openshift.com/pipelines/latest/about/about-pipelines.html)
  uses the Tekton Operator under the hood
