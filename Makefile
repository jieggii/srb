fmt:
	pdm run isort bot/
	pdm run black bot/

lint:
	pdm run flake8 bot/

run-local:
	pdm run dotenv -f .env run python -m bot
