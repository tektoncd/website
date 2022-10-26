---
title: Tekton Graduation
likTitle: Tekton Graduation
date: 2022-10-26
author: "Andrea Frittoli"
description: >
  From founding project to graduated, a brief history of Tekton
---

We're very happy to announce that Tekton as reached graduated status within the
Continuous Delivery Foundation (CDF). The CDF Technical Oversight Committee
(TOC) conducted public [voting][voting-email] to decide on the graduation status
for Tekton, and the result was unanimously positive. The Tekton community is
very proud of the results of the vote and will continue working to make Tekton
better and safer for its users.

In this blog post I will explore a bit of the history of Tekton, its "road to
graduation" and what this milestone means for the project.

## Early Days

The Tekton project has its roots in [Knative][knative], where it is initially
called "Knative Build" and later "Knative Pipeline". The project is spun off in
August 2018, when it got it's current name and a new home on GitHub as
["tektoncd/pipeline"][pipeline-repo]. Here's one of the project's very first
commits:

```git
commit 49d2316d71e8c315e0a8fd76008bc2920f56b3c3
Author: Christie Wilson <bobcatfish@gmail.com>
Date:   Fri Aug 31 17:15:35 2018 -0700

Add pipeline strawman example

@dlorenc @ImJasonH @tejal29 @aaron-prindle and I have been working on a
strawman proposal for adding a Pipeline CRD and also for possibly
envolving the Build CRD into a slightly more generic Task CRD.

This PR demonstrates some paper prototype examples of what it could look
like to define pipelines using the CRDs described in the README.
```

A few months later, in March 2019, [Tekton is donated][cdf-creation-blog] to the
newly formed [Continuos Delivery Foundation (CDF)][cdf]. 

## Growing the community

Since then the project has thrived thanks to a rich community of contributors.
One of earlier repositories to be created is the community one, where the
project documented its governance, code of conduct and contributing guidelines.

At the end of 2019 Tekton the number of repositories had grown to eleven. A
regular monthly release cadence is established - Pipeline has 9 releases and in
March 2020 the beta version of the Tekton Pipeline API was
[released][pipeline-beta-release]. During this time, we also implemented the
project's release automation using Tekton itself.

The "results" and "chains" project were started in spring 2020, and in August
the Tekton Hub was [officially launched][tekton-hub-launch].

The Tekton community kept growing thanks to Tekton adopters and end-users
contributing features, ideas and issues.

{{< imgproc contributions Fit 700x500 >}} Contributions and contributors to
Tekton Projects over time. Source <a
href="https://tekton.devstats.cd.foundation/d/74/contributions-chart?orgId=1&from=1540938487786&to=1666996087786&var-period=m&var-metric=contributions&var-repogroup_name=All&var-country_name=All&var-company_name=All&var-company=all&viewPanel=5&theme=light&kiosk=">devstats</a>.
{{< /imgproc >}}

## Focus on security

One year later, it's now 2021, Tekton has matured considerably, while remaining
true to its nature of having a small footprint and giving users full flexibility
in how they setup their CI/CD system through Tekton.

This very flexibility has enabled Tekton to become the base for the
implementation of more opinionated services on top, ranging from open source
projects, and cloud services as well as end-user platforms for DevOps services.

It's now prime time to focus more thoroughly on security! In July 2021 the
Tekton Vulnerability Team is formed. Tekton pipelines release v0.29 is the first
one to be signed through Tekton chains, with the provenance Rekor UUID included
in the release notes.

End user adoption shows how Tekton, with the help of Tekton Chains, can help
solve software supply chain security challenges.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Very excited to see SolarWinds Trebuchet really exploring the full potential of Tekton!! 😻 <a href="https://twitter.com/hashtag/SupplyChainSecurityCon?src=hash&amp;ref_src=twsrc%5Etfw">#SupplyChainSecurityCon</a> <a href="https://twitter.com/hashtag/KubeCon?src=hash&amp;ref_src=twsrc%5Etfw">#KubeCon</a> <a href="https://t.co/IFJKvED1q7">https://t.co/IFJKvED1q7</a> <a href="https://t.co/bS1UuBGuxh">pic.twitter.com/bS1UuBGuxh</a></p>&mdash; tektoncd (@tektoncd) <a href="https://twitter.com/tektoncd/status/1447608787737538560?ref_src=twsrc%5Etfw">October 11, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

