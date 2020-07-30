#### Try it out

Please wait while your Tekton playground is starting, this may take a few minutes.

Once it is ready you can check the installed versions:
`tkn version`{{execute}}

Try out some of the [examples](https://github.com/tektoncd/pipeline/tree/master/examples) from the Tekton Pipeline repo.

For example:
`kubectl apply -f https://raw.githubusercontent.com/tektoncd/pipeline/master/examples/v1beta1/pipelineruns/output-pipelinerun.yaml`{{execute}}

You can track the progress of the `PipelineRuns` using:

`kubectl get pipelineruns`{{execute}}

`tkn pipelinerun list`{{execute}}

or check out the Tekton Dashboard at http://[[HOST_SUBDOMAIN]]-9097-[[KATACODA_HOST]].environments.katacoda.com/
