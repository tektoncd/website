FROM klakegg/hugo:ext-ubuntu as website
RUN apt -y update && apt -y install git build-essential python3-venv python3-pip
COPY . /src
RUN git config --global --add safe.directory /src
RUN npm install
RUN npm install -g netlify-cli

RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/usr/bin/netlify"]
CMD ["dev"]
