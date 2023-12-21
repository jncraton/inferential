all: test

lint:
	python3 -m black . --check
	npx prettier@3.0.3 --check *.md static/*.js

test: lint
	pytest

format:
	python3 -m black .
	npx prettier@3.0.3 --write .

clean:
	rm -rf .pytest_cache __pycache__
