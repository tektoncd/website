FROM gcr.io/google-appengine/python

RUN virtualenv /env -p python3

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV PORT 8080

COPY app /cache/app

RUN pip install -r /cache/app/requirements.txt

WORKDIR /cache/app
CMD gunicorn -b :$PORT main:app