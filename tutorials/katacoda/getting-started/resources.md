So far you have been specifying resources using only their
types (`git`) but not their values (the URL of the GitHub
repository). Tekton uses pipeline resources to
store these values; to create the `git` pipeline resource used for this
scenario, for example, you can create a YAML file as follows:

```yaml
apiVersion: tekton.dev/v1alpha1
kind: PipelineResource
metadata:
  # The name of the pipeline resource
  name: example-git
spec:
  type: git
  params:
  # The revision/branch of the repository
  - name: revision
    value: master
  # The URL of the repository
  - name: url
    value: https://github.com/tektoncd/website
```

The example above is also available at
`website/tutorials/katacoda/getting-started/src/tekton-katacoda/resources/git.yaml`. To
apply it, run the command below:

`cd ~/website/tutorials/katacoda/getting-started/src/tekton-katacoda/ && kubectl apply -f resources/git.yaml`{{execute}}
