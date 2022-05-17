# Subscriptions reminder telegram bot
## Dependencies
* [pdm](https://github.com/pdm-project/pdm)
* [docker(https://github.com/docker/cli)]
* [docker-compose](https://github.com/docker/compose)

## Running
Run make at first to do some stuff with dependencies and build docker containers for **bot** and **daemon**:

`make`

Don't waste your time - set environment variables in `.env` file. (Use `.env.example` as template) while make is running.

The last step - run this garbage:

`docker-compose up`

Enjoy.
