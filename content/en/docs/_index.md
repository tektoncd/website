
---
title: "Welcome to Tekton"
linkTitle: "Documentation"
weight: 20
menu:
  main:
    weight: 20
---

Tekton is an open-source cloud native CI/CD (Continuous Integration and
Delivery/Deployment) solution. It allows developers to build, test, and
deploy across destinations using a Kubernetes cluster of their own.

The Tekton project consists of the following components:


- **[Tekton Pipelines](https://github.com/tektoncd/pipeline/blob/main/docs/README.md)** provides basic building blocks (tasks and pipelines) of a CI/CD workflow

- **[Tekton Triggers](https://github.com/tektoncd/triggers/blob/main/README.md)** allows you to instantiate pipelines based on events.

- **[Tekton CLI](https://github.com/tektoncd/cli/blob/main/README.md)** provides a command-line interface called `tkn`, built on top
  of the Kubernetes CLI, that allows you to interact with Tekton.

- **[Tekton Dashboard](https://github.com/tektoncd/dashboard/blob/main/README.md)** is a Web-based graphical interface for Tekton
  Pipelines that displays information about the execution of your pipelines. It is currently a work-in-progress.

- **[Tekton Catalog](https://github.com/tektoncd/catalog/blob/main/README.md)** is a repository of high-quality, community-contributed
  Tekton building blocks - `Tasks`, `Pipelines`, and so on - that are ready for use in your own pipelines.

- **[Tekton Hub](https://github.com/tektoncd/hub/blob/main/README.md)** is a Web-based graphical interface for accessing the Tekton Catalog.

- **[Tekton Operator](https://github.com/tektoncd/operator/blob/main/README.md)** is a Kubernetes [Operator pattern](https://operatorhub.io/what-is-an-operator)
  that allows you to install, update, and remove Tekton projects on your Kubernetes cluster.

Tekton Pipelines provide k8s-style resources for declaring CI/CD-style pipelines.  

![Pipeline](/docs/concepts/concept-tasks-pipelines.png)


{{% alert title="Note" color="success" %}}

Tekton provides a number of interactive tutorials at [tekton.dev/try](/try)
for developers to get hands-on experience with the project.

{{% /alert %}}
