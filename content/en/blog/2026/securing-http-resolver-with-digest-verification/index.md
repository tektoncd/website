---
title: Securing HTTP Resolver with Digest Verification
linkTitle: Securing HTTP Resolver with Digest Verification
date: 2026-02-04
author: "Zaki Shaikh, Red Hat"
description: >
  Introducing digest validation support for the HTTP resolver to secure your PipelineRuns by verifying remote Tekton resources.
---

## Overview

When fetching remote resources like Tasks and Pipelines from HTTP URLs for your PipelineRun, there's always a risk that the content could be tampered with during transit or at the source. To address this security concern, the Tekton HTTP resolver now supports optional digest validation, allowing users to verify the integrity of fetched content against a known cryptographic hash.

This feature enables users to specify an expected digest (SHA256 or SHA512) in their PipelineRun definitions. The resolver will then validate the fetched content against this digest before proceeding, ensuring that only verified, untampered resources are executed in your pipelines.

## Why Digest Verification Matters

When using the HTTP resolver to fetch remote Tasks or Pipelines for your PipelineRun, several attack vectors could compromise your build process:

1. **Man-in-the-Middle Attacks**: An attacker intercepting network traffic could modify the content of fetched resources.
2. **Compromised Source Repositories**: If the source repository is compromised, malicious code could be injected into your CI/CD pipeline.
3. **DNS Hijacking**: Attackers could redirect your requests to a malicious server serving altered content.

By providing a digest at the time of PipelineRun creation, you establish a cryptographic guarantee that the executed Pipeline or Task matches exactly what you intended to run. This ensures your PipelineRun only executes verified, untampered resources.

## How It Works

The HTTP resolver now accepts an optional `digest` parameter that specifies the expected hash of the fetched content. The digest must be provided in the format `<algorithm>:<hash>`, where the supported algorithms are:

- `sha256` - 256-bit hash (64 hexadecimal characters)
- `sha512` - 512-bit hash (128 hexadecimal characters)

When a digest is provided, the resolver:

1. Fetches the content from the specified URL
2. Computes the hash of the fetched content using the specified algorithm
3. Compares the computed hash against the provided digest
4. Only returns the content if the hashes match; otherwise, the resolution fails with an error

## Enabling the HTTP Resolver

To use the HTTP resolver, ensure that the feature flag is enabled in your Tekton Pipelines installation. The `enable-http-resolver` flag should be set to `true` in the resolver's feature flags ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: resolvers-feature-flags
  namespace: tekton-pipelines-resolvers
data:
  enable-http-resolver: "true"
```

## Usage Examples

### Basic Pipeline Resolution with Digest Verification

Here's an example of using the HTTP resolver with SHA256 digest verification to fetch a Pipeline from a remote repository:

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: secure-http-demo
spec:
  pipelineRef:
    resolver: http
    params:
      - name: url
        value: https://raw.githubusercontent.com/tektoncd/catalog/main/pipeline/build-push-gke-deploy/0.1/build-push-gke-deploy.yaml
      - name: digest
        value: sha256:e1a86b942e85ce5558fc737a3b4a82d7425ca392741d20afa3b7fb426e96c66b
```

### Task Resolution with SHA512 Digest

For users requiring stronger hash guarantees, SHA512 is also supported:

```yaml
apiVersion: tekton.dev/v1
kind: TaskRun
metadata:
  name: secure-task-run
spec:
  taskRef:
    resolver: http
    params:
      - name: url
        value: https://raw.githubusercontent.com/tektoncd-catalog/git-clone/main/task/git-clone/git-clone.yaml
      - name: digest
        value: sha512:a1b2c3d4e5f6...your-128-character-sha512-hash...
```

### Using with Authentication

The digest verification works seamlessly with the HTTP resolver's authentication features:

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: authenticated-secure-demo
spec:
  pipelineRef:
    resolver: http
    params:
      - name: url
        value: https://raw.githubusercontent.com/myorg/private-repo/main/pipeline.yaml
      - name: http-username
        value: git
      - name: http-password-secret
        value: github-token
      - name: http-password-secret-key
        value: token
      - name: digest
        value: sha256:f37cdd0e86d35ac97a65e11c8c2b9af12345678901234567890abcdef1234567
