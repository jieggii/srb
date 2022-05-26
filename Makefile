bot := ./services/bot
daemon := ./services/daemon
srblib := ./srblib
srblib-wheel := srblib-0.1.0-py3-none-any.whl

.PHONY: prepare clean build run

prepare:  # prepare dependencies before building docker containers
	cd $(srblib) && poetry build --format wheel
	cp -r $(srblib)/dist/$(srblib-wheel) $(bot)/
	cp -r $(srblib)/dist/$(srblib-wheel) $(daemon)/

	cd $(bot) && poetry export -o requirements.txt && sed -i '/srblib/d' requirements.txt
	cd $(daemon) && poetry export -o requirements.txt && sed -i '/srblib/d' requirements.txt

clean:  # clean everything that was created by `prepare` target
	rm -rf $(srblib)/dist/
	rm -f $(bot)/$(srblib-wheel) $(daemon)/$(srblib-wheel)
	rm -f $(bot)/requirements.txt $(daemon)/requirements.txt

build: prepare  # build docker containers and clean garbage
	docker compose build
	make clean

run: build
	docker compose up -d
