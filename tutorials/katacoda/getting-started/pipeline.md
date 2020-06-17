You can now build the two tasks into a Tekton pipeline. Open and edit
`website/tutorials/katacoda/getting-started/src/tekton-katacoda/pipelines/pipelineTemplate.yaml`.

The pipeline must include all the resources the tasks within
use. Add them in the `spec.resources` field:

```yaml
spec:
  resources:
  - name: git
    type: git
```

In other words, to trigger this pipeline, one must provide a resource of
the `git` type, which Tekton will pass to tasks requesting them.

Then you can add tasks to the `spec.tasks` field using their names:

```yaml
  tasks:
  # The name of the task in this pipeline
  - name: build-test-app
    taskRef:
      # The name of the task
      name: build-test-app
    resources:
      # The input and output resources this specific task uses
  # The name of the task in this pipeline
  - name: deploy-app
    taskRef:
      # The name of the task
      name: deploy-app
```

The name of a task is available in the `metadata.name` field of its
specification.

Additionally, you must specify the input and output resources each specific
task requires so that the Tekton pipeline can allocate them correctly:

```yaml
tasks:
  - name: build-test-app
    taskRef:
      name: build-test-app
    resources:
      inputs:
      - name: git
        resource: git
  ...
```

The pipeline is now ready. If you have not followed every step above, a
complete pipeline specification is available at
`website/tutorials/katacoda/getting-started/src/tekton-katacoda/pipelines/pipeline.yaml`.
To apply this pipeline, run the command below:

`cd ~/website/tutorials/katacoda/getting-started/src/tekton-katacoda/ && kubectl apply -f pipelines/pipeline.yaml`{{execute}}
