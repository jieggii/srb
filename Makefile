.PHONY: build-srblib prepare-bot prepare-daemon prepare build-bot build-daemon build
bot := services/bot
daemon  := services/daemon
srblib-wheel := srblib/dist/srblib--py3-none-any.whl

build-srblib:
	pdm build --no-sdist --no-clean --project srblib

prepare-bot:
	cd $(bot) && pdm export --prod --format requirements --output requirements.txt
	cp $(srblib-wheel) $(bot)

prepare-daemon:
	cd $(daemon) && pdm export --prod --format requirements --output requirements.txt
	cp $(srblib-wheel) $(daemon)

prepare: build-srblib prepare-bot prepare-daemon

build-bot:
	docker build --tag srb-bot $(bot)

build-daemon:
	docker build --tag srb-daemon $(daemon)

build: build-bot build-daemon