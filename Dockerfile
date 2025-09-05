FROM klakegg/hugo:0.107.0-ext-ubuntu as website
RUN apt-get -y update && apt-get -y install git build-essential python3-venv python3-pip
COPY . /src
RUN git config --global --add safe.directory /src
RUN npm install
RUN npm install -g netlify-cli@19.1.7

RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/usr/bin/netlify"]
CMD ["dev"]