In March 2022, thanks to the the sponsorship of the CDF, Tekton completed an
[independent security audit][security-audit].

Later that year, Tekton achieves the [OpenSSF Best Practices
badges][openssf-badge] for its six core components.

## Long Term Support 

In October 2022 the Tekton community defines its [policy for long term support
(LTS)][lts-policy]:

> The Tekton project maintains four release branches for each project, created
one every three months, which results in a overall support window of
approximately one year for each of these releases.

These releases are called LTS, and throughout the support period, patch releases
may be created to resolve:

- CVEs (under the advisement of the Tekton Vulnerability Team)
- dependency issues (including base image updates)
- critical core component issues

The community-wide policy can be extended by each project. Pipeline continuous
with its monthly cadence, and it selects four releases a year for LTS.

{{< imgproc releases Fit 700x500 >}} Tekton Pipeline Releases and their support
window. {{< /imgproc >}}

## Graduation

The Graduated Stage for projects under the CD Foundation umbrella is when they
have reached their growth goals and are now on a sustaining cycle of
development, maintenance, and long-term support. Graduated Stage projects are
used commonly in enterprise production environments and have large,
well-established project communities.

More specifically, the Technical Oversight Committee (TOC) [defines
graduation][graduation-charter] as a set of requirements about project maturity,
best practices, security stance and adoption. 

Tekton is the second project to graduate from the CD Foundation, after Jenkins.
All the details about the twelve graduation criteria be found in the [graduation
proposal][graduation-proposal].

{{< imgproc banner Fit 700x500 >}}{{< /imgproc >}}

## What's Next

Graduation is a great milestone for the project and a great responsibility too.
The community will continue to work on improving Tekton, while keeping the
project stable and secure.

We are working on several security features like trusted resources and trusted
workloads, as well as releasing the v1 version of the API.

## Acknowledgments

The graduation has been the result of the years long work of the Tekton
community. Congratulations and thank you to all the Tekton contributors who made
it possible!

Thank you for the the CDF for hosting the project and supporting it, especially
through the security audit. Thank you to the TOC for their support and
sponsorship as well as to the CDF team, Fatih, Jesse and Roxanne for their great
work with marketing and organizing the [press release][press-release].

[knative]: https://knative.dev
[cdf-creation-blog]:
    https://cd.foundation/blog/2019/03/12/introducing-the-continuous-delivery-foundation-the-new-home-for-tekton-jenkins-jenkins-x-and-spinnaker/
[cdf]: https://cd.foundation
[tekton-hub-launch]:
    https://cd.foundation/blog/2020/08/10/introducing-tekton-hub/
[pipeline-repo]: https://github.com/tektoncd/pipeline
[pipeline-beta-release]:
    https://github.com/tektoncd/pipeline/releases/tag/v0.11.0
[security-audit]:
    https://cd.foundation/blog/2022/08/26/tekton-security-review-completed/
[graduation-charter]:
    https://github.com/cdfoundation/toc/blob/b4844654fe5d355496481bed1bff3166889584ed/PROJECT_LIFECYCLE.md#graduated-stage
[graduation-proposal]:
    https://github.com/cdfoundation/toc/blob/main/proposals/tekton/graduation.md
[lts-policy]:
    https://github.com/tektoncd/community/blob/main/releases.md#support-policy
[openssf-badge]: https://bestpractices.coreinfrastructure.org/en
[press-release]:
    https://cd.foundation/announcement/2022/10/25/cd-foundation-welcomes-new-software-supply-chain-security-project-pyrsia-announces-tekton-graduation-and-cdevents-release/
[voting-email]: https://lists.cd.foundation/g/cdf-toc/topic/94265202#861