---
title: "Tekton Pipelines v1.16.0: Secure by Default, Sharper Traces"
linkTitle: "Tekton Pipelines v1.16.0"
date: 2026-08-31
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipelines v1.16.0 enables restricted security contexts by default for Tekton-injected containers, adds new tracing spans for task parameter and workspace substitution, and fixes critical libcurl CVEs in the resolvers base image.
---

We're excited to announce the release of [Tekton Pipelines v1.16.0 "Manx WALL-E"](https://github.com/tektoncd/pipeline/releases/tag/v1.16.0)!

🎉 *Secure by default, sharper traces* 🎉

## Action Required: `set-security-context` Enabled by Default

The headline change in this release: the `set-security-context` feature flag now defaults to `true` ([#9589](https://github.com/tektoncd/pipeline/pull/9589), [#10680](https://github.com/tektoncd/pipeline/pull/10680)). Tekton-injected TaskRun containers and Affinity Assistants now get a restricted-compatible `SecurityContext` out of the box.

This applies only to containers Tekton itself injects — user-defined Steps and Sidecars are unaffected and must still supply their own restricted-compatible security contexts if you're running under a `restricted` Pod Security Standard.

**If the generated security contexts are incompatible with your images or Kubernetes implementation**, you can opt back out:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
  namespace: tekton-pipelines
data:
  set-security-context: "false"
```

## Sharper Tracing

Continuing the tracing work from recent releases:

- **Task parameter and workspace substitution spans** — the TaskRun reconciler now emits tracing spans around parameter and workspace variable substitution, improving observability into where reconciliation time is spent ([#10271](https://github.com/tektoncd/pipeline/pull/10271))
- **Root span lifecycle fix** — the root tracing span in TaskRun and PipelineRun reconcilers now covers the full reconciliation cycle instead of ending immediately after initialization, giving a more accurate picture of reconciliation duration ([#9699](https://github.com/tektoncd/pipeline/pull/9699))
- **CustomRun tracing test coverage** — added test coverage for `initTracing` span propagation in the notifications controller ([#10559](https://github.com/tektoncd/pipeline/pull/10559))

## Security Fix: libcurl CVEs in Resolvers Image

The `resolvers` container image's base (`tini-git`, built on Alpine) shipped `libcurl 8.14.1`, affected by several low-to-medium severity advisories: CVE-2026-8927, CVE-2026-8926, CVE-2026-11856, and CVE-2026-9079. This release bumps the base image to Alpine 3.24, which ships `libcurl 8.21.0` and resolves all applicable advisories ([#10642](https://github.com/tektoncd/pipeline/pull/10642)).

## Get Started

Install or upgrade to v1.16.0:

```shell
kubectl apply -f https://infra.tekton.dev/tekton-releases/pipeline/previous/v1.16.0/release.yaml
```

Check out the full [release notes](https://github.com/tektoncd/pipeline/releases/tag/v1.16.0) and [documentation](https://github.com/tektoncd/pipeline/tree/v1.16.0/docs) for more details.

---

*Have questions or feedback? Join us on [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*
