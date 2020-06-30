In this section, we will import a Tekton Pipeline to build and deploy the
demo Nodejs app called [MyApp](https://github.com/ncskier/myapp). MyApp displays
a random picture of a cat.

## Open the Tekton Dashboard Import Tekton resources page

Click on the following link to go directly to the Import Tekton resources page:
https://[[HOST_SUBDOMAIN]]-80-[[KATACODA_HOST]].environments.katacoda.com/#/importresources

Or navigate to the Import Tekton resources page in the Dashboard.

## Import the MyApp Tekton resources

We want to import the Tekton resources that are defined in the
[`tekton/`](https://github.com/ncskier/myapp/tree/master/tekton) directory of
MyApp. Import these Tekton resources into the `default` Namespace by
filling in the form with the following information:

Repository URL: `https://github.com/ncskier/myapp`{{copy}}

Namespace: `default`

Repository directory: `tekton/`{{copy}}

Service Account `tekton-dashboard`

The form should look like the following:

![Import Tekton resources screenshot.](./assets/import-tekton-resources.png)

Click the `Import and Apply` button.

## View the progress importing the Tekton resources

The Dashboard creates a PipelineRun to import the specified Tekton resources.

Click on the `View status of this run` link at the bottom of the page to view
the status of importing the Tekton resources for MyApp.

![View status of importing Tekton resources screenshot.](./assets/view-status-of-pipeline0.png)

The Tekton resources have been imported when the PipelineRun has completed.

![Import Tekton resources PipelineRun logs screenshot.](./assets/import-pipelinerun-logs.png)
