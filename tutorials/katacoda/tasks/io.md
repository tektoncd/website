As explained earlier, in this scenario you will run a number of tests on a
client app. To achieve this, Tekton must first retrieve the source code of
the app as an input.

Tekton supports the following resource types as inputs and outputs:

* `git`: A `git` repository. Tekton will clone the repository automatically.
* `pullRequest`: A pull request from a source control system.
* `image`: An image in a remote repository
* `cluster`: A Kubernetes cluster (different from the one Tekton is running on).
* `storage`: A file or directory from a blob storage system.
* `cloudevent`: A cloud event to send at the completion of a task.

You can view the specifics of these resource types 
[here](https://tekton.dev/docs/pipelines/resources/#resource-types). For now
you will use a `git` type resource as input for your task.

Open `website/tutorials/katacoda/tasks/src/tekton-katacoda/tasks/taskTemplate.yaml`, and
edit the field `spec.resources.inputs`. Add a resource of the `git` type
with the name `git`.

```yaml
...
spec:
  resources:
    inputs:
    - name: git
      type: git
...
```

Tekton will clone the input GitHub repository at the path `/workspace/git`,
where `git` is the name of the resource.  Note that the task specification
above does not include the actual URL of the repository; instead, Tekton
requires that you create a Tekton PipelineResource, another Kubernetes
Custom Resource provided by Tekton, to specify the details of the `git`
resource your task uses. This design decouples input and output specifics
from tasks, allowing you to easily switch configurations at runtime.

In this scenario, you will clone the source code from the GitHub repository
`github.com/tektoncd/website`; the PipelineResource is available
at `website/tutorials/katacoda/tasks/src/tekton-katacoda/pipelineResources/git.yaml`:

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

`kubectl apply -f website/tutorials/katacoda/tasks/src/tekton-katacoda/pipelineResources/git.yaml`{{execute}}
