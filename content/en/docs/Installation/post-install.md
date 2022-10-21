<!---
---
title: Post-installation configurations
titleLink: Post-installation configurations
weight: 3
description: >
  Additional configurations when installing Tekton Pipelines
---
--->

This document describes additional options to configure your Tekton Pipelines installation.

- [Configuring CloudEvents notifications](#configuring-cloudevents-notifications)
- [Installing and configuring remote Task and Pipeline resolution](#installing-and-configuring-remote-task-and-pipeline-resolution)
- [Configuring self-signed cert for private registry](#configuring-self-signed-cert-for-private-registry)
- [Customizing basic execution parameters](#customizing-basic-execution-parameters)
    - [Customizing the Pipelines Controller behavior](#customizing-the-pipelines-controller-behavior)
    - [Alpha Features](#alpha-features)
    - [Beta Features](#beta-features)
- [Configuring High Availability](#configuring-high-availability)
- [Configuring tekton pipeline controller performance](#configuring-tekton-pipeline-controller-performance)
- [Creating a custom release of Tekton Pipelines](#creating-a-custom-release-of-tekton-pipelines)
- [Verify Tekton Pipelines release](#verify-tekton-pipelines-release)
    - [Verify signatures using `cosign`](#verify-signatures-using-cosign)
    - [Verify the tansparency logs using `rekor-cli`](#verify-the-transparency-logs-using-rekor-cli)
- [Next steps](#next-steps)

## Configuring CloudEvents notifications

When configured so, Tekton can generate `CloudEvents` for `TaskRun`,
`PipelineRun` and `Run`lifecycle events. The main configuration parameter is the
URL of the sink. When not set, no notification is generated.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-defaults
  namespace: tekton-pipelines
  labels:
    app.kubernetes.io/instance: default
    app.kubernetes.io/part-of: tekton-pipelines
data:
  default-cloud-events-sink: https://my-sink-url
```

Additionally, CloudEvents for `Runs` require an extra configuration to be
enabled. This setting exists to avoid collisions with CloudEvents that might
be sent by custom task controllers:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
  namespace: tekton-pipelines
  labels:
    app.kubernetes.io/instance: default
    app.kubernetes.io/part-of: tekton-pipelines
data:
  send-cloudevents-for-runs: true
```

## Configuring self-signed cert for private registry

The `SSL_CERT_DIR` is set to `/etc/ssl/certs` as the default cert directory. If
you are using a self-signed cert for private registry and the cert file is not
under the default cert directory, configure your registry cert in the
`config-registry-cert` `ConfigMap` with the key `cert`.

## Customizing basic execution parameters

You can specify your own values that replace the default service account
(`ServiceAccount`), timeout (`Timeout`), and Pod template (`PodTemplate`) values
used by Tekton Pipelines in `TaskRun` and `PipelineRun` definitions. To do so,
modify the ConfigMap `config-defaults` with your desired values.

The example below customizes the following:

- the default service account from `default` to `tekton`.

- the default timeout from 60 minutes to 20 minutes.

- the default `app.kubernetes.io/managed-by` label is applied to all Pods
  created to execute `TaskRuns`.

- the default Pod template to include a node selector to select the node where
  the Pod will be scheduled by default. A list of supported fields is available
  [here](https://github.com/tektoncd/pipeline/blob/main/docs/podtemplates.md#supported-fields).

  For more information, see [`PodTemplate` in
  `TaskRuns`](./taskruns.md#specifying-a-pod-template) or [`PodTemplate` in
  `PipelineRuns`](./pipelineruns.md#specifying-a-pod-template).

- the default `Workspace` configuration can be set for any `Workspaces` that a
  Task declares but that a TaskRun does not explicitly provide

- the default maximum combinations of `Parameters` in a `Matrix` that can be
  used to fan out a `PipelineTask`. For more information, see
  [`Matrix`](matrix.md).

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-defaults
data:
  default-service-account: "tekton"
  default-timeout-minutes: "20"
  default-pod-template: |
    nodeSelector:
      kops.k8s.io/instancegroup: build-instance-group
  default-managed-by-label-value: "my-tekton-installation"
  default-task-run-workspace-binding: |
    emptyDir: {}
  default-max-matrix-combinations-count: "1024"
```

**Note:** The `_example` key in the provided
[config-defaults.yaml](./../config/config-defaults.yaml) file lists the keys you
can customize along with their default values.

### Customizing the Pipelines Controller behavior

To customize the behavior of the Pipelines Controller, modify the ConfigMap
`feature-flags` via `kubectl edit configmap feature-flags -n tekton-pipelines`.
The flags in this ConfigMap are as follows:

- `disable-affinity-assistant` - set this flag to `true` to disable the
  [Affinity Assistant][affinity-assistant] that is used to provide Node Affinity
  for `TaskRun` pods that share workspace volume.  The Affinity Assistant is
  incompatible with other affinity rules configured for `TaskRun` pods.

  **Note:** Affinity Assistant use [Inter-pod affinity and
  anti-affinity][affinity] that require substantial amount of processing which can
  slow down scheduling in large clusters significantly. We do not recommend using
  them in clusters larger than several hundred nodes

  **Note:** Pod anti-affinity requires nodes to be consistently labelled, in
  other words every node in the cluster must have an appropriate label matching
  `topologyKey`. If some or all nodes are missing the specified `topologyKey`
  label, it can lead to unintended behavior.

- `await-sidecar-readiness`: set this flag to `"false"` to allow the Tekton
  controller to start a TasksRun's first step immediately without waiting for
  sidecar containers to be running first. Using this option should decrease the
  time it takes for a TaskRun to start running, and will allow TaskRun pods to
  be scheduled in environments that don't support [Downward API][downward-api]
  volumes (e.g. some virtual kubelet implementations). However, this may lead to
  unexpected behaviour with Tasks that use sidecars, or in clusters that use
  injected sidecars (e.g. Istio). Setting this flag to `"false"` will mean the
  `running-in-environment-with-injected-sidecars` flag has no effect.

- `running-in-environment-with-injected-sidecars`: set this flag to `"false"` to
  allow the Tekton controller to start a TasksRun's first step immediately if it
  has no Sidecars specified.  Using this option should decrease the time it takes
  for a TaskRun to start running.  However, for clusters that use injected
  sidecars (e.g. Istio) this can lead to unexpected behavior.

- `require-git-ssh-secret-known-hosts`: set this flag to `"true"` to require
  that Git SSH Secrets include a `known_hosts` field. This ensures that a git
  remote server's key is validated before data is accepted from it when
  authenticating over SSH. Secrets that don't include a `known_hosts` will
  result in the TaskRun failing validation and not running.

- `enable-tekton-oci-bundles`: set this flag to `"true"` to enable the tekton
  OCI bundle usage (see [the tekton bundle
  contract](./tekton-bundle-contracts.md)). Enabling this option allows the use
  of `bundle` field in `taskRef` and `pipelineRef` for `Pipeline`, `PipelineRun`
  and `TaskRun`. By default, this option is disabled (`"false"`), which means it
  is disallowed to use the `bundle` field.

- `disable-creds-init` - set this flag to `"true"` to [disable Tekton's built-in
  credential initialization](auth.md#disabling-tektons-built-in-auth) and use
  Workspaces to mount credentials from Secrets instead.  The default is `false`.
  For more information, see the [associated
  issue](https://github.com/tektoncd/pipeline/issues/3399).

- `enable-custom-tasks`: set this flag to `"true"` to enable the use of custom
  tasks in pipelines.

- `enable-api-fields`: set this flag to "stable" to allow only the most stable
  features to be used. Set it to "alpha" to allow [alpha
  features](#alpha-features) to be used.

- `embedded-status`: set this flag to "full" to enable full embedding of
  `TaskRun` and `Run` statuses in the `PipelineRun` status. Set it to "minimal"
  to populate the `ChildReferences` field in the `PipelineRun` status with name,
  kind, and API version information for each `TaskRun` and `Run` in the
  `PipelineRun` instead. Set it to "both" to do both. For more information, see
  [Configuring usage of `TaskRun` and `Run` embedded
  statuses](pipelineruns.md#configuring-usage-of-taskrun-and-run-embedded-statuses).

- `resource-verification-mode`: Setting this flag to "enforce" will enforce
  verification of tasks/pipeline. Failing to verify will fail the
  taskrun/pipelinerun. "warn" will only log the err message and "skip" will skip
  the whole verification.

For example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  enable-api-fields: "alpha" # Allow alpha fields to be used in Tasks and Pipelines.
```

[affinity]: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity
[affinity-assistant]: ./workspaces.md#specifying-workspace-order-in-a-pipeline-and-affinity-assistants
[downward-api]: https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/


### Alpha Features

Alpha features are still in development and their syntax is subject to change.
To enable these, set the `enable-api-fields` feature flag to `"alpha"` in the
`feature-flags` ConfigMap alongside your Tekton Pipelines deployment via
`kubectl patch cm feature-flags -n tekton-pipelines -p
'{"data":{"enable-api-fields":"alpha"}}'`.  Setting `enable-api-fields` to
"alpha" also enables [beta features](#beta-features).

Features currently in "alpha" are:

| Feature                                                                                               | TEP                                                                                                                        | Release                                                              | Individual Flag             |
|:------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------|:----------------------------|
| [Bundles ](./pipelineruns.md#tekton-bundles)                                                          | [TEP-0005](https://github.com/tektoncd/community/blob/main/teps/0005-tekton-oci-bundles.md)                                | [v0.18.0](https://github.com/tektoncd/pipeline/releases/tag/v0.18.0) | `enable-tekton-oci-bundles` |
| [`Runs` and `Custom Tasks`](./runs.md)                                                                | [TEP-0002](https://github.com/tektoncd/community/blob/main/teps/0002-custom-tasks.md)                                      | [v0.19.0](https://github.com/tektoncd/pipeline/releases/tag/v0.19.0) | `enable-custom-tasks`       |
| [Isolated `Step` & `Sidecar` `Workspaces`](./workspaces.md#isolated-workspaces)                       | [TEP-0029](https://github.com/tektoncd/community/blob/main/teps/0029-step-workspaces.md)                                   | [v0.24.0](https://github.com/tektoncd/pipeline/releases/tag/v0.24.0) |                             |
| [Hermetic Execution Mode](./hermetic.md)                                                              | [TEP-0025](https://github.com/tektoncd/community/blob/main/teps/0025-hermekton.md)                                         | [v0.25.0](https://github.com/tektoncd/pipeline/releases/tag/v0.25.0) |                             |
| [Propagated `Parameters`](./taskruns.md#propagated-parameters)                                        | [TEP-0107](https://github.com/tektoncd/community/blob/main/teps/0107-propagating-parameters.md)                            | [v0.36.0](https://github.com/tektoncd/pipeline/releases/tag/v0.36.0) |                             |
| [Propagated `Workspaces`](./pipelineruns.md#propagated-workspaces)                                    | [TEP-0111](https://github.com/tektoncd/community/blob/main/teps/0111-propagating-workspaces.md)                      |            v0.40.0                                                          |                             |
| [Windows Scripts](./tasks.md#windows-scripts)                                                         | [TEP-0057](https://github.com/tektoncd/community/blob/main/teps/0057-windows-support.md)                                   | [v0.28.0](https://github.com/tektoncd/pipeline/releases/tag/v0.28.0) |                             |
| [Debug](./debug.md)                                                                                   | [TEP-0042](https://github.com/tektoncd/community/blob/main/teps/0042-taskrun-breakpoint-on-failure.md)                     | [v0.26.0](https://github.com/tektoncd/pipeline/releases/tag/v0.26.0) |                             |
| [Step and Sidecar Overrides](./taskruns.md#overriding-task-steps-and-sidecars)                        | [TEP-0094](https://github.com/tektoncd/community/blob/main/teps/0094-specifying-resource-requirements-at-runtime.md)       |   [v0.34.0](https://github.com/tektoncd/pipeline/releases/tag/v0.34.0)                                                                   |                             |
| [Matrix](./matrix.md)                                                                                 | [TEP-0090](https://github.com/tektoncd/community/blob/main/teps/0090-matrix.md)                                            | [v0.38.0](https://github.com/tektoncd/pipeline/releases/tag/v0.38.0) |                             |
| [Embedded Statuses](pipelineruns.md#configuring-usage-of-taskrun-and-run-embedded-statuses)           | [TEP-0100](https://github.com/tektoncd/community/blob/main/teps/0100-embedded-taskruns-and-runs-status-in-pipelineruns.md) |   [v0.35.0](https://github.com/tektoncd/pipeline/releases/tag/v0.35.0)     |     embedded-status                 |
| [Task-level Resource Requirements](compute-resources.md#task-level-compute-resources-configuration)   | [TEP-0104](https://github.com/tektoncd/community/blob/main/teps/0104-tasklevel-resource-requirements.md)                   | [v0.39.0](https://github.com/tektoncd/pipeline/releases/tag/v0.39.0)  |                             |
| [Object Params and Results](pipelineruns.md#specifying-parameters)                                    | [TEP-0075](https://github.com/tektoncd/community/blob/main/teps/0075-object-param-and-result-types.md)                     | [v0.38.0](https://github.com/tektoncd/pipeline/releases/tag/v0.38.0) |                             |
| [Array Results](pipelineruns.md#specifying-parameters)                                                | [TEP-0076](https://github.com/tektoncd/community/blob/main/teps/0076-array-result-types.md)                                | [v0.38.0](https://github.com/tektoncd/pipeline/releases/tag/v0.38.0) |                             |
| [Trusted Resources](./trusted-resources.md)                                                | [TEP-0091](https://github.com/tektoncd/community/blob/main/teps/0091-trusted-resources.md)                                | N/A |     resource-verification-mode                        |

### Beta Features

Beta features are fields of stable CRDs that follow our "beta" [compatibility
policy](../api_compatibility_policy.md).  To enable these features, set the
`enable-api-fields` feature flag to `"beta"` in the `feature-flags` ConfigMap
alongside your Tekton Pipelines deployment via 

```bash
kubectl patch cm feature-flags -n tekton-pipelines -p '{"data":{"enable-api-fields":"beta"}}'

```

For beta versions of Tekton CRDs, setting `enable-api-fields` to "beta" is the
same as setting it to "stable".

## Configuring High Availability

If you want to run Tekton Pipelines in a way so that webhooks are resiliant
against failures and support high concurrency scenarios, you need to run a
[Metrics Server][metrics] in your Kubernetes cluster. This is required by the
[Horizontal Pod Autoscalers][hor-autoscale] to compute replica count.

See [HA Support for Tekton Pipeline Controllers](./enabling-ha.md) for
instructions on configuring High Availability in the Tekton Pipelines
Controller.

The default configuration is defined in
[webhook-hpa.yaml](./../config/webhook-hpa.yaml) which can be customized to
better fit specific use cases.

[hor-autoscale]: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
[metrics]: https://github.com/kubernetes-sigs/metrics-server

## Configuring tekton pipeline controller performance

Out-of-the-box, Tekton Pipelines Controller is configured for relatively
small-scale deployments but there have several options for configuring
Pipelines' performance are available. See the [Performance
Configuration](tekton-controller-performance-configuration.md) document which
describes how to change the default ThreadsPerController, QPS and Burst settings
to meet your requirements.

## Platform Support

The Tekton project provides support for running on x86 Linux Kubernetes nodes.

The project produces images capable of running on other architectures and
operating systems, but may not be able to help debug issues specific to those
platforms as readily as those that affect Linux on x86.

The controller and webhook components are currently built for:

- linux/amd64
- linux/arm64
- linux/arm (Arm v7)
- linux/ppc64le (PowerPC)
- linux/s390x (IBM Z)

The entrypoint component is also built for Windows, which enables TaskRun
workloads to execute on Windows nodes.  See [Windows documentation](windows.md)
for more information.

Additional components to support PipelineResources may be available for other
architectures as well.

## Creating a custom release of Tekton Pipelines

You can create a custom release of Tekton Pipelines by following and customizing
the steps in [Creating an official release](create-release).  For example, you
might want to customize the container images built and used by Tekton Pipelines.

[create-release]: https://github.com/tektoncd/pipeline/blob/main/tekton/README.md#create-an-official-release

## Verify Tekton Pipelines Release

> We will refine this process over time to be more streamlined. For now, please
> follow the steps listed in this section to verify Tekton pipeline release.

Tekton Pipeline's images are being signed by [Tekton Chains][chains] since
[0.27.1][]. You can verify the images with `cosign` using the [Tekton's public
key][tek-key].

[chains]: https://github.com/tektoncd/chains
[0.27.1]: https://github.com/tektoncd/pipeline/releases/tag/v0.27.1
[tek-key]: https://raw.githubusercontent.com/tektoncd/chains/main/tekton.pub

### Verify signatures using `cosign`

With Go 1.16+, you can install `cosign` by running:

```shell
go install github.com/sigstore/cosign/cmd/cosign@latest
```

You can verify Tekton Pipelines official images using the Tekton public key:

```shell
cosign verify -key https://raw.githubusercontent.com/tektoncd/chains/main/tekton.pub gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/controller:v0.28.1
```

which results in:

```
Verification for gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/controller:v0.28.1 --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - The signatures were verified against the specified public key
  - Any certificates were verified against the Fulcio roots.
{
  "Critical": {
    "Identity": {
      "docker-reference": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/controller"
    },
    "Image": {
      "Docker-manifest-digest": "sha256:0c320bc09e91e22ce7f01e47c9f3cb3449749a5f72d5eaecb96e710d999c28e8"
    },
    "Type": "Tekton container signature"
  },
  "Optional": {}
}
```

The verification shows a list of checks performed and returns the digest in
`Critical.Image.Docker-manifest-digest` which can be used to retrieve the
provenance from the transparency logs for that image using `rekor-cli`.

### Verify the transparency logs using `rekor-cli`

Install the `rekor-cli` by running:

```shell
go install -v github.com/sigstore/rekor/cmd/rekor-cli@latest
```

Now, use the digest collected from the previous
[section](#verify-signatures-using-cosign) in
`Critical.Image.Docker-manifest-digest`. For example,
`sha256:0c320bc09e91e22ce7f01e47c9f3cb3449749a5f72d5eaecb96e710d999c28e8`.

Search the transparency log with the digest just collected:

```shell
rekor-cli search --sha sha256:0c320bc09e91e22ce7f01e47c9f3cb3449749a5f72d5eaecb96e710d999c28e8
```

which results in:

```
Found matching entries (listed by UUID):
68a53d0e75463d805dc9437dda5815171502475dd704459a5ce3078edba96226
```

Tekton Chains generates provenance based on the custom [format][provenance-spec]
in which the `subject` holds the list of artifacts which were built as part of
the release. For the Pipeline release, `subject` includes a list of images
including pipeline controller, pipeline webhook, etc. Use the `UUID` to get the
provenance:

```shell
rekor-cli get --uuid 68a53d0e75463d805dc9437dda5815171502475dd704459a5ce3078edba96226 --format json | jq -r .Attestation | base64 --decode | jq
```

which results in:

```shell
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://tekton.dev/chains/provenance",
  "subject": [
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/controller",
      "digest": {
        "sha256": "0c320bc09e91e22ce7f01e47c9f3cb3449749a5f72d5eaecb96e710d999c28e8"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/entrypoint",
      "digest": {
        "sha256": "2fa7f7c3408f52ff21b2d8c4271374dac4f5b113b1c4dbc7d5189131e71ce721"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/git-init",
      "digest": {
        "sha256": "83d5ec6addece4aac79898c9631ee669f5fee5a710a2ed1f98a6d40c19fb88f7"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/imagedigestexporter",
      "digest": {
        "sha256": "e4d77b5b8902270f37812f85feb70d57d6d0e1fed2f3b46f86baf534f19cd9c0"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/kubeconfigwriter",
      "digest": {
        "sha256": "55963ed3fb6157e5f8dac7a315a794ebe362e46714631f9c79d79d33fe769e4d"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/nop",
      "digest": {
        "sha256": "59b5304bcfdd9834150a2701720cf66e3ebe6d6e4d361ae1612d9430089591f8"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/pullrequest-init",
      "digest": {
        "sha256": "4992491b2714a73c0a84553030e6056e6495b3d9d5cc6b20cf7bc8c51be779bb"
      }
    },
    {
      "name": "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/webhook",
      "digest": {
        "sha256": "bf0ef565b301a1981cb2e0d11eb6961c694f6d2401928dccebe7d1e9d8c914de"
      }
    }
  ],
  ...
```

Now, verify the digest in the `release.yaml` by matching it with the provenance,
for example, the digest for the release `v0.28.1`:

```shell
curl -s https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.28.1/release.yaml | grep github.com/tektoncd/pipeline/cmd/controller:v0.28.1 | awk -F"github.com/tektoncd/pipeline/cmd/controller:v0.28.1@" '{print $2}'
```

which results in:

```shell
sha256:0c320bc09e91e22ce7f01e47c9f3cb3449749a5f72d5eaecb96e710d999c28e8
```

Now you can verify the deployment specifications in the `release.yaml` to match
each of these images and their digest.  The `tekton-pipelines-controller`
deployment specification has a container named `tekton-pipeline-controller` and
a
list of image references with their digest as part of the `args`:

```yaml
      containers:
        - name: tekton-pipelines-controller
          image: gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/controller:v0.28.1@sha256:0c320bc09e91e22ce7f01e47c9f3cb3449749a5f72d5eaecb96e710d999c28e8
          args: [
            # These images are built on-demand by `ko resolve` and are replaced
            # by image references by digest.
              "-kubeconfig-writer-image",
              "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/kubeconfigwriter:v0.28.1@sha256:55963ed3fb6157e5f8dac7a315a794ebe362e46714631f9c79d79d33fe769e4d",
              "-git-image",
              "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/git-init:v0.28.1@sha256:83d5ec6addece4aac79898c9631ee669f5fee5a710a2ed1f98a6d40c19fb88f7",
              "-entrypoint-image",
              "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/entrypoint:v0.28.1@sha256:2fa7f7c3408f52ff21b2d8c4271374dac4f5b113b1c4dbc7d5189131e71ce721",
              "-nop-image",
              "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/nop:v0.28.1@sha256:59b5304bcfdd9834150a2701720cf66e3ebe6d6e4d361ae1612d9430089591f8",
              "-imagedigest-exporter-image",
              "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/imagedigestexporter:v0.28.1@sha256:e4d77b5b8902270f37812f85feb70d57d6d0e1fed2f3b46f86baf534f19cd9c0",
              "-pr-image",
              "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/pullrequest-init:v0.28.1@sha256:4992491b2714a73c0a84553030e6056e6495b3d9d5cc6b20cf7bc8c51be779bb",
```

Similarly, you can verify the rest of the images which were published as part of
the Tekton Pipelines release:

```shell
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/kubeconfigwriter
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/git-init
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/entrypoint
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/nop
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/imagedigestexporter
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/pullrequest-init
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/webhook
```

[provenance-spec]: https://github.com/tektoncd/chains/blob/main/PROVENANCE_SPEC.md

---

{{% comment %}}
Except as otherwise noted, the content of this page is licensed under the
[Creative Commons Attribution 4.0 License][cca4], and code samples are licensed
under the [Apache 2.0 License][apache2l].
{{% /comment %}}

[cca4]: https://creativecommons.org/licenses/by/4.0/
[apache2l]: https://www.apache.org/licenses/LICENSE-2.0
