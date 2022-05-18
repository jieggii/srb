bot := services/bot
daemon  := services/daemon
srblib-wheel := srblib/dist/srblib--py3-none-any.whl


all: prepare-prod docker-build

build-srblib:
	pdm build --no-sdist --no-clean --project srblib

prepare-dev-srblib:
	cd srblib && pdm install

prepare-dev-bot:
	cd $(bot) && pdm install
	cd $(bot) && pdm add --dev -e ../../srblib

prepare-prod-bot:
	cd $(bot) && pdm export --prod --format requirements --output requirements.txt
	cp $(srblib-wheel) $(bot)

prepare-dev-daemon:
	cd $(daemon) && pdm install
	cd $(daemon) && pdm add --dev -e ../../srblib

prepare-prod-daemon:
	cd $(daemon) && pdm export --prod --format requirements --output requirements.txt
	cp $(srblib-wheel) $(daemon)

prepare-prod: build-srblib prepare-prod-bot prepare-prod-daemon
prepare-dev: prepare-dev-srblib prepare-dev-bot prepare-dev-daemon

docker-build-bot:
	docker build --tag srb-bot $(bot)

docker-build-daemon:
	docker build --tag srb-daemon $(daemon)

docker-build: docker-build-bot docker-build-daemon

clean:
	rm -rf srblib/__pypackages__/
	rm -rf srblib/dist/

	rm -rf $(bot)/__pypackages__/
	rm -rf $(bot)/requirements.txt
	rm -rf $(bot)/srblib--py3-none-any.whl

	rm -rf $(daemon)/__pypackages__/
	rm -rf $(daemon)/requirements.txt
	rm -rf $(daemon)/srblib--py3-none-any.whl
