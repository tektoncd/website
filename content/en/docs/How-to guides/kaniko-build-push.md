<!--
---
title: "Build and push an image with Tekton"
linkTitle: "Build and push an image with Tekton"
weight: 2
description: >
  Create a Pipeline to fetch the source code, build, and push an image with
  Kaniko and Tekton.
---
-->

This guide shows you how to:

1.  Create a Task to clone source code from a git repository.
1.  Create a second Task to use the cloned code to build a Docker image and push
    it to a registry.

If you are already familiar with Tekton and just want to see the example, you
can [skip to the full code samples](#full-code-samples).

## Prerequisites

1.  To follow this How-to you must have a Kubernetes cluster up and running and
    [kubectl][kubectl] properly configured to issue commands to your cluster.

1.  Install Tekton Pipelines:
    
    ```bash
    kubectl apply --filename \
    https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
    ```

    See the [Pipelines installation documentation][pipelines-inst] for other
    installation options.

1.  Install the [Tekton CLI, `tkn`][tkn-inst], on your machine.

If this is your first time using Tekton Pipelines, we recommend that you
complete the [Getting Started tutorials][getting-started] before proceeding with
this guide.

[pipelines-inst]: /docs/pipelines/install/
[tkn-inst]: /docs/cli/
[getting-started]: /docs/getting-started/
[kubectl]: https://kubernetes.io/docs/tasks/tools/#kubectl

## Clone the repository

Create a new Pipeline, `pipeline,yaml`, that uses the *git clone* Task to [clone
the source code from a git repository][tekton-clone]:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: clone-build-push
spec:
  description: | 
    This pipeline clones a git repo, builds a Docker image with Kaniko and
    pushes it to a registry
  params:
  - name: repo-url
    type: string
  workspaces:
  - name: shared-data
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
    workspaces:
    - name: output
      workspace: shared-data
    params:
    - name: url
      value: $(params.repo-url)
```

Then create the corresponding `pipelinerun.yaml` file:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: clone-build-push-run
spec:
  pipelineRef:
    name: clone-build-push
  workspaces:
  - name: shared-data
    volumeClaimTemplate:
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 1Gi
  params:
  - name: repo-url
    value: https://github.com/google/docsy-example.git
```

For this how-to we are using a public repository as an example. You can also
[use *git clone* with private repositories, using SSH
authentication][tekton-git-auth].

[tekton-clone]: /docs/how-to-guides/clone-repository/ 
[tekton-git-auth]: /docs/how-to-guides/clone-repository/#git-authentication
[git-clone]: https://hub.tekton.dev/tekton/task/git-clone

## Build the container image with Kaniko

To build the image use the [Kaniko][kaniko] Task from the [community
hub][tekton-hub]. 

1.  Add the image reference to the `params` section in `pipeline.yaml`:

    ```yaml
    params: 
    - name: image-reference
      type: string
    ```

    This parameter is used to add the tag corresponding the container registry
    where you are going to push the image. 

1.  Create the new `build-push` Task in the same `pipeline.yaml` file:

    ```yaml
    tasks:
    ...
      - name: build-push
        runAfter: ["fetch-source"]
        taskRef:
          name: kaniko
        workspaces:
        - name: source
          workspace: shared-data
        params:
        - name: IMAGE
          value: $(params.image-reference)
    ```

    This new Task refers to `kaniko`, which is going to be installed from the
    [community hub][tekton-hub]. A Task has its own set of `workspaces` and
    `params` passed down from the parameters and Workspaces defined at Pipeline
    level. In this case, the Workspace `source` and the value of `IMAGE`. Check
    the [kaniko Task documentation][kaniko] to see all the available options.

1.  Instantiate the `build-push` Task. Add the value of `image-reference` to
    the `params` section in `pipelinerun.yaml`:

    ```yaml
    params:
    - name: image-reference
      value: container.registry.com/sublocation/my_app:version
    ```

    Replace `container.registry.com/sublocation/my_app:version` with the actual
    tag for your registry. You can [set up a local registry][local-registry] for
    testing purposes.

Check the [full code samples](#full-code-samples) to see how all the pieces fit
together.

[kaniko]: https://hub.tekton.dev/tekton/task/kaniko
[tekton-hub]: https://hub.tekton.dev/
[local-registry]: https://gist.github.com/trisberg/37c97b6cc53def9a3e38be6143786589 

### Container registry authentication

In most cases, to push the image to a container registry you must provide
authentication credentials first.

1.  Set up authentication with the Docker credential helper and generate the
    Docker configuration file, `~/.docker/config.json`, for your registry. This
    step is different depending on your registry.

    - [Google Artifact Registry][google-ar]
    - [Red Hat Quay][rh-quay]
    - [Docker Hub][docker-hub]
    - [Azure container registry][azure]
    - [Amazon ECR][az-ecr]
    - [Jfrog Artifactory][jfrog]

    Check your cloud provider documentation to complete this step.

1.  Create a [Kubernetes Secret][secrets], `docker-credentials.yaml` with your
    credentials:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: docker-credentials
    data:
      config.json: efuJAmF1...
    ```

    The value of `config.json` is the base64-encoded `~/.docker/config.json`
    file. You can get this data with the following command:

    ```bash
    cat ~/.docker/config.json | base64 -w0
    ```

1.  Update `pipeline.yaml` and add a Workspace to mount the credentials
    directory:

    At the Pipeline level:

    ```yaml
    workspaces:
    - name: docker-credentials
    ```

    And under the `build-push` Task:

    ```yaml
    workspaces:
    - name: dockerconfig
      workspace: docker-credentials
    ```

1.  Instantiate the new `docker-credentials` Workspace in your
    `pipelinerun.yaml` file by adding a new entry under `workspaces`:

    ```yaml
    - name: docker-credentials
      secret:
        secretName: docker-credentials
    ```

See the complete files in the [full code samples section](#full-code-samples).

[secrets]: https://kubernetes.io/docs/concepts/configuration/secret/
[rh-quay]: https://access.redhat.com/documentation/en-us/red_hat_quay/3.4/html-single/use_red_hat_quay/index#allow-robot-access-user-repo
[google-ar]: https://cloud.google.com/artifact-registry/docs/docker/authentication
[docker-hub]: https://docs.docker.com/engine/reference/commandline/login/#credentials-store
[azure]: https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#individual-login-with-azure-ad
[az-ecr]: https://aws.amazon.com/blogs/compute/authenticating-amazon-ecr-repositories-for-docker-cli-with-credential-helper/
[jfrog]: https://www.jfrog.com/confluence/display/JFROG/Using+Docker+V1#UsingDockerV1-3.SettingUpAuthentication

## Run your Pipeline

You are ready to install the Tasks and run the pipeline.

1.  Install the `git-clone` and `kaniko` Tasks:

    ```bash
    tkn hub install task git-clone
    tkn hub install task kaniko
    ```

1.  Apply the Secret with your Docker credentials.

    ```bash
    kubectl apply -f docker-credentials.yaml
    ```

1.  Apply the Pipeline:

    ```bash
    kubectl apply -f pipeline.yaml
    ```

1.  Apply the PipelineRun:

    ```bash
    kubectl apply -f pipelinerun.yaml
    ```

1.  Monitor the Pipeline execution:

    ```bash
    tkn pipelinerun logs clone-build-push-run -f
    ```

    After a few seconds, the output confirms that the image was built and
    pushed successfully:
  
    ```
    [fetch-source : clone] + '[' false '=' true ]
    [fetch-source : clone] + '[' false '=' true ]
    [fetch-source : clone] + '[' false '=' true ]
    [fetch-source : clone] + CHECKOUT_DIR=/workspace/output/
    [fetch-source : clone] + '[' true '=' true ]
    [fetch-source : clone] + cleandir
    [fetch-source : clone] + '[' -d /workspace/output/ ]
    [fetch-source : clone] + rm -rf '/workspace/output//*'
    [fetch-source : clone] + rm -rf '/workspace/output//.[!.]*'
    [fetch-source : clone] + rm -rf '/workspace/output//..?*'
    [fetch-source : clone] + test -z 
    [fetch-source : clone] + test -z 
    [fetch-source : clone] + test -z 
    [fetch-source : clone] + /ko-app/git-init '-url=https://github.com/google/docsy-example.git' '-revision=' '-refspec=' '-path=/workspace/output/' '-sslVerify=true' '-submodules=true' '-depth=1' '-sparseCheckoutDirectories='
    [fetch-source : clone] {"level":"info","ts":1654637310.4419358,"caller":"git/git.go:170","msg":"Successfully cloned https://github.com/google/docsy-example.git @ 1c7f7e300c90cd690ca5be66b43fe58713bb21c9 (grafted, HEAD) in path /workspace/output/"}
    [fetch-source : clone] {"level":"info","ts":1654637320.384655,"caller":"git/git.go:208","msg":"Successfully initialized and updated submodules in path /workspace/output/"}
    [fetch-source : clone] + cd /workspace/output/
    [fetch-source : clone] + git rev-parse HEAD
    [fetch-source : clone] + RESULT_SHA=1c7f7e300c90cd690ca5be66b43fe58713bb21c9
    [fetch-source : clone] + EXIT_CODE=0
    [fetch-source : clone] + '[' 0 '!=' 0 ]
    [fetch-source : clone] + printf '%s' 1c7f7e300c90cd690ca5be66b43fe58713bb21c9
    [fetch-source : clone] + printf '%s' https://github.com/google/docsy-example.git

    [build-push : build-and-push] WARN
    [build-push : build-and-push] User provided docker configuration exists at /kaniko/.docker/config.json 
    [build-push : build-and-push] INFO Retrieving image manifest klakegg/hugo:ext-alpine 
    [build-push : build-and-push] INFO Retrieving image klakegg/hugo:ext-alpine from registry index.docker.io 
    [build-push : build-and-push] INFO Built cross stage deps: map[]                
    [build-push : build-and-push] INFO Retrieving image manifest klakegg/hugo:ext-alpine 
    [build-push : build-and-push] INFO Returning cached image manifest              
    [build-push : build-and-push] INFO Executing 0 build triggers                   
    [build-push : build-and-push] INFO Unpacking rootfs as cmd RUN apk add git requires it. 
    [build-push : build-and-push] INFO RUN apk add git                              
    [build-push : build-and-push] INFO Taking snapshot of full filesystem...        
    [build-push : build-and-push] INFO cmd: /bin/sh                                 
    [build-push : build-and-push] INFO args: [-c apk add git]                       
    [build-push : build-and-push] INFO Running: [/bin/sh -c apk add git]            
    [build-push : build-and-push] fetch https://dl-cdn.alpinelinux.org/alpine/v3.14/main/x86_64/APKINDEX.tar.gz
    [build-push : build-and-push] fetch https://dl-cdn.alpinelinux.org/alpine/v3.14/community/x86_64/APKINDEX.tar.gz
    [build-push : build-and-push] OK: 76 MiB in 41 packages
    [build-push : build-and-push] INFO[0012] Taking snapshot of full filesystem...        
    [build-push : build-and-push] INFO[0013] Pushing image to us-east1-docker.pkg.dev/tekton-tests/tektonstuff/docsy:v1 
    [build-push : build-and-push] INFO[0029] Pushed image to 1 destinations               

    [build-push : write-url] us-east1-docker.pkg.dev/my-tekton-tests/tekton-samples/docsy:v1
    ```

## Full code samples

The Pipeline:

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: clone-build-push
spec:
  description: |
    This pipeline clones a git repo, builds a Docker image with Kaniko and
    pushes it to a registry
  params:
  - name: repo-url
    type: string
  - name: image-reference
    type: string
  workspaces:
  - name: shared-data
  - name: docker-credentials
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
    workspaces:
    - name: output
      workspace: shared-data
    params:
    - name: url
      value: $(params.repo-url)
  - name: build-push
    runAfter: ["fetch-source"]
    taskRef:
      name: kaniko
    workspaces:
    - name: source
      workspace: shared-data
    - name: dockerconfig
      workspace: docker-credentials
    params:
    - name: IMAGE
      value: $(params.image-reference)
```

The PipelineRun:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: clone-build-push-run
spec:
  pipelineRef:
    name: clone-build-push
  workspaces:
  - name: shared-data
    volumeClaimTemplate:
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 1Gi
  - name: docker-credentials
    secret:
      secretName: docker-credentials
  params:
  - name: repo-url
    value: https://github.com/google/docsy-example.git
  - name: image-reference
    value: container.registry.com/sublocation/my_app:version 
```

The Docker credentials Kubernetes Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: docker-credentials
data:
  config.json: efuJAmF1...
```

Use your credentials as the value of the `data` field. Check the [registry
authentication section](#container-registry-authentication) for more
information.

## Further reading

- [Clone a git repository with Tekton][tekton-clone].
- [More Tekton Pipelines examples (code)][tekton-examples].

[tekton-examples]: https://github.com/tektoncd/pipeline/tree/main/examples


