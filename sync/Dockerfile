FROM python:3.7

WORKDIR /app
# Only copy specific values instead of the entire directory.
# We're primarily trying to avoid pulling in config/, since it's confusing that
# it will not be used.
COPY sync.py sync.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "sync.py" ]
