---
title: "Getting Started with Pipelines"
linkTitle: "Getting Started with Pipelines"
weight: 1
description: >
  Prerequisites, Installation, and Basic Usage
---

## Prerequisites

* Completed the [Getting Started example](/docs/getting-started/).

## Extending your first CI/CD Workflow with a second Task and a Pipeline

As you learned previously, with Tekton, each operation in your CI/CD workflow becomes a `Step`,
which is executed with a container image you specify. `Steps` are then
organized in `Tasks`, which run as a [Kubernetes pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)
in your cluster. You can further organize `Tasks` into `Pipelines`, which 
can control the order of execution of several `Tasks`. 

To create a second `Task`, create a Kubernetes object using the Tekton API with
the kind `Task`. The following YAML file specifies a `Task` with one simple
`Step`, which prints a `Goodbye World!` message using
[the official Ubuntu image](https://hub.docker.com/_/ubuntu/):

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: goodbye
spec:
  steps:
    - name: goodbye
      image: ubuntu
      script: |
        #!/bin/bash
        echo "Goodbye World!"
```

Write the YAML above to a file named `task-goodbye.yaml`, and apply it to your Kubernetes cluster:

```bash
kubectl apply -f task-goodbye.yaml
```

To run this task with Tekton, you need to create a `TaskRun`, which is
another Kubernetes object used to specify run time information for a `Task`. 

To view this `TaskRun` object you can run the following Tekton CLI (`tkn`) command:

```shell
tkn task start goodbye --dry-run
```

After running the command above, the following `TaskRun` definition should be shown:

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  generateName: goodbye-run-
spec:
  taskRef:
    name: goodbye
```

To use the `TaskRun` above to start the `echo` `Task`, you can either use 
`tkn` or `kubectl`.

Start with `tkn`:

```shell
tkn task start goodbye
```

Start with `kubectl`:

```shell
# use tkn's --dry-run option to save the TaskRun to a file
tkn task start goodbye --dry-run > taskRun-goodbye.yaml
# create the TaskRun
kubectl create -f taskRun-goodbye.yaml
```

Tekton will now start running your `Task`. To see the logs of the `TaskRun`, run 
the following `tkn` command:

```shell
tkn taskrun logs --last -f 
```

It may take a few moments before your `Task` completes. When it executes, it should 
show the following output:

```
[goodbye] Goodbye World!
```

To create a `Pipeline`, create a Kubernetes object using the Tekton API with
the kind `Pipeline`. The following YAML file specifies a `Pipeline`.

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: hello-goodbye
spec:
  tasks:
  - name: hello
    taskRef:
      name: hello
  - name: goodbye
    runAfter:
     - hello
    taskRef:
      name: goodbye
```

Write the YAML above to a file named `pipeline-hello-goodbye.yaml`, and apply it to your Kubernetes cluster:

```bash
kubectl apply -f pipeline-hello-goodbye.yaml
```

To run this pipeline with Tekton, you need to create a `pipelineRun`, which is
another Kubernetes object used to specify run time information for a `Pipeline`. 

To view this `pipelineRun` object you can run the following Tekton CLI (`tkn`) command:

```shell
tkn pipeline start hello-goodbye --dry-run
```

After running the command above, the following `TaskRun` definition should be shown:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: hello-goodbye-run-
spec:
  pipelineRef:
    name: hello-goodbye
```

To use the `pipelineRun` above to start the `echo` `Pipeline`, you can either use 
`tkn` or `kubectl`.

Start with `tkn`:

```shell
tkn pipeline start hello-goodbye
```

Start with `kubectl`:

```shell
# use tkn's --dry-run option to save the pipelineRun to a file
tkn pipeline start hello-goodbye --dry-run > pipelineRun-hello-goodbye.yaml
# create the pipelineRun
kubectl create -f pipelineRun-hello-goodbye.yaml
```

Tekton will now start running your `Pipeline`. To see the logs of the `pipelineRun`, run 
the following `tkn` command:

```shell
tkn pipelinerun logs --last -f 
```

It may take a few moments before your `Pipeline` completes. When it executes, it should 
show the following output:

```
[hello : hello] Hello World!

[goodbye : goodbye] Goodbye World!
```



## What's next

Now you have the core component of Tekton, Tekton Pipelines, installed on
your Kubernetes or OpenShift cluster with the Tekton CLI installed on your local
machine. If you would like to install more components, see the list below:

* [Tekton Triggers](/docs/triggers)
* [Tekton Dashboard](/docs/dashboard)

Learn more about Tekton in [Concepts](/docs/concepts/).
