---
title: "Tekton Pipelines Reaches 1.0: Stability Today, Innovation Tomorrow"
linkTitle: "Tekton Pipelines Reaches 1.0: Stability Today, Innovation Tomorrow"
date: 2025-05-23
author: "Vincent Demeester, Red Hat"
description: >
  Tekton Pipeline component v1.0.0 release announcement.
---

We're thrilled to announce the official 1.0 release of the Tekton Pipelines component ([`tektoncd/pipeline`](https://github.com/tektoncd/pipeline) repository) ! While this marks a significant milestone for the project, it's important to note that the stability you've come to rely on with the v1 API has been a reality for over two years. This release solidifies that foundation while paving the way for even more exciting changes in the Tekton ecosystem.

The version 1.0 brings several key updates, reinforcing the project's commitment to stability and a streamlined user experience. Notably, the `StepAction` feature has graduated to General Availability (GA), signifying its maturity and readiness for production use.
Furthermore, this release includes significant enhancements and bug fixes for the Git resolver, improving its reliability and performance. We've also seen the recent introduction and ongoing development of the HTTP resolver, offering greater flexibility in how your pipelines fetch tasks and other resources. You can learn more about resolvers and their capabilities in the [Tekton documentation](https://tekton.dev/docs/pipelines/resolution/).
Finally, the deprecated `ClusterTask` resource has been removed, encouraging the adoption of the more flexible and namespaced `Task` resource or the use of the cluster resolver.

The 1.0 release is not the finish line; it's a significant step forward on an exciting journey and one we could or should have done a while ago. Looking ahead, we'll be focused on stability, performance and user experience.

- Graduate `StepAction` to the v1 API, ensuring long-term stability and support for this powerful feature.
- Working towards a `v2` of the resolvers, with a strong focus on improving both usability and performance.
- Investing in better observability and metrics to provide users with clearer insights into their Pipeline executions.

Our goal is to make Tekton Pipelines even more intuitive and efficient for developers and operators alike.

Independently of the release, we are also making a significant step in the evolution of the Tekton project as we transition to the Cloud Native Computing Foundation (CNCF). You can follow the progress of this transition in the [CNCF TOC issue](https://github.com/cncf/toc/issues/1310). Joining the CNCF will provide Tekton with a neutral home and access to a vibrant and supportive ecosystem. This move will foster even greater collaboration, expand our community reach, and ensure the long-term sustainability and growth of Tekton Pipelines for the benefit of all cloud-native practitioners.

We invite you to explore the 1.0 release, engage with our growing community, and contribute to the future of cloud-native CI/CD. The best is yet to come!
