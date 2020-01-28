---
title: "Installing Tekton Pipelines"
linkTitle: "Install"
weight: 20
menu:
  main:
    weight: 20
---

To add Teketon to the Kubernetes Cluster on version 1.11 or later grant cluster-admin permissions to the current user.

* [Installing Tekton Pipelines](#installing-tekton-pipelines)
* [Installing Tekton Pipelines on OpenShift/MiniShift](#installing-tekton-pipelines-on-openshiftminishift)
* [Versions](#versions)

### Installing Tekton Pipelines

To add the Tekton Pipelines component to an existing cluster:

1. Run the
   [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
   command to install [Tekton Pipelines](https://github.com/tektoncd/pipeline)
   and its dependencies:

   ```bash
   kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
   ```

1. Run the
   [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)
   command to monitor the Tekton Pipelines components until all of the
   components show a `STATUS` of `Running`:

   ```bash
   kubectl get pods --namespace tekton-pipelines
   ```


You are now ready to create and run Tekton Pipelines 🙌

- See [Tekton Pipeline tutorial](./tutorial.md) to get started.
- Look at the
  [examples](https://github.com/tektoncd/pipeline/tree/master/examples)

### Installing Tekton-Pipeline on OpenShift 4/CRC

1. Install Tekton-Pipeline by accessing the console
2. Select `Catalog/Operator > Operator Hub`
3. Search for `OpenShift Pipelines Operator`
4. Click on `Subscribe` 

**Note**: Tekton-Pipeline will automatically begin installation 😊

## Versions

The versions of Tekton Pipelines available are:

* [Officially released versions](https://github.com/tektoncd/pipeline/releases), e.g. `v0.6.0`
* [Nightly releases](../tekton/README.md#nightly-releases) are
  published every night to `gcr.io/tekton-nightly`
* `HEAD` - To install the most recent, unreleased code in the repo see
  [the development
  guide](https://github.com/tektoncd/pipeline/blob/master/DEVELOPMENT.md)

## Custom Releases

The [release Task](./../tekton/README.md) can be used for creating a custom
release of Tekton Pipelines. This can be useful for advanced users that need to
configure the container images built and used by the Pipelines components.

---

Except as otherwise noted, the content of this page is licensed under the
[Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/),
and code samples are licensed under the
[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).