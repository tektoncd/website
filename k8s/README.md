This directory includes the Kubernetes configuration for deploying this
website, which uses Tekton to:

- Clone the website from the tektoncd/website repository
- Synchronizes contents from specified Tekton repositories
- Build the website with Hugo
- Deploys thew website via Firebase
