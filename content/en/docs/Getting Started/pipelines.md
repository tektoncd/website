<!--
---
title: "Getting Started with Pipelines"
linkTitle: "Getting Started with Pipelines"
weight: 2
description: >
  Create and run your first Tekton Pipeline
---
-->

This tutorial shows you how to:

+   Create two Tasks.
+   Create a Pipeline containing your Tasks.
+   Use `PipelineRun` to instantiate and run the Pipeline containing your Tasks.

For this tutorial we are going to use [minikube][minikube] to run the commands
locally.

## Prerequisites

1.  Complete the [Getting started with Tasks](/docs/getting-started/tasks/)
    tutorial. *Do not clean up your resources*, skip the last section.

1.  [Install `tkn`, the Tekton CLI](/docs/cli/).

## Create and run a second Task

You already have a *Hello World!* Task. To create a second *Goodbye World!*
Task:

1.  Create a new file named  `goodbye-world.yaml` and add the following
    content:

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

1.  Apply your Task file:

    ```bash
    kubectl apply --filename goodbye-world.yaml
    ```

When a Task is part of a Pipeline you don't have to instantiate it, the Pipeline
is going to take care of that.

## Create and run a Pipeline

A **[Pipeline](/docs/pipelines/pipelines/)** defines an ordered series of Tasks
arranged in a specific execution order as part of your CI/CD workflow.

In this section you are going to create your first Pipeline, that will include
both the *Hello World!* and *Goodbye World!* Tasks.

1.  Create a new file named  `hello-goodbye-pipeline.yaml` and add the following
    content:

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

1.  Apply your Pipeline configuration to your cluster:

    ```bash
    kubectl apply --filename hello-goodbye-pipeline.yaml
    ```

1.  Instantiate your Pipeline with a `PipelineRun` object. Create a new file
    named `hello-goodbye-pipeline-run.yaml` with the following content:

    ```yaml
    apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      name: hello-goodbye-run
    spec:
      pipelineRef:
        name: hello-goodbye
    ```

1.  Start your Pipeline by applying the `PipelineRun` configuration to your
    cluster:

    ```bash
    kubectl apply --filename hello-goodbye-pipeline-run.yaml
    ```

    You see the following output:

    ```bash
    pipelinerun.tekton.dev/hello-goodbye-run created
    ```

    Tekton now starts running your Pipeline.

1.  To see the logs of the `PipelineRun`, use the following command:

    ```bash
    tkn pipelinerun logs hello-goodbye-run -f -n default
    ```

    The output shows both Tasks completed successfully:

    <pre>
    [hello : hello] Hello World!

    [goodbye : goodbye] Goodbye World!
    </pre>

## Cleanup

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

## Further reading

- [Tasks](/docs/pipelines/tasks)
- [Pipelines](/docs/pipelines/pipelines)

Other useful resources

- [Convenience scripts to run Kind][kind-setup]
- [Instructions to setup Minikube and Docker][local-setup]

[minikube]: https://minikube.sigs.k8s.io/docs/start/
[kind]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[kind-setup]: https://github.com/tektoncd/plumbing/tree/main/hack
[kubectl]: https://github.com/tektoncd/pipeline/blob/main/docs/developers/local-setup.md
[local-setup]: https://github.com/tektoncd/pipeline/blob/main/docs/developers/local-setup.md

