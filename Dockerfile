FROM klakegg/hugo:ext-alpine as dependencies

WORKDIR /app
RUN apk add git gcc build-base python3-dev py3-pip
COPY . /app
RUN npm install
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip3 install -r requirements.txt
RUN make sync


FROM klakegg/hugo:ext-alpine as website
COPY . /src
RUN git config --global --add safe.directory /src
COPY --from=dependencies /app/node_modules /src/node_modules
COPY --from=dependencies /app/content/en/docs/Pipelines /src/content/en/docs/Pipelines
COPY --from=dependencies /app/content/en/docs/Triggers /src/content/en/docs/Triggers
COPY --from=dependencies /app/content/en/docs/CLI /src/content/en/docs/CLI
COPY --from=dependencies /app/content/en/vault /src/content/en/vault
COPY --from=dependencies /app/sync/.cache /src/sync/.cache

CMD ["serve", "--baseURL http://localhost:8888/", "--buildDrafts", "--buildFuture", "--disableFastRender", "--ignoreCache", "--watch"]
