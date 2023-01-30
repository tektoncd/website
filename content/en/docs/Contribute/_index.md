<!--
---
title: "Contribute to Documentation"
linkTitle: "Contribute to Documentation"
weight: 0
description: > 
  Contribution guidelines
---
-->

If you would like to contribute to Tekton documentation, we’re happy to have your help!
Anyone can contribute, whether you’re new to the project or you’ve been around a long time,
and whether you self-identify as a developer, an end user, or someone who just can’t stand
seeing typos.

## Contribution types

You can request an improvement by filing an issue or update the documentation yourself by
filing a pull request against the relevant [Tekton repository](https://github.com/tektoncd).

Here's how we handle different types of documentation work:

- **A quick fix**, such as a typo or a simple clarification, can typically be submitted
  directly in a pull request.
- **A larger change**, such as updating an existing page or creating a brand new page,
  needs to be tracked by an issue. You can either request the update in the issue, or
  submit the update using a pull request linked to the issue.

## Contribution process

**Example:** “I want to update the Smurfcaptor tutorial for Tekton.”

If you're making a quick fix, such as a typo, or adding a few words of clarification, simply
submit a pull request against the relevant [Tekton repository](https://github.com/tektoncd).
If you're submitting a larger change, also create an issue that describes the new or updated
content and link the pull request to it.

**Note:** If you're creating a new page, make sure to include its proposed location within the
Tekton documentation set.

Assign the pull request and if applicable, the accompanying issue to one of the
[Tekton website approvers][approvers]. The pull request then goes through
technical and editorial review, and is published on the Tekton documentation
website. Depending on our current workload, the review may take some time. Once
the review is complete, the pull request is published to the Tekton
documentation site.

Documentation contributions should be technically accurate and easy to understand. See the rest
of this guide to learn how to produce clear, concise, and informative documentation.

[approvers]: https://github.com/tektoncd/website/blob/main/OWNERS

## Requesting a documentation improvement

**Example:** "You should document Tekton integration with Smurfcaptor.”

If you found a problem with Tekton documentation but can't fix it yourself, you can request a
documentation improvement by creating an issue against the relevant [Tekton repository](https://github.com/tektoncd)

We evaluate the need to determine the scope of the requested content and an estimated delivery
time based on our current workload. We then place the issue in the documentation queue.

Once a pull request is created that addresses the issue, it goes through technical and editorial
review, and is published on the Tekton documentation website.

## Submitting a documentation change

Submit a documentation change by opening a pull request against the relevant
[Tekton repository](https://github.com/tektoncd). Documentation for each project is stored
in the `docs` directory within the repository.

Tekton documentation is mirrored on the [Tekton website](https://tekton.dev) with the GitHub
repositories acting as the source of truth. If you are adding a new page to a project's documentation,
you must also [add it to the website's configuration](https://github.com/tektoncd/website/tree/main/sync/config)
so that it's picked up by the synchronization script and appears in the navigation tree in the
"Documentation" section. Depending on the content you're adding, you may also want to add links
to your new page to existing Tekton documentation.

## I need help!

If you're not sure how to address a certain documentation issue, join the
[#docs channel](https://app.slack.com/client/TJ45YV83X/CQYFEE00K) on the Tekton Slack and ask!

