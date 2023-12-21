all: test

lint:
	python3 -m black . --check
	npx prettier@3.0.3 --check .

test: lint
	pytest

format:
	python3 -m black .
	npx prettier@3.0.3 --write .

run:
	flask --app inferential run

clean:
	rm -rf .pytest_cache __pycache__
