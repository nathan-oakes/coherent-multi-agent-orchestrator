fmt:
	python -m ruff check --fix .
	python -m ruff format .

test:
	python -m pytest -q

run:
	cmao
