Katacoda is now starting your experimental Kubernetes cluster and configuring
Tekton. **It may take a few moments to complete**.

## Check installation progress

Run `kubectl cluster-info`{{execute}} to check if the Kubernetes cluster has
been started. You should see the addresses of your Kubernetes cluster master
node and DNS in the output **when the initialization completes**.

Run `kubectl get pods --namespace tekton-pipelines`{{execute}} to check if
Tekton has been installed. All the components listed in the output should
have the status `running` **when the initialization completes**.

The environment is now fully functional.

## Getting the code

We’ve put everything you need for this scenario in a GitHub repository.
To clone this repository, run the following command:

`git clone https://github.com/tektoncd/website`{{execute}}

Open the directory `website/tutorials/katacoda/runs/src`.
The directory consists of three subdirectories and one file: 

* `app/`: the app to test in this scenario.
* `tekton-katacoda/`: Tekton resource specifications you will use in this scenario.
* `Dockerfile`: a Dockerfiles for building `app/` into a runnable container image.
