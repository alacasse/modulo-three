APP_IMAGE  := modulo-three-app
TEST_IMAGE := modulo-three-test
ARGS       ?= 1011
PRE_COMMIT_HOME ?= $(CURDIR)/.cache/pre-commit

.PHONY: app-build app-run test-build test-run test lint format typecheck check pre-commit-install pre-commit-run docs

app-build:
	docker build -t $(APP_IMAGE) -f Dockerfile .

app-run: app-build
	docker run --rm $(APP_IMAGE) $(ARGS)

test-build:
	docker build -t $(TEST_IMAGE) -f Dockerfile.test .

test-run: test-build
	docker run --rm $(TEST_IMAGE)

test:
	python -m pytest -q tests

lint:
	.venv/bin/ruff check modulo_three tests
	.venv/bin/ruff format --check modulo_three tests

format:
	.venv/bin/ruff format modulo_three tests

typecheck:
	.venv/bin/mypy modulo_three tests
	.venv/bin/pyright

check: lint typecheck test

pre-commit-install:
	PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) .venv/bin/pre-commit install --hook-type pre-commit --hook-type pre-push

pre-commit-run:
	PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) .venv/bin/pre-commit run --all-files

docs:
	@echo "TODO: wire docs generation command"
