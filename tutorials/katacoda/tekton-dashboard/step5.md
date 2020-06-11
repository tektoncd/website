In this section, we will view the PipelineRun logs to monitor its progress.
Then, we will open MyApp.

## Monitor the PipelineRun logs

View the PipelineRun logs for the MyApp PipelineRun by clicking on the link in
the creation notification at the top of the page.

![PipelineRun creation notification screenshot.](https://raw.githubusercontent.com/ncskier/katacoda/master/tekton-dashboard/images/pipeline-run-created-notification.png)

Or select the PipelineRun from the list of PipelineRuns.

![View the running PipelineRun logs for MyApp screenshot.](https://raw.githubusercontent.com/ncskier/katacoda/master/tekton-dashboard/images/pipeline-run-running.png)

Verify both the `build` and `deploy` tasks have passed.

![View the completed PipelineRun logs for MyApp screenshot.](https://raw.githubusercontent.com/ncskier/katacoda/master/tekton-dashboard/images/pipeline-run-completed.png)

## Open the Deployed App

MyApp will be running on port `3000`. Click on the following link to open the
app:
https://[[HOST_SUBDOMAIN]]-3000-[[KATACODA_HOST]].environments.katacoda.com/

![View MyApp screenshot.](https://raw.githubusercontent.com/ncskier/katacoda/master/tekton-dashboard/images/view-myapp.png)