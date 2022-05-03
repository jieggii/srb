fmt:
	pdm run isort bot/
	pdm run black bot/

run-local:
	pdm run dotenv -f .env run python -m bot
