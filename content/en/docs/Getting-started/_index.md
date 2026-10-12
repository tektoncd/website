---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 1
no_list: true
---

Tekton is an open-source, cloud-native CI/CD framework that runs on Kubernetes.
It lets you define pipelines as code, run tasks in isolated containers, and
integrate with any Git provider or artifact registry.

Check the [Concepts](/docs/concepts/) section to understand how Tasks, Pipelines,
and Runs fit together.

## Choose Your Path

<div class="docs-landing-grid">

<a href="/docs/getting-started/pipelines/" class="docs-landing-card">
  <h3 class="docs-landing-title">Build a Pipeline</h3>
  <p class="docs-landing-desc">Chain multiple Tasks into a Pipeline that clones, tests, builds, and deploys.</p>
</a>

<a href="/docs/getting-started/pipelines-as-code/" class="docs-landing-card">
  <h3 class="docs-landing-title">Pipelines as Code</h3>
  <p class="docs-landing-desc">Git-native CI/CD — define pipelines in a <code>.tekton/</code> directory alongside your source.</p>
</a>

<a href="/docs/getting-started/tasks/" class="docs-landing-card">
  <h3 class="docs-landing-title">Create Your First Task</h3>
  <p class="docs-landing-desc">Define a Task with steps, run it, and see the results — the fundamental building block.</p>
</a>

<a href="/docs/getting-started/triggers/" class="docs-landing-card">
  <h3 class="docs-landing-title">Set Up Triggers</h3>
  <p class="docs-landing-desc">Automatically start Pipelines from Git push, PR events, or webhooks.</p>
</a>

<a href="/docs/getting-started/supply-chain-security/" class="docs-landing-card">
  <h3 class="docs-landing-title">Supply Chain Security</h3>
  <p class="docs-landing-desc">Sign and attest your build artifacts with Tekton Chains.</p>
</a>

</div>

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
