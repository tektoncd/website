---
title: Tekton
layout: hextra-home
---

{{< hextra/hero-badge link="https://www.cncf.io/" >}}
  <span>CNCF Incubating Project</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}

<div class="hx-mt-6 hx-mb-6">
{{< hextra/hero-headline >}}
  Cloud Native CI/CD
{{< /hextra/hero-headline >}}
</div>

<div class="hx-mb-8">
{{< hextra/hero-subtitle >}}
  Tekton is a powerful and flexible open-source framework&nbsp;<br class="sm:hx-block hx-hidden" />for creating CI/CD systems on Kubernetes.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6" style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center;">
{{< hextra/hero-button text="Get Started" link="/docs/getting-started/" >}}
{{< hextra/hero-button text="Documentation" link="/docs/" style="alt" >}}
</div>

<div class="hx-mt-6"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Standardization"
    subtitle="Standardizes CI/CD tooling and processes across vendors, languages, and deployment environments. Works with Jenkins, Jenkins X, Skaffold, Knative, and more."
    style="background: radial-gradient(ellipse at 50% 80%,rgba(0,16,159,0.12),hsla(0,0%,100%,0));"
  >}}
  {{< hextra/feature-card
    title="Built-in Best Practices"
    subtitle="Scalable, serverless, cloud native CI/CD execution out of the box. Build, test, and deploy without managing infrastructure."
    style="background: radial-gradient(ellipse at 50% 80%,rgba(185,128,208,0.12),hsla(0,0%,100%,0));"
  >}}
  {{< hextra/feature-card
    title="Maximum Flexibility"
    subtitle="Abstracts the underlying implementation so you choose the build, test, and deploy workflow based on your team's requirements."
    style="background: radial-gradient(ellipse at 50% 80%,rgba(0,16,159,0.08),hsla(0,0%,100%,0));"
  >}}
{{< /hextra/feature-grid >}}

<div class="hx-mt-16">

## Explore Tekton

{{< cards >}}
  {{< card link="/docs/installation/" title="Install Tekton" icon="download" subtitle="Get Tekton running on your Kubernetes cluster" >}}
  {{< card link="/docs/getting-started/" title="Try Tekton" icon="play" subtitle="Walk through your first Task and Pipeline" >}}
  {{< card link="/docs/concepts/overview/" title="Concepts" icon="book-open" subtitle="Understand how Tasks, Pipelines, and Runs work" >}}
  {{< card link="/docs/pipelines/" title="Tasks & Pipelines" icon="code" subtitle="Build CI/CD workflows with the core building blocks" >}}
  {{< card link="/docs/chains/" title="Supply Chain Security" icon="shield-check" subtitle="Artifact signatures and attestations" >}}
  {{< card link="/community/" title="Community" icon="user-group" subtitle="Join the Tekton community and contribute" >}}
{{< /cards >}}

</div>

<div class="cncf-banner">
  <a href="https://www.cncf.io/" class="cncf-banner-inner">
    <img src="/partner-logos/cncf.png" alt="CNCF" class="cncf-logo" />
    <span>Tekton is an incubating project at the <strong>Cloud Native Computing Foundation</strong></span>
  </a>
</div>
