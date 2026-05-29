---
title: "Tekton Pipelines v1.13.0: Compressed Results, Timeout Fixes, and Observability"
linkTitle: "Tekton Pipelines v1.13.0: Compressed Results, Timeout Fixes, and Observability"
date: 2026-05-29
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.13.0 brings termination message compression to fit more results in the 4KB limit, fixes finally tasks not running on timeout, and adds OpenTelemetry tracing to the notifications controller.
---

We're excited to announce the release of [Tekton Pipelines v1.13.0 "Pixie-bob Project 2501"](https://github.com/tektoncd/pipeline/releases/tag/v1.13.0)!

🎉 *Squeezing more out of every pipeline: compressed results & timeout fixes* 🎉

## Termination Message Compression

The biggest new feature is optional termination message compression ([#9682](https://github.com/tektoncd/pipeline/pull/9682)). Kubernetes limits termination messages to 4KB, which constrains how many results a Task step can produce. With the new alpha feature flag `enable-termination-message-compression`, Tekton now uses flate compression to fit approximately **5.7x more results** in the same 4KB limit.

Key details:
- **Zero new dependencies** — uses Go stdlib only
- **Full backward compatibility** — the parser auto-detects compressed messages
- Enable with: `enable-termination-message-compression: "true"` in `feature-flags` ConfigMap (requires `enable-api-fields: "alpha"`)

## Finally Tasks Now Run After Tasks Timeout

A long-standing bug ([#6794](https://github.com/tektoncd/pipeline/issues/6794)) caused finally tasks to be skipped when the `tasks` timeout was exceeded. The PipelineRun was immediately marked as Failed without giving finally tasks a chance to run — defeating the purpose of having cleanup tasks.

This is now fixed ([#9709](https://github.com/tektoncd/pipeline/pull/9709)). When tasks timeout but finally tasks still need to run, the pipeline continues with reason `PipelineRunTimeoutRunningFinally` until finally tasks complete, mirroring the existing `CancelledRunningFinally` pattern.

## TEP-0137: CloudEvents Formats Configuration

Building on v1.12.0's notifications controllers, the `formats` field in `config-events` is now active ([#9776](https://github.com/tektoncd/pipeline/pull/9776)). The default value is `tektonv1`, which preserves existing behaviour. Setting an invalid or unrecognised format value logs a warning and suppresses event emission for that format.

## OpenTelemetry Tracing for Notifications

The TaskRun notifications controller now emits OpenTelemetry spans ([#9912](https://github.com/tektoncd/pipeline/pull/9912)), covering `ReconcileKind`, `ReconcileRunObject`, and `EmitCloudEvents`. This enables operators to trace CloudEvent delivery latency end-to-end.

## Additional Fixes

- **Affinity assistant volume names**: Long workspace names no longer cause StatefulSet failures — names are automatically truncated with a hash suffix to stay within the 63-character Kubernetes limit ([#9752](https://github.com/tektoncd/pipeline/pull/9752))
- **Default resource requirements**: Internal containers (entrypoint, sidecar-logresults, etc.) now inherit default resource requirements from `config-defaults`, preventing scheduling issues on clusters with LimitRange policies ([#9366](https://github.com/tektoncd/pipeline/pull/9366))
- **Resolver cache TTL**: Per-resolver TTL values in individual resolver ConfigMaps are now correctly respected instead of always falling back to the global TTL ([#9625](https://github.com/tektoncd/pipeline/pull/9625))
- **Resolver validation**: Resolvers now only permit resolving StepActions, Tasks, and Pipelines — arbitrary data resolution is no longer allowed ([#9588](https://github.com/tektoncd/pipeline/pull/9588))

## Upgrade Notice

**Resolver validation** ([#9588](https://github.com/tektoncd/pipeline/pull/9588)): Tekton Resolvers are now only permitted to resolve StepActions, Tasks, and Pipelines. Custom resolvers or ResolutionRequests which use the Resolver API for other object types will no longer function.

## Get Started

Install or upgrade to v1.13.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/previous/v1.13.0/release.yaml
```

Check out the full [release notes](https://github.com/tektoncd/pipeline/releases/tag/v1.13.0) and [documentation](https://github.com/tektoncd/pipeline/tree/v1.13.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
