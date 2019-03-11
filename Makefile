NODE_BIN = node_modules/.bin
FIREBASE = $(NODE_BIN)/firebase
PROJECT  = tekton

serve:
	hugo server \
	--buildDrafts \
	--buildFuture \
	--disableFastRender \
	--ignoreCache

build:
	hugo

deploy: build
	$(FIREBASE) deploy --project $(PROJECT)