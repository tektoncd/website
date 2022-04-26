<!--
---
title: "Install Tekton Triggers"
linkTitle: "Tekton Triggers"
weight: 3
description: >
  Install Tekton Triggers on you cluster
---
-->

## Prerequisites

-   [Kubernetes] cluster version 1.18 or later.
-   Admin privileges to the user running the installation.
-   [Kubectl].
-   [Tekton Pipelines](/docs/installation/pipelines/)

## Installation

1.  Log on to your Kubernetes cluster with the same user account that installed
    Tekton Pipelines.

1.  Depending on which version of Tekton Triggers you want to install, run one
    of the following commands:

    -   **Latest official release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml
        ```

    -   **Nightly release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases-nightly/triggers/latest/release.yaml
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases-nightly/triggers/latest/interceptors.yaml
        ```

    -   **Specific Release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/triggers/previous/VERSION_NUMBER/release.yaml
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/triggers/previous/VERSION_NUMBER/interceptors.yaml
        ```

        Replace `VERSION_NUMBER` with the numbered version you want to install.
        For example, `v0.19.1`.

    -   **Untagged Release**

        If your container runtime does not support `image-reference:tag@digest` (for
        example, `cri-o` used in OpenShift 4.x):

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/triggers/latest/release.notags.yaml
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.notags.yaml
        ```

1.  To monitor the installation, run:

    ```bash
    kubectl get pods --namespace tekton-pipelines --watch
    ```

    When all components show `Running` under the `STATUS` column the installation is
    complete. Hit *Ctrl + C* to stop monitoring.

## Further reading

See the [Triggers reference documentation][triggers] to learn more about usage
and configuration options.

[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[kubectl]: https://kubernetes.io/docs/tasks/tools/#kubectl
[triggers]: /docs/triggers/
