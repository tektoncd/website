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

<div style="text-align:center; margin-bottom:2rem;">
  <h2 style="font-size:2rem; font-weight:800;">Why Tekton?</h2>
  <p style="opacity:0.55; font-size:1rem; margin-top:0.25rem;">Built for Kubernetes from day one</p>
</div>

<div class="why-tekton-grid">
  <a href="/docs/concepts/overview/" class="why-tekton-card">
    <div class="why-tekton-accent" style="background:#1d4ed8;"></div>
    <div class="why-tekton-title">
      <div class="why-tekton-icon" style="background:#eff6ff; color:#1d4ed8;">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </div>
      <h3>Cloud Native</h3>
    </div>
    <p>Runs on Kubernetes, uses containers as building blocks, and treats clusters as first-class resources.</p>
  </a>
  <a href="/docs/pipelines/" class="why-tekton-card">
    <div class="why-tekton-accent" style="background:#0d9488;"></div>
    <div class="why-tekton-title">
      <div class="why-tekton-icon" style="background:#f0fdfa; color:#0d9488;">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="8" y1="12" x2="16" y2="12"/><polyline points="12 8 16 12 12 16"/></svg>
      </div>
      <h3>Decoupled</h3>
    </div>
    <p>One Pipeline can deploy to any Kubernetes cluster. Tasks run in isolation and resources swap easily between runs.</p>
  </a>
  <a href="/docs/pipelines/" class="why-tekton-card">
    <div class="why-tekton-accent" style="background:#7c3aed;"></div>
    <div class="why-tekton-title">
      <div class="why-tekton-icon" style="background:#f5f3ff; color:#7c3aed;">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
      </div>
      <h3>Typed Resources</h3>
    </div>
    <p>Typed resources enable easy swapping of implementations — e.g. Kaniko vs Buildkit for image builds.</p>
  </a>
</div>

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
