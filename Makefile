.PHONY: sync
sync:
	python sync/sync.py

.PHONY: serve
serve:
	hugo server \
	--buildDrafts \
	--buildFuture \
	--disableFastRender \
	--ignoreCache \
	--watch

.PHONY: production-build
production-build: sync
	hugo

.PHONY: preview-build
preview-build: sync
	hugo --baseURL $(DEPLOY_PRIME_URL)
