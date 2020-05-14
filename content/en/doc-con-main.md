<!--
---
linkTitle: "Contributing to Tekton Documentation"
weight: 1
---
-->
# Contributing to Tekton Documentation

If you would like to contribute to Tekton documentation, we’re happy to have your help!
Anyone can contribute, whether you’re new to the project or you’ve been around a long time,
and whether you self-identify as a developer, an end user, or someone who just can’t stand
seeing typos.

This guide covers the following topics:

- [Contribution types](#contribution-types)
- [Contribution process](#contribution-process)
- [Requesting a documentation improvement](#requesting-a-documentation-improvement)
- [Submitting a documentation change](#submitting-a-documentation-change)
- [I need help!](#i-need-help)

Before you begin contributing, you should also read the following:

- [Content guidelines for Tekton documentation](doc-con-content.md)
- [Formatting conventions for Tekton documentation](doc-con-formatting.md)
- [Writing high quality documentation for Tekton](doc-con-writing.md)

## Contribution types

You can request an improvement by filing an issue or update the documentation yourself by
filing a pull request against the relevant [Tekton repository](https://github.com/tektoncd).
Assign your issue or pull request to @sergetron, Tekton's technical writer, for triage.

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

Assign the pull request and if applicable, the accompanying issue to @sergetron, Tekton's
technical writer. The pull request then goes through technical and editorial review, and is
published on the Tekton documentation website. Depending on our current workload, the review
may take some time. Once the review is complete, the pull request is published to the Tekton
documentation site.

Documentation contributions should be technically accurate and easy to understand. See the rest
of this guide to learn how to produce clear, concise, and informative documentation.

## Requesting a documentation improvement

**Example:** "You should document Tekton integration with Smurfcaptor.”

If you found a problem with Tekton documentation but can't fix it yourself, you can request a
documentation improvement by creating an issue against the relevant [Tekton repository](https://github.com/tektoncd)
and assigning it to @sergetron, Tekton's technical writer. 

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
you must also [add it to the website's configuration](https://github.com/tektoncd/website/tree/master/sync/config)
so that it's picked up by the synchronization script and appears in the navigation tree in the
"Documentation" section. Depending on the content you're adding, you may also want to add links
to your new page to existing Tekton documentation.

## I need help!

If you're not sure how to address a certain documentation issue, join the
[#docs channel](https://app.slack.com/client/TJ45YV83X/CQYFEE00K) on the Tekton Slack and ask! 

Also, before and while you contribute, read the following topics:

- [Content guidelines for Tekton documentation](doc-con-content.md)
- [Formatting conventions for Tekton documentation](doc-con-formatting.md)
- [Writing high quality documentation for Tekton](doc-con-writing.md)
