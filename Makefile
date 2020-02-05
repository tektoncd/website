NODE_BIN = node_modules/.bin
FIREBASE = $(NODE_BIN)/firebase
PROJECT  = tekton

clean:
	rm -rf public resources

serve:
	hugo server \
	--buildDrafts \
	--buildFuture \
	--disableFastRender \
	--ignoreCache

build:
	hugo

production-build:
	hugo

deploy: clean build
	$(FIREBASE) deploy --project $(PROJECT)

open:
	open https://$(PROJECT).firebaseapp.com
