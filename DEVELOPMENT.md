# Developing the Tekton website

- [Developing the Tekton website](#developing-the-tekton-website)
  - [Running Locally](#running-locally)
  - [tekton.dev](#tektondev)

## Running Locally


The [tekton.dev](#tekton.dev) is deployed on Netlify. Netlify will invoke
[the Makefile](.Makefile) to build the website.

This is configured in:

* [netlify.toml](netlify.toml)
* [runtime.txt](runtime.txt) (the python runtime)
* [requirements.txt](requirements.txt) (the python requirements)

To run it locally you will need to install:

* [Hugo](https://gohugo.io/) [version 0.53](netlify.toml)
* `npm` to install Hugo's requirements:
  * `npm install` (in directory with [package.json](package.json))

Then you can run [hugo commands](https://gohugo.io/getting-started/usage/) such as:

```bash
hugo server
```

To run the [Makefile](Makefile) you will need more dependencies and flags:

* `python` aliased to python3.7 - [sync.py](sync/sync.py) is running `python` but assumes this is python3 (configured in [runtime.txt](runtime.txt))
* `pip`, to install python requirements:
  * Install with `pip install -r requirements.txt`

To run the makefile locally, you'll have to set the env var:

* [`DEPLOY_PRIME_URL`](https://docs.netlify.com/configure-builds/environment-variables/) to the path to your website files

For example:

```bash
DEPLOY_PRIME_URL=localhost make preview-build
```

## tekton.dev

- tekton.dev currently points at http://tekton-old.netlify.com/ which is deployed
  from [the website-old branch](https://github.com/tektoncd/website/tree/website-old)
- The WIP new website is at https://tekton-dev.netlify.com/ and tekton.dev will be updated
  to point at it once https://github.com/tektoncd/website/labels/kind%2Fbeta-blocking are completed
