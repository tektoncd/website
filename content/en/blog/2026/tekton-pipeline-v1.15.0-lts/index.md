---
title: "Tekton Pipelines v1.15.0 LTS: Tracing, Resilient Resolution, and Battle-Tested Fixes"
linkTitle: "Tekton Pipelines v1.15.0 LTS"
date: 2026-08-18
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.15.0 is a Long Term Support (LTS) release featuring end-to-end OpenTelemetry tracing, configurable backoffs, a grace period for transient container errors, and critical fixes for resolution reliability, sidecar handling, and result extraction.
---

We're excited to announce the release of [Tekton Pipelines v1.15.0 "Toyger Orisa"](https://github.com/tektoncd/pipeline/releases/tag/v1.15.0)! This is a **Long Term Support (LTS)** release, supported until July 2027.

🎉 *Steady under pressure — end-to-end tracing, configurable backoffs and battle-tested fixes* 🎉

This post covers the highlights of both v1.14.0 and v1.15.0, since v1.14.0 was a regular release stepping stone to this LTS.

## What Makes This an LTS Release?

LTS releases receive security and critical bug fixes for an extended period. If you prefer stability over bleeding-edge features, LTS releases are your upgrade targets. The previous LTS was [v1.12.0]({{< relref "/blog/2026/tekton-pipeline-v1.12.0/index.md" >}}); users on v1.12.0 can upgrade directly to v1.15.0 with no breaking changes.

Read more about [LTS releases and our support policy](https://github.com/tektoncd/community/blob/main/releases.md#support-policy).

## End-to-End OpenTelemetry Tracing (v1.14.0)

The biggest theme of v1.14.0 was **comprehensive distributed tracing**, wiring OpenTelemetry spans throughout the entire reconciliation lifecycle:

- **Error recording on spans** — Pod creation failures and TaskRun/CustomRun creation errors are now recorded on trace spans ([#10273](https://github.com/tektoncd/pipeline/pull/10273), [#10272](https://github.com/tektoncd/pipeline/pull/10272))
- **Cancel and timeout paths** — PipelineRun cancellation and timeout code paths now emit spans ([#10269](https://github.com/tektoncd/pipeline/pull/10269))
- **Log-to-trace correlation** — TraceID and SpanID are injected into structured log output when tracing is enabled ([#10140](https://github.com/tektoncd/pipeline/pull/10140))
- **TaskRun validation spans** — Validation functions emit their own spans for finer-grained performance analysis ([#9907](https://github.com/tektoncd/pipeline/pull/9907))
- **Notifications controller tracing** — CustomRun and PipelineRun notifications reconcilers now have full OTel span coverage ([#10097](https://github.com/tektoncd/pipeline/pull/10097), [#10266](https://github.com/tektoncd/pipeline/pull/10266))

## Configurable Git Resolver Backoff (v1.15.0)

The git resolver now supports configurable backoff for requests ([#10422](https://github.com/tektoncd/pipeline/pull/10422)). This lets operators tune retry behavior for environments with flaky git connectivity, reducing unnecessary failures without overwhelming upstream servers.

## Grace Period for Transient Container Errors (v1.15.0)

A new `default-create-container-error-timeout` configuration option in `config-defaults` provides a grace period before failing TaskRuns on transient `CreateContainerError` / `CreateContainerConfigError` with "context deadline exceeded" ([#10326](https://github.com/tektoncd/pipeline/pull/10326)). The default is `0` (fail fast, preserving existing behavior), but operators can set a duration to ride out transient issues like image pull hiccups.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-defaults
  namespace: tekton-pipelines
data:
  default-create-container-error-timeout: "5m"
```

## Resolution Reliability (v1.15.0)

Several fixes make remote resolution significantly more robust:

- **ResolutionRequest status preservation** — Lifecycle updates no longer overwrite resolver-written status fields ([#10487](https://github.com/tektoncd/pipeline/pull/10487))
- **Leader-election bucket ownership** — Resolver replicas no longer process ResolutionRequests outside their leader-election bucket ([#10480](https://github.com/tektoncd/pipeline/pull/10480))
- **Stuck PipelineRuns** — PipelineRuns stuck in `ResolvingTaskRef` when a ResolutionRequest completion event is missed are now periodically requeued ([#10429](https://github.com/tektoncd/pipeline/pull/10429))
- **All Tekton kinds** — ResolutionRequests can now resolve PipelineRuns, TaskRuns, Runs, and CustomRuns in addition to the previously supported Pipelines, Tasks, and StepActions ([#10242](https://github.com/tektoncd/pipeline/pull/10242), v1.14.0)

## Sidecar and Result Fixes (v1.15.0)

- **Sidecar-logs result extraction** — Fixed a regression (since v1.9.0) that dropped *all* TaskRun results when a single result's JSON exceeded 4096 bytes but was within the configured `max-result-size` ([#10403](https://github.com/tektoncd/pipeline/pull/10403))
- **Sidecar restartPolicy preservation** — The `restartPolicy` field (native Kubernetes sidecar support) is no longer dropped during v1beta1 ↔ v1 API conversion ([#10392](https://github.com/tektoncd/pipeline/pull/10392))

## Validation and Stability

- **Stricter pipeline variable validation** — Pipeline validation now rejects invalid variable references like `$(new_image)` in task parameters with a clear error message, instead of silently accepting them ([#10050](https://github.com/tektoncd/pipeline/pull/10050), v1.14.0)
- **Cross-architecture entrypoint fix** — Fixed `"could not find command for platform"` errors when the controller and worker nodes run on different CPU architectures ([#10077](https://github.com/tektoncd/pipeline/pull/10077), v1.14.0)
- **Matrix overflow guard** — Fixed an integer overflow in matrix combination counting that could bypass `max-matrix-combinations` validation ([#10431](https://github.com/tektoncd/pipeline/pull/10431))
- **Debug script mount** — Debug breakpoint scripts are now mounted read-only in step containers ([#10362](https://github.com/tektoncd/pipeline/pull/10362))
- **RestrictLength panic** — Fixed a panic when a PipelineRun with an embedded pipeline spec sets a `generateName` with no alphanumeric characters ([#10421](https://github.com/tektoncd/pipeline/pull/10421))
- **Concurrent map writes** — Fixed a controller crash when resolving multiple StepAction references with object parameters ([#10324](https://github.com/tektoncd/pipeline/pull/10324), v1.14.0)

## Upgrade Path from Previous LTS

| From | To | Key Considerations |
|------|----|--------------------|
| v1.12.0 LTS | v1.15.0 LTS | Smooth upgrade; new features are opt-in via ConfigMap |
| v1.9.0 LTS | v1.15.0 LTS | Review [v1.12.0 LTS blog]({{< relref "/blog/2026/tekton-pipeline-v1.12.0/index.md" >}}) for notifications controller changes |

## Get Started

Install or upgrade to v1.15.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/previous/v1.15.0/release.yaml
```

Check out the full release notes for [v1.14.0](https://github.com/tektoncd/pipeline/releases/tag/v1.14.0) and [v1.15.0](https://github.com/tektoncd/pipeline/releases/tag/v1.15.0), and the [documentation](https://github.com/tektoncd/pipeline/tree/v1.15.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
