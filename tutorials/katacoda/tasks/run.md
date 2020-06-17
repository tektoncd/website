Now you may run the task and see it in action. If you have not followed every
step earlier, a completed task specification is available at
`website/tutorials/katacoda/tasks/src/tekton-katacoda/tasks/task.yaml`.

To apply this task, run the command below:

`kubectl apply -f website/tutorials/katacoda/tasks/src/tekton-katacoda/tasks/task.yaml`{{execute}}

To start the task, run the command below:

`kubectl apply -f website/tutorials/katacoda/tasks/src/tekton-katacoda/tasks/taskRun.yaml`{{execute}}

You can check the status of your pipeline with the following command:

`kubectl get taskruns/example-task-run -o yaml`{{execute}}

The output should look as follows:

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
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
error occur when running the task, the cause will be reported in these
fields with instructions for troubleshooting. If everything runs smoothly, you
should see an `All Steps have completed executing` message with a `Succeeded`
reason listed.
