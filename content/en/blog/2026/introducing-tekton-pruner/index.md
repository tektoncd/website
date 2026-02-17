---
title: Introducing Tekton Pruner
linkTitle: Introducing Tekton Pruner
date: 2026-02-05
author: "Shubham Bhardwaj, Red Hat"
description: >
  Automate the cleanup of completed PipelineRuns and TaskRuns with Tekton Pruner
---

[Tekton Pruner](https://github.com/tektoncd/pruner) automatically cleans up completed PipelineRuns and TaskRuns based on retention policies you define.

## The Problem

Tekton does not delete PipelineRuns and TaskRuns after completion. Over time, this increases etcd storage usage and degrades API performance.

## Before: Job-Based Pruner

The Tekton Operator has a [job-based pruner](https://tekton.dev/docs/operator/tektonconfig/#pruner) configured via `TektonConfig`:

```yaml
pruner:
  disabled: false
  schedule: "0 8 * * *"
  startingDeadlineSeconds: 100  # optional
  resources:
    - taskrun
    - pipelinerun
  keep: 3
  # keep-since: 1440
  # NOTE: you can use either "keep" or "keep-since", not both
  prune-per-resource: true
```

The operator creates a CronJob based on this config:

- `schedule`: Cron expression for when cleanup runs. `0 8 * * *` means daily at 8 AM.
- `resources`: Which resources to prune - `taskrun`, `pipelinerun`, or both.
- `keep`: Retain the last N runs. With `keep: 3`, only the 3 most recent runs are kept.
- `keep-since`: Alternative to `keep`. Retain runs from the last N minutes. `keep-since: 1440` keeps runs from the last 24 hours. You can use one or the other, not both.
- `prune-per-resource`: When `true`, limits apply per pipeline/task name. When `false`, the limit is global across the namespace.
- `startingDeadlineSeconds`: How long the CronJob can be delayed before it's considered missed.

You can also override at the namespace level using annotations:

```yaml
metadata:
  annotations:
    operator.tekton.dev/prune.resources: "taskrun,pipelinerun"
    operator.tekton.dev/prune.keep-since: "7200"
    operator.tekton.dev/prune.keep: "5"
```

This works, but there are gaps.

First, if you installed Tekton Pipelines with `kubectl apply` instead of the Operator, you don't have this pruner. 

Second, the batch model creates pressure. Run multiple pipelines a day with a daily cleanup schedule, and you've got 500 completed PipelineRuns in etcd by the time the CronJob fires. In high-throughput environments, that's real load on your API server.

Third, one policy per namespace is limiting. Your nightly test runs don't need the same retention as production deployments. But with the Operator pruner, they get the same treatment unless you split them into separate namespaces.

## Tekton Pruner

Tekton Pruner is event-driven. When a PipelineRun or TaskRun completes, the controller evaluates it against your policies right then. No accumulation between scheduled runs.

It also works without the Operator - install it alongside any Tekton Pipelines deployment.

The configuration model is hierarchical. Set cluster-wide defaults, override per namespace, and use label selectors to apply different policies to different pipelines within the same namespace. Your test pipelines can be cleaned up in minutes while production runs could stick around for a week.

One thing to keep in mind: if you're using Tekton Chains for provenance or Tekton Results for long-term storage, set your TTL high enough for them to do their job. Chains needs a few seconds to sign and store attestations. Delete a PipelineRun before Chains processes it and that provenance is gone.

## Installation

### Via Tekton Operator

If you're using the Tekton Operator, enable Tekton Pruner through TektonConfig. You need to disable the old job-based pruner first:

```yaml
apiVersion: operator.tekton.dev/v1alpha1
kind: TektonConfig
metadata:
  name: config
spec:
  pruner:
    disabled: true  # disable the job-based pruner
  tektonpruner:
    disabled: false
    global-config:
      enforcedConfigLevel: global
      ttlSecondsAfterFinished: 3600
      successfulHistoryLimit: 5
      failedHistoryLimit: 3
```

### Standalone Installation

If you installed Tekton Pipelines without the Operator:

```bash
export VERSION=0.3.5  # check https://github.com/tektoncd/pruner/releases for latest
kubectl apply -f "https://infra.tekton.dev/tekton-releases/pruner/previous/v${VERSION}/release.yaml"
```

### Verify

```bash
kubectl get pods -n tekton-pipelines -l app=tekton-pruner-controller
```

You should see the controller pod running. The controller handles pruning logic and serves the validating webhook that checks ConfigMaps before they're applied.

## Configuration

ConfigMaps need these labels (since v0.3.0):

```yaml
labels:
  app.kubernetes.io/part-of: tekton-pruner
  pruner.tekton.dev/config-type: global  # or 'namespace'
```

### Cluster-Wide Defaults

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tekton-pruner-default-spec
  namespace: tekton-pipelines
  labels:
    app.kubernetes.io/part-of: tekton-pruner
    pruner.tekton.dev/config-type: global
data:
  global-config: |
    enforcedConfigLevel: global
    ttlSecondsAfterFinished: 3600
    successfulHistoryLimit: 5
    failedHistoryLimit: 3
```


- **TTL**: Once the time passes after completion, the run is deleted. Doesn't matter if you're under the history limit.
- **History limit**: Deletes oldest runs when count exceeds the limit. Only matters if TTL hasn't already deleted them.

**Example**: `ttlSecondsAfterFinished: 300` and `historyLimit: 3`. You run a pipeline 5 times.

1. History limit kicks in → keeps 3, deletes 2 oldest
2. 5 minutes later, TTL expires → all 3 remaining runs deleted

History limit kept 3, but TTL deleted them anyway once 5 minutes passed. If you want runs to persist, increase TTL or use only history limits.

### Per-Namespace Config

Set `enforcedConfigLevel: namespace` to allow namespace-level overrides.

**Inline approach** - define everything in the global ConfigMap:

```yaml
data:
  global-config: |
    enforcedConfigLevel: namespace
    ttlSecondsAfterFinished: 3600
    namespaces:
      production:
        ttlSecondsAfterFinished: 604800
        successfulHistoryLimit: 20
      dev:
        ttlSecondsAfterFinished: 1800
```

**Separate ConfigMaps** - namespace owners manage their own:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tekton-pruner-namespace-spec
  namespace: my-team
  labels:
    app.kubernetes.io/part-of: tekton-pruner
    pruner.tekton.dev/config-type: namespace
data:
  ns-config: |
    ttlSecondsAfterFinished: 7200
    successfulHistoryLimit: 10
```

### Label-Based Selectors

Different pipelines in the same namespace can have different policies:

```yaml
data:
  ns-config: |
    pipelineRuns:
      - selector:
        - matchLabels:
            app: critical-service
        ttlSecondsAfterFinished: 604800
        successfulHistoryLimit: 50
      - selector:
        - matchLabels:
            app: test-jobs
        ttlSecondsAfterFinished: 300
        successfulHistoryLimit: 3
```

Selectors only work in namespace-level ConfigMaps.

## What to Watch Out For

**System namespaces are off-limits.** Don't create namespace-level ConfigMaps in `kube-*`, `openshift-*`, `tekton-pipelines`, or other `tekton-*` namespaces.

**Webhook validates your config.** If your ConfigMap is rejected, check the labels and YAML syntax. The webhook will tell you what's wrong.


## Checking Logs

```bash
kubectl logs -n tekton-pipelines -l app=tekton-pruner-controller -f
```

You'll see entries when resources are pruned, along with which policy triggered the deletion.

## Config Reference

| Field | What it does |
|-------|--------------|
| `enforcedConfigLevel` | `global` applies cluster-wide, `namespace` allows per-ns overrides |
| `ttlSecondsAfterFinished` | Delete runs older than this many seconds after completion |
| `successfulHistoryLimit` | Keep this many successful runs per pipeline |
| `failedHistoryLimit` | Keep this many failed runs per pipeline |
| `historyLimit` | Used when success/failed limits aren't set |

## Links

- [GitHub](https://github.com/tektoncd/pruner)
- [Architecture docs](https://github.com/tektoncd/pruner/blob/main/ARCHITECTURE.md)
- [Getting started tutorial](https://github.com/tektoncd/pruner/blob/main/docs/tutorials/getting-started.md)
