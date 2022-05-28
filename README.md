# srb - subscriptions reminder (telegram) bot
(Work is still in progress)

It will remind you about your paid subscriptions so that you don't forget to pay or cancel them on time.

## Dependencies
* docker
* docker-compose (as docker plugin)

## Running
1. Create `./.env` file (use `./.env.example` as a template)
2. Run `docker compose build`
3. Run `docker compose up` to start the bot with its mongodb and notification daemon
