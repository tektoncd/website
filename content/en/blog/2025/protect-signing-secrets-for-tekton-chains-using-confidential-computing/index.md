---
title: Protect Signing Secrets for Tekton Chains using Confidential Computing
linkTitle: Protect Signing Secrets for Tekton Chains using Confidential Computing
date: 2025-04-23
author: "Puneet Punamiya and Pradipta Banerjee, Red Hat"
description: >
  Integrating Tekton pipelines and chains with confidential computing
---


## What is Tekton Chains?

[Tekton Chains](https://github.com/tektoncd/chains/blob/main/README.md), a part of the Tekton project, provides tools to generate, store, and sign provenance for artifacts built with Tekton Pipelines.

Technically it's a Kubernetes Custom Resource Definition (CRD) controller that allows you to manage your supply chain security in Tekton.  Chains observes Tekton Pipelines and generates provenance for the artifacts built the Pipelines.


The following diagram from the Tekton Chains [tutorial](https://github.com/tektoncd/chains/blob/main/docs/tutorials/getting-started-tutorial.md) shows the Tekton Chains workflow

![Tekton Chains workflow diagram showing the process from pipeline execution to provenance generation and signing](./image1.png "Tekton Chains workflow diagram")

Src: https://tekton.dev/docs/chains/getting-started-tutorial/


To summarise, here are the steps in Tekton Chains provenance signing

1. Create signing secret (eg. cosign key-pair - cosign.pub, cosign.key, cosign.password)
2. Save the signing secret as K8s secret - named signing-secrets
in tekton-chains ns
3. Create the pipelineRun object (execute your pipeline)
4. Chains controller watches for pipelineRun completion and creates a snapshot
5. Sign the snapshot using the private part of the signing secret (eg. cosign.key)
6. As a consumer, verify the provenance by by checking the signature using the public part of the signing secret (eg. cosign.pub)

## What is Confidential Computing?

Confidential computing protects your workload and data from unauthorised entities — the host or hypervisor, system administrators, service providers, other virtual machines (VMs) and processes on the host.

Confidential computing protects the data in use, completing the data security triad — securing data at rest, in-transit, and in-use. Only the data owner has access to the data. 

![Diagram illustrating the three states of data protection: data at rest, data in transit, and data in use, with confidential computing protecting data in use](./image2.png)

This key functionality gives you the additional confidence to run your sensitive workloads in untrusted infrastructure (e.g. third-party data-centers, public cloud) and reap the benefits of scale and cost-efficiency.

<div align="center">
  <img src="./image3.png">
</div>

A Trusted Execution Environment (TEE) is at the heart of a confidential computing solution. TEEs are secure and isolated environments provided by confidential computing (CC) enabled hardware that prevents unauthorised access or modification of applications and data while in use. You’ll also hear the terms “enclaves” or “secure enclaves”. “TEEs” and “enclaves” are used interchangeably.

So to reap the benefits of confidential computing, your application needs to run inside a TEE (secure enclave) for it to be protected.


## How can you leverage Confidential Computing in the Kubernetes ecosystem?

In the Kubernetes world, there are two broad ways for you to use confidential computing:

**Confidential Cluster**: The entire Kubernetes cluster is running inside a confidential environment. The cluster nodes are confidential VMs, and any workload deployed on these cluster nodes benefits from confidentiality.

**Confidential Container**: The Kubernetes pod is running inside a confidential environment. This approach is more granular, where confidentiality is available to the workload of your choice.

![Comparison diagram showing confidential cluster approach versus confidential container approach in Kubernetes environments](./image4.png)

Both confidential Kubernetes clusters and containers aim to enhance data security and privacy of Kubernetes workloads by leveraging hardware-based encryption and attestations for trust.

## Tekton Chains and Confidential Computing

In order to secure Tekton Chains code and the signing secrets from threats by privileged admins, you can leverage confidential computing.

We have used the confidential container (CoCo) approach to secure Tekton chains.


## Confidential Containers (CoCo)
Confidential Containers (CoCo) refers to a pod running inside the TEE.

The CNCF Confidential Containers (CoCo) project is leading the effort to standardise confidential computing at the pod level and simplify its consumption in Kubernetes. This enables Kubernetes users to deploy confidential container workloads using familiar workflows and tools without extensive knowledge of the underlying confidential computing technologies.

## Confidential Containers (CoCo) building blocks

Following is a high level architecture of a typical CoCo deployment in Kubernetes.

![High-level architecture diagram of Confidential Containers (CoCo) deployment in Kubernetes, showing TEE, CVM, enclave software stack, and attestation components](./image5.png)

As shown in the diagram, CoCo uses Linux Confidential Virtual Machine (CVM) executing inside a TEE as the foundation. Using CVM as the foundation enables lift-and-shift of existing container workloads.

The container images are downloaded and kept inside the enclave and can be either signed and/or encrypted.

The components inside the CVM, namely image-rs, kata-agent, confidential data hub (CDH), attestation agent (AA) are collectively referred to as the enclave software stack.  The enclave software stack is measured, which means that a trusted cryptographic algorithm is used to measure these entities running within the CVM. These measurements can be used for attestation purposes. Access to secrets—including encryption keys to decrypt the container image itself or to unlock a database used by the workload—can be controlled, released only when the enclave is attested to be valid.

Attestation is the process of verifying that an enclave measurement meets some specified criteria set by the workload or data owner (mentioned as Relying party in the diagram). The attestation agent is responsible for initiating attestation and fetching of the secrets from the key broker service (KBS).  For detailed information refer to the following documentation.


The CNCF CoCo project provides the following components
  - Enclave software stack - https://github.com/confidential-containers/guest-components
  - Relying Party Services -  https://github.com/confidential-containers/trustee
  - CoCo operator - https://github.com/confidential-containers/operator
  - Trustee operator - https://github.com/confidential-containers/trustee-operator
  - CoCo enablement for Kata containers local hypervisor - https://github.com/kata-containers/kata-containers
  - CoCo enablement for Kata containers remote hypervisor - https://github.com/confidential-containers/cloud-api-adaptor 


### Tekton Chains and Confidential Containers (CoCo)

Recall from Tekton Chains [signing workflow](https://docs.google.com/document/d/1ivTjtZ1D_gjSBeaDqn4FGwIoBDid2xt3u4knVknDzzo/edit?tab=t.0#bookmark=id.7m33px6pnidl), the signing secret is stored as Kubernetes secret accessible to any cluster admin.  If you are using third party services, you would want to protect the signing secret even from the cluster admin. CoCo allows you to do that, by ensuring that the signing secret is only available inside the TEE with no access to the cluster admin.


In the following sections we'll see how the signing secrets can be protected using CoCo.

### Setup
For the purpose of this blog, we'll be using CoCo in AWS leveraging the Kata containers remote hypervisor setup provided via the CoCo cloud-api-adaptor project.

Instructions to set up CoCo on AWS - https://confidentialcontainers.org/docs/examples/aws-simple.

KBS setup details are described in the following [blog](https://confidentialcontainers.org/blog/2024/06/10/deploy-trustee-in-kubernetes/).

For other environments refer to the CoCo documentation - https://confidentialcontainers.org/docs/getting-started

### Tekton Chains Setup

Instructions to install Tekton Chains Installation -  https://github.com/tektoncd/chains?tab=readme-ov-file#installation

#### Signing Secrets for Tekton Chains

We'll be using the `sealed secrets` functionality of CoCo. A sealed secret is a way to encapsulate confidential data such that it can be accessed only inside a Trusted Execution Environment (TEE) after verification of the TEE environment.
There are two types of sealed secrets in CoCo - envelope and vault.

We'll be using the `vault` type. A vault secret is a pointer to a secret that is stored remotely in a KMS. In the CoCo environment this is managed by the Compute attestation operator as shown previously.
When deploying a workload as CoCo, the CoCo runtime components inside the TEE will retrieve the actual secret from the remote provider and make it available to the workload. This happens transparently.


Let's see an example of a vault type sealed secret.
The first step is to create a json file containing the location of the secret in a specified format.

An example json file `secret.json` is shown below. Note the `name` and the `provider`. This defines the location of the actual secret `secret`.

```bash
cat secret.json

{
    "version": "0.1.0",
    "type": "vault",
    "name": "kbs:///default/mysecret/secret",
    "provider": "kbs",
    "provider_settings": {},
    "annotations": {}
}
```


The sealed secret is of the form - `sealed.JWS header.JWS body (secret content).signature`

For using sealed secrets in K8s, we use the following:
`sealed.fakejwsheader.base64url(secret content).fakesignature`

Continuing with `secret.json` example, the sealed secret will be the following:

```bash
cat secret.json | basenc --base64url -w0

ewogICAgInZlcnNpb24iOiAiMC4xLjAiLAogICAgInR5cGUiOiAidmF1bHQiLAogICAgIm5hbWUiOiAia2JzOi8vL2RlZmF1bHQvbXlzZWNyZXQvc2VjcmV0IiwKICAgICJwcm92aWRlciI6ICJrYnMiLAogICAgInByb3ZpZGVyX3NldHRpbmdzIjoge30sCiAgICAiYW5ub3RhdGlvbnMiOiB7fQp9Cgo=

sealed_secret=sealed.fakejwsheader.ewogICAgInZlcnNpb24iOiAiMC4xLjAiLAogICAgInR5cGUiOiAidmF1bHQiLAogICAgIm5hbWUiOiAia2JzOi8vL2RlZmF1bHQvbXlzZWNyZXQvc2VjcmV0IiwKICAgICJwcm92aWRlciI6ICJrYnMiLAogICAgInByb3ZpZGVyX3NldHRpbmdzIjoge30sCiAgICAiYW5ub3RhdGlvbnMiOiB7fQp9Cgo=.fakesignature
```

Now let's see how we can use this approach to protect the signing secrets for Tekton Chains.

As mentioned previously, a CoCo deployment uses a trusted environment to store the secrets and releases it to the workload. The actual secret will be in the trusted environment whereas the sealed secret will be used in the untrusted environment running Tekton Chains.

Generate cosign key-pairs - cosign.pub, cosign.key, cosign.password

```bash
cosign generate-key-pair
```

Store the keys in the KBS. In my setup the cosign are stored under `default/cosign-secrets/{cosign.key,cosign.pub,cosign.password}`

Create sealed secrets to be used by the Tekton chains controller


### `cosign.key.json`
```json
{
    "version": "0.1.0",
    "type": "vault",
    "name": "kbs:///default/cosign-secrets/cosign.key",
    "provider": "kbs",
    "provider_settings": {},
    "annotations": {}
}
```

**Sealed secret**  
```sealed.fakejwsheader.ewogICAgInZlcnNpb24iOiAiMC4xLjAiLAogICAgInR5cGUiOiAidmF1bHQiLAogICAgIm5hbWUiOiAia2JzOi8vL2RlZmF1bHQvY29zaWduLXNlY3JldHMvY29zaWduLmtleSIsCiAgICAicHJvdmlkZXIiOiAia2JzIiwKICAgICJwcm92aWRlcl9zZXR0aW5ncyI6IHt9LAogICAgImFubm90YXRpb25zIjoge30KfQo=.fakesignature```

---

### `cosign.pub.json`
```json
{
    "version": "0.1.0",
    "type": "vault",
    "name": "kbs:///default/cosign-secrets/cosign.pub",
    "provider": "kbs",
    "provider_settings": {},
    "annotations": {}
}
```

**Sealed secret**  
`sealed.fakejwsheader.ewogICAgInZlcnNpb24iOiAiMC4xLjAiLAogICAgInR5cGUiOiAidmF1bHQiLAogICAgIm5hbWUiOiAia2JzOi8vL2RlZmF1bHQvY29zaWduLXNlY3JldHMvY29zaWduLnB1YiIsCiAgICAicHJvdmlkZXIiOiAia2JzIiwKICAgICJwcm92aWRlcl9zZXR0aW5ncyI6IHt9LAogICAgImFubm90YXRpb25zIjoge30KfQo=.fakesignature`

---

### `cosign.password.json`
```json
{
    "version": "0.1.0",
    "type": "vault",
    "name": "kbs:///default/cosign-secrets/cosign.password",
    "provider": "kbs",
    "provider_settings": {},
    "annotations": {}
}
```

**Sealed secret**  
`sealed.fakejwsheader.ewogICAgInZlcnNpb24iOiAiMC4xLjAiLAogICAgInR5cGUiOiAidmF1bHQiLAogICAgIm5hbWUiOiAia2JzOi8vL2RlZmF1bHQvY29zaWduLXNlY3JldHMvY29zaWduLnBhc3N3b3JkIiwKICAgICJwcm92aWRlciI6ICJrYnMiLAogICAgInByb3ZpZGVyX3NldHRpbmdzIjoge30sCiAgICAiYW5ub3RhdGlvbnMiOiB7fQp9Cg==.fakesignature`

---

#### The `signing-secrets` looks like this

```yaml
apiVersion: v1
data:
  cosign.key: c2VhbGVkLmZha2Vqd3NoZWFkZXIuZXdvZ0lDQWdJblpsY25OcGIyNGlPaUFpTUM0eExqQWlMQW9nSUNBZ0luUjVjR1VpT2lBaWRtRjFiSFFpTEFvZ0lDQWdJbTVoYldVaU9pQWlhMkp6T2k4dkwyUmxabUYxYkhRdlkyOXphV2R1TFhObFkzSmxkSE12WTI5emFXZHVMbXRsZVNJc0NpQWdJQ0FpY0hKdmRtbGtaWElpT2lBaWEySnpJaXdLSUNBZ0lDSndjbTkyYVdSbGNsOXpaWFIwYVc1bmN5STZJSHQ5TEFvZ0lDQWdJbUZ1Ym05MFlYUnBiMjV6SWpvZ2UzMEtmUW89LmZha2VzaWduYXR1cmUK
  cosign.password: c2VhbGVkLmZha2Vqd3NoZWFkZXIuZXdvZ0lDQWdJblpsY25OcGIyNGlPaUFpTUM0eExqQWlMQW9nSUNBZ0luUjVjR1VpT2lBaWRtRjFiSFFpTEFvZ0lDQWdJbTVoYldVaU9pQWlhMkp6T2k4dkwyUmxabUYxYkhRdlkyOXphV2R1TFhObFkzSmxkSE12WTI5emFXZHVMbkJoYzNOM2IzSmtJaXdLSUNBZ0lDSndjbTkyYVdSbGNpSTZJQ0pyWW5NaUxBb2dJQ0FnSW5CeWIzWnBaR1Z5WDNObGRIUnBibWR6SWpvZ2UzMHNDaUFnSUNBaVlXNXViM1JoZEdsdmJuTWlPaUI3ZlFwOUNnPT0uZmFrZXNpZ25hdHVyZQo=
  cosign.pub: c2VhbGVkLmZha2Vqd3NoZWFkZXIuZXdvZ0lDQWdJblpsY25OcGIyNGlPaUFpTUM0eExqQWlMQW9nSUNBZ0luUjVjR1VpT2lBaWRtRjFiSFFpTEFvZ0lDQWdJbTVoYldVaU9pQWlhMkp6T2k4dkwyUmxabUYxYkhRdlkyOXphV2R1TFhObFkzSmxkSE12WTI5emFXZHVMbkIxWWlJc0NpQWdJQ0FpY0hKdmRtbGtaWElpT2lBaWEySnpJaXdLSUNBZ0lDSndjbTkyYVdSbGNsOXpaWFIwYVc1bmN5STZJSHQ5TEFvZ0lDQWdJbUZ1Ym05MFlYUnBiMjV6SWpvZ2UzMEtmUW89LmZha2VzaWduYXR1cmUK
immutable: true
kind: Secret
metadata:
  name: signing-secrets
  namespace: tekton-chains
type: Opaque
```

---

## ⚙️ Custom Tekton Chains Deployment

Update the `TektonConfig` CR:

📖 [Tekton Operator Deployment Options](https://github.com/tektoncd/operator/blob/main/docs/TektonConfig.md#deployments)

```yaml
chain:
  options:
    deployments:
      tekton-chains-controller:
        spec:
          template:
            spec:
              containers:
              - name: tekton-chains-controller
                runtimeClassName: kata-remote
```

---

## 🚀 Run the Pipeline

Now you can run your pipeline and let Tekton chains sign the provenance using secrets that are only available inside the confidential environment.


We'll use the following sample from the getting started guide - https://github.com/tektoncd/chains/blob/main/docs/tutorials/getting-started-tutorial.md


```bash
kubectl create -f pipelinerun.yaml

tkn pr list

tkn pr describe

export PR_UID=$(tkn pr describe --last -o jsonpath='{.metadata.uid}')

tkn pr describe --last \
  -o jsonpath="{.metadata.annotations.chains\.tekton\.dev/signature-pipelinerun-$PR_UID}" \
  | base64 -d > metadata.json
```

---

## ✅ Cosign Verification

```bash
cosign verify-blob-attestation --insecure-ignore-tlog \
  --key cosign.pub --signature metadata.json \
  --type slsaprovenance --check-claims=false /dev/null
```

```
WARNING: Skipping tlog verification is an insecure practice that lacks of transparency and auditability verification for the blob attestation.
Verified OK
```

---

## 🔍 Confidentiality Verification

The following output is from the controller container.

As you can see the actual secrets are available in the volume mount path. Also the secrets are in memory.



```bash
cat /sealed/signing-secrets/cosign.pub
```

```bash
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEnI15trNzbvWtdAfVyNKRnY7/vrAP
vNnJ/gkCnoBNaaBWL/JgbdfQxF8PXMGXuoDvUFuePHwR7OY5xAoEGaVePw==
-----END PUBLIC KEY-----
/ $ cat /sealed/signing-secrets/cosign.key
-----BEGIN ENCRYPTED SIGSTORE PRIVATE KEY-----
eyJrZGYiOnsibmFtZSI6InNjcnlwdCIsInBhcmFtcyI6eyJOIjo2NTUzNiwiciI6
OCwicCI6MX0sInNhbHQiOiJYMVV6d0h3Uy9iUTJNa1FDV2NsUmFZRkdLTnpTTnJz
cy8yOFRyWEw2eEgwPSJ9LCJjaXBoZXIiOnsibmFtZSI6Im5hY2wvc2VjcmV0Ym94
Iiwibm9uY2UiOiI2bjhtSDRna2ZzaGQ3L3pBbTdOVk93WnNycVZVL3FNdCJ9LCJj
aXBoZXJ0ZXh0IjoiZERuaXZWWDRSZnZ6b2tTS2RVaUNRZG5taksxckd6SmlmMmVM
dWxudmo3dzFnbnpMMFdGdnhpRW16MUthc1RscjlhVDg3bFhoVGtqZmpRYU1pL3hT
NHkrRi9RMm5yc0xvcUNLUnNsREdOL016UnlBZjdXQkp4dU9jMGZtdWFiL1ZuM1lJ
aWVDOTBzdjhzZC9TdzBmWi8rVjJrUkEvRStkQk1QZmdUSnFqTzdwSUFoTWNVR01s
YlEyaWxmS01WempUR1hYbk5iODVwUEk2OHc9PSJ9
-----END ENCRYPTED SIGSTORE PRIVATE KEY-----
/ $

uname -a
Linux tekton-chains-controller-5c6c9684-cl4dn 6.11.5-100.fc39.x86_64 #1 SMP PREEMPT_DYNAMIC Tue Oct 22 19:26:45 UTC 2024 x86_64 Linux


# The unsealed secrets are in memory

/ $ df -h
Filesystem                Size      Used Available Use% Mounted on
overlay                   5.9G    166.5M      5.7G   3% /
tmpfs                    64.0M         0     64.0M   0% /dev
tmpfs                     5.9G    166.5M      5.7G   3% /sealed/signing-secrets
tmpfs                     5.9G    166.5M      5.7G   3% /etc/hosts
tmpfs                     5.9G    166.5M      5.7G   3% /dev/termination-log
tmpfs                     5.9G    166.5M      5.7G   3% /etc/hostname
tmpfs                     5.9G    166.5M      5.7G   3% /etc/resolv.conf
shm                      14.7G         0     14.7G   0% /dev/shm
tmpfs                     5.9G    166.5M      5.7G   3% /var/run/sigstore/cosign
tmpfs                     5.9G    166.5M      5.7G   3% /var/run/secrets/kubernetes.io/serviceaccount
tmpfs                    64.0M         0     64.0M   0% /proc/kcore
tmpfs                    64.0M         0     64.0M   0% /proc/keys
tmpfs                    64.0M         0     64.0M   0% /proc/latency_stats
tmpfs                    64.0M         0     64.0M   0% /proc/timer_list
```

---

The following screenshot shows the CVM running the container workload - `podvm-tekton-chains-controller-....` using an `"r6a"` instance type which is an AMD SNP confidential compute instance.

<div align="center">
  <img src="./image6.png">
</div>

<div align="center">
  <img src="./image7.png">
</div>

### References

https://github.com/tektoncd/chains

https://tekton.dev/docs/getting-started/supply-chain-security/

https://github.com/confidential-containers/guest-components/blob/main/confidential-data-hub/docs/SEALED_SECRET.md

https://opensource.googleblog.com/2023/03/getting-to-slsa-level-2-with-tekton-and-tekton-chains.html

https://github.com/tektoncd/operator/pull/2441
