# Developing the Tekton website

- [Setting up your dev environment](#setup)
- [Deploying changes](#deploying)

## Setup

Before working on website issues, be sure to have the following installed:

- [Yarn](https://yarnpkg.com/en/)
- [Hugo](https://gohugo.io/)

You can [use the `hugo` command](https://gohugo.io/getting-started/usage/)
to interact with the site locally and see the results
[before deploying](#deploying).

## Deploying

At the moment, deployments are done manually after a merge to master.
Eventually we plan to move to [netlify](https://www.netlify.com/) (once we
transfer ownership of the `tekton.dev` domain to the Linux Foundation),
which would provide us with gitops based automation.

- Currently we are hosting `tekton.dev` on [firebase](https://firebase.google.com/)
- The `firebase` project is called `tekton`
- [Members of the Tekton governing board](https://github.com/tektoncd/community/blob/master/governance.md)
  and other Linux Foundation contributors have access to the firebase project

Instructions for deploying Hugo based sites to Firebase:
https://gohugo.io/hosting-and-deployment/hosting-on-firebase/
