# sync

This directory includes a helper script for synchronizing contents
from specified Tekton repositories to this repository.

To run this script locally, set up a Python 3 environment with appropriate
Google Cloud Platform credentials, and execute the following command:

```bash
pip3 install -r requirements.txt
python3 sync.py
```

## Usage

```bash
       USAGE: sync.py [flags]
flags:

sync.py:
  -c,--config: Config directory
    (default: 'config')

Try --helpfull to get a list of all flags.
```
