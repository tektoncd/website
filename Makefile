.PHONY: sync
sync:
	git config http.postBuffer 524288000
	python3 sync/sync.py --update-cache

.PHONY: serve
serve: sync
	hugo server \
	--baseURL $(URL) \
	--buildDrafts \
	--buildFuture \
	--disableFastRender \
	--ignoreCache \
	--liveReloadPort 8888 \
	--watch

.PHONY: production-build
production-build: sync
	hugo --baseURL $(URL)

.PHONY: preview-build
preview-build: sync
	hugo --baseURL $(DEPLOY_PRIME_URL)
