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
git clone https://github.com/tektoncd/website && cd website
```
Step 2
```bash
npm install
```
Step 3
```bash
pip install -r requirements.txt
```
Step 4
```bash
python3 sync/sync.py
```
Step 5
```bash
netlify dev
```

## tekton.dev

- The latest website is available at [https://tekton.dev/](https://tekton.dev/).
- The old website is available at [https://tekton-old.netlify.app/](https://tekton-old.netlify.app/) and based on the branch [website-old](https://github.com/tektoncd/website/tree/website-old).
