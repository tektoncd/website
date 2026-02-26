---
title: "Artifact Storage in Tekton Chains"
linkTitle: "Storage in Chains"
date: 2026-02-16
author: "Naomi Gelman"
description: >
  A summary of the storage options available for storing attestations.
---

Tekton Chains observes `TaskRun` and `PipelineRun` executions, captures relevant information, and stores it in a cryptographically-signed format. This post details the supported storage backends and how they organize and persist these artifacts.

## Overview

Chains supports multiple storage backends, allowing you to store signatures and attestations in the location that best fits your infrastructure (e.g., OCI registry, GCS bucket, or directly on the Kubernetes objects).

### What is an Attestation?
Attestation is a signed, metadata-rich statement that provides authenticated evidence about how an artifact (like a container image) was built.
An attestation explains the provenance—details like which Git commit was used, which steps were run, and what dependencies were involved.

You can configure multiple backends simultaneously using the `artifacts.taskrun.storage`, `artifacts.pipelinerun.storage`, and `artifacts.oci.storage` keys in the `chains-config` [ConfigMap](https://tekton.dev/docs/chains/config/), for example:

```yaml
  # Store TaskRun artifacts in both Tekton (annotations) and OCI registry
  artifacts.taskrun.storage: "tekton,oci"
  
  # Store PipelineRun artifacts in GCS and Tekton
  artifacts.pipelinerun.storage: "gcs,tekton"
  
  # Store OCI image signatures in the OCI registry
  artifacts.oci.storage: "oci"
```

## Storage Backends

### Tekton (Default)

The `tekton` backend stores signatures and payloads directly on the `TaskRun` or `PipelineRun` object as annotations. This is the default storage backend.

*   **Configuration Key**: `tekton`
*   **Storage Location**: Kubernetes Annotations
*   **Format**: Base64 encoded strings

#### Annotation Keys
Chains uses the following annotation pattern, where `<key>` is typically the UID of the object or a configured short key:

*   `chains.tekton.dev/payload-<key>`: The raw payload (e.g., in-toto statement).
*   `chains.tekton.dev/signature-<key>`: The signature of the payload.
*   `chains.tekton.dev/cert-<key>`: The public certificate (if using x509).
*   `chains.tekton.dev/chain-<key>`: The certificate chain (if applicable).

For example: <chains.tekton.dev/signature-taskrun-2fd61624-79db-430f-a4f4-2839dd20cfad>

**Pros**:
*   Zero external dependencies.
*   Easy to inspect with `kubectl describe`.

**Cons**:
*   Limited by Kubernetes object size limits (etcd). Large payloads may fail to store.

---

### OCI (Open Container Initiative)

The `oci` backend stores signatures and attestations in an OCI registry. This is particularly useful for container image artifacts, as the signature stays with the image. Examples of supported OCI registries include: Quay.io, Docker Hub.


*   **Configuration Key**: `oci`
*   **Storage Location**: OCI Registry
*   **Dependencies**: `cosign` conventions

#### Behavior
*   **For Images**: Chains attaches the signature to the image manifest in the registry using the `cosign` specification. The signature is saved under a different SHA, with the suffix .att
*   **Repository**: By default, signatures are stored in the same repository as the image. You can override this by setting `storage.oci.repository` in the configuration.


#### Configuration
| Key | Description |
| :--- | :--- |
| `storage.oci.repository` | Optional. The OCI repository to store signatures/attestations in, instead of alongside the image. |
| `storage.oci.repository.insecure` | Optional. Set to `true` to allow insecure (HTTP) connections. |

---

### GCS (Google Cloud Storage)

The `gcs` backend stores artifacts as files in a Google Cloud Storage bucket.


*   **Configuration Key**: `gcs`
*   **Storage Location**: GCS Bucket

#### Path Structure
Chains organizes files using the following naming convention:

**TaskRuns**:
*   `taskrun-<namespace>-<name>/<key>.signature`
*   `taskrun-<namespace>-<name>/<key>.payload`
*   `taskrun-<namespace>-<name>/<key>.cert` (optional)
*   `taskrun-<namespace>-<name>/<key>.chain` (optional)

**PipelineRuns**:
*   `pipelinerun-<namespace>-<name>/<key>.signature`
*   `pipelinerun-<namespace>-<name>/<key>.payload`
*   ...

#### Configuration
| Key | Description |
| :--- | :--- |
| `storage.gcs.bucket` | **Required**. The name of the GCS bucket. |

**Authentication**: Chains uses standard Google Cloud Application Default Credentials. Ensure the Chains controller service account has `storage.objects.create` permissions on the bucket.

---

### DocDB (Document Database)

The `docdb` backend stores artifacts in a document-oriented database. It supports Firestore, MongoDB, and others via the `gocloud.dev/docstore` abstraction.


*   **Configuration Key**: `docdb`
*   **Storage Location**: Document Collection

#### Document Structure
Each entry is stored as a `SignedDocument` with the following fields:
*   `Signed`: The raw payload.
*   `Signature`: The signature.
*   `Object`: The unmarshaled object/payload.
*   `Name`: The key/ID.
*   `Cert`: The certificate.
*   `Chain`: The certificate chain.


#### Configuration
| Key | Description |
| :--- | :--- |
| `storage.docdb.url` | **Required**. The go-cloud URI for the collection (e.g., `firestore://...`, `mongo://...`). |
| `storage.docdb.mongo-server-url` | Optional. MongoDB connection string. |

**MongoDB Authentication**:
You can provide the MongoDB connection string via:
1.  `storage.docdb.mongo-server-url-path`: Path to a file containing the URL (recommended for secrets).
2.  `storage.docdb.mongo-server-url-dir`: Directory containing a `MONGO_SERVER_URL` file.
3.  `storage.docdb.mongo-server-url`: Direct string in config (less secure).
4.  `MONGO_SERVER_URL` environment variable.

---
### Grafeas

The `grafeas` backend stores artifacts as Notes and Occurrences in a Grafeas server (specifically Google Container Analysis).

Grafeas is a searchable metadata index — it doesn't store "big" files. It stores structured Notes and Occurrences, which are JSON metadata records containing signed attestations and build provenance.

A "Note" is the definition of what is stored, and an "Occurrence" is the actual record. A Note can point to many Occurrences, whereas an Occurrence can only point to one Note. This backend creates two types of Notes:
- **ATTESTATION** — for OCI image simplesigning payloads
- **BUILD** — for in-toto provenance payloads (TaskRun / PipelineRun)

> **Note:** The server address is **hardcoded** to Google Container Analysis (`containeranalysis.googleapis.com`) and authenticates via Application Default Credentials. You need a GCP project with Container Analysis enabled and `gcloud auth application-default login` configured locally.

Once a **TaskRun or PipelineRun** finishes, Chains will create a Note (if one doesn't already exist) and **one or more Occurrences** for that run — one per artifact URI produced.

*   **Configuration Key**: `grafeas`
*   **Storage Location**: Google Container Analysis API

#### Structure
*   **Attestations (simplesigning)**: Stored as `ATTESTATION` Occurrences linked to an Attestation Note (`<noteid>-simplesigning`).
*   **Build Provenance (in-toto)**: Stored as `BUILD` Occurrences linked to a Build Note (`<noteid>-<kindname>-intoto`). One Occurrence is created per artifact URI, all sharing the same payload and signature but differing in `ResourceUri`.
*   **Resource URI**: Occurrences are linked to the artifact URI (e.g., `IMAGE_URL@IMAGE_DIGEST`).

#### Configuration
| Key | Description |
| :--- | :--- |
| `storage.grafeas.projectid` | **Required**. The GCP project ID for Container Analysis. |
| `storage.grafeas.noteid` | Optional. Prefix for Note IDs. Defaults to `tekton-<namespace>`. |
| `storage.grafeas.notehint` | Optional. Human-readable name for the Attestation Note hint. |

---

### Archivista

The `archivista` backend stores artifacts in an Archivista service (an in-toto attestation store).

*   **Configuration Key**: `archivista`
*   **Storage Location**: Archivista Service

#### Configuration
| Key | Description |
| :--- | :--- |
| `storage.archivista.url` | **Required**. The URL of the Archivista service (e.g., `https://archivista.testifysec.io`). |

**Note**: Currently, the Archivista backend supports **storage only**. Retrieval of signatures/payloads via the Chains interface is not available.

---

### PubSub

The `pubsub` backend publishes the signature and payload to a Pub/Sub topic. This is useful for event-driven architectures where downstream systems need to react to new attestations.

*   **Configuration Key**: `pubsub` (implicit via provider config)
*   **Storage Location**: Pub/Sub Topic (Kafka or In-Memory)

#### Configuration
| Key | Description |
| :--- | :--- |
| `storage.pubsub.provider` | **Required**. The provider type: `kafka` or `inmemory`. |
| `storage.pubsub.topic` | **Required**. The topic name to publish to. |
| `storage.pubsub.kafka.bootstrap.servers` | Required for `kafka` provider. Comma-separated list of brokers. |

**Note**: This backend is **write-only**. Retrieval is not supported.

