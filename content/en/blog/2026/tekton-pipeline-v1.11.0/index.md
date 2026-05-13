---
title: "Tekton Pipelines v1.11.0: TaskRun Pending, Multi-URL Hub Resolver, and PVC Auto-Cleanup"
linkTitle: "Tekton Pipelines v1.11.0: TaskRun Pending, Multi-URL Hub Resolver, and PVC Auto-Cleanup"
date: 2026-03-30
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.11.0 brings TaskRun pending status parity with PipelineRun, multi-URL support for the Hub Resolver, optional PVC auto-cleanup, and important bug fixes for resolver security and metrics.
---

We're excited to announce the release of [Tekton Pipelines v1.11.0 "Javanese Jocasta"](https://github.com/tektoncd/pipeline/releases/tag/v1.11.0)! This release focuses on feature parity, resolver improvements, and stability fixes.

## TaskRun Pending Status

TaskRuns now support a **pending status**, bringing feature parity with PipelineRun. You can create a TaskRun in a pending state and start it later by clearing the `spec.status` field — useful for scheduling, quota management, or approval gates.

```yaml
apiVersion: tekton.dev/v1
kind: TaskRun
metadata:
  name: my-taskrun
spec:
  status: TaskRunPending
  taskRef:
    name: my-task
```

When a TaskRun is pending, no Pod is created until the status is cleared. The TaskRun's `status.conditions` will report `Pending` with a clear reason, and the pending duration is tracked separately from the execution duration.

See [PR #9376](https://github.com/tektoncd/pipeline/pull/9376) for details.

## Multi-URL Hub Resolver

The Hub Resolver now supports **multiple Artifact Hub URLs** and a new per-resolution `url` parameter. This means you can query multiple Hub instances (e.g., the public Artifact Hub and a private internal instance) and override the URL on a per-resolution basis.

```yaml
taskRef:
  resolver: hub
  params:
    - name: name
      value: git-clone
    - name: url
      value: https://my-internal-hub.example.com
```

See [PR #9465](https://github.com/tektoncd/pipeline/pull/9465) for details.

## PVC Auto-Cleanup for Workspaces

A new **optional annotation** allows automatic cleanup of PersistentVolumeClaims created via `volumeClaimTemplate` when a PipelineRun or TaskRun completes. This prevents PVC accumulation in clusters with high pipeline throughput.

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: my-pipelinerun
  annotations:
    tekton.dev/auto-cleanup-pvc: "true"
spec:
  workspaces:
    - name: shared-data
      volumeClaimTemplate:
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 1Gi
```

See [PR #9284](https://github.com/tektoncd/pipeline/pull/9284) for details.

## Multiple Git Credentials on the Same Host

Two fixes improve support for **multiple Git credentials on the same host** — a common need when accessing multiple repositories on the same Git provider with different credentials:

- **`useHttpPath` support**: Git credential helpers now respect `useHttpPath`, allowing different credentials for different repositories on the same host. ([#9143](https://github.com/tektoncd/pipeline/pull/9143))
- **SSH host aliases**: When multiple SSH credentials target the same host, Tekton now generates unique host aliases in the SSH config, preventing credential conflicts. ([#9643](https://github.com/tektoncd/pipeline/pull/9643))

## Bug Fixes

### Cluster Resolver Namespace Access Control

Fixed whitespace and wildcard handling bugs in the Cluster Resolver's namespace access control. Previously, extra whitespace in the allowed-namespaces configuration or wildcard patterns could bypass access restrictions. ([#9592](https://github.com/tektoncd/pipeline/pull/9592))

### Cancelled PipelineRun Metrics

Cancelled PipelineRuns now correctly record completion metrics. Previously, cancelling a PipelineRun did not update the `pipelinerun_duration_seconds` or `pipelinerun_total` metrics, making it difficult to track cancellation rates. ([#9658](https://github.com/tektoncd/pipeline/pull/9658))

### Resolution Framework Fixes

- **Context key collision and ownerRef nil panic**: Fixed a context key collision between the resolution framework and the Tekton Pipelines controller that could cause nil pointer panics when processing ownerReferences. ([#9593](https://github.com/tektoncd/pipeline/pull/9593))
- **Explicit namespace validation**: `GetNameAndNamespace` no longer silently falls back to the "default" namespace. Instead, it returns an explicit error when the namespace cannot be determined, preventing resources from being created in the wrong namespace. ([#9594](https://github.com/tektoncd/pipeline/pull/9594))

### Cache Race Condition

Fixed a race condition in the resource cache using `singleflight`, preventing duplicate concurrent fetches and corrupted cache entries. ([#9364](https://github.com/tektoncd/pipeline/pull/9364))

## Infrastructure

- **Webhook TLS configuration**: Adopted centralized `WEBHOOK_*` TLS configuration from Knative, simplifying TLS setup for the admission webhook. ([#9466](https://github.com/tektoncd/pipeline/pull/9466))
- **Step-init idempotency**: Made step-init symlink creation idempotent, preventing errors on container restarts.
- **CI security hardening**: Added [zizmor](https://github.com/woodruffw/zizmor) GitHub Actions security analysis and fixed identified issues (permissions, injection, pinned actions).

## Get Started

Install or upgrade to v1.11.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/latest/release.yaml
```

Check out the full [release notes](https://github.com/tektoncd/pipeline/releases/tag/v1.11.0) and [documentation](https://github.com/tektoncd/pipeline/tree/v1.11.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
