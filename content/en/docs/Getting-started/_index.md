---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 1
description: >
  Get started with Tekton
---

Tekton is an open-source, cloud-native CI/CD framework that runs on Kubernetes.
It lets you define pipelines as code, run tasks in isolated containers, and
integrate with any Git provider or artifact registry.

Check the [Concepts](/docs/concepts/) section to understand how Tasks, Pipelines,
and Runs fit together.

## Choose Your Path

{{< cards >}}
  {{< card link="/docs/getting-started/pipelines/" title="Build a Pipeline" icon="archive" subtitle="Chain multiple Tasks into a Pipeline that clones, tests, builds, and deploys." >}}
  {{< card link="/docs/getting-started/pipelines-as-code/" title="Pipelines as Code" icon="document-text" subtitle="Git-native CI/CD — define pipelines in a .tekton/ directory alongside your source." >}}
  {{< card link="/docs/getting-started/tasks/" title="Create Your First Task" icon="play" subtitle="Define a Task with steps, run it, and see the results — the fundamental building block." >}}
  {{< card link="/docs/getting-started/triggers/" title="Set Up Triggers" icon="lightning-bolt" subtitle="Automatically start Pipelines from Git push, PR events, or webhooks." >}}
  {{< card link="/docs/getting-started/supply-chain-security/" title="Supply Chain Security" icon="shield-check" subtitle="Sign and attest your build artifacts with Tekton Chains." >}}
{{< /cards >}}

## What You'll Need

- A **Kubernetes cluster** (v1.27+) — [kind](https://kind.sigs.k8s.io/),
  [minikube](https://minikube.sigs.k8s.io/), or any managed cluster
- **kubectl** configured to talk to your cluster
- **Tekton Pipelines** installed — see the [Installation guide](/docs/installation/)

## Step-by-Step

1. **Install Tekton** on your cluster by following the
   [installation instructions](/docs/installation/).

2. **Create your first Task** — a Task defines one or more steps that run in
   containers. Start with the [Tasks tutorial](/docs/getting-started/tasks/).

3. **Build a Pipeline** — combine Tasks into an end-to-end workflow. See the
   [Pipelines tutorial](/docs/getting-started/pipelines/).

4. **Automate with Triggers** — fire Pipelines from Git events. See
   [Triggers](/docs/getting-started/triggers/).

5. **Secure your supply chain** — add signing and attestation with
   [Tekton Chains](/docs/getting-started/supply-chain-security/).

## Git-Native CI/CD

For a fully Git-native experience, try
[Pipelines as Code](https://pipelinesascode.com/docs/getting-started/).
Define your pipelines in a `.tekton/` directory and get automatic PR checks
with GitHub, GitLab, Bitbucket, or Forgejo.
