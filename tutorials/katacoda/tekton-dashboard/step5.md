In this section, we will view the PipelineRun logs to monitor its progress.
Then, we will open MyApp.

## Monitor the PipelineRun logs

View the PipelineRun logs for the MyApp PipelineRun by clicking on the link in
the creation notification at the top of the page.

![PipelineRun creation notification screenshot.](./assets/pipeline-run-created-notification.png)

Or select the PipelineRun from the list of PipelineRuns.

![View the running PipelineRun logs for MyApp screenshot.](./assets/pipeline-run-running.png)

Verify both the `build` and `deploy` tasks have passed.

![View the completed PipelineRun logs for MyApp screenshot.](./assets/pipeline-run-completed.png)

## Open the Deployed App

Expose the app on port 3000:
```bash
kubectl port-forward --address=0.0.0.0 service/myapp 3000:3000 > /dev/null 2>&1 &
```{{execute}}

Click on the following link to open the app:
https://[[HOST_SUBDOMAIN]]-3000-[[KATACODA_HOST]].environments.katacoda.com/

![View MyApp screenshot.](./assets/view-myapp.png)
