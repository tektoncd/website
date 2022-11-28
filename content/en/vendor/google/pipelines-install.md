Before you proceed, create or select a project on Google Cloud and [install the
gcloud CLI][gcloud-install] on your computer. 

To install Tekton Pipelines:

1.  Enable the Google Kubernetes Engine (GKE) API:

    ```bash
    gcloud services enable container.googleapis.com
    ``` 

1.  Create a cluster with Workload Identity enabled. For example:

    ```bash
    gcloud container clusters create tekton-cluster \
      --num-nodes=<nodes> \
      --region=<location> \
      --workload-pool=<project-id>.svc.id.goog
    ```

    Where:

    + `<location>` is the cluster location. For example, `us-central1`.
      See the documentation about [regional][regional-c] and [zonal][zonal-c]
      clusters for more information.

    + `<project-id>` is the project ID.

    + `<nodes>` is the number of nodes. 

    Workload Identity allows your GKE cluster to access Google Cloud services
    using an [Identity Access Management (IAM)][iam-overview] service account.
    For example, the [Tekton build and push guide][kaniko-tuto] explains how to
    authenticate to Artifact Registry on a cluster with Workload Identity
    enabled.

    You can also [enable Workload Idenitity][wi-enable] on an existing cluster.

1.  Follow the regular Kubernetes installation steps.

**Private clusters**

If you are running a [private cluster][private-cluster] and experience [problems
with GKE DNS resolution][gke-issue], allow the port `8443` in your firewall
rules.

```bash
gcloud compute firewall-rules update <firewall_rule_name> --allow tcp:8443
```

See the documentation about [firewall rules for private
clusters][private-cluster-fw] for more information.

**Autopilot**

If you are using [Autopilot mode][autopilot] on your GKE cluster and
experience [some problems][ap-issue], try the following:

1.  Allow port `8443` in your firewall rules.

    ```bash
    gcloud compute firewall-rules update <firewall_rule_name> --allow tcp:8443
    ```

1.  Disable the affinity assistant.

    ```bash
    kubectl patch cm feature-flags -n tekton-pipelines \
      -p '{"data":{"disable-affinity-assistant":"true"}}'
    ```

1.  Increase the ephemeral storage.


[location]: https://cloud.google.com/artifact-registry/docs/repositories/repo-locations
[gke-issue]: https://github.com/tektoncd/pipeline/issues/3317#issuecomment-708066087
[gcloud-install]: https://cloud.google.com/sdk/docs/install
[gcloud-project]: https://cloud.google.com/resource-manager/docs/creating-managing-projects
[iam-overview]: https://cloud.google.com/iam/docs/overview
[regional-c]: https://cloud.google.com/kubernetes-engine/docs/concepts/regional-clusters
[zonal-c]: https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-zonal-cluster
[private-cluster]: https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept
[private-cluster-fw]: https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#add_firewall_rules
[kaniko-tuto]: /docs/how-to-guides/kaniko-build-push/#container-registry-authentication
[autopilot]: https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview
[ap-issue]: https://github.com/tektoncd/pipeline/issues/3798
[wi-enable]: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#enable-existing-cluster

