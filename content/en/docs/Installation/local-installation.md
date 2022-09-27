<!--
---
title: "Local Kubernetes cluster"
linkTitle: "Local cluster"
weight: 1
description: >
  Set up a Kubernetes cluster on your computer to test Tekton.
---
-->

There are several tools to run a local Kubernetes cluster on your computer. The
Tekton documentation often includes instructions for either **minikube** or
**kind**. 

See the corresponding [minikube][] and [kind][] documentation to learn how to
install and set up a cluster on your computer. 

You can find some additional resources on the Tekton repositories:

- Instructions to run both tools with a local registry are available on the
  [Pipelines repository][local-setup].

- You can find some convenience scripts to run Tekton components with kind on
  the [plumbing repository][kind-setup].

## Further reading

-   [Getting started with Tasks][tasks-intro]

[minikube]: https://minikube.sigs.k8s.io/docs/start/
[kind]: https://kind.sigs.k8s.io/docs/user/quick-start/
[kind-setup]: https://github.com/tektoncd/plumbing/tree/main/hack
[local-setup]: https://github.com/tektoncd/pipeline/blob/main/docs/developers/local-setup.md
[tasks-intro]: /docs/getting-started/tasks/

