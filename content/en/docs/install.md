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


## Installing Tekton Pipelines

To add the Tekton Pipelines component to an existing cluster:

1. Run the
   [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
   command to install [Tekton Pipelines](https://github.com/tektoncd/pipeline)
   and its dependencies:

   ```bash
   kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
   ```

   _(Previous versions will be available at `previous/$VERSION_NUMBER`, e.g.
   https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.2.0/release.yaml.)_

1. Run the
   [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)
   command to monitor the Tekton Pipelines components until all of the
   components show a `STATUS` of `Running`:

   ```bash
   kubectl get pods --namespace tekton-pipelines
   ```

   Tip: Instead of running the `kubectl get` command multiple times, you can
   append the `--watch` flag to view the component's status updates in real
   time. Use CTRL + C to exit watch mode.

You are now ready to create and run Tekton Pipelines:

- See [Tekton Pipeline tutorial](./tutorial.md) to get started.
- Look at the
  [examples](https://github.com/tektoncd/pipeline/tree/master/examples)

### Installing Tekton Pipelines on OpenShift/MiniShift

The `tekton-pipelines-controller` service account needs the `anyuid` security
context constraint in order to run the webhook pod.

_See
[Security Context Constraints](https://docs.openshift.com/container-platform/3.11/admin_guide/manage_scc.html)
for more information_

1. First, login as a user with `cluster-admin` privileges. The following example
   uses the default `system:admin` user (`admin:admin` for MiniShift):

   ```bash
   # For MiniShift: oc login -u admin:admin
   oc login -u system:admin
   ```

1. Run the following commands to set up the project/namespace, and to install
   Tekton Pipelines:

   ```bash
   oc new-project tekton-pipelines
   oc adm policy add-scc-to-user anyuid -z tekton-pipelines-controller
   oc apply --filename https://storage.googleapis.com/tekton-releases/latest/release.yaml
   ```

   _See
   [here](https://docs.openshift.com/container-platform/3.11/cli_reference/get_started_cli.html)
   for an overview of the `oc` command-line tool for OpenShift._

1. Run the `oc get` command to monitor the Tekton Pipelines components until all
   of the components show a `STATUS` of `Running`:

   ```bash
   oc get pods --namespace tekton-pipelines --watch
   ```
   
## Versions

The versions of Tekton Pipelines available are:

* [Officially released versions](https://github.com/tektoncd/pipeline/releases), e.g. `v0.6.0`
* [Nightly releases](../tekton/README.md#nightly-releases) are
  published every night to `gcr.io/tekton-nightly`
* `HEAD` - To install the most recent, unreleased code in the repo see
  [the development
  guide](https://github.com/tektoncd/pipeline/blob/master/DEVELOPMENT.md)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-defaults
data:
  default-service-account: "tekton"
  default-timeout-minutes: "20"
  default-pod-template: |
    annotations:
      cluster-autoscaler.kubernetes.io/safe-to-evict: 'false'
```

*NOTE:* The `_example` key in the provided [config-defaults.yaml](./../config/config-defaults.yaml)
file contains the keys that can be overriden and their default values.

## Custom Releases

The [release Task](./../tekton/README.md) can be used for creating a custom
release of Tekton Pipelines. This can be useful for advanced users that need to
configure the container images built and used by the Pipelines components.

---

Except as otherwise noted, the content of this page is licensed under the
[Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/),
and code samples are licensed under the
[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
s