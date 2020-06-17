A `pipelineRun` is a specific execution of a pipeline. Similarly, A taskRun is a
specific execution of a task. When a pipelineRun or taskRun is
created in a Kubernetes cluster, Tekton will automatically run the associated
task or pipeline. PipelineRuns and taskRuns track the execution statuses of
tasks and pipelines; in addition, they help you connect input and output
resources with tasks and pipelines.

## PipelineRun

To specify a pipelineRun, create a Kubernetes Custom Resource with the
following fields:

* `apiVersion`: The API version of the pipelineRun, such as `tekton.dev/v1beta1`.
* `kind`: Tekton pipelineRuns always have the `kind` `PipelineRun`.
* `metadata`: The metadata of the pipelineRun, such as its name.
* `spec`: The specification of the pipelineRun, including the pipeline it triggers
and its input and output resources.

### `spec`

`spec` specifies the details of the pipelineRun. It must include the
specification of a pipeline or a reference to it. For example, the YAML
file below describes a pipelineRun named `build-test-deploy-run` that is
associated with a pipeline named `build-test-deploy`:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
    name: build-test-deploy-run
spec:
    pipelineRef:
        name: build-test-deploy
```

Additionally, `spec` may include the the following fields:

* `resources`: The input and output resources the associated pipeline uses.
* `serviceAccountName` and `serviceAccountNames`: one or a number of service
accounts that the associated pipeline (or specific tasks inside the pipeline)
uses.
* `timeout`: A timeout in seconds after which the pipelineRun will fail.

[You can view the full list of fields that `spec` supports here](https://tekton.dev/docs/pipelines/pipelineruns/).

## TaskRun

To specify a taskRun, create a Kubernetes Custom Resource with the
following fields:

* `apiVersion`: The API version of the taskRun, such as `tekton.dev/v1beta1`.
* `kind`: Tekton taskRuns always have the `kind` `TaskRun`.
* `metadata`: The metadata of the taskRun, such as its name.
* `spec`: The specification of the taskRun, including the task it triggers
and its input and output resources.

### `spec`

`spec` specifies the details of the taskRun. It must include the
specification of a task or a reference to it. For example, the YAML
file below describes a taskRun named `build-run` that is
associated with a task named `build`:

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
    name: build-run
spec:
    taskRef:
        name: build
```

Additionally, `spec` may include the the following fields:

* `resources`: The input and output resources the associated task uses.
* `params`: The input paramaters the associated task uses.
* `serviceAccountName`: the service account that the associated task uses.
* `timeout`: A timeout in seconds after which the taskRun will fail.

[You can view the full list of fields that `spec` supports here](https://tekton.dev/docs/pipelines/taskruns/).

As explained in the earlier section, this scenario requires that you
create a TaskRun and PipelineRun that
trigger a task and a pipeline respectively, which downloads an app
from GitHub and runs some tests.

The task and the pipeline are available at
`website/tutorials/katacoda/runs/src/tekton-katacoda/tasks/task.yaml` and
`website/tutorials/katacoda/runs/src/tekton-katacoda/pipelines/pipeline.yaml`
respectively.

The task includes only one step, where
the system uses the `pytest` command in the [official Python container image](https://hub.docker.com/_/python)
to run a simple test in the app you clone from GitHub:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: example-task
spec:
  resources:
    inputs:
    - name: git
      type: git
  steps:
  - name: pytest
    image: python
    script : |
		  #!/bin/bash
      cd /workspace/git/runs/src/app 
		  pip install -r requirements.txt 
		  pip install -r dev_requirements.txt 
		  pytest .
```

And the pipeline simply wraps the task:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: example-pipeline
spec:
  resources:
  - name: git
    type: git
  tasks:
  - name: example-task
    taskRef:
      name: example-task
    resources:
      inputs:
      - name: git
        resource: git
```

To apply the task and the pipeline, run the command below:

`kubectl apply -f website/tutorials/katacoda/runs/src/tekton-katacoda/tasks/task.yaml`{{execute}}
`kubectl apply -f website/tutorials/katacoda/runs/src/tekton-katacoda/pipelines/pipeline.yaml`{{execute}}

To create a taskRun for the task, open
`website/tutorials/katacoda/runs/src/tekton-katacoda/tasks/taskRunTemplate.yaml`.
Edit the `spec.taskRef` section:

```yaml
spec:
    taskRef:
        name: example-task
```

To create a pipelineRun for the pipeline, open
`website/tutorials/katacoda/runs/src/tekton-katacoda/pipelines/pipelineRunTemplate.yaml`.
Edit the `spec.pipelineRef` section:

```yaml
spec:
    pipelineRef:
        name: example-pipeline
```
