With the input ready, you may now ask Tekton to perform the actual tests, in
the form of a step.

The input GitHub repository in the previous step includes a simple Python app
for you to run tests against. It has already specified a number of unit tests,
which are runnable with the [`pytest`](https://docs.pytest.org/en/latest/) framework.
To add this as a step, open `tutorials/katacoda/tasks/src/tekton-katacoda/tasks/taskTemplate.yaml`
and edit the field `specs.steps`:

```yaml
specs:
    inputs:
    ...
    steps:
      # The name of the step
    - name: pytest
      # The builder image to use
      # Here you will use the official Python image from DockerHub (https://hub.docker.com/_/python)
      # which includes the pytest framework
      image: python
      # The command to run with the builder image
      # Here you will run the bash shell to start the Python interpreter
			script: |
			  #!/bin/bash
        cd /workspace/git/tasks/src/client 
				pip install -r requirements.txt 
				pip install -r dev_requirements.txt 
				pytest .
    ...
```

## About Builder Images

Any OCI image can be a builder image, such as the ones available in [DockerHub](https://hub.docker.com/).
If you are familiar with containers, you can also build one of your own and
ask Tekton to use it. They are capable of executing virtually all the operations
commonly seen in a CI/CD workflow, such as compiling the source code,
connecting to a cloud service provider, and providing insights and analyses
into artifacts.

DockerHub provides many pre-built images for you to choose from; in addition,
[Google Cloud Build Official Builder Images](https://github.com/GoogleCloudPlatform/cloud-builders)
also features a number of options available to you.
