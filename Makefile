DEV_IMAGE  := modulo-three-dev
APP_IMAGE  := modulo-three-app
ARGS       ?= --interactive
DOCKER_TTY := $(shell if [ -t 0 ] && [ -t 1 ]; then echo -it; else echo -i; fi)
PRE_COMMIT_HOME ?= $(CURDIR)/.cache/pre-commit
PYRIGHT_CACHE_HOME ?= $(CURDIR)/.cache/pyright-python
DEV_FINGERPRINT := $(shell cat pyproject.toml Dockerfile.dev | sha256sum | cut -d' ' -f1)

.PHONY: ensure-dev-image build-dev build run run-dev test lint format typecheck check pre-commit-install pre-commit docs

ensure-dev-image:
	@current=$$(docker image inspect -f '{{ index .Config.Labels "org.modulo-three.dev-fingerprint" }}' $(DEV_IMAGE) 2>/dev/null || true); \
	if [ "$$current" != "$(DEV_FINGERPRINT)" ]; then \
		$(MAKE) build-dev; \
	fi

build-dev:
	docker build --build-arg DEV_FINGERPRINT=$(DEV_FINGERPRINT) -t $(DEV_IMAGE) -f Dockerfile.dev .

build:
	docker build -t $(APP_IMAGE) -f Dockerfile .

run: build
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
	@echo "Project documentation:"
	@echo " - README.md"
	@find docs -maxdepth 1 -type f -name '*.md' | sort | sed 's#^# - #'
