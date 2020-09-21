.PHONY: sync
sync:
	pip install -r requirements.txt
	python3 -m flake8 sync/sync.py
	python3 -m flake8 sync/test_sync.py
	coverage run sync/test_sync.py
	coverage report -m sync/sync.py
	python3 sync/sync.py

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
