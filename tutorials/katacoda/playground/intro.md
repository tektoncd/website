[Tekton](https://tekton.dev) is a cloud native continuous integration and delivery (CI/CD) solution. It allows developers to build, test, and deploy across cloud providers and on-premises systems.

This playground features a pre-configured Kubernetes cluster with two nodes, one configured as the Control Plane node and a second worker node. It also comes with Tekton installed, so that you can experiment, explore, and learn about Tekton as you see fit. The following components are available:

- Tekton Pipelines
- Tekton Dashboard
- Tekton CLI

Additionally, the Kubernetes cluster includes:

- A PersistentVolume for [artifact storage](https://github.com/tektoncd/pipeline/blob/v0.13.2/docs/install.md#configuring-artifact-storage)
