# Developing the Tekton website

- [Developing the Tekton website](#developing-the-tekton-website)
- [Running in a Docker container](#running-in-a-docker-container)
- [Running Natively](#running-natively)
- [tekton.dev](#tektondev)

## Running in a Docker container

### Prerequisites

Install [Docker Compose](https://docs.docker.com/compose/install/).

### Setup

1. Build the Docker image

   ```bash
   docker-compose build

   ```

1. Run the built image

   ```bash
   docker-compose up
   ```

1. Verify that the website is working

   Open your web browser and type `http://localhost:8888` in the navigation bar.
   This opens a local instance of the website, you can now make changes in the
   documentation and those changes will immediately show up in the browser after
   you save.

To remove the produced images run:

```bash
docker-compose rm
```

## Running Natively

### Prerequisites

* [python3](https://www.python.org/downloads/) 
* [hugo v0.107.0 (EXTENDED VERSION)](https://github.com/gohugoio/hugo/releases/v0.107.0)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [git 1.8.5 or later](https://github.com/git/git/releases)
* [npm v6.14.5](https://nodejs.org/en/)
* [node v14.3.0](https://nodejs.org/en/)
* [netlify cli](https://cli.netlify.com/getting-started)
* [netlify account](https://app.netlify.com/)

### Setup

1. Clone the repository

   ```bash
   git clone https://github.com/tektoncd/website && cd website
   ```

1. Install the required node modules

   ```bash
   npm install
   ```

1. Install the dependencies for the [sync script](https://github.com/tektoncd/website/blob/master/sync/README.md)

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    
   pip3 install -r requirements.txt

   ```

1. Run the sync script

   ```bash
   ./sync/sync.py
   ```

1. Serve the website locally

   ```bash
   netlify dev
   ```

1. Verify that the website is working

   Open your web browser and type `http://localhost:8888` in the navigation bar.
   This opens a local instance of the website, you can now make changes in the
   documentation and those changes will immediately show up in the browser after
   you save.

The `sync.py` script clones the required repositories to a local cache folder, by default `sync/.cache`.
You can modify content and create commits in your local cache to test changes to the original docs.

To force and update of the local cache, use `./sync/sync.py --update-cache`.

## tekton.dev

- The latest website is available at [https://tekton.dev/](https://tekton.dev/).
- The old website is available at [https://tekton-old.netlify.app/](https://tekton-old.netlify.app/) and based on the branch [website-old](https://github.com/tektoncd/website/tree/website-old).
