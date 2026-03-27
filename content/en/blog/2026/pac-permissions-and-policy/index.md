---
title: "Understanding Permissions and Policy in Pipelines-as-Code"
linkTitle: "Permissions and Policy in Pipelines-as-Code"
date: 2026-03-27
author: "Chmouel Boudjnah, Red Hat"
description: >
  How Pipelines-as-Code controls who can trigger pipelines from Git events,
  from default authorization checks to fine-grained per-repository policy configuration.
---

When CI/CD pipelines are triggered directly from Git events, controlling *who*
can run those pipelines becomes a critical security concern. An unreviewed pull
request from an external contributor could execute arbitrary code in your CI
environment. Pipelines-as-Code (PAC) addresses this with a layered
authorization model that balances security with usability.

This post walks through how PAC decides whether to run a pipeline, from the
default checks that happen automatically to the fine-grained policy system you
can configure per repository.

## Default Authorization

When no explicit policy is configured, PAC applies a series of checks (on
GitHub) to determine whether the sender of an event is allowed to trigger a
pipeline. These checks run in order, and the first one that succeeds grants
access:

1. **Repository owner** -- If the sender's username matches the repository
   owner (i.e., this is a personal repository), they are always allowed.

2. **Same-repository pull request** -- If a pull request's head and base come
   from the same repository (different branches, not a fork), the sender is
   allowed. This covers bots like Dependabot or Renovate that push branches
   directly.

3. **Organization membership** -- If the sender is a public member of the
   organization that owns the repository, they are allowed.

4. **Repository collaborator** -- If the sender is a collaborator on the
   repository (with any permission level), they are allowed.

5. **OWNERS file** -- As a final fallback, PAC checks for a Prow-compatible
   `OWNERS` file in the default branch of the repository. If the sender is
   listed there, they are allowed (more on this below).

If none of these checks pass, the pipeline is **not** triggered, and the pull
request is left in a pending state waiting for approval.

## Approving External Contributors with `/ok-to-test`

For contributors who are not collaborators or org members (typically first-time
or external contributors), PAC provides the `/ok-to-test` comment mechanism.

An authorized user (someone who passes the checks above) can comment
`/ok-to-test` on a pull request to approve it for CI. Once approved, PAC
triggers the pipeline for that PR.

Related commands:

- `/test <pipeline-name>` -- Trigger a specific pipeline (same authorization
  rules as `/ok-to-test`).
- `/retest <pipeline-name>` -- Re-trigger only **failed** pipelines. This
  distinction is intentional: `/retest` will not re-run successful pipelines,
  which prevents abuse.

### Remembering Approvals Across Pushes

By default, every new push to an approved PR requires a new `/ok-to-test`
comment. This is the most secure behavior but can be tedious for active PRs
from trusted external contributors.

The `remember-ok-to-test` setting (in the `pipelines-as-code` ConfigMap)
changes this behavior. When enabled, PAC scans previous comments on the PR
looking for an `/ok-to-test` from an authorized user. If found, the new push
is automatically approved without requiring another comment.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pipelines-as-code
  namespace: pipelines-as-code
data:
  remember-ok-to-test: "true"
```

> **Security consideration:** Enabling `remember-ok-to-test` means that once a
> contributor is approved, all their subsequent pushes to the same PR run CI
> automatically -- without further review. A contributor whose initial commits
> looked harmless could later push malicious code that executes in your CI
> environment without anyone explicitly approving it. Keep this setting
> disabled (the default) if your threat model includes contributors who may
> turn hostile after gaining initial trust, or combine it with
> `require-ok-to-test-sha` to at least pin approvals to specific commits.

### Preventing Race Conditions with SHA Verification

There is a subtle attack vector: a malicious contributor could push a bad
commit right after an `/ok-to-test` comment is posted but before the CI picks
it up. The `require-ok-to-test-sha` setting addresses this by requiring the
`/ok-to-test` comment to include the specific commit SHA being approved:

```
/ok-to-test abc123def
```

This ensures the approval is pinned to a specific commit, not just the PR in
general.

## Policy-Based Access Control

The default checks work well for small teams, but larger organizations often
need more precise control. PAC supports team-based policies configured
directly in the Repository custom resource.

### Configuring Policies

Policies are defined under `spec.settings.policy` in the Repository CR:

```yaml
apiVersion: "pipelinesascode.tekton.dev/v1alpha1"
kind: Repository
metadata:
  name: my-repo
