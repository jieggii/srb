# srb - subscriptions reminder (telegram) bot
(Work is still in progress)

It will remind you about your paid subscriptions so that you don't forget to pay or cancel them on time.

## Dependencies
* python >= 3.10
* poetry
* docker
* docker-compose (as docker plugin)
* make

## Running
1. Create `./.env` file (use `./.env.example` as a template)
2. Run `make` command
3. Run `docker compose up` to start the bot with its mongodb and notification daemon

## Architecture
There are two services: the **bot**@./services/bot (Telegram bot) and the **daemon**@/services/daemon (notification daemon).
They both use the same local python package - **srblib**@./srblib/. To install **srblib** into docker container
we need some extra tricky steps which will be run by `make` command, that's why we need it. I also think that poetry installation 
(a package manager) into docker container is overhead, that's why we export dependencies into `requirements.txt` and install them
in containers via `pip install -r requirements.txt`. 

