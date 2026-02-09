DEV_IMAGE  := modulo-three-dev
APP_IMAGE  := modulo-three-app
ARGS       ?= --interactive
DOCKER_TTY := $(shell if [ -t 0 ] && [ -t 1 ]; then echo -it; else echo -i; fi)
PRE_COMMIT_HOME ?= $(CURDIR)/.cache/pre-commit
PYRIGHT_CACHE_HOME ?= $(CURDIR)/.cache/pyright-python

.PHONY: ensure-dev-image build-dev build-app run run-dev test lint format typecheck check pre-commit-install pre-commit docs

ensure-dev-image:
	@if ! docker image inspect $(DEV_IMAGE) >/dev/null 2>&1; then \
		$(MAKE) build-dev; \
	fi

build-dev:
	docker build -t $(DEV_IMAGE) -f Dockerfile.dev .

build-app:
	docker build -t $(APP_IMAGE) -f Dockerfile .

run: build-app
	docker run --rm $(DOCKER_TTY) $(APP_IMAGE) $(ARGS)

run-dev: ensure-dev-image
	docker run --rm $(DOCKER_TTY) -v $(CURDIR):/app $(DEV_IMAGE) python -m modulo_three $(ARGS)

test: ensure-dev-image
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) pytest -q tests

lint: ensure-dev-image
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) ruff check modulo_three tests

format: ensure-dev-image
	docker run --rm -v $(CURDIR):/app $(DEV_IMAGE) ruff format modulo_three tests

typecheck: ensure-dev-image
	docker run --rm -v $(PYRIGHT_CACHE_HOME):/root/.cache/pyright-python -v $(CURDIR):/app $(DEV_IMAGE) sh -c "mypy modulo_three tests && pyright"

check: lint typecheck test

pre-commit-install: ensure-dev-image
	docker run --rm -e PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) -v $(PRE_COMMIT_HOME):/root/.cache/pre-commit -v $(CURDIR):/app $(DEV_IMAGE) pre-commit install --hook-type pre-commit --hook-type pre-push

pre-commit: ensure-dev-image
	docker run --rm -e PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) -v $(PRE_COMMIT_HOME):/root/.cache/pre-commit -v $(CURDIR):/app $(DEV_IMAGE) pre-commit run --all-files

docs:
	@echo "TODO: wire docs generation command"
