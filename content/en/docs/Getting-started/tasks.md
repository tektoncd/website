<!--
---
title: "Getting started with Tasks"
likTitle: "Tasks"
weight: 1
description: >
  Set up and run your first Tekton Task
---
!-->

This tutorial shows you how to 

1. Create a Kubernetes cluster with [minikube](https://minikube.sigs.k8s.io/).
1. Install Tekton pipelines.
1. Create a Task.
1. Use `TaskRun` to instantiate and run the Task.

## Prerequisites

1.  [Install minikube](https://minikube.sigs.k8s.io/docs/start/). You only have
    to complete the step 1, "Installation".

1.  [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).

## Create a Kubernetes cluster

Create a cluster:

```bash
minikube start --kubernetes-version v1.33.1
```

The process takes a few seconds, you see an output similar to the following,
depending on the [minikube driver](https://minikube.sigs.k8s.io/docs/drivers/)
that you are using:

```
😄  minikube v1.36.0 on Darwin 15.5 (arm64)
✨  Using the qemu2 driver based on user configuration
🌐  Automatically selected the builtin network
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🔥  Creating qemu2 VM (CPUs=2, Memory=6000MB, Disk=20000MB) ...
📦  Preparing Kubernetes v1.33.1 on containerd 1.7.23 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

You can check that the cluster was successfully created with `kubectl`:

```bash
kubectl cluster-info
```

The output confirms that Kubernetes is running:

```
Kubernetes control plane is running at https://localhost:64858
CoreDNS is running at https://localhost:64858/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## Install Tekton Pipelines

1. To install the latest version of Tekton Pipelines, use `kubectl`:

   ```bash
   kubectl apply --filename \
   https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
   ```

1. Monitor the installation:

   ```bash
   kubectl get pods --namespace tekton-pipelines --watch
   ```

    When both `tekton-pipelines-controller` and `tekton-pipelines-webhook` show
    `1/1` under the `READY` column, you are ready to continue. For example:

    ```
    NAME                                          READY   STATUS    RESTARTS   AGE
    tekton-events-controller-786b59d5cd-jt7d9     0/1     Running   0          2s
    tekton-pipelines-controller-59b6cdbbc-2kw2w   0/1     Running   0          2s
    tekton-pipelines-webhook-74b5cdfcc4-g4qj2     0/1     Running   0          2s
    tekton-pipelines-controller-59b6cdbbc-2kw2w   1/1     Running   0          11s
    tekton-events-controller-786b59d5cd-jt7d9     1/1     Running   0          11s
    tekton-pipelines-webhook-74b5cdfcc4-g4qj2     1/1     Running   0          11s
    ```

    Hit *Ctrl + C* to stop monitoring.

## Create and run a basic Task

A **Task**, represented in the API as an object of kind `Task`, defines a
series of **Steps** that run sequentially to perform logic that the Task
requires. Every Task runs as a pod on the Kubernetes cluster, with each step
running in its own container.

1.  To create a Task, open your favorite editor and create a file named
    `hello-world.yaml` with the following content:

    ```yaml
    apiVersion: tekton.dev/v1
    kind: Task
    metadata:
      name: hello
    spec:
      steps:
        - name: echo
          image: alpine
          script: |
            #!/bin/sh
            echo "Hello World"
    ```

1.  Apply the changes to your cluster:

    ```bash
    kubectl apply --filename hello-world.yaml
    ```

      The output confirms that the Task was created successfully:

      ```
      task.tekton.dev/hello created
      ```

1.  A `TaskRun` object instantiates and executes this Task. Create another
    file named `hello-world-run.yaml` with the following content:

    ```yaml
    apiVersion: tekton.dev/v1
    kind: TaskRun
    metadata:
      name: hello-task-run
    spec:
      taskRef:
        name: hello
    ```

1.  Apply the changes to your cluster to launch the Task:

    ```bash
    kubectl apply --filename hello-world-run.yaml
    ``` 

1.  Verify that everything worked correctly:

    ```bash
    kubectl get taskrun hello-task-run
    ```

    The output of this command shows the status of the Task:

     
    ```
    NAME             SUCCEEDED   REASON      STARTTIME   COMPLETIONTIME
    hello-task-run   True        Succeeded   28s         3s
    ```

    The value `True` under `SUCCEEDED` confirms that TaskRun completed with no errors.


1.  Take a look at the logs:

    ```bash
    kubectl logs --selector=tekton.dev/taskRun=hello-task-run
    ```

    The output displays the message:

    ```
    Hello World
    ```

## Cleanup

To learn about Tekton Pipelines, skip this section and proceed to the [next
tutorial][pipelines-qs].

To delete the cluster that you created for this guide run:

```bash
minikube delete
```

The output confirms that the cluster was deleted:

```
🔥  Deleting "minikube" in qemu2 ...
💀  Removed all traces of the "minikube" cluster.
```

## Further Reading:

We recommend that you complete [Getting started with Pipelines][pipelines-qs].

For more complex examples see:

- [Clone a git repository with Tekton][git-howto].
- [Build and push a container image with Tekton][kaniko-howto].

[pipelines-qs]: /docs/getting-started/pipelines/
[git-howto]: /docs/how-to-guides/clone-repository/
[kaniko-howto]: /docs/how-to-guides/kaniko-build-push/