spec:
  url: "https://github.com/my-org/my-repo"
  settings:
    policy:
      ok_to_test:
        - ci-admins
      pull_request:
        - ci-users
```

Two actions can be controlled:

- **`pull_request`** -- Restricts who can trigger CI on their own pull
  requests. When set, *only* members of the listed teams can trigger pipelines,
  regardless of whether they are org owners or collaborators.

- **`ok_to_test`** -- Restricts who can approve external PRs via `/ok-to-test`
  or `/retest` comments. This is independent from the `pull_request` policy:
  `pull_request` controls who can trigger CI from their own PRs, while
  `ok_to_test` controls who can approve someone else's PR via comments.

The team names refer to **GitHub organization teams**. PAC checks team
membership via the GitHub API.

### How Policy Interacts with Other Checks

When a policy is set, it changes the authorization flow:

1. **Policy allows** -- The sender is a member of one of the listed teams.
   Pipeline runs immediately.
2. **Policy denies** -- The sender is not in any listed team. PAC then falls
   back to the **OWNERS file**. If the sender is listed in OWNERS, they are
   still allowed.
3. **Policy not set** -- The regular default checks (owner, collaborator, org
   member, etc.) apply as described above.

This design means OWNERS file members always have a path to trigger pipelines,
even when they are not part of the policy teams.

### Security-Conservative Defaults

PAC takes a deliberately conservative approach:

- **Empty policy list = deny all.** If you set `pull_request: []` (an empty
  list), no one can trigger CI through that action (except OWNERS file
  members). This prevents accidental misconfiguration from granting broad
  access.

- **Unknown team = deny.** If a team name in the policy does not exist on the
  GitHub organization, PAC treats it as a denial rather than silently ignoring
  it. This surfaces configuration errors immediately.

## The OWNERS File

PAC supports a Prow-compatible `OWNERS` file as a fallback authorization
mechanism. The file is read from the **default branch** of the repository (not
the PR branch), so contributors cannot grant themselves access by modifying it
in their PR.

A basic OWNERS file:

```yaml
approvers:
  - alice
  - bob
reviewers:
  - charlie
```

Both `approvers` and `reviewers` are treated as authorized users for CI
purposes.

### Aliases

For larger teams, you can use an `OWNERS_ALIASES` file to define groups:

```yaml
aliases:
  core-team:
    - alice
    - bob
    - charlie
  ci-team:
    - dave
    - eve
```

Then reference the alias in OWNERS:

```yaml
approvers:
  - core-team
reviewers:
  - ci-team
```

### Filters

OWNERS also supports a filters-based format. When filters are used, PAC
matches against the `.*` filter (all files):

```yaml
filters:
  ".*":
    approvers:
      - alice
    reviewers:
      - bob
```

## Provider Support

The policy system (team-based `pull_request` and `ok_to_test` actions) is
currently supported on:

| Provider | Policy Support |
|----------|---------------|
| GitHub App | Full |
| GitHub Webhook | Full |
| Forgejo/Gitea | Full |
| GitLab | Not supported |
| Bitbucket Cloud | Not supported |
| Bitbucket Data Center | Not supported |

The default ACL checks (collaborator, org member, OWNERS file) and the
`/ok-to-test` mechanism work across all providers, though the exact checks
vary by provider capabilities.

> **Note:** If you accidentally configure a policy on an unsupported provider,
> it will deny all users (since team membership checks always fail), falling
> back only to the OWNERS file. It is not silently ignored.

## Summary

PAC's authorization model provides defense in depth:

- **Default checks** cover the common case where org members and collaborators
  should be able to run CI freely.
- **`/ok-to-test`** gives a controlled path for external contributors, with
  options to remember approvals or require SHA pinning.
- **Policies** let you restrict CI to specific teams when you need tighter
  control than collaborator-level access.
- **OWNERS files** serve as a repo-level override that works regardless of
  policy settings.

For more details, see the
[Policy on Actions](https://pipelinesascode.com/docs/advanced/policy-authorization/)
documentation.
