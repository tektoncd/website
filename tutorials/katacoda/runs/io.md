A pipelineRun or a taskRun **must** include all the input and output
resources its associated pipeline or task uses. You may declare
them directly in the specification, or use a name reference that Tekton resolves
automatically at the time of execution.

For example, if you have a pipeline, `build-test`, that uses a `git` type
resource, `my-repo`, as input and an `image` type resource, `my-image` as
output, its pipelineRun should look like this:

```yaml
spec:
    pipelineRef: build-test
    resources:
    - name: my-repo
      resourceSpec:
        type: git
        params:
          ...
    - name: my-image
      resourceSpec:
        type: image
        params:
          ...
```

Note that the example above declares resources directly in the pipelineRun.
Alternatively, you may create the resources separately first in your Kubernetes
cluster:

```yaml
apiVersion: tekton.dev/v1alpha1
kind: PipelineResource
metadata:
  name: some-repo
spec:
  type: git
  params:
    ...
```

and use its name, `some-repo` as a reference in the pipelineRun:

```yaml
spec:
    pipelineRef: build-test
    resources:
    - name: my-repo
      resourceRef:
        name: some-repo
    ...
```

In this scenario, you will clone the source code from the GitHub repository
`github.com/tektoncd/website` as an input; the PipelineResource is
available at `website/tutorials/katacoda/runs/src/tekton-katacoda/pipelineResources/git.yaml`:

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

To apply this resource, run the command below:

`kubectl apply -f website/tutorials/katacoda/runs/src/tekton-katacoda/pipelineResources/git.yaml`{{execute}}

To use this resource with the task and the pipeline your just created,
edit the two files again.

Open
`website/tutorials/katacoda/runs/src/tekton-katacoda/tasks/taskRunTemplate.yaml` and
edit the `spec.inputs` section:

```yaml
spec:
    ...
    resources:
      inputs:
      - name: git
        resourceRef:
          name: example-git
```

Similarly, open `website/tutorials/katacoda/runs/src/tekton-katacoda/pipelines/pipelineRunTemplate.yaml`
and edit the `spec.resources` section:

```yaml
spec:
  ...
  resources:
  - name: git
    resourceRef:
      name: example-git
```
