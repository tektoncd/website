---
title: "Getting Started with Pipelines as Code"
linkTitle: "Pipelines as Code"
weight: 2
description: >
  Use Pipelines as Code for Git-native CI/CD with Tekton
---

[Pipelines as Code](https://pipelinesascode.com/) lets you define your CI/CD
pipelines using Tekton PipelineRuns and Tasks in files stored directly alongside
your source code — versioned, reviewed, and collaborated on just like your
application code.

## Why Pipelines as Code?

- **Git-native**: Pipeline definitions live in a `.tekton/` directory in your repo
- **Automatic PR checks**: Pipeline runs trigger on pull requests and pushes,
  with status reported directly on the PR
- **Multi-provider**: Works with GitHub, GitLab, Bitbucket, and Forgejo
- **GitOps commands**: Control pipelines from PR comments — `/retest`, `/test`,
  `/cancel`
- **Automatic resolution**: Tasks are resolved from your repo, Artifact Hub, or
  remote URLs

## Get Started

The fastest way to try Pipelines as Code:

1. **Install** on a [kind](https://kind.sigs.k8s.io/) cluster or
   [OpenShift Local](https://developers.redhat.com/products/openshift-local/overview):

   ```bash
   tkn pac bootstrap
   ```

2. **Create a repository** with a `.tekton/` directory containing your
   PipelineRun YAML.

3. **Open a Pull Request** and watch the pipeline run with status checks.

For the full walkthrough, see the
[Pipelines as Code Getting Started guide](https://pipelinesascode.com/docs/getting-started/).

## Learn More

{{< cards >}}
  {{< card link="https://pipelinesascode.com/docs/guide/" title="Authoring Guide" icon="book-open" subtitle="Learn how to author and structure your pipeline definitions." >}}
  {{< card link="https://pipelinesascode.com/docs/guide/gitops_commands/" title="GitOps Commands" icon="terminal" subtitle="Control pipeline runs directly from PR comments." >}}
  {{< card link="https://pipelinesascode.com/docs/guide/resolver/" title="Task Resolution" icon="search" subtitle="Automatic resolution from local files, Artifact Hub, and remote URLs." >}}
{{< /cards >}}
