<!--
---
title: "Concept model"
linkTitle: "Concept model"
weight: 2
description: >

  Basic Tekton components and data model
---
-->

## Steps, Tasks, and Pipelines

A **step** is an operation in a CI/CD workflow, such as running some unit tests
for a Python web app, or the compilation of a Java program. Tekton performs
each step with a container image you provide. For example, you may use the
[official Go image](https://hub.docker.com/_/golang) to compile a Go program
in the same manner as you would on your local workstation (`go build`).

A **task** is a collection of **steps** in order. Tekton runs a task in
the form of a [Kubernetes pod](https://kubernetes.io/docs/concepts/workloads/pods/),
where each step becomes a running container in the pod. This design allows you
to set up a shared environment for a number of related steps; for example,
you may mount a [Kubernetes volume](https://kubernetes.io/docs/concepts/storage/volumes/)
in a task, which will be accessible inside each step of the task.

A **pipeline** is a collection of **tasks** in order. Tekton collects all the
tasks, connects them in a directed acyclic graph (DAG), and executes the graph
in sequence. In other words, it creates a number of Kubernetes pods and
ensures that each pod completes running successfully as desired. Tekton grants
developers full control of the process: one may set up a fan-in/fan-out
scenario of task completion, ask Tekton to retry automatically should
a flaky test exists, or specify a condition that a task must meet before
proceeding.

**Tasks** and **pipelines** are specified as [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
in a Kubernetes cluster.

![Tasks and Pipelines](/docs/concepts/concept-tasks-pipelines.png)

## TaskRuns and PipelineRuns

A **pipelineRun**, as its name implies, is a specific execution of a **pipeline**.
For example, you may ask Tekton to run your CI/CD workflow twice a day, and
each execution will become a **pipelineRun** resource trackable in your
Kubernetes cluster. You can view the status of your CI/CD workflow, including
the specifics of each task execution with **pipelineRuns**.

Similarly, a **taskRun** is a specific execution of a **task**. **TaskRuns**
are also available when you choose to run a task outside a pipeline, with
which you may view the specifics of each step execution in a task.

**TaskRuns** and **pipelineRuns** connect **resources** with **tasks** and
**pipelines**. A run must include the actual addresses of resources, such as
the URLs of repositories, its task or pipeline needs. This design allows
developers to reuse tasks and pipelines for different inputs and outputs.

You may create **taskRuns** or **pipelineRuns** manually, which triggers
Tekton to run a task or a pipeline immediately. Alternately, one may ask a
Tekton component, such as Tekton Triggers, to create a run automatically on
demand; for example, you may want to run a pipeline every time a new pull
request is checked into your git repository.

![Runs](/docs/concepts/concept-runs.png)

**TaskRuns** and **pipelineRuns** are specified as [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
in a Kubernetes cluster.

## How Tekton works

Loosely speaking, at its core, Tekton Pipelines functions by wrapping each
of your steps. More specifically, Tekton Pipelines injects an `entrypoint`
binary in step containers, which executes the command you specify when
the system is ready.

Tekton Pipelines tracks the state of your pipeline using
[Kubernetes Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/).
These annotations are projected inside each step container in the form
of files with the
[Kubernetes Downward API](https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/#the-downward-api).
The `entrypoint` binary watches the projected files closely, and will only
start the provided command if a specific annotation appears as files. For
example, when you ask Tekton to run two steps consecutively in a task,
the `entrypoint` binary injected into the second step container will
wait idly until the annotations report that the first step container
has successfully completed.

In addition, Tekton Pipelines schedules some containers to run automatically
before and after your step containers, so as to support specific built-in
features, such as the retrieval of input resources and the uploading of
outputs to blob storage solutions. You can track their running statuses as
well via **taskRuns** and **pipelineRuns**. The system also performs a number
of other operations to set up the environment before running the step
containers; for more information, see [Tasks and Pipelines](/docs/pipelines).

## What's next

Learn more about Tekton Pipelines in [Tasks and Pipelines](/docs/pipelines).
