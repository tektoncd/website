---
title: Tekton
layout: hextra-home
---

{{< hextra/hero-badge link="https://www.cncf.io/blog/2026/03/24/tekton-becomes-a-cncf-incubating-project/" >}}
  <span>CNCF Incubating Project</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}

<div class="hx-mt-6 hx-mb-6" style="text-align:center;">
{{< hextra/hero-headline >}}
  Cloud Native CI/CD
{{< /hextra/hero-headline >}}
</div>

<div class="hx-mb-8" style="text-align:center;">
{{< hextra/hero-subtitle >}}
  Tekton is a powerful and flexible open-source framework&nbsp;<br class="sm:hx-block hx-hidden" />for creating CI/CD systems on Kubernetes.
{{< /hextra/hero-subtitle >}}
</div>

<div style="display:flex; gap:0.75rem; flex-wrap:wrap; justify-content:center; align-items:center; margin:3rem auto; width:100%; text-align:center;">
{{< hextra/hero-button text="Get Started" link="/docs/getting-started/" >}}
{{< hextra/hero-button text="Documentation" link="/docs/" style="alt" >}}
</div>

<div style="display:flex; justify-content:center; margin:3rem auto 4rem;">
  <img src="/images/workflow.svg" alt="Tekton CI/CD workflow: Clone → Unit Tests → Build → Deploy" style="width:1000px; max-width:none; height:auto;" />
</div>

<div style="text-align:center; margin-bottom:1.5rem;">
  <h2 style="font-size:1.75rem; font-weight:800;">Why Tekton?</h2>
</div>

{{< cards >}}
  {{< card link="/docs/concepts/overview/" title="Cloud Native" icon="cloud" subtitle="Runs on Kubernetes, uses containers as building blocks, and treats clusters as first-class resources." >}}
  {{< card link="/docs/pipelines/" title="Decoupled" icon="switch-horizontal" subtitle="One Pipeline can deploy to any Kubernetes cluster. Tasks run in isolation and resources swap easily between runs." >}}
  {{< card link="/docs/pipelines/" title="Typed Resources" icon="code" subtitle="Typed resources enable easy swapping of implementations — e.g. Kaniko vs Buildkit for image builds." >}}
{{< /cards >}}

<div style="text-align:center; margin: 3.5rem 0 1.5rem;">
  <h2 style="font-size:1.75rem; font-weight:800;">Trusted By</h2>
  <p style="opacity:0.6; font-size:0.95rem; margin-bottom:1.5rem;">Industry leaders building with Tekton in production</p>
</div>

<div class="adopters-grid">
  <span class="adopter">Red Hat</span>
  <span class="adopter">IBM</span>
  <span class="adopter">Google</span>
  <span class="adopter">Alibaba</span>
  <span class="adopter">Marriott Vacations</span>
  <span class="adopter">Nubank</span>
  <span class="adopter">OneStock</span>
  <span class="adopter">AllianzDirect</span>
  <span class="adopter">Kadaster</span>
  <span class="adopter">Giant Swarm</span>
  <span class="adopter">Alauda</span>
</div>

<div style="text-align:center; margin: 3rem 0 1.5rem;">
  <h2 style="font-size:1.75rem; font-weight:800;">Get Started</h2>
</div>

{{< cards >}}
  {{< card link="/docs/installation/" title="Install Tekton" icon="download" subtitle="Get Tekton running on your Kubernetes cluster in minutes." >}}
  {{< card link="/docs/getting-started/pipelines/" title="Build a Pipeline" icon="archive" subtitle="Chain Tasks together into a complete CI/CD workflow." >}}
  {{< card link="/docs/getting-started/pipelines-as-code/" title="Pipelines as Code" icon="document-text" subtitle="Git-native CI/CD — define pipelines alongside your source code." >}}
  {{< card link="/docs/chains/" title="Supply Chain Security" icon="shield-check" subtitle="Sign and attest artifacts automatically with Tekton Chains." >}}
  {{< card link="/docs/getting-started/tasks/" title="Create Your First Task" icon="play" subtitle="Hands-on tutorial: build and run a Task step by step." >}}
  {{< card link="/community/" title="Join the Community" icon="user-group" subtitle="Connect with contributors, join Slack, and help shape Tekton." >}}
{{< /cards >}}

<div class="cncf-banner">
  <a href="https://www.cncf.io/blog/2026/03/24/tekton-becomes-a-cncf-incubating-project/" class="cncf-banner-inner">
    <img src="/partner-logos/cncf.png" alt="CNCF" class="cncf-logo" />
    <span>Tekton is an incubating project at the <strong>Cloud Native Computing Foundation</strong></span>
  </a>
</div>
