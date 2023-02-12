all: black isort flake8 mypy pyright pylint

black:
	poetry run black .

isort:
	poetry run isort .

flake8:
	poetry run flake8

mypy:
	poetry run mypy

pyright:
	poetry run pyright

pylint:
	poetry run pylint bolt11/
