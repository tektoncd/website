---
title: "Tekton Pipelines v1.12.0 LTS: Notifications Controllers, Security Hardening, and Performance"
linkTitle: "Tekton Pipelines v1.12.0 LTS: Notifications Controllers, Security Hardening, and Performance"
date: 2026-05-04
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.12.0 is a Long Term Support (LTS) release featuring TEP-0137 notifications controllers for PipelineRun and TaskRun events, critical security fixes, and reconciler performance improvements.
---

We're excited to announce the release of [Tekton Pipelines v1.12.0 "Exotic Shorthair Elektrobots LTS"](https://github.com/tektoncd/pipeline/releases/tag/v1.12.0)! This is a **Long Term Support (LTS)** release, supported until May 2027.

## TEP-0137: Notifications Controllers

The headline feature of v1.12.0 is the implementation of [TEP-0137](https://github.com/tektoncd/community/blob/main/teps/0137-cloudevents-controller.md) — dedicated notifications controllers for PipelineRun and TaskRun CloudEvents.

### What Changed

CloudEvents for **PipelineRuns** and **TaskRuns** are now sent by a dedicated `tekton-events-controller` deployment, rather than being embedded in the PipelineRun and TaskRun reconcilers. This separation improves:

- **Reliability**: Event delivery no longer competes with reconciliation work
- **Observability**: CloudEvent delivery status is visible via `kubectl describe pipelinerun/taskrun` (look for `CloudEventSent` / `CloudEventFailed` Kubernetes Events)
- **Coverage**: New `dev.tekton.event.pipelinerun.queued.v1` and `dev.tekton.event.taskrun.queued.v1` events are emitted when resources are created but not yet processed

### Upgrade Notice

**ACTION REQUIRED**: Operators must ensure the `tekton-events-controller` Deployment is running after upgrading. It is included in the standard `release.yaml` manifest.

The `send-cloudevents-for-runs` feature flag is **deprecated** — its default has changed from `false` to `true`, meaning CloudEvents for CustomRuns are now sent by default when a sink is configured in `config-events`.

See PRs [#9677](https://github.com/tektoncd/pipeline/pull/9677), [#9674](https://github.com/tektoncd/pipeline/pull/9674), and [#9774](https://github.com/tektoncd/pipeline/pull/9774) for details.

## Security Fixes

This release includes several important security fixes:

- **Git argument injection** (GHSA-94jr-7pqp-xhcq): Prevented argument injection via the revision parameter in the git resolver ([#9660](https://github.com/tektoncd/pipeline/pull/9660))
- **API token validation**: System API tokens are now rejected when used with user-controlled `serverURL` ([#9659](https://github.com/tektoncd/pipeline/pull/9659))
- **HTTP resolver OOM prevention**: Response body size is now limited to prevent denial-of-service via large payloads ([#9656](https://github.com/tektoncd/pipeline/pull/9656))
- **VolumeMount path normalization**: Paths are normalized before checking the `/tekton/` restriction, closing a bypass via path traversal ([#9655](https://github.com/tektoncd/pipeline/pull/9655))
- **Source URI pattern matching**: Whitespace trimming and resolver prefix stripping harden provenance URI validation ([#9653](https://github.com/tektoncd/pipeline/pull/9653), [#9654](https://github.com/tektoncd/pipeline/pull/9654))

## Performance Improvements

Three targeted optimizations reduce controller overhead:

- **Reduced reconcile churn for completed PipelineRuns**: The controller no longer re-reconciles PipelineRuns that have already completed, significantly reducing API server load in clusters with many finished runs ([#9919](https://github.com/tektoncd/pipeline/pull/9919))
- **Skip SetDefaults on completed TaskRuns**: Defaulting logic is no longer invoked on the hot path for done TaskRuns ([#9921](https://github.com/tektoncd/pipeline/pull/9921))
- **Faster label/annotation comparison**: `maps.Equal` replaces `reflect.DeepEqual` for label and annotation comparisons, reducing allocations ([#9776](https://github.com/tektoncd/pipeline/pull/9776))

## Better TaskRun Failure Reasons

TaskRun failure reasons now distinguish between different pod-level failure types instead of reporting a generic "Failed" reason. The new reasons include:

- `PodEvicted` — pod was evicted by the kubelet
- `InitContainerOOM` / `InitContainerFailed` — init container issues
- `StepOOM` / `StepFailed` — step-level failures
- `SidecarOOM` / `SidecarFailed` — sidecar issues

This makes it much easier to diagnose why a TaskRun failed without digging into pod events.

See [#9368](https://github.com/tektoncd/pipeline/pull/9368) for details.

## Get Started

Install or upgrade to v1.12.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/previous/v1.12.0/release.yaml
```

Check out the full [release notes](https://github.com/tektoncd/pipeline/releases/tag/v1.12.0) and [documentation](https://github.com/tektoncd/pipeline/tree/v1.12.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
