FROM klakegg/hugo:0.94.2-ext-alpine as dependencies
# Install the dependencies and sync remote files
RUN apk add git gcc build-base python3-dev py3-pip
WORKDIR /app
COPY . /app
RUN npm install
RUN pip3 install -r requirements.txt
RUN make sync

FROM klakegg/hugo:0.94.2-ext-alpine as website
#Later versions have errors inside a container
RUN npm install -g netlify-cli@9.16.7 
COPY . /src
COPY --from=dependencies /app/node_modules /src/node_modules
COPY --from=dependencies /app/content/en/docs/Reference /src/content/en/docs/Reference

ENTRYPOINT ["/usr/local/node/bin/netlify"]
CMD ["dev"]
