With all the tasks, pipeline resources, and the pipeline itself applied,
you can set your CI/CD system in motion. To trigger a pipeline manually,
create (once again) a YAML file of the `pipelineRun` kind. The specification
should include the name of the pipeline, and the pipeline resources it uses:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
name: build-test-deploy-app-run
spec:
  pipelineRef:
  name: build-test-deploy-app
  resources:
  - name: git
    resourceRef:
      name: example-git
```

To apply the `pipelineRun` specification, run the command below:

`cd ~/website/tutorials/katacoda/getting-started/src/tekton-katacoda/ && kubectl apply -f pipelines/run.yaml`{{execute}}

## Almost done

You can check the status of your pipeline with the following command:

`kubectl get pipelineruns/build-test-deploy-app-run -o yaml`{{execute}}

The output should look as follows:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  ...  
spec:
  ...
status:
  completionTime: ...
  conditions:
  - lastTransitionTime: ...
    message: ...
    reason: ...
    status: ...
    type: ...
  startTime: ...
  taskRuns:
    ...
```

It may take a few moments before Tekton finishes executing your
pipeline. **Check the message, reason, and status Tekton reports**. Should an
error occur when running the pipeline, the cause will be reported in these
fields with instructions for troubleshooting. If everything runs smoothly, you
should see an `All Steps have completed executing` message with a `Succeeded`
reason listed.

## Check out the deployment in the cluster

1. Find the IP of your deployed service:

    `kubectl get svc`{{execute}}

    Write down the `CLUSTER-IP` of `mysvc`.

2. Run the following command to access the service:

    `curl http://YOUR-CLUSTER-IP/hello`
  
    Replace `YOUR-CLUSTER-IP` with the value of your own. It may take a few
    moments before your app gets ready. You should see
    `Hello World!` returned as the output.
