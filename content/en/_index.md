---
title: Tekton
layout: hextra-home
---

<div class="tekton-hero">
  <div class="tekton-hero-text">
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

<div class="hx-mb-6 hero-buttons">
{{< hextra/hero-button text="Get Started" link="/docs/getting-started/" >}}
{{< hextra/hero-button text="Documentation" link="/docs/" style="alt" >}}
</div>
  </div>
  <div class="tekton-hero-logo">
    <img src="/images/tekton-horizontal-color.png" alt="Tekton" />
  </div>
</div>

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

<div class="explore-grid">
  <a href="/docs/installation/" class="explore-card">
    <span class="explore-icon">{{< icon name="download" >}}</span>
    <strong>Install Tekton</strong>
    <span>Get Tekton running on your Kubernetes cluster</span>
  </a>
  <a href="/docs/getting-started/" class="explore-card">
    <span class="explore-icon">{{< icon name="play" >}}</span>
    <strong>Try Tekton</strong>
    <span>Walk through your first Task and Pipeline</span>
  </a>
  <a href="/docs/concepts/overview/" class="explore-card">
    <span class="explore-icon">{{< icon name="book-open" >}}</span>
    <strong>Concepts</strong>
    <span>Understand how Tasks, Pipelines, and Runs work</span>
  </a>
  <a href="/docs/pipelines/" class="explore-card">
    <span class="explore-icon">{{< icon name="code" >}}</span>
    <strong>Tasks &amp; Pipelines</strong>
    <span>Build CI/CD workflows with the core building blocks</span>
  </a>
  <a href="/docs/chains/" class="explore-card">
    <span class="explore-icon">{{< icon name="shield-check" >}}</span>
    <strong>Supply Chain Security</strong>
    <span>Artifact signatures and attestations</span>
  </a>
  <a href="/community/" class="explore-card">
    <span class="explore-icon">{{< icon name="user-group" >}}</span>
    <strong>Community</strong>
    <span>Join the Tekton community and contribute</span>
  </a>
</div>

</div>

<div class="cncf-banner">
  <a href="https://www.cncf.io/" class="cncf-banner-inner">
    <img src="/partner-logos/cncf.png" alt="CNCF" class="cncf-logo" />
    <span>Tekton is an incubating project at the <strong>Cloud Native Computing Foundation</strong></span>
  </a>
</div>
