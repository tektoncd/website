<!--
---
title: "Install Tekton Pipelines"
linkTitle: "Tekton Pipelines"
weight: 2
description: >
  Install Tekton Pipelines on you cluster
---
-->

## Prerequisites

-   [Kubernetes] cluster version 1.21 or later.
-   Admin privileges to the user running the installation.
-   [Kubectl].

## Installation

To install Tekton Pipelines on your cluster.
{{% tabs %}}

{{% tab "Kubernetes" %}}

1.  Depending on which version of Tekton Pipelines you want to install, run one
    of the following commands:

    -   **Latest official release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
        ```

    -   **Nightly release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases-nightly/pipeline/latest/release.yaml
        ```

    -   **Specific Release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/pipeline/previous/VERSION_NUMBER/release.yaml
        ```

        Replace `VERSION_NUMBER` with the numbered version you want to install.
        For example, `v0.31.4`.

    -   **Untagged Release**

        If your container runtime does not support `image-reference:tag@digest` (for
        example, `cri-o` used in OpenShift 4.x):

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/pipeline/latest/release.notags.yaml
        ```

1.  To monitor the installation, run:

    ```bash
    kubectl get pods --namespace tekton-pipelines --watch
    ```

    When all components show `Running` under the `STATUS` column the installation is
    complete. Hit *Ctrl + C* to stop monitoring.

{{% alert title="Note" color="info" %}}
*Some cloud providers, such as GKE, may require that you open the port 8443 in
the firewall rules so that the Tekton Pipelines webhook is reachable.*
{{% /alert %}}

{{% /tab %}}

{{% tab "OpenShift" %}}

1.  Log on as a user with the  `cluster-admin` privileges. The following example
    uses the default `system:admin` user:

    ```bash
    oc login -u system:admin
    ```

1.  Set up the namespace (project) and configure the service account:

    ```bash
    oc new-project tekton-pipelines
    oc adm policy add-scc-to-user anyuid -z tekton-pipelines-controller
    oc adm policy add-scc-to-user anyuid -z tekton-pipelines-webhook
    ```
1.  Install Tekton pipelines

    ```bash
    oc apply --filename \
    https://storage.googleapis.com/tekton-releases/pipeline/latest/release.notags.yaml
    ```

1.  To monitor the installation, run:

    ```bash
    kubectl get pods --namespace tekton-pipelines --watch
    ```

    When all components show `Running` under the `STATUS` column the installation is
    complete.

See the [OpenShift CLI][openshift] documentation for more information about the
`oc` command.

[openshift]: https://docs.openshift.com/container-platform/latest/welcome/index.html
{{% /tab %}}

{{% /tabs %}}

## Further reading

See the [Pipelines repository documentation](/docs/pipelines/install/) for more
installation and configuration options.

[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[kubectl]: https://kubernetes.io/docs/tasks/tools/#kubectl
