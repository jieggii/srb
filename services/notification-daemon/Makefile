fmt:
	pdm run isort daemon/
	pdm run black daemon/

run:
	pdm run dotenv -f ../../.env run python -m daemon
