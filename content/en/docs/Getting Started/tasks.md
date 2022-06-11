---
title: "Getting started with Tasks"
likTitle: "Tasks"
weight: 1
description: >
  Set up and run your first Tekton task
---

This tutorial shows you how to 

1. Create a Kubernetes cluster with [minikube](https://minikube.sigs.k8s.io/).
1. Install Tekton pipelines.
1. Create a task.
1. Use `TaskRun` to instantiate and run your task.

## Prerequisites

1.  [Install minikube](https://minikube.sigs.k8s.io/docs/start/). You only have
    to complete the step 1, "Installation".
1.  [Install kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)

## Create your Kubernetes cluster

Create a cluster

```bash
minikube start
```

The process takes a few seconds, you see an output symilar to the following,
depending on the [minikube driver](https://minikube.sigs.k8s.io/docs/drivers/)
that you are using:

<pre>
😄  minikube v1.25.1
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.23.1 on Docker 20.10.12 ...
    ▪ kubelet.housekeeping-interval=5m
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
</pre>

You can check that the cluster was successfully created with `kubectl`:

```bash
kubectl cluster-info
```

The output confirms that Kubernetes is running:

<pre>
Kubernetes control plane is running at https://127.0.0.1:39509
CoreDNS is running at
https://127.0.0.1:39509/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
</pre>

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
Watch the components using their names under the `NAME` column, when all components show `Running` under the `STATUS` column, the installation
is complete.

Hit *Ctrl + C* to stop monitoring.

## Create and run a basic task

A **task**, represented in the API as an object of kind `Task`, defines a
series of **steps** that run sequentially to perform logic that the task
requires. Every task runs as a pod on your Kubernetes cluster, with each step
running in its own container.

1.  To create a task, open your favorite editor and create a file named
    `hello-world.yaml` with the following content:

    ```yaml
    apiVersion: tekton.dev/v1beta1
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

    


1.  Apply the changes your cluster:

    ```bash
    kubectl apply --filename hello-world.yaml
    ```

      The output confirms that the task was completed successfully.

      ```bash
      task.tekton.dev/hello created
      ```

1.  To run this task, you must instantiate it using `TaskRun`. Create another
    file named `hello-world-run.yaml` with the following content:

    ```yaml
    apiVersion: tekton.dev/v1beta1
    kind: TaskRun
    metadata:
      name: hello-task-run
    spec:
      taskRef:
        name: hello
    ```

1.  Apply the changes to your cluster to launch the task:

    ```bash
    kubectl apply --filename hello-world-run.yaml
    ``` 

1.  Verify that everything worked correctly:

    ```bash
    kubectl get taskrun hello-task-run
    ```

    The output of this command shows the status of the task

     <pre>
     NAME                               SUCCEEDED    REASON       STARTTIME   COMPLETIONTIME
     hello-task-run          True         Succeeded    22h         22h
     </pre>

    The value `True` under `SUCCEEDED` confirms that TaskRun completed with no errors.


1.  Take a look at the logs:

    ```
    kubectl logs --selector=tekton.dev/taskRun=hello-task-run
    ```

    The output displays the message:

    ```
    Hello World
    ```

## Cleanup

If you want to continue and create a pipeline, do not delete your cluster and
proceed to the [next tutorial](/docs/getting-started/pipelines/).

To delete the cluster that you created for this quickstart run:

```bash
minikube delete
```

The output confirms that your cluster was deleted:

<pre>
🔥  Deleting "minikube" in docker ...
🔥  Deleting container "minikube" ...
🔥  Removing /home/user/.minikube/machines/minikube ...
💀  Removed all traces of the "minikube" cluster.
</pre>
