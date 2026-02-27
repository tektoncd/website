---
title: "Tekton Pipelines v1.10.0: Observability, Evolved"
linkTitle: "Tekton Pipelines v1.10.0: Observability, Evolved"
date: 2026-02-27
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.10.0 migrates metrics from OpenCensus to OpenTelemetry, bringing modern observability to your CI/CD pipelines.
---

We're excited to announce the release of [Tekton Pipelines v1.10.0](https://github.com/tektoncd/pipeline/releases/tag/v1.10.0)! The headline for this release is a major infrastructure change: **the migration from OpenCensus to OpenTelemetry** for all metrics instrumentation.

## OpenCensus to OpenTelemetry Migration

[OpenCensus has been deprecated](https://opentelemetry.io/blog/2023/sunsetting-opencensus/) in favor of [OpenTelemetry](https://opentelemetry.io/), and Tekton Pipelines now follows suit. This release migrates all PipelineRun and TaskRun metrics to OpenTelemetry instruments — histograms, counters, and gauges — and updates the underlying Knative dependency to v1.19.

### What Changed

- **Infrastructure metrics renamed**: Go runtime, Workqueue, and K8s Client metrics move from the `tekton_pipelines_controller_` prefix to standard OpenTelemetry/Knative namespaces (e.g., `kn_workqueue_*`, `go_*`).
- **New `reason` label**: Duration metrics for PipelineRuns and TaskRuns now include a `reason` label (e.g., `Completed`, `Succeeded`) for more granular breakdown.
- **Removed metrics**: `tekton_pipelines_controller_reconcile_count` and `tekton_pipelines_controller_reconcile_latency` have been removed. Use `kn_workqueue_process_duration_seconds` and `kn_workqueue_adds_total` instead.
- **Preserved compatibility**: Core metrics like `pipelinerun_total`, `taskrun_total`, and `taskruns_pod_latency_milliseconds` retain their original names and labels.

### What You Need to Do

1. **Update your `config-observability` ConfigMap** to use `metrics-protocol: prometheus` (or `grpc`/`http`) instead of the old `metrics.backend-destination`. If you were already using Prometheus, no changes are needed.
2. **Update your dashboards**:
   - Replace `tekton_pipelines_controller_workqueue_*` queries with `kn_workqueue_*`
   - Replace `tekton_pipelines_controller_go_*` queries with standard `go_*` metrics
   - Account for the new `reason` label on duration metrics

See [PR #9043](https://github.com/tektoncd/pipeline/pull/9043) for the full migration table and details.

## Other Highlights

### New Features

- **SHA-256 support for Git resolver**: The Git resolver now validates SHA-256 commit hashes (64 characters), future-proofing for Git v3+ which will use SHA-256 instead of SHA-1. ([#9278](https://github.com/tektoncd/pipeline/pull/9278))

### Bug Fixes

- **Pipeline results from failed tasks**: Pipeline-level results now correctly include results from failed, cancelled, and timed-out tasks. Previously, results referencing non-successful task outputs were left as unresolved variable strings. ([#9367](https://github.com/tektoncd/pipeline/pull/9367))
- **Pipeline param defaults with context variables**: Fixed a bug where PipelineRun validation failed when a pipeline parameter's default value referenced a non-parameter variable like `$(context.pipelineRun.name)`. ([#9386](https://github.com/tektoncd/pipeline/pull/9386))
- **ResolutionRequest CRD on Kubernetes 1.33+**: Removed redundant `shortNames` from the ResolutionRequest CRD that caused `ShortNamesConflict` on Kubernetes 1.33+. ([#9398](https://github.com/tektoncd/pipeline/pull/9398))

## Get Started

Install or upgrade to v1.10.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/previous/v1.10.0/release.yaml
```

Check out the full [release notes](https://github.com/tektoncd/pipeline/releases/tag/v1.10.0) and [documentation](https://github.com/tektoncd/pipeline/tree/v1.10.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
