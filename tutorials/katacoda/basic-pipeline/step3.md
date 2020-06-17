In this section, we will create the pipeline combining the two tasks.

To create a `Pipeline`, create a Kubernetes object using the Tekton API with
the kind `Pipeline`. The following YAML file specifies a `Pipeline`.

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: hello-goodbye
spec:
  tasks:
  - name: hello
    taskRef:
      name: hello
  - name: goodbye
    runAfter: 
      - hello
    taskRef:
      name: goodbye
```{{copy}}

Write the YAML above to a file named `pipeline-hello-goodbye.yaml`, and apply it to your Kubernetes cluster:

```bash
kubectl apply -f pipeline-hello-goodbye.yaml
```{{execute}}

To run this pipeline with Tekton, you need to create a `pipelineRun`, which is
another Kubernetes object used to specify run time information for a `Pipeline`. 

To view this `pipelineRun` object you can run the following Tekton CLI (`tkn`) command:

```bash
tkn pipeline start hello-goodbye --dry-run
```{{execute}}

After running the command above, the following `PipelineRun` definition should be shown:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: hello-goodbye-run-
spec:
  pipelineRef:
    name: hello-goodbye
```{{copy}}

To use the `pipelineRun` above to start the `echo` `Pipeline`, you can either use 
`tkn` or `kubectl`.

Start with `tkn`:

```bash
tkn pipeline start hello-goodbye
```{{execute}}

Start with `kubectl`:

```bash
# use tkn's --dry-run option to save the pipelineRun to a file
tkn pipeline start hello-goodbye --dry-run > pipelineRun-hello-goodbye.yaml
# create the pipelineRun
kubectl create -f pipelineRun-hello-goodbye.yaml
```{{execute}}

Tekton will now start running your `Pipeline`. To see the logs of the `pipelineRun`, run 
the following `tkn` command:

```bash
tkn pipelinerun logs --last -f 
```{{execute}}

It may take a few moments before your `Pipeline` completes. When it executes, it should 
show the following output:

```console
[hello : hello] Hello World!
[hello : hello] + set -e
[hello : hello] + echo Hello World!

[goodbye : goodbye] Goodbye World!
[goodbye : goodbye] + set -e
[goodbye : goodbye] + echo Goodbye World!
```
