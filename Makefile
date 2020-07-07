.PHONY: init ci reformat reformat-check flake8 isort isort-check lint

init:
	poetry install

ci:
	poetry run pytest --cov=./

reformat:
	black .

reformat-check:
	black --check .

flake8:
	flake8 .

isort:
	isort -y

isort-check:
	isort --check-only --diff

lint: reformat-check flake8 isort-check
