<!--
---
title: "Getting Started with Triggers"
linkTitle: "Getting Started with Triggers"
weight: 3
description: >
  Create and run your first Tekton Trigger.
---
-->

This tutorial shows you how to

+   Install Tekton Triggers.
+   Create a Trigger Template.
+   Create a Trigger Bind.
+   Create an Event Listener.

This guide uses a local cluster with [minikube][].

## Before you begin

1.  Complete the two previous Getting Started tutorials: [Tasks][gs-tasks] and
    [Pipelines][gs-pipelines]. *Do not clean up your resources*, skip the last
    section.

1.  Install [curl][] if it's not already available on your system.

## Overview

You can use Tekton Triggers to modify the behavior of your CI/CD Pipelines
depending on external events. The basic implementation you are going to create
in this guide comprises three main components:

1.  An `EventListener` object that listens to the world waiting for "something"
    to happen.

1.  When an event happens, the  Event Listener passes the information
    associated with that event on to a `TriggerBinding` object, which in turn
    encodes the information into variables that are then passed on to a
    `TriggerTemplate` object.

1.  The `TriggerTemplate` object uses the variables to instantiate and run a
    Pipeline.

![Triggers flow diagram](/images/TriggerFlow.svg)

An optional `ClusterInterceptor` object can be added to validate and process
data.

You are going to create a Tekton Trigger to run the `hello-goodbye` Pipeline
when the Event Listener detects an event.

## Install Tekton Triggers

1.  Use `kubectl` to install Tekton Triggers:

    ```bash
    kubectl apply --filename \
    https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
    kubectl apply --filename \
    https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml
    ```

1.  Monitor the installation:

    ```bash
    kubectl get pods --namespace tekton-pipelines --watch
    ```

    When `tekton-triggers-controller`, `tekton-triggers-webhook`, and
    `tekton-triggers-core-controller` show `1/1` under the `READY` column, you
    are ready to continue. For example:

    ```
    NAME                                                 READY   STATUS    RESTARTS        AGE
    tekton-pipelines-controller-68b8d87687-8mzvt         1/1     Running   2 (4d13h ago)   4d19h
    tekton-pipelines-webhook-6fb6dd6d75-7jfz6            1/1     Running   2 (104s ago)    4d19h
    tekton-triggers-controller-74b654c6bc-24ds7          1/1     Running   2 (104s ago)    4d19h
    tekton-triggers-core-interceptors-79f4dbb969-sk2dk   1/1     Running   3 (104s ago)    4d19h
    tekton-triggers-webhook-56885c9875-nx499             1/1     Running   2 (104s ago)    4d19h
    ```

    Hit *Ctrl + C* to stop monitoring.

## Create a Trigger Template

A Trigger Template defines what happens when an event is detected.

1.  Create a new file named `trigger-template.yaml` and add the following:

    ```yaml
    apiVersion: triggers.tekton.dev/v1beta1
    kind: TriggerTemplate
    metadata:
      name: hello-template
    spec:
      params:
      - name: username
        default: "Kubernetes"
      resourcetemplates:
      - apiVersion: tekton.dev/v1beta1
        kind: PipelineRun
        metadata:
          generateName: hello-goodbye-run-
        spec:
          pipelineRef:
            name: hello-goodbye
          params:
          - name: username
            value: $(tt.params.username)
    ```

    The `PipelineRun` object that you created in the previous tutorial is now
    included in the template declaration. This trigger expects the `username`
    parameter to be available; if it's not, it assigns a default value:
    "Kubernetes".

1.  Apply the Trigger Template to your cluster:

    ```bash
    kubectl apply -f trigger-template.yaml
    ```

## Create a Trigger Binding

A Trigger Binding instantiates the Trigger Template, the same way you had to
create a Pipeline Run to instantiate the Pipeline.

1.  Create a file named `trigger-binding.yaml` with the following content:

    ```yaml
    apiVersion: triggers.tekton.dev/v1beta1
    kind: TriggerBinding
    metadata:
      name: hello-binding
    spec: 
      params:
      - name: username
        value: $(body.username)
    ```

    This Trigger Binding gets some information and saves it in the `username`
    variable.

1.  Apply the Trigger Binding:

    ```bash
    kubectl apply -f trigger-binding.yaml
    ```

## Create an Event Listener

The `EventListener` object encompasses both the Trigger Template and the
Trigger Binding. 

1.  Create a file named `event-listener.yaml` and add the following:

    ```yaml
    apiVersion: triggers.tekton.dev/v1beta1
    kind: EventListener
    metadata:
      name: hello-listener
    spec:
      serviceAccountName: tekton-robot
      triggers:
        - name: hello-trigger 
          bindings:
          - ref: hello-binding
          template:
            ref: hello-template
    ```

    This declares that when an event is detected, it will run the Trigger
    Binding and the Trigger Template.

