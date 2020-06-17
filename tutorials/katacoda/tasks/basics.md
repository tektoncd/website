A Tekton task is a collection of steps to run in a CI/CD workflow. To specify
a Tekton task, create a Kubernetes Custom Resource with the following fields:

* `apiVersion`: The API version of the task, such as `tekton.dev/v1beta1`.
* `kind`: Tekton Tasks always have the `kind` `Task`.
* `metadata`: The metadata of the task, such as its name.
* `spec`: The specification of the task, including each step of the task.

Below is an example of a Tekton task:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: example-task
spec:
  steps:
  - name: example-step
    ...
```

## `spec`

`spec` specifies the details of the task. It must include one or more
steps, each of which uses a builder image to perform an operation. For example,
the YAML file below instructs Tekton to build a [Go](https://golang.org/)
app using [the official `golang` image from DockerHub](https://hub.docker.com/_/golang/).

```yaml
spec:
  steps:
  - name: build-go-src
    # Uses builder image golang from DockerHub (https://hub.docker.com/_/golang)
    # to compile an app coded with Go 1.12.
    image: golang:1.12
		script: |
		  #!/bin/bash
			go build example-app
  ...
```

Additionally, `spec` may include the the following fields:

* `resources`: The input resources (e.g. source code from GitHub), 
and the output resources (e.g. a container image) this task creates.
* `params`: The input parameters the task uses.
* `volumes`: One or more [Kuberentes Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
available to the task. You may mount them in one or more of the steps.
* `sidecars`: One or more sidecar containers that run alongside the steps.

[You can view the full list of fields that `spec` supports here](https://tekton.dev/docs/pipelines/tasks).
