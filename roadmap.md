# Tekton Website 2022 Roadmap

We are continually working to improve the user experience on the Tekton website.

The following is a (non-comprehensive) list of things we are working on or
planning to work on in 2022:

- Use a single framework for all the introductory tutorials. Probably
  [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/), which is available
  for Windows, Mac, and Linux.

- Update Katakoda tutorials or look for a feasible alternative and try to keep
  the content close to what the tutorials cover.

- Reorder the main navigation panel to a structure that follows a logical order
  instead of the current one.

- Update link in [tekton.dev](https://tekton.dev) to take users to the "Getting
  started" section, since the interactive tutorial are currently out of date.

- Work on a solution to communicate the status: alpha, beta, stable, or
  deprecated; of the components.

- Update the website theme to the latest version of Docsy.

- Come up with a solution to avoid content drifting as the components are
  updated. Try to keep the how-to always up-to-date.


## Updates to documentation structure

This structure is intended to make the documentation more friendly for newcomers
without disrupting the current content too much. We hope to reorganize the
current documentation and create new content, the site will look close to the
following (see also the [content
guidelines](https://tekton.dev/docs/contribute/doc-con-content/) to learn what
to expect from each type of document):

- **Installation** (*tutorials*) - Basic installation steps for several
  components, to be used as a prerequisite for getting started. Link to the
  installation readmes for further information about setup.

  - Pipelines
  - Triggers
  - CLI
  - Operator

- **Getting Started** (*tutorials*) - Guides for newcomers. Mostly "Hello World"
  tutorials for every component.
  
  - Getting started with Tasks
  - Getting started with Pipelines
  - Getting started with Triggers
  - Getting started with Tekton CLI

- **Concepts** (*explanations*) - Details about how things work. Rationale
  behind implementation decisions and anything else worth explaining.

  - Tekton Overview
  - Pipelines
  - Triggers

- **How-to guides** (*how-to*) - Real-life examples.

  - Build and deploy a container with Tekton.
  - Setup Tekton Triggers with GitHub
  - Pushing container containers images to a Registry.
  - Using (cloud provider) storage with Tekton.
  - Cloning private repositories.
  - (New ideas and contributions are welcome)

- **Reference** (*reference*) - Detailed documentation about every component.
  Mostly the current documents.

  - Pipelines
  - Triggers
  - CLI
  - Operator
  - Dashboard
  - Result
  - Chains
  - API docs (organize APIs for every project)

- **Contribute to documentation** (*how-to*)

  - Run the site locally
  - Content guidelines
  - Formatting conventions
  - Tips and tricks for good writing


## Announcements

We're working to add support for announcements using the blog feature of the
Docsy template. A blog post will be published for each release of a Tekton
component describing the new features, changes, and bug fixes in that release.
See [issue 218](https://github.com/tektoncd/website/issues/218).

## Community page

Create a "Community" page using the community page feature of the Docsy
template. The page will display content from the
[tektoncd/community](https://github.com/tektoncd/community) repo. See [issue
217](https://github.com/tektoncd/website/issues/217).

## Versioned URLs for the /docs folder

Right now, the website provides an unversioned URL to current release docs in
the /docs folder and versioned URLs to previous release docs in the /vault
folder. However, any links to docs for a given release pointing to the /docs
folder become irrelevant as soon as a new release is out. To remedy this, we
want to implement versioned URLs for the /docs folder as well.