1.  Event Listeners require a service account to run. To create the service
    account for this example create a file named `rbac.yaml` and add the
    following:

    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: tekton-robot
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: triggers-example-eventlistener-binding
    subjects:
    - kind: ServiceAccount
      name: tekton-robot
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: tekton-triggers-eventlistener-roles
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: triggers-example-eventlistener-clusterbinding
    subjects:
    - kind: ServiceAccount
      name: tekton-robot
      namespace: default
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: tekton-triggers-eventlistener-clusterroles
    ```

    For now think about this part as an implementation detail for this tutorial.
    You don't have to understand what's going on in this file.

1.  Apply the file to your cluster:

    ```bash
    kubectl apply -f rbac.yaml
    ```

##  Running the Trigger

You have everything you need to run this Trigger and start listening for events.

1.  Create the Event Listener:

    ```bash
    kubectl apply -f event-listener.yaml
    ```

1.  To be able to communicate outside the cluster, enable port-forwarding:

    ```bash
    kubectl port-forward service/el-hello-listener 8080
    ```

    The output confirms that port-forwarding is working:

    ```
    kubectl port-forward service/el-hello-listener 8080
    Forwarding from 127.0.0.1:8080 -> 8080
    Forwarding from [::1]:8080 -> 8080    
    ```

    Keep this service running, don't close the terminal.

##  Monitor the Trigger

Now that the event Listener is running, you can send an event and see what
happens:

1.  Open a new terminal and submit a payload to the cluster:

    ```bash
    curl -v \
       -H 'content-Type: application/json' \
       -d '{"username": "Tekton"}' \
       http://localhost:8080
    ```

    You can change "Tekton" for any string you want. This value will be
    ultimately read by teh `goodbye-world` Task.

    The response is successful:

    ```
    < HTTP/1.1 202 Accepted
    < Content-Type: application/json
    < Date: Fri, 30 Sep 2022 00:11:19 GMT
    < Content-Length: 164
    <
    {"eventListener":"hello-listener","namespace":"default","eventListenerUID":"35dd0858-3692-4bb5-8c4f-1bf6d705bb73","eventID":"1a0a1120-7833-4078-9f30-0e3688f27dde"}
    * Connection #0 to host localhost left intact
    ```

1.  This event triggers a Pipeline Run, check the Pipeline Runs on your
    cluster :

    ```bash
    kubectl get pipelineruns
    ```

    The output confirms the pipeline is working:

    ```
    NAME                      SUCCEEDED   REASON      STARTTIME   COMPLETIONTIME
    hello-goodbye-run         True        Succeeded   24m         24m
    hello-goodbye-run-8hckl   True        Succeeded   81s         72s
    ```

    You see two Pipeline Runs, the first one created in the previous guide,
    the last one was created by the Trigger.

1.	Check the Pipeline Run logs. The name is auto-generated adding a suffix
    for every run. Replace `hello-goodbye-run-xvwfm` in the follwing command
    with your own output to check the logs: 

    ```bash
    tkn pipelinerun logs hello-goodbye-run-xvwfm -f
    ```

    And you get the expected output:

    ```
    [hello : echo] Hello World

    [goodbye : goodbye] Goodbye Tekton!
    ```

     Both Tasks completed successfuly. Congratulations!


## Clean up

1.  Press *Ctrl + C* in the terminal running the port-forwarding process to stop
    it.

1.  Delete the cluster:

    ```bash
    minikube delete
    ```

    The output confirms that the cluster was deleted:

    ```
    🔥  Deleting "minikube" in docker ...
    🔥  Deleting container "minikube" ...
    🔥  Removing /home/user/.minikube/machines/minikube ...
    💀  Removed all traces of the "minikube" cluster.
    ```

## Further reading 

For more complex Pipelines examples check:

- [Clone a git repository with Tekton][git-howto].
- [Build and push a container image with Tekton][kaniko-howto].

You can find more Tekton Triggers examples on the [Triggers GitHub
repository][triggers-repo].

[gs-tasks]: /docs/getting-started/tasks/
[gs-pipelines]: /docs/getting-started/pipelines/
[curl]: https://curl.se/download.html
[minikube]: https://minikube.sigs.k8s.io/docs/start/
[triggers-repo]: https://github.com/tektoncd/triggers/tree/main/examples
[git-howto]: /docs/how-to-guides/clone-repository/
[kaniko-howto]: /docs/how-to-guides/kaniko-build-push/
