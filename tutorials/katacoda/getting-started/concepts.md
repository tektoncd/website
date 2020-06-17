To build a CI/CD system with Tekton, you need to specify a Tekton pipeline.
A pipeline consists of one or more Tekton tasks, each of which may include
several steps. Additionally, a task may take some pipeline resources as
inputs and outputs.

For example, if you plan to build a CI/CD system that builds source code
from your GitHub repository into a container image, the Tekton pipeline may
look as follows:

![architecture](https://github.com/tektoncd/website/tree/master/tutorials/katacoda/getting-started/images/architecture.png?raw=true)
