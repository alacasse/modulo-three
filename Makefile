DEV_IMAGE  := modulo-three-dev
APP_IMAGE  := modulo-three-app
ARGS       ?= --interactive
DOCKER_TTY := $(shell if [ -t 0 ] && [ -t 1 ]; then echo -it; else echo -i; fi)
PRE_COMMIT_HOME ?= $(CURDIR)/.cache/pre-commit

.PHONY: build-dev build-app run run-dev test lint format typecheck check pre-commit-install pre-commit docs

build-dev:
	docker build -t $(DEV_IMAGE) -f Dockerfile.dev .

build-app:
	docker build -t $(APP_IMAGE) -f Dockerfile .

run: build-app
	docker run --rm $(DOCKER_TTY) $(APP_IMAGE) $(ARGS)

run-dev: build-dev
	docker run --rm $(DOCKER_TTY) -v $(CURDIR):/app $(DEV_IMAGE) python -m modulo_three $(ARGS)

test: build-dev
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) pytest -q tests

lint: build-dev
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) ruff check modulo_three tests

format: build-dev
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) ruff format modulo_three tests

typecheck: build-dev
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) sh -c "mypy modulo_three tests && pyright"

check: lint typecheck test

pre-commit-install: build-dev
	docker run --rm -e PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) -v $(PRE_COMMIT_HOME):/root/.cache/pre-commit -v $(CURDIR):/app $(DEV_IMAGE) pre-commit install --hook-type pre-commit --hook-type pre-push

pre-commit: build-dev
	docker run --rm -e PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) -v $(PRE_COMMIT_HOME):/root/.cache/pre-commit -v $(CURDIR):/app $(DEV_IMAGE) pre-commit run --all-files

docs:
	@echo "TODO: wire docs generation command"
