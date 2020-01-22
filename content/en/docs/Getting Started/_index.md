---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 1
description: >
  Prerequisites, Installation, and Basic Usage
---

{{% pageinfo %}}
WIP
{{% /pageinfo %}}

{{% tutorial name="Getting started with Tekton"
             katacoda-src="ratrosyu/getting-started"
             github-lnk="michaelawyu/tekton-examples/tree/master/getting-started"
             qwiklabs-lnk="" %}}

## Prerequisites

{{% tabs %}}
{{% tab "Kubernetes" %}}
* A Kubernetes cluster with 1.11 or later releases installed.
* Enable [Role-Based Access Control(RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
in the cluster.
* Grant current user `cluster-admin` privileges.

If you are using [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/),
see [Kubernetes Engine Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart)
for instructions on setting up a Kubernetes cluster. **GKE clusters have RBAC
enabled and persistent volumes available by default**; to grant current user 
the required privilege, run the following command:

```sh
kubectl create clusterrolebinding cluster-admin-binding \
                                  --clusterrole=cluster-admin \
                                  --user=$(gcloud config get-value core/account)
```

For other cloud providers or Minikube installations, refer to their
documentation for more information.
{{% /tab %}}

{{% tab "OpenShift" %}}
* An OpenShift cluster with 3.11 or later releases installed.
* Install the [OpenShift Container Platform CLI tool](https://docs.openshift.com/container-platform/3.11/cli_reference/get_started_cli.html#installing-the-cli).
* Sign in as a user with `cluster-admin` privileges.

    ```sh
    # Example #1: sign in using the default `system:admin` user with an OpenShift cluster
    oc login -u system:admin
    # Example #2: sign in using the default `admin:admin` user with a MiniShift cluster
    oc login -u admin:admin
    ```

{{% /tab %}}
{{% /tabs %}}

## Installation

To install Tekton, run the command below:

```sh
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

{{% alert title="Note" color="success" %}}
This command automatically installs the latest official release of Tekton. If
you would like to install a previous version, use

```
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/previous/YOUR-VERSION/release.yaml
```

Replace `YOUR-VERSION` with the release you prefer. [You can find the full list
of official Tekton releases on GitHub](https://github.com/tektoncd/pipeline/releases). 

Additionally, Tekton project pushes nightly releases every night to
`gcr.io/tekton-nightly`. If you are feeling adventurous and would like to
experiment with the most recent, unreleased code, see [Tekton Development Guide](https://github.com/tektoncd/pipeline/blob/master/DEVELOPMENT.md).
{{% /alert %}}

It may take a few moments before the installation completes. You can check
the progress with the following command:

```sh
kubectl get pods --namespace tekton-pipelines
```

Confirm that every component listed has the status `Running`.

### One last step

To run a CI/CD workflow, you need to provide Tekton a [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
for storage purposes. Tekton requests a volume of `5Gi` and
the default storage class unless otherwise configured. **Your Kubernetes
cluster, such as one from Google Kubernetes Engine, may have persistent volumes
set up at the time of creation, thus no extra step is required**; if not, you
may have to create them manually. Alternatively, you may ask Tekton
to use a [Google Cloud Storage](https://cloud.google.com/storage) bucket
or an [AWS Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/)
bucket instead. Note that the performance of Tekton may vary depending on
the storage option you choose.

{{% alert title="Note" color="success" %}}
You can check available persistent volumes and storage classes with the
commands below:

```
kubectl get pv
kubectl get storageclasses
```
{{% /alert %}}

These storage options can be configured using [`ConfigMap`](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)s:

{{% tabs %}}
{{% tab "Persistent Volumes" %}}
If you would like to configure the size and storage class of the Persistent
Volume Tekton requests, update the default `config-artifact-pvc` `configMap`.
This `configMap` includes two attributes:

* `size`: the size of the volume
* `storageClassName`: the name of the storage class of the volume

The following example asks Tekton to request a Persistent Volume of `10Gi` and
the `manual` storage class instead of the default one:

```
kubectl create configmap config-artifact-pvc \
                         --from-literal=size=10Gi \
                         --from-literal=storageClassName=manual \
                         -o yaml -n tekton-pipelines | kubectl replace -f -
```
{{% /tab %}}

{{% tab "Buckets" %}}
If you would like to use Google Cloud Storage or AWS S3 buckets instead,
remove the default `config-artifact-pvc` `configMap` and create another
one of the name `config-artifact-bucket`. This `configMap` includes the
following attributes:

* `location`: the address of the bucket, such as `gs://my-gcs-bucket/`
* (?)
{{% /tab %}}
{{% /tabs %}}

Also, Tekton uses the default service account in your Kubernetes cluster
unless otherwise configured; if you would like to override this option,
update the `default-service-account` attribute of the `ConfigMap`
`config-defaults`:

```
kubectl create configmap config-defaults \
                         --from-literal=default-service-account=YOUR-SERVICE-ACCOUNT \
                         -o yaml -n tekton-pipelines | kubectl replace -f -
```

## What's next

Now you have the core component of Tekton, Tekton Pipelines, installed on
your Kubernetes/OpenShift cluster. If you would like to install more
components, see the list below:

[WIP]

Learn more about Tekton in [Concepts](/docs/concepts/).
