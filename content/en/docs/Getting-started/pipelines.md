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

This guide uses a local cluster with [minikube][].

## Prerequisites

1.  Complete the [Getting started with Tasks](/docs/getting-started/tasks/)
    tutorial. *Do not clean up your resources*, skip the last section.

1.  [Install `tkn`, the Tekton CLI](/docs/cli/).

## Create and run a second Task

You already have a "Hello World!" Task. To create a second "Goodbye!"
Task:

1.  Create a new file named  `goodbye-world.yaml` and add the following
    content:

    ```yaml
    apiVersion: tekton.dev/v1beta1
    kind: Task
    metadata:
      name: goodbye
    spec:
      params:
      - name: username
        type: string
      steps:
        - name: goodbye
          image: ubuntu
          script: |
            #!/bin/bash
            echo "Goodbye $(params.username)!"
    ```

    This Task takes one parameter, `username`. Whenever this Task is used a
    value for that parameter must be passed to the Task.

1.  Apply the Task file:

    ```bash
    kubectl apply --filename goodbye-world.yaml
    ```

When a Task is part of a Pipeline, Tekton creates a `TaskRun` object for every
task in the Pipeline.

## Create and run a Pipeline

A **Pipeline** defines an ordered series of Tasks arranged in a specific
execution order as part of the CI/CD workflow.

In this section you are going to create your first Pipeline, that will include
both the "Hello World!" and "Goodbye!" Tasks.

1.  Create a new file named  `hello-goodbye-pipeline.yaml` and add the following
    content:

    ```yaml
    apiVersion: tekton.dev/v1beta1
    kind: Pipeline
    metadata:
      name: hello-goodbye
    spec:
      params:
      - name: username
        type: string
      tasks:
        - name: hello
          taskRef:
            name: hello
        - name: goodbye
          runAfter:
            - hello
          taskRef:
            name: goodbye
          params:
          - name: username
            value: $(params.username)
    ```

    The Pipeline defines the parameter `username`, which is then passed to the
    `goodbye` Task.

1.  Apply the Pipeline configuration to your cluster:

    ```bash
    kubectl apply --filename hello-goodbye-pipeline.yaml
    ```

1.  A **PipelineRun**, represented in the API as an object of kind
    `PipelineRun`, sets the value for the parameters and executes a Pipeline. To
    create  PipelineRun, create a new file named
    `hello-goodbye-pipeline-run.yaml` with the following:

    ```yaml
    apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      name: hello-goodbye-run
    spec:
      pipelineRef:
        name: hello-goodbye
      params:
      - name: username
        value: "Tekton"
    ```
    
    This sets the actual value for the `username` parameter: `"Tekton"`.

1.  Start the Pipeline by applying the `PipelineRun` configuration to your
    cluster:

    ```bash
    kubectl apply --filename hello-goodbye-pipeline-run.yaml
    ```

    You see the following output:

    ```
    pipelinerun.tekton.dev/hello-goodbye-run created
    ```

    Tekton now starts running the Pipeline.

1.  To see the logs of the `PipelineRun`, use the following command:

    ```bash
    tkn pipelinerun logs hello-goodbye-run -f -n default
    ```

    The output shows both Tasks completed successfully:

    <pre>
    [hello : echo] Hello World!

    [goodbye : goodbye] Goodbye Tekton!
    </pre>

## Cleanup

To learn about Tekton Triggers, skip this section and proceed to the
[next tutorial][triggers-qs].

To delete the cluster that you created for this guide run:

```bash
minikube delete
```

The output confirms that the cluster was deleted:

<pre>
🔥  Deleting "minikube" in docker ...
🔥  Deleting container "minikube" ...
🔥  Removing /home/user/.minikube/machines/minikube ...
💀  Removed all traces of the "minikube" cluster.
</pre>

## Further reading

We recommend that you complete [Getting started with Triggers][triggers-qs].

For more complex examples check:

- [Clone a git repository with Tekton][git-howto].
- [Build and push a container image with Tekton][kaniko-howto].

[minikube]: https://minikube.sigs.k8s.io/docs/start/
[kind]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[kubectl]: https://github.com/tektoncd/pipeline/blob/main/docs/developers/local-setup.md
[git-howto]: /docs/how-to-guides/clone-repository/
[kaniko-howto]: /docs/how-to-guides/kaniko-build-push/
[triggers-qs]: /docs/getting-started/triggers/
