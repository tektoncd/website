---
title: "Tekton Pipelines v1.17.0: Clearer Failures, Sharper Traces"
linkTitle: "Tekton Pipelines v1.17.0: Clearer Failures, Sharper Traces"
date: 2026-10-01
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.17.0 surfaces Pod infrastructure failures on TaskRun status, expands reconcile tracing, and hardens a Windows script-injection gap.
---

We're excited to announce the release of [Tekton Pipelines v1.17.0 "Egyptian Mau Robocop"](https://github.com/tektoncd/pipeline/releases/tag/v1.17.0)!

🎉 *Clearer failures, sharper traces* 🎉

## Surfacing Pod Infrastructure Failures

A new alpha feature flag `surface-pod-events` ([#10690](https://github.com/tektoncd/pipeline/pull/10690)) surfaces Pod infrastructure failure reasons — from Warning events such as `FailedMount`, `FailedScheduling`, and `FailedCreatePodSandBox` — directly onto the TaskRun status condition. Previously, a Pod stuck pending for infrastructure reasons produced an unhelpful, generic message. With this flag enabled, operators get an immediately actionable reason without digging through `kubectl describe pod`.

## Expanded Reconcile Tracing

Building on existing OpenTelemetry tracing support, this release adds:

- A `reconcile.write_intent` span attribute ([#10827](https://github.com/tektoncd/pipeline/pull/10827)) classifying each reconciliation as no-op, status-only, metadata-only, or metadata-and-status — making it easier to spot reconciliations that trigger an etcd write.
- Tagging of TaskRun `ReconcileKind` spans on cancellation and timeout ([#10664](https://github.com/tektoncd/pipeline/pull/10664)), so these terminal paths are distinguishable in traces.

## Security Fix: Windows Script Injection

A defense-in-depth gap in Windows script handling has been closed ([#10822](https://github.com/tektoncd/pipeline/pull/10822)). `placeScriptInContainer` now uses a non-expandable PowerShell here-string, so a script body containing a literal `"@` line can no longer terminate the generated command early.

## Additional Fixes

- **Task resolution errors now include the task name** ([#10800](https://github.com/tektoncd/pipeline/pull/10800)), making it much easier to tell which task failed to resolve.
- **`tt.params` as a valid variable-reference prefix** ([#10688](https://github.com/tektoncd/pipeline/pull/10688)): Pipelines can now reference `$(tt.params.<name>)` in task params, `when` expressions, and matrix params/includes, so a `PipelineSpec` embedded by Tekton Triggers keeps its substitutions without failing validation.
- **Resolver isolation**: resolvers no longer fail `ResolutionRequests` belonging to a different resolver after a leader election or pod restart ([#10548](https://github.com/tektoncd/pipeline/pull/10548)).
- **Controller startup panic logs** now print the underlying error correctly instead of a malformed `%!w(...)` marker ([#10430](https://github.com/tektoncd/pipeline/pull/10430)).

## Get Started

Install or upgrade to v1.17.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/previous/v1.17.0/release.yaml
```

Check out the full [release notes](https://github.com/tektoncd/pipeline/releases/tag/v1.17.0) and [documentation](https://github.com/tektoncd/pipeline/tree/v1.17.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
