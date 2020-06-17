Now you can use the taskRun and the pipelineRun created in earlier steps to
run the task and the pipeline. If you have not followed every step so far,
a complete taskRun and a complete pipelineRun are available at
`website/tutorials/katacoda/runs/src/tekton-katacoda/tasks/taskRun.yaml` and
`website/tutorials/katacoda/runs/src/tekton-katacoda/pipelines/pipelineRun.yaml`
respectively.

## Running the task

To run the task, execute the command below:

`kubectl apply -f website/tutorials/katacoda/runs/src/tekton-katacoda/tasks/taskRun.yaml`{{execute}}

It may take a few moments to complete. You can check its status with command
`kubectl get taskruns/example-task-run -o yaml`{{execute}}.

TaskRuns include the execution status of the associated task, including the
status of each step. Should there be an error, you can check with the taskRun
for the details. Logs in a specific taskRun are associated with the Kubernetes
pod running the task; you may access them in the same manner as you would
with a regular Kubernetes pod in your Kubernetes cluster.

## Running the pipeline

To run the task, execute the command below:

`kubectl apply -f website/tutorials/katacoda/runs/src/tekton-katacoda/pipelines/pipelineRun.yaml`{{execute}}

It may take a few moments to complete. You can check its status with command
`kubectl get pipelineruns/example-pipeline-run -o yaml`{{execute}}.

PipelineRuns include the execution status of the associated pipeline, including the
status of each task. Should there be an error, you can check with the pipelineRun
for the details. Logs for a specific task are associated with the Kubernetes
pod running the task; you may access them in the same manner as you would
with a regular Kubernetes pod in your Kubernetes cluster.
