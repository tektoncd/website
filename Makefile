.PHONY: sync
sync:
	python3 sync/sync.py --update-cache

.PHONY: serve
serve:
	hugo server \
	--baseURL $(URL) \
	--buildDrafts \
	--buildFuture \
	--disableFastRender \
	--ignoreCache \
	--watch

.PHONY: production-build
production-build: sync
	hugo --baseURL $(URL)

.PHONY: preview-build
preview-build: sync
	hugo --baseURL $(DEPLOY_PRIME_URL)
