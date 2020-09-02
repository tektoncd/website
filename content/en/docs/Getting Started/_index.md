---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 1
description: >
  Prerequisites, Installation, and Basic Usage
---

{{% tutorial name="Getting started with Tekton"
             katacoda-src="ratrosyu/getting-started"
             github-lnk="michaelawyu/tekton-examples/tree/master/getting-started"
             qwiklabs-lnk="" %}}

## Prerequisites

* A Kubernetes cluster version 1.15 or higher for Tekton Pipelines v0.11.0 or higher, or a Kubernetes 
cluster version 1.11 or higher for Tekton releases before v0.11.0.
* Enable [Role-Based Access Control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
in the cluster.
* Grant current user the `cluster-admin` role.

If you don't already have a cluster, you can create one for testing with `kind`.
[Install `kind`](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) and create a cluster by running [`kind create cluster`](https://kind.sigs.k8s.io/docs/user/quick-start/#creating-a-cluster). This
will create a cluster running locally, with RBAC enabled and your user granted
the `cluster-admin` role.

## Installation

To install the core component of Tekton, Tekton Pipelines, run the command below:

```sh
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

If your container runtime does not support `image-reference:tag@digest` (for example, like cri-o used in OpenShift 4.x), use `release.notags.yaml` instead:

```sh
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.notags.yaml
```

{{% alert title="Note" color="success" %}}
This command automatically installs the latest official release of the
Tekton core component, Tekton Pipelines. If
you would like to install a previous version, use

```
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/previous/YOUR-VERSION/release.yaml
```

Replace `YOUR-VERSION` with the release you prefer. [You can find the full list
of official Tekton releases on GitHub](https://github.com/tektoncd/pipeline/releases). 

Additionally, Tekton Pipelines pushes nightly releases every night to
`gcr.io/tekton-nightly`. If you are feeling adventurous and would like to
experiment with the most recent, unreleased code, see [Tekton Development Guide](https://github.com/tektoncd/pipeline/blob/master/DEVELOPMENT.md).
{{% /alert %}}

It may take a few moments before the installation completes. You can check
the progress with the following command:

```sh
kubectl get pods --namespace tekton-pipelines
```

Confirm that every component listed has the status `Running`.

### Persistent volumes

To run a CI/CD workflow, you need to provide Tekton a [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
for storage purposes. Tekton requests a volume of `5Gi` with
the default storage class by default. **Your Kubernetes
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

These storage options can be configured using [`ConfigMaps`](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/):

{{% tabs %}}
{{% tab "Persistent Volumes" %}}
If you would like to configure the size and storage class of the Persistent
Volume Tekton requests, update the default `config-artifact-pvc` `configMap`.
This `configMap` includes two attributes:

* `size`: the size of the volume
* `storageClassName`: the name of the storage class of the volume

The following example asks Tekton to request a Persistent Volume of `10Gi` with
the `manual` storage class when running a workflow:

```
kubectl create configmap config-artifact-pvc \
                         --from-literal=size=10Gi \
                         --from-literal=storageClassName=manual \
                         -o yaml -n tekton-pipelines \
                         --dry-run=client | kubectl replace -f -
```
{{% /tab %}}

{{% tab "Buckets" %}}
If you would like to use Google Cloud Storage or AWS S3 buckets instead,
remove the default `config-artifact-pvc` `configMap` and create another
one of the name `config-artifact-bucket`. This `configMap` includes the
following attributes:

* `location`: the address of the bucket, such as `gs://my-gcs-bucket/`
* `bucket.service.account.secret.name`: the name of the
[Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/)
where the service account credentials for accessing the bucket reside.
* `bucket.service.account.secret.key`: the name of the key in the secret which
Tekton should use
* `bucket.service.account.field.name`: the name of the environment variable
to use when setting up the credentials. Defaults to `GOOGLE_APPLICATION_CREDENTIALS`;
use `BOTO_CONFIG` if you plan to use an AWS S3 bucket.

The following example asks Tekton to use a Google Cloud Storage bucket for
storage when running a workflow:

```
kubectl create configmap config-artifact-pvc \
                         --from-literal=location=gs://MY-GCS-BUCKET \
                         --from-literal=bucket.service.account.secret.name=my-secret \
                         --from-literal=bucket.service.account.secret.key=my-key \
                         -o yaml -n tekton-pipelines \
                         --dry-run=client | kubectl replace -f -
```

And the `my-secret` Kubernetes secret is configured as follows:

```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: kubernetes.io/opaque
stringData:
  my-key: MY-SERVICE-ACCOUNT-JSON-KEY
```
{{% /tab %}}
{{% /tabs %}}

Also, Tekton uses the default service account in your Kubernetes cluster
unless otherwise configured; if you would like to override this option,
update the `default-service-account` attribute of the `ConfigMap`
`config-defaults`:

```
kubectl create configmap config-defaults \
                         --from-literal=default-service-account=YOUR-SERVICE-ACCOUNT \
                         -o yaml -n tekton-pipelines \
                         --dry-run=client  | kubectl replace -f -
```

### Set up the CLI

For your convenience, it is recommended that you install the Tekton CLI, `tkn`,
together with the core component of Tekton, Tekton Pipelines.

{{% tabs %}}

{{% tab "macOS" %}}
`tkn` is available on macOS via [`brew`](https://brew.sh/):

```bash
brew tap tektoncd/tools
brew install tektoncd/tools/tektoncd-cli
```

You can also download it as a tarball from the [`tkn` Releases page](https://github.com/tektoncd/cli/releases).
After downloading the file, extract it to your `PATH`:

```bash
# Replace YOUR-DOWNLOADED-FILE with the file path of your own.
sudo tar xvzf YOUR-DOWNLOADED-FILE -C /usr/local/bin/ tkn
```

{{% /tab %}}

{{% tab "Windows" %}}
`tkn` is available on Windows via [Chocolatey](https://chocolatey.org/):

```cmd
choco install tektoncd-cli --confirm
```

You can also download it as a `.zip` file from the [`tkn` Releases page](https://github.com/tektoncd/cli/releases).
After downloading the file, add it to your `Path`:

* Uncompress the `.zip` file.
* Open **Control Panel** > **System and Security** > **System** > **Advanced System Settings**.
* Click **Environment Variables**, select the `Path` variable and click **Edit**.
* Click **New** and add the path to your uncompressed file.
* Click **OK**.
{{% /tab %}}

{{% tab "Linux" %}}
`tkn` is available on Linux as a `.deb` package (for Debian, Ubuntu and
other deb-based distros) and `.rpm` package (for Fedora, CentOS, and other
rpm-based distros).

* Debian, Ubuntu, and other deb-based distros

    Find the `.deb` package of the `tkn` release you would like to install on
    the [`tkn` Releases page](https://github.com/tektoncd/cli/releases) and
    install it with

    ```bash
    # Replace LINK-TO-THE-PACKAGE with the package URL you would like to use.
    rpm -Uvh LINK-TO-THE-PACKAGE
    ```

    If you are using the latest releases of Ubuntu or Debian, you may use the
    TektonCD CLI PPA instead:

    ```bash
    sudo apt update;sudo apt install -y gnupg
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3EFE0E0A2F2F60AA
    echo "deb http://ppa.launchpad.net/tektoncd/cli/ubuntu eoan main"|sudo tee /etc/apt/sources.list.d/tektoncd-ubuntu-cli.list
    sudo apt update && sudo apt install -y tektoncd-cli
    ```

* Fedora, CentOS, and other rpm-based distros

    Find the `.rpm` package of the `tkn` release you would like to install on
    the [`tkn` Releases page](https://github.com/tektoncd/cli/releases) and
    install it with

    ```bash
    # Replace LINK-TO-THE-PACKAGE with the package URL you would like to use.
    rpm -Uvh LINK-TO-THE-PACKAGE
    ```

    If you are using Fedora 30/31, CentOS 7/8, EPEL, or RHEL 8, @chmousel
    provides an unofficial `copr` package repository for installing the
    package:

    ```bash
    dnf copr enable chmouel/tektoncd-cli
    dnf install tektoncd-cli
    ```

Alternatively, you may download `tkn` as a tarball:

Find the tarball of the `tkn` release for your platform (`ARM` or `X86-64`)
you would like to install on the [`tkn` Releases page](https://github.com/tektoncd/cli/releases)
and install it with

```bash
# Replace LINK-TO-TARBALL with the package URL you would like to use.
curl -LO LINK-TO-TARBALL
# Replace YOUR-DOWNLOADED-FILE with the file path of your own.
sudo tar xvzf YOUR-DOWNLOADED-FILE -C /usr/local/bin/ tkn
```
{{% /tab %}}

{{% /tabs %}}

## Your first CI/CD workflow with Tekton

With Tekton, each operation in your CI/CD workflow becomes a `Step`,
which is executed with a container image you specify. `Steps` are then
organized in `Tasks`, which run as a [Kubernetes pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)
in your cluster. You can further organize `Tasks` into `Pipelines`, which 
can control the order of execution of several `Tasks`. 

To create a `Task`, create a Kubernetes object using the Tekton API with
the kind `Task`. The following YAML file specifies a `Task` with one simple
`Step`, which prints a `Hello World!` message using
[the official Ubuntu image](https://hub.docker.com/_/ubuntu/):

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: hello
spec:
  steps:
    - name: hello
      image: ubuntu
      command:
        - echo
      args:
        - "Hello World!"
```

Write the YAML above to a file named `task-hello.yaml`, and apply it to your Kubernetes cluster:

```bash
kubectl apply -f task-hello.yaml
```

To run this task with Tekton, you need to create a `TaskRun`, which is
another Kubernetes object used to specify run time information for a `Task`. 

To view this `TaskRun` object you can run the following Tekton CLI (`tkn`) command:

```shell
tkn task start hello --dry-run
```

After running the command above, the following `TaskRun` definition should be shown:

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  generateName: hello-run-
spec:
  taskRef:
    name: hello
```

To use the `TaskRun` above to start the `echo` `Task`, you can either use 
`tkn` or `kubectl`.

Start with `tkn`:

```shell
tkn task start hello
```

Start with `kubectl`:

```shell
# use tkn's --dry-run option to save the TaskRun to a file
tkn task start hello --dry-run > taskRun-hello.yaml
# create the TaskRun
kubectl create -f taskRun-hello.yaml
```

Tekton will now start running your `Task`. To see the logs of the last `TaskRun`, run 
the following `tkn` command:

```shell
tkn taskrun logs --last -f 
```

It may take a few moments before your `Task` completes. When it executes, it should 
show the following output:

```
[hello] Hello World!
```

## What's next

Now you have the core component of Tekton, Tekton Pipelines, installed on
your cluster with the Tekton CLI installed on your local
machine. Continue to experiment with pipelines with the 
[Getting Started - Pipelines](./pipelines). If you would like to install 
more components, see the list below:

* [Tekton Triggers](/docs/triggers)
* [Tekton Dashboard](/docs/dashboard)

Learn more about Tekton in [Concepts](/docs/concepts/).
