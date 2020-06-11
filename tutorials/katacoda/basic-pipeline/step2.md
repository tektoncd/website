In this section, we will build upon the first task we created and create
a second task and verify it. It may seem repeatitive, but this is just an
example. (after you're done just imagine what you could do!)

## Extending your first CI/CD Workflow with a second Task and a Pipeline

As you learned previously, with Tekton, each operation in your CI/CD workflow becomes a `Step`,
which is executed with a container image you specify. `Steps` are then
organized in `Tasks`, which run as a [Kubernetes pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)
in your cluster. You can further organize `Tasks` into `Pipelines`, which 
can control the order of execution of several `Tasks`. 

To create a second `Task`, create a Kubernetes object using the Tekton API with
the kind `Task`. The following YAML file specifies a `Task` with one simple
`Step`, which prints a `Goodbye World!` message using
[the official Ubuntu image](https://hub.docker.com/_/ubuntu/):

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: goodbye
spec:
  steps:
    - name: goodbye
      image: ubuntu
      script: |
        set -e
        echo "Goodbye World!"
```{{copy}}

Write the YAML above to a file named `task-goodbye.yaml`, and apply it to your Kubernetes cluster:

```bash
kubectl apply -f task-goodbye.yaml
```{{execute}}

To run this task with Tekton, you need to create a `TaskRun`, which is
another Kubernetes object used to specify run time information for a `Task`. 

To view this `TaskRun` object you can run the following Tekton CLI (`tkn`) command:

```bash
tkn task start goodbye --dry-run
```{{execute}}

After running the command above, the following `TaskRun` definition should be shown:

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  generateName: goodbye-run-
spec:
  taskRef:
    name: goodbye
```{{copy}}

To use the `TaskRun` above to start the `echo` `Task`, you can either use 
`tkn` or `kubectl`.

Start with `tkn`:

```bash
tkn task start goodbye
```{{execute}}

Start with `kubectl`:

```bash
# use tkn's --dry-run option to save the TaskRun to a file
tkn task start goodbye --dry-run > taskRun-goodbye.yaml
# create the TaskRun
kubectl create -f taskRun-goodbye.yaml
```{{execute}}

Tekton will now start running your `Task`. To see the logs of the `TaskRun`, run 
the following `tkn` command:

```bash
tkn taskrun logs --last -f 
```{{execute}}

It may take a few moments before your `Task` completes. When it executes, it should 
show the following output:

```console
[goodbye] Goodbye World!
```
