<!--
---
title: "Local installation"
linkTitle: "Local installation"
weight: 2
description: >
  Install Tekton components on your local computer.
---
-->

If you are going to test Tekton locally on your computer, two possible
alternatives for that are **minikube** and **kind**. The [Getting
Started](/docs/getting-started/) guides show you how to run several simple
examples using minikube.

{{% tabs %}}

{{% tab "Minikube" %}}

1.  [Install minikube][minikube] on your computer.

1.  [Install kubectl][kubectl] on your computer.

1.  Create a cluster.

    ```bash
    minikube start
    ```

1.  Verify that the cluster is working correctly.

    ```bash
    kubectl cluster-info
    ```

The output confirms that Kubernetes is up and running:

```
Kubernetes control plane is running at https://127.0.0.1:39509
CoreDNS is running at
https://127.0.0.1:39509/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

[minikube]: https://minikube.sigs.k8s.io/docs/start/
[kubectl]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation

{{% /tab %}}

{{% tab "Kind" %}}

1.  [Install kind][kind] on your
    computer.

1.  [Install kubectl][kubectl]
    on your computer.

1.  Create a cluster.

    ```bash
    kind create cluster
    ```

1.  Verify that the cluster is working correctly.

    ```bash
    kubectl cluster-info
    ```

The output confirms that Kubernetes is up and running:

```
Kubernetes control plane is running at https://127.0.0.1:39509
CoreDNS is running at
https://127.0.0.1:39509/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
[kind]: https://kind.sigs.k8s.io/docs/user/quick-start/
[kubectl]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation

{{% /tab %}}

{{% /tabs %}}

After you have a local cluster up and running, follow the instructions in the
corresponding installation guide for each component.

## Further reading

-   [Getting started with Tasks][tasks-intro]

Other resources

-   [Set up a local Development environment with Minikube or Kind][local-setup]
-   [Convenience scripts to run Kind][kind-setup]

[kind-setup]: https://github.com/tektoncd/plumbing/tree/main/hack
[local-setup]: https://github.com/tektoncd/pipeline/blob/main/docs/developers/local-setup.md
[tasks-intro]: /docs/getting-started/tasks/
