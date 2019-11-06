# tekton.dev (Under Construction)

## Getting started

tekton.dev is generated with [Hugo](https://gohugo.io/). To build the site
locally, [install Hugo](https://gohugo.io/getting-started/installing/)
and run `hugo server` at the root of the project.

`/helper` includes a simple script for syncing contents from other Tekton
repositories. To run this script, set up Python 3.7 and run the command below:

```bash
pip install helper/requirements.txt && python helper/helper.py
```

It will by default scans for `sync.yaml` under sub-directories of `content`
and download files from other repositories accordingly. An example of
`sync.yaml` is available at `content/en/docs/Triggers/sync.yaml`.

To deploy this site manually to Firebase Hosting, [set up Firebase CLI](https://github.com/firebase/firebase-tools),
authenticate to the staging GCP/Firebase project (`firebase login`)
and run command `hugo && firebase deploy`.

`k8s/` includes a workflow that builds and deploys the site automatically.
The specs have been applied to a K8S cluster in the staging GCP project.
To manually run the pipeline,
[connect to the K8S cluster](https://cloud.google.com/kubernetes-engine/docs/quickstart#get_authentication_credentials_for_the_cluster)
and apply `k8s/pipelineRun.yaml`.