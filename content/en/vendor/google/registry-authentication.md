**GKE Workload Identity**

If you are running your Pipelines on Google Kubernetes Engine (GKE), [create a
cluster with Workload Identity enabled][wi-create] or [enable Workload Identity
on an existing cluster][wi-enable]. This allows you to to run your pipeline and
push images to [Artifact Registry][ar-overview] without authentication
credentials. If you are using Workload Identity, **skip step 2** when you [run
your pipeline](#run-your-pipeline).

Set up an Artifact Registry repository:

1.  Enable the Artifact Registry API:

    ```bash
    gcloud services enable artifactregistry.googleapis.com
    ```

1.  Create a Docker  repository to push the image to:

    ```bash
    gcloud artifacts repositories create <repository-name> \
      --repository-format=docker \
      --location=us-central1 --description="Docker repository"
    ```

    Replace:

    -   `<repository-name>` with the name of your repository.
    -   `<location>` with the name of your preferred [location][]. For example,
        `us-central1`.

Configure the GKE cluster to allow the Pipeline to push images to Artifact
Registry:

1.  Create a Kubernetes Service Account:

    ```bash
    kubectl create serviceaccount <sa-name>
    ```

    Where `<sa-name>` is the name of the service account. For example, `tekton-sa`.

1.  Create a Google Service Account with the same name:

    ```bash
    gcloud iam service-accounts create <sa-name>
    ```

1.  Grant the Google Service Account permissions to push to the Artifact
    Registry container repository:

    ```bash
    gcloud artifacts repositories add-iam-policy-binding <ar-repository> \
      --location <location> \
      --member=serviceAccount:build-robot@<project_id>.iam.gserviceaccount.com \
      --role=roles/artifactregistry.reader \
      --role=roles/artifactregistry.writer
    ```

    Where

    - `<ar-repository>` is the name of the [repository][ar-repos].
    - `<location>` is the repository [repository location][location].
    - `<project_id>` is the [project id][project-id].

1.  Set up the Workload Identity mappings on the Kubernetes cluster:

    ```bash
    kubectl annotate serviceaccount \
    <sa-name> \
    iam.gke.io/gcp-service-account=build-robot@<project_id>.iam.gserviceaccount.com
    ```

1.  Set up Workload Identity mappings for the Google Service Account:

    ```bash
    gcloud iam service-accounts add-iam-policy-binding \
      --role roles/iam.workloadIdentityUser \
      --member "serviceAccount:<project_id>.svc.id.goog[default/<sa-name>]" \
      build-robot@<project_id>.iam.gserviceaccount.com
    ```

This creates two service accounts, an [IAM service account][iam-account] and a
[Kubernetes service account][k8s-account], and "links" them. Workload Identity
allows workloads in your GKE cluster to impersonate IAM service accounts to
access Google Cloud services.

**Use Docker authentication**

If you prefer to use Docker authentication to push your image to Artifact
Registry, there are two options:

- [Use the gcloud credential helper][gcloud-auth].
- [Use the Standalone Docker credential helper][standalone-auth].

In both cases your credentials are saved to a Docker configuration file in your
user home directory: `$HOME/.docker/config.json`. Use this file to follow the
"General Authentication" instructions.

[workload-identity]: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
[wi-create]: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#enable_on_cluster
[wi-enable]: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#enable-existing-cluster
[location]: https://cloud.google.com/artifact-registry/docs/repositories/repo-locations
[ar-repos]: https://cloud.google.com/artifact-registry/docs/repositories/create-repos
[project-id]: https://cloud.google.com/resource-manager/docs/creating-managing-projects
[iam-account]: https://cloud.google.com/iam/docs/service-accounts
[k8s-account]: https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/
[gcloud-auth]: https://cloud.google.com/artifact-registry/docs/docker/authentication#gcloud-helper
[standalone-auth]: https://cloud.google.com/artifact-registry/docs/docker/authentication#standalone-helper
[ar-overview]: https://cloud.google.com/artifact-registry/docs/overview

