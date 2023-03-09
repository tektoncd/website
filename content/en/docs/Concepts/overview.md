<!--
---
title: "Overview"
linkTitle: "Overview"
weight: 1
description: >

  Components, benefits and caveats, common usage.
---
-->



## What is Tekton?

Tekton is a cloud-native solution for building CI/CD pipelines. It consists of Tekton Pipelines, which provides
the building blocks, and of supporting components, such as Tekton CLI and Tekton Catalog, that make Tekton a complete
ecosystem. Tekton is part of the [CD Foundation](https://cd.foundation/), a
[Linux Foundation](https://www.linuxfoundation.org/projects/) project.

Tekton installs and runs as an extension on a Kubernetes cluster and comprises a set of Kubernetes Custom Resources
that define the building blocks you can create and reuse for your pipelines. Once installed, Tekton Pipelines becomes 
available via the Kubernetes CLI (kubectl) and via API calls, just like pods and other resources. 

## Who uses Tekton?

Tekton users typically fall into the following categories:

- **Platform engineers** who build CI/CD systems for the developers in their organization. 
- **Developers** who use those CI/CD systems to do their work. 

## What are the benefits of Tekton?

Tekton provides the following benefits to builders and users of CI/CD systems:

- **Customizable.** Tekton entities are fully customizable, allowing for a high degree of flexibility. Platform engineers
  can define a highly detailed catalog of building blocks for developers to use in a wide variety of scenarios.
- **Reusable.** Tekton entities are fully portable, so once defined, anyone within the organization can use a given
  pipeline and reuse its building blocks. This allows developers to quickly build complex pipelines without "reinventing
  the wheel."
- **Expandable.** Tekton Catalog is a community-driven repository of Tekton building blocks. You can quickly create new and
  expand existing pipelines using pre-made components from the Tekton Catalog.
- **Standardized.** Tekton installs and runs as an extension on your Kubernetes cluster and uses the well-established
  Kubernetes resource model. Tekton workloads execute inside Kubernetes containers.
- **Scalable.** To increase your workload capacity, you can simply add nodes to your cluster. Tekton scales with your cluster
  without the need to redefine your resource allocations or any other modifications to your pipelines.

## What are the components of Tekton?

Tekton consists of the following components:

- **[Tekton Pipelines][pipelines]** is the foundation of Tekton. It defines a
  set of Kubernetes [Custom Resources][k-resources] that act as building blocks
  from which you can assemble CI/CD pipelines.

- **[Tekton Triggers][triggers]** allows you to instantiate pipelines based on events.
  For example, you can trigger the instantiation and execution of a pipeline
  every time a PR is merged against a GitHub repository. You can also build a user
  interface that launches specific Tekton triggers.

- **[Tekton CLI][cli]** provides a command-line interface called `tkn`, built on top
  of the Kubernetes CLI, that allows you to interact with Tekton.

- **[Tekton Dashboard][dashboard]** is a Web-based graphical interface for
  Tekton Pipelines that displays information about the execution of your
  pipelines. It is currently a work-in-progress.

- **[Tekton Catalog][catalog]** is a repository of high-quality, community-contributed
  Tekton building blocks - `Tasks`, `Pipelines`, and so on - that are ready for
  use in your own pipelines.

- **[Tekton Hub][hub]** is a Web-based graphical interface for accessing the Tekton Catalog.

- **[Tekton Operator][operator]** is a Kubernetes [Operator
  pattern](https://operatorhub.io/what-is-an-operator) that allows you to
  install, update, and remove Tekton projects on your Kubernetes cluster.

- **[Tekton Chain][chains]** provides tools to generate, store, and sign
  provenance for artifacts built with Tekton Pipelines.

[pipelines]: https://github.com/tektoncd/pipeline/blob/main/docs/README.md
[triggers]: https://github.com/tektoncd/triggers/blob/main/README.md
[cli]: https://github.com/tektoncd/cli/blob/main/README.md
[dashboard]: https://github.com/tektoncd/dashboard/blob/main/docs/README.md
[catalog]: https://github.com/tektoncd/catalog/blob/v1beta1/README.md
[hub]: https://github.com/tektoncd/hub/blob/main/README.md
[operator]: https://github.com/tektoncd/operator/blob/main/README.md
[chains]: https://github.com/tektoncd/chains/blob/main/README.md
[k-resources]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/

## How do I work with Tekton?

To install Tekton, you need a Kubernetes cluster running a
[version of Kubernetes specified for the current Tekton release](https://github.com/tektoncd/pipeline/#want-to-start-using-pipelines).
Once installed, you can interact with Tekton using one of the following:

- **[The tkn CLI](https://github.com/tektoncd/cli/blob/main/README.md)**, also known as the Tekton CLI, is the preferred command-line method
  for interacting with Tekton. `tkn` provides a quick and streamlined experience, including high-level commands and color coding. To use it,
  you only need to be familiar with Tekton.
- **[The kubectl CLI](https://kubernetes.io/docs/reference/kubectl/overview/)**, also known as the Kubernetes CLI, provides substantially more
  granularity for controlling Tekton at the expense of higher complexity. Interacting with Tekton via kubectl is typically reserved for debugging
  your pipelines and troubleshooting your builds.
- **[The Tekton APIs](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/)**, currently
  available for [Pipelines](https://pkg.go.dev/github.com/tektoncd/pipeline/pkg/apis/pipeline/v1beta1?tab=doc) and
  [Triggers](https://pkg.go.dev/github.com/tektoncd/triggers@v0.5.0/pkg/apis/triggers/v1alpha1?tab=doc), allow you to programmatically interact
  with Tekton components. This is typically reserved for highly customized CI/CD systems. In most scenarios, `tkn` and `kubectl` are the preferred 
  methods of controlling Tekton.

We also recommend having the following items configured on your Kubernetes cluster:

- Persistent volume claims for specifying inputs and outputs.
- Permissions appropriate to your environment and business needs.
- Storage for building and pushing images (if applicable).

## What can I do with Tekton?

Tekton introduces the concept of `Tasks`, which specify the workloads you want to run:

- [`Task`](https://github.com/tektoncd/pipeline/blob/main/docs/tasks.md) - defines a series of ordered `Steps`, and each `Step` invokes a specific
  build tool on a specific set of inputs and produces a specific set of outputs, which can be used as inputs in the next `Step`.

- [`Pipeline`](https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md) - defines a series of ordered `Tasks`, and just like `Steps` in a
  `Task`, a `Task` in a `Pipeline` can use the output of a previously executed `Task` as its input.

- [`TaskRun`](https://github.com/tektoncd/pipeline/blob/main/docs/taskruns.md) - instantiates a specific `Task` to execute on a particular set of
  inputs and produce a particular set of outputs. In other words, the `Task` tells Tekton what to do, and a `TaskRun` tells Tekton what to do it **on**,
  as well as any additional details on how to exactly do it, such as build flags.

- [`PipelineRun`](https://github.com/tektoncd/pipeline/blob/main/docs/pipelineruns.md) - instantiates a specific `Pipeline` to execute on a particular
  set of inputs and produce a particular set of outputs to particular destinations.

Each `Task` executes in its own Kubernetes Pod. Thus, by default, `Tasks` within a `Pipeline` do not share data. To share data among `Tasks`,
you must explicitly configure each `Task` to make its outputs available to the next `Task` and to ingest the outputs of a previously executed
`Task` as its inputs, whichever is applicable. 

### When to use which?

- `Task` - useful for simpler workloads such as running a test, a lint, or building a Kaniko cache. A single `Task` executes in a single
  Kubernetes Pod, uses a single disk, and generally keeps things simple.
- `Pipeline` - useful for complex workloads, such as static analysis, as well as testing, building, and deploying complex projects.

### I want to learn more!

-  See [the Tekton concept model](/docs/concepts/concept-model) to learn more
   about the basics of how Tekton tasks and pipelines interact.

-  Run your first pipeline following the [Getting
   Started](/docs/getting-started/) guide.

