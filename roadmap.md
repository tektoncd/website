# Tekton Website Roadmap

We are continually working to improve the user experience on the Tekton website.

The following is a list of projects we are working on or planning to work on in the near future:

## Tutorial improvements

We are working on revamping and updating our tutorials to make ramping up on Tekton and its components easier for new users. We want to make our tutorials easier to understand and more relatable to real life scenarios.

## Announcements

We're working to add support for announcements using the blog feature of the Docsy template. A blog post will be published for each release of a Tekton component describing the new features, changes, and bug fixes in that release. See [issue 218](https://github.com/tektoncd/website/issues/218).

## Community page

Create a "Community" page using the community page feature of the Docsy template. The page will display content from the [tektoncd/community](https://github.com/tektoncd/community) repo. See [issue 217](https://github.com/tektoncd/website/issues/217).

## "Getting Started" guides for Tekton

We are working on "Getting Started" guides for Tekton that will describe how to deploy, configure, and integrate Tekton Pipelines with other Tekton components to create a fully working build environment.

## Versioned URLs for the /docs folder

Right now, the website provides an unversioned URL to current release docs in the /docs folder and versioned URLs to previous release docs in the /vault folder. However, any links to docs for a given release pointing to the /docs folder become irrelevant as soon as a new release is out. To remedy this, we want to implement versioned URLs for the /docs folder as well.