```

## Calculating Digests

Before using digest verification, you need to calculate the hash of your Tekton resource. You can use standard command-line tools available on all major operating systems:

### SHA256 Digest

```bash
# Calculate sha256 digest
curl -sL https://raw.githubusercontent.com/owner/repo/main/task/task.yaml | sha256sum
```

### SHA512 Digest

```bash
# Calculate sha512 digest
curl -sL https://raw.githubusercontent.com/owner/repo/main/task/task.yaml | sha512sum
```

The output will be a hexadecimal string that you can use as the digest value. Remember to prefix it with the algorithm name (e.g., `sha256:` or `sha512:`).

{{% alert title="Tip" color="primary" %}}
`sha256sum` and `sha512sum` commands are available on all major Linux distributions and macOS. On Windows, you can use PowerShell's `Get-FileHash` cmdlet or install tools like Git Bash.
{{% /alert %}}

## Error Handling

When digest validation fails, the HTTP resolver returns a clear error message to help diagnose the issue:

| Error Scenario | Example Error Message |
|----------------|----------------------|
| Invalid format | `invalid digest format: sha256` |
| Unsupported algorithm | `invalid digest algorithm: sha1` |
| Invalid hash length | `invalid sha256 digest value, expected length: 64, got: 8` |
| Hash mismatch | `SHA mismatch, expected abc123..., got def456...` |

These errors will appear in the PipelineRun or TaskRun status, allowing you to quickly identify and fix any configuration issues.

## Best Practices

### 1. Pin Your Remote Resources

When using the HTTP resolver with digest verification, consider pinning your remote resources to specific commits or tags rather than branches:

```yaml
# Good: Pinned to a specific commit
- name: url
  value: https://raw.githubusercontent.com/tektoncd/catalog/abc123def/pipeline/my-pipeline.yaml
- name: digest
  value: sha256:e1a86b942e85ce5558fc737a3b4a82d7425ca392741d20afa3b7fb426e96c66b

# Risky: Using a branch that can change
- name: url
  value: https://raw.githubusercontent.com/tektoncd/catalog/main/pipeline/my-pipeline.yaml
```

### 2. Automate Digest Updates

Consider automating the process of updating digests when your remote resources change. This can be integrated into your GitOps workflow or CI/CD process.

### 3. Use SHA256 for Standard Use Cases

SHA256 provides sufficient security for most use cases and produces shorter digest values. Use SHA512 only if your security requirements specifically mandate it.

### 4. Document Your Digests

Maintain documentation of which digests correspond to which versions of your resources. This helps with auditing and troubleshooting.

## Integration with Tekton Chains

This feature complements [Tekton Chains](https://tekton.dev/docs/chains/) for comprehensive pipeline security. While Chains provides attestation and provenance for your build artifacts, digest verification ensures the integrity of the resources used to perform those builds.

Together, they provide end-to-end security for your PipelineRuns:

- **Digest verification** ensures the integrity of your build definitions (Tasks and Pipelines)
- **Tekton Chains** provides signed attestations for your build outputs

## Backward Compatibility

The `digest` parameter is optional, ensuring full backward compatibility with existing configurations. Existing PipelineRuns and TaskRuns that don't specify a digest will continue to work as before, fetching content without verification.

## Conclusion

Digest verification for the HTTP resolver is a significant step toward securing your PipelineRuns. By enabling users to cryptographically verify the integrity of remote resources before execution, this feature helps prevent tampering attacks and ensures that your pipelines execute exactly the code you intend.

We encourage all users who fetch Tasks and Pipelines from HTTP URLs to adopt digest verification as part of their security best practices. The feature is designed to be easy to use while providing strong security guarantees through constant-time comparison and support for industry-standard hashing algorithms.

For more information about the HTTP resolver and its configuration options, refer to the [HTTP Resolver documentation](https://tekton.dev/docs/pipelines/resolution/http-resolver/).

---

*Have questions or feedback about this feature? Join the conversation on the [Tekton Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or open an issue on [GitHub](https://github.com/tektoncd/pipeline/issues).*

