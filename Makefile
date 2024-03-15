install:
	poetry install --only main
install-dev:
	poetry install
test:
	poetry run python -m pytest .
run:
	poetry run python scraper/main.py
