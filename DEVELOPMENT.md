# Developing the Tekton website

- [Developing the Tekton website](#developing-the-tekton-website)
- [Running Locally](#running-locally)
- [tekton.dev](#tektondev)

## Dependencies

* [python3](https://www.python.org/downloads/) 
* [hugo (EXTENDED VERSION)](https://github.com/gohugoio/hugo/releases)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [npm v6.14.5](https://nodejs.org/en/)
* [node v14.3.0](https://nodejs.org/en/)
* [netlify cli](https://cli.netlify.com/getting-started)
* [netlify account](https://app.netlify.com/)

## Running Locally

Step 1
```bash
# Clone the repo
git clone https://github.com/tektoncd/website && cd website
```

Step 2
```bash
# Install node modules
npm install
```

Step 3
```bash
Install the sync script (https://github.com/tektoncd/website/blob/master/sync/README.md)
python3 -m venv .venv
source .venv/bin/activate    
pip3 install -r requirements.txt

```
Step 4
```bash
# Run the sync.
# This clones docs repositories to local cache and builds the
# documentation content for the website
./sync/sync.py
```

Step 5
```bash
# Build and serve the website locally
netlify dev
```

The `sync.py` script clones the required repositories to a local cache folder, by default `sync/.cache`.
You can modify content and create commits in your local cache to test changes to the original docs.

To force and update of the local cache, use `./sync/sync.py --update-cache`.

## tekton.dev

- The latest website is available at [https://tekton.dev/](https://tekton.dev/).
- The old website is available at [https://tekton-old.netlify.app/](https://tekton-old.netlify.app/) and based on the branch [website-old](https://github.com/tektoncd/website/tree/website-old).
