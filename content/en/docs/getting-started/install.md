---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 20
menu:
  main:
    weight: 20
---

This is a quick guide to get started with tekton

* [Install Tekton](#install-tekton)

## Install Tekton

To add Teketon to the Kubernetes on version 1.11 or later grant cluster-admin permissions to the current user.

* [Installing Tekton Pipelines](#installing-tekton-pipelines)
* [Installing Tekton Pipelines on OpenShift/MiniShift](#installing-tekton-pipelines-on-openshift-4crc)
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

- Look at the
  [examples](https://github.com/tektoncd/pipeline/tree/master/examples)

### Installing Tekton Pipelines on OpenShift 4/CRC

1. Install Tekton-Pipeline by accessing the console
2. Select `Catalog/Operator > Operator Hub`
3. Search for `OpenShift Pipelines Operator`
4. Click on `Subscribe` 

**Note**: OpenShift Pipelines Operator will automatically begin installation of Tekton 😊

## Versions

The versions of Tekton Pipelines available are:

* [Officially released versions](https://github.com/tektoncd/pipeline/releases), e.g. `v0.6.0`
* [Nightly releases](https://gcr.io/tekton-nightly) are
  published every night to `gcr.io/tekton-nightly`
* `HEAD` - To install the most recent, unreleased code in the repo see
  [the development
  guide](https://github.com/tektoncd/pipeline/blob/master/DEVELOPMENT.md)
  
---

Except as otherwise noted, the content of this page is licensed under the
[Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/),
and code samples are licensed under the
[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
