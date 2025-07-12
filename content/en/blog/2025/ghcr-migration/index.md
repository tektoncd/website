---
title: Migration to Github Container Registry
linkTitle: Migration to Github Container Registry
date: 2025-04-03
author: "Stanislav Jakuschevskij, IBM"
description: >
    How to migrate your images from gcr.io to ghcr.io and why we migrated
---

## Why and How

Dear Tekton users and contributors, to reduce costs, we've migrated all our releases to the free tier on [ghcr.io/tektoncd](http://ghcr.io/tektoncd).

All new Tekton releases are exclusively on [ghcr.io/tektoncd](http://ghcr.io/tektoncd). Old releases are also now available on [ghcr.io/tektoncd](http://ghcr.io/tektoncd).

Please migrate your old releases to ghcr.io immediately since we have limited funding to allocate to gcr.io egress.

To migrate you need to replace `gcr.io/tekton-releases` with `ghcr.io/tektoncd` in all your images including all image references in the manifests, not only those that specify the `image` of the deployment, e.g. in the Tekton pipelines controller deployment:

```yaml
containers:
- name: tekton-pipelines-controller
  image: ghcr.io/tektoncd/pipeline/controller-...                    # <<== HERE
  args: [
    "-entrypoint-image", "ghcr.io/tektoncd/pipeline/entrypoint-...", # <<== HERE
    "-nop-image", "ghcr.io/tektoncd/pipeline/nop-...",               # <<== HERE
    "-sidecarlogresults-image", "ghcr.io/tektoncd/pipeline/side...", # <<== HERE
    "-workingdirinit-image", "ghcr.io/tektoncd/pipeline/working...", # <<== HERE
    # ...
]
```

Find all the gcr entries in other components and update them similar to the Tekton pipelines controller.

In general the change should resemble this:

```sh
# old
gcr.io/tekton-releases/github/tektoncd/pipeline/cmd/entrypoint:v0.9.2

# new
ghcr.io/tektoncd/github.com/tektoncd/pipeline/cmd/entrypoint:v0.9.2
```

You could run:

```sh
sed -e 's,gcr.io/tekton-releases,ghcr.io/tektoncd,g' 
```

## End of Life Releases

We started enforcing the download of Tekton images from `ghcr.io`.

Here are the details of what changed:

- Tekton LTS releases originally released to `gcr.io` will remain available on `gcr.io` until the EOL date.
- The same images are available on `ghcr.io`, so we ask users to please update their manifests and download images from `ghcr.io` to save egress bandwidth costs.
- Any EOL Tekton release will only be available on `ghcr.io`.
- Images on `gcr.io` will be removed from public access over the next few days.
- New releases will only be made on `ghcr.io`, so no action is required.

Please feel free to reach out to us via [Slack](https://github.com/tektoncd/community/blob/main/contact.md#slack) or our [mailing list](https://github.com/tektoncd/community/blob/main/contact.md#mailing-list) if you have any questions.

The original info mails were sent on our mailing list and if you're in our google group you can read them [here](https://groups.google.com/g/tekton-dev/c/RoEFXeNZjKE).
