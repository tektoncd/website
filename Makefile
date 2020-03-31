serve:
	python sync/sync.py && \
	hugo server \
	--buildDrafts \
	--buildFuture \
	--disableFastRender \
	--ignoreCache \
	--watch

production-build:
	python sync/sync.py && hugo

preview-build:
	python sync/sync.py && hugo --baseURL $(DEPLOY_PRIME_URL)
