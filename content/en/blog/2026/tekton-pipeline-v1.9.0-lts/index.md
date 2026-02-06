---
title: "Tekton Pipelines v1.9.0 LTS: Continued Innovation and Stability"
linkTitle: "Tekton Pipelines v1.9.0 LTS"
date: 2026-02-02
author: "Vincent Demeester, Red Hat"
description: >
  Announcing Tekton Pipeline v1.9.0 LTS with a summary of all the improvements since v1.0.0.
---

We're excited to announce the release of Tekton Pipelines v1.9.0, our latest Long-Term Support (LTS) release! Since the milestone [v1.0.0 release](https://github.com/tektoncd/pipeline/releases/tag/v1.0.0) in May 2025, the project has continued to evolve with significant new features, performance improvements, and stability enhancements. This post summarizes the journey from v1.0.0 to v1.9.0, organized by LTS milestones.

## Installation

```shell
kubectl apply -f https://infra.tekton.dev/releases/pipeline/previous/v1.9.0/release.yaml
```

## v1.0.0 → v1.3.0 LTS (May - August 2025)

The first LTS after v1.0.0 focused on **controller resilience and performance**.

### Features

- **Exponential backoff retry** - Improved handling of transient webhook issues during Pod, TaskRun, and CustomRun creation. Configurable via the `wait-exponential-backoff` ConfigMap. [Documentation](https://tekton.dev/docs/pipelines/additional-configs/#exponential-backoff-for-taskrun-and-customrun-creation)

- **Controller HA improvements** - Anti-affinity rules ensure controller replicas are scheduled on different nodes for better availability

- **PodTemplate param substitution** - Enables multi-arch builds with Matrix by allowing param substitution in TaskRunSpecs' PodTemplate. This lets you target nodes with specific architectures. [Documentation](https://tekton.dev/docs/pipelines/matrix/)
  
  ```yaml
  apiVersion: tekton.dev/v1
  kind: PipelineRun
  metadata:
    name: multi-arch-build
  spec:
    pipelineSpec:
      tasks:
      - name: build
        matrix:
          params:
          - name: arch
            value: ["amd64", "arm64"]
        taskSpec:
          steps:
          - name: build
            image: golang:1.21
            script: |
              echo "Building for $(params.arch)"
              GOARCH=$(params.arch) go build -o app-$(params.arch) .
        # PodTemplate with param substitution to schedule on correct architecture
        podTemplate:
          nodeSelector:
            kubernetes.io/arch: $(params.arch)
  ```

- **Configurable threading** - `THREADS_PER_CONTROLLER` environment variable for tuning controller performance based on cluster size

- **OOM detection** - TaskRuns that fail due to Out-Of-Memory (OOM) conditions now clearly show the termination reason in status

### Fixes

- Retryable validation errors no longer fail PipelineRuns
- PVC cleanup improvements - already-deleted PVCs no longer cause errors
- Fixed `managed-by` annotation propagation to Pods

### Breaking Changes

- **Deprecated metrics removed** - Use `pipelinerun_total` instead of `pipelinerun_count`, `taskrun_total` instead of `taskrun_count`, etc.
- **linux/arm images dropped** - armv5, armv6, armv7 are no longer supported

## v1.3.0 LTS → v1.6.0 LTS (August - October 2025)

The second LTS brought **major new features** for remote resolution and pipeline composition.

### Features

- **Resolvers caching** - Automatic caching for bundle, git, and cluster resolvers. Three modes available: `always`, `never`, and `auto` (default, caches only immutable references). Configurable cache size and TTL via ConfigMap.

  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: resolvers-feature-flags
    namespace: tekton-pipelines-resolvers
  data:
    enable-bundles-resolver-caching: "true"
    bundles-resolver-cache-ttl: "1h"
    bundles-resolver-cache-size: "100"
  ```

- **Pipelines-in-Pipelines ([TEP-0056](https://github.com/tektoncd/community/blob/main/teps/0056-pipelines-in-pipelines.md))** - Reference existing Pipelines as tasks within another Pipeline, enabling powerful composition and reuse patterns. [Documentation](https://tekton.dev/docs/pipelines/pipelines-in-pipelines/)

  ```yaml
  apiVersion: tekton.dev/v1
  kind: Pipeline
  metadata:
    name: integration-pipeline
  spec:
    tasks:
    - name: run-unit-tests
      taskRef:
        name: unit-test-pipeline
        kind: Pipeline
    - name: run-e2e-tests
      taskRef:
        name: e2e-test-pipeline
        kind: Pipeline
      runAfter:
      - run-unit-tests
  ```

- **`managedBy` field** - Delegate PipelineRun/TaskRun lifecycle control to external controllers for custom orchestration scenarios. [Documentation](https://tekton.dev/docs/pipelines/pipelineruns/#delegating-reconciliation)

  ```yaml
  apiVersion: tekton.dev/v1
  kind: PipelineRun
  metadata:
    name: externally-managed
  spec:
    managedBy: custom-orchestrator
    pipelineRef:
      name: my-pipeline
  ```

- **Concurrent StepActions resolution** - Significantly faster TaskRun startup when using multiple remote StepActions

- **Task timeout overrides** - Override individual task timeouts via `spec.taskRunSpecs[].timeout`. [Documentation](https://tekton.dev/docs/pipelines/pipelineruns/#specifying-taskrunspecs)

  ```yaml
  apiVersion: tekton.dev/v1
  kind: PipelineRun
  metadata:
    name: custom-timeouts
  spec:
    pipelineRef:
      name: my-pipeline
    taskRunSpecs:
    - pipelineTaskName: slow-task
      timeout: 2h
  ```

- **Quota-aware PVC handling** - PipelineRuns wait for quota availability instead of failing immediately

- **Array values in When expressions** - More flexible conditional execution. [Documentation](https://tekton.dev/docs/pipelines/pipelines/#guard-task-execution-using-when-expressions)

- **Step displayName** - Human-readable names for steps for better observability

- **ARM64 tested releases** - E2E tests now run on ARM64 architecture

### Fixes

- Fixed signal handling in SidecarLog for Kubernetes-native sidecar functionality
- Pods for timed-out TaskRuns are now retained when `keep-pod-on-cancel` is enabled
- Correct step status ordering when using StepActions

## v1.6.0 LTS → v1.9.0 LTS (October 2025 - January 2026)

The latest LTS focuses on **stability, observability, and pod configuration**.

### Features

- **`hostUsers` field in PodTemplate** - Control user namespace isolation for Task pods. [Documentation](https://tekton.dev/docs/pipelines/podtemplates/)

  ```yaml
  apiVersion: tekton.dev/v1
  kind: TaskRun
  metadata:
    name: secure-task
  spec:
    podTemplate:
      hostUsers: false
    taskSpec:
      steps:
      - name: run
        image: alpine
        script: echo "Running with user namespace isolation"
  ```

- **Digest validation for HTTP resolver** - Ensure integrity of remotely fetched resources by validating SHA256 digests

- **ServiceAccount inheritance for Affinity Assistants** - Better workspace management with proper credentials

- **Improved error messages** - Actual result size now included when exceeding `maxResultSize` for easier troubleshooting

### Fixes

- **Major performance fix** - Resolved issues causing massive invalid status updates that impacted API server load and stability
- **Parameter resolution** - Fixed defaults with object references
- **Timeout handling** - Prevented excessive reconciliation when timeout is disabled
- **Pod configuration errors** - Early detection instead of waiting for timeout
- **Race conditions** - Fixed TaskRun status issues during timeout handling
- **Sidecar stopping** - Fixed 409 conflict errors by using Patch instead of Update
- **Matrix validation** - Prevented panics from invalid result references (v1beta1)

## LTS Support Policy

With v1.9.0 being an LTS release, it will receive security and critical bug fixes for an extended period. Users upgrading from previous LTS versions can expect a smooth transition:

| From | To | Key Considerations |
|------|----|--------------------|
| v1.0.0 | v1.3.0 LTS | Update metric dashboards for renamed metrics |
| v1.3.0 LTS | v1.6.0 LTS | Smooth upgrade, new features opt-in |
| v1.6.0 LTS | v1.9.0 LTS | Smooth upgrade, stability improvements |

Read more about [LTS releases and our support policy](https://github.com/tektoncd/community/blob/main/releases.md#support-policy).

## Looking Ahead

The Tekton Pipelines project continues to focus on:

- **Performance** - Reducing reconciliation overhead and improving startup times
- **User experience** - Better error messages, observability, and debugging tools
- **Resolver improvements** - Working towards v2 resolvers with enhanced caching and usability
- **Kueue integration ([TEP-0164](https://github.com/tektoncd/community/pull/1241))** - Native support for [Kueue](https://kueue.sigs.k8s.io/) job queueing to enable better resource management and fair-sharing in multi-tenant environments

We're also making progress on our transition to the [Cloud Native Computing Foundation (CNCF)](https://github.com/cncf/toc/issues/1310), which will provide Tekton with a neutral home and access to a broader ecosystem.

## Get Involved

We invite you to try v1.9.0 LTS, provide feedback, and contribute to the project:

- [GitHub Repository](https://github.com/tektoncd/pipeline)
- [Documentation](https://tekton.dev/docs/)
- [Community Slack](https://tektoncd.slack.com) (#tekton)
- [Release Notes](https://github.com/tektoncd/pipeline/releases/tag/v1.9.0)

Thank you to all the contributors who made these releases possible!
