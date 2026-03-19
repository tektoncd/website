---
title: Pipelines-as-Code Joins the Tekton Organization
linkTitle: Pipelines-as-Code Joins the Tekton Organization
date: 2026-03-19
author: "Chmouel Boudjnah, Red Hat"
description: >
  Pipelines-as-Code is now an official Tekton project at tektoncd/pipelines-as-code
---

We're excited to announce that Pipelines-as-Code (PAC) is now an official
Tekton project! After nearly four years under the `openshift-pipelines`
organization where it was first created in April 2021, PAC has found its
permanent home in the `tektoncd` organization at
[github.com/tektoncd/pipelines-as-code](https://github.com/tektoncd/pipelines-as-code).
GitHub automatically redirects requests from the old URL, so no action is needed.

## What Is Pipelines-as-Code?

Pipelines-as-Code brings a Git-native workflow to Tekton. Instead of managing
pipeline definitions separately from your application code, PAC lets you store
them in a `.tekton/` directory alongside your source — versioned, reviewed, and
shipped together.

Key features:

- **Multi-provider support**: GitHub Apps and Webhooks, GitLab, Bitbucket Cloud
  and Data Center, and Forgejo
- **ChatOps**: trigger or cancel runs directly from pull request comments using
  `/test`, `/retest`, `/cancel`, or skip with `[skip ci]`
- **Inline task resolution**: PAC fetches remote tasks from Artifact Hub and
  resolves them before submitting to the cluster, so your pipelines stay
  self-contained
- **Automated housekeeping**: old PipelineRuns are pruned automatically, and
  superseded runs are cancelled when a new commit is pushed
- **No cluster changes required**: pipelines live with the code, making them
  easy to review, update, and roll back

## Matching in Action

Place a file like `.tekton/pull-request.yaml` in your repository:

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: pull-request
  annotations:
    pipelinesascode.tekton.dev/on-event: "[pull_request]"
    pipelinesascode.tekton.dev/on-target-branch: "[main]"
spec:
  pipelineSpec:
    tasks:
      - name: run-tests
        taskSpec:
          steps:
            - name: test
              image: alpine
              script: echo "tests passed"
```

PAC reads the annotations on each file in `.tekton/`, matches them against the
incoming webhook event and target branch, and submits only the matching
PipelineRuns to the cluster. Everything else is ignored.

## Get Started

Follow the tutorials and documentation to get started with Pipelines-as-Code at:

[pipelinesascode.com/docs/getting-started/](https://pipelinesascode.com/docs/getting-started/).

This will guide you through installing PAC in your cluster,
connecting a repository, and creating your first pull request-triggered pipeline
managed by PAC.

## Enterprise Adoption

Pipelines-as-Code is already running in production across organizations of all
sizes — from small teams shipping a handful of services to large engineering
organizations managing hundreds of repositories. Teams use PAC to standardize
CI/CD without requiring platform teams to manage pipeline definitions centrally.
Its Git-native model fits naturally into existing code review workflows, and
features like automatic pruning and run cancellation have proven valuable for
teams dealing with high commit velocity.

The multi-provider support has made it a practical choice for organizations that
operate across multiple Git hosting platforms simultaneously, and its lightweight
footprint means it scales equally well for smaller workloads.

## What's Next?

Moving to the `tektoncd` organization is more than a rename — it reflects PAC's
role as a core part of the Tekton ecosystem and opens the door to closer
collaboration with other Tekton projects and contributors.

The documentation is located at
[pipelinesascode.com](https://pipelinesascode.com/), and the code is located at
[github.com/tektoncd/pipelines-as-code](https://github.com/tektoncd/pipelines-as-code).

We welcome contributions of all kinds: bug reports, feature requests,
documentation improvements, and code. Join the conversation in the
[`#pipelinesascode` channel on the Tekton Slack](https://tektoncd.slack.com/archives/C04URDDJ9MZ),
[open an issue](https://github.com/tektoncd/pipelines-as-code/issues/new), or
browse [good first
issues](https://github.com/tektoncd/pipelines-as-code/issues?q=is%3Aopen+label%3A%22good+first+issue%22)
if you want to get started with code contributions.
