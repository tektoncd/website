In this section, we will build the first task.

With Tekton, each operation in your CI/CD workflow becomes a Step, which is executed with a container image you specify. Steps are then organized in Tasks, which run as a Kubernetes pod in your cluster. You can further organize Tasks into Pipelines, which can control the order of execution of several Tasks.

To create a Task, create a Kubernetes object using the Tekton API with the kind Task. The following YAML file specifies a Task with one simple Step, which prints a Hello World! message using the official Ubuntu image:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: hello
spec:
  steps:
    - name: hello
      image: ubuntu
      command:
        - echo
      script: |
        set -e
        echo "Hello World!"
```{{copy}}

Write the YAML above to a file named task-hello.yaml, and apply it to your Kubernetes cluster:

```bash
kubectl apply -f task-hello.yaml
```{{execute}}

To run this task with Tekton, you need to create a TaskRun, which is another Kubernetes object used to specify run time information for a Task.

To view this TaskRun object you can run the following Tekton CLI (`tkn`) command:

```bash
tkn task start hello --dry-run
```{{execute}}

After running the command above, the following TaskRun definition should be shown:

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  generateName: hello-run-
spec:
  taskRef:
    name: hello
```{{copy}}

To use the TaskRun above to start the hello Task, you can either use tkn or kubectl.

Start with tkn:

```bash
tkn task start hello
```{{execute}}

Start with kubectl:

```bash
# use tkn's --dry-run option to save the TaskRun to a file
tkn task start hello --dry-run > taskRun-hello.yaml
# create the TaskRun
kubectl create -f taskRun-hello.yaml
```{{execute}}

Tekton will now start running your Task. To see the logs of the last TaskRun, run the following tkn command:

```bash
tkn taskrun logs --last -f
```{{execute}}

It may take a few moments before your Task completes. When it executes, it should show the following output:

```console
[hello] Hello World!
```
