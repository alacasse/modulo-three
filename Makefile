APP_IMAGE  := modulo-three-app
TEST_IMAGE := modulo-three-test
ARGS       ?= 1011

.PHONY: app-build app-run test-build test-run

app-build:
	docker build -t $(APP_IMAGE) -f Dockerfile .

app-run: app-build
	docker run --rm $(APP_IMAGE) $(ARGS)

test-build:
	docker build -t $(TEST_IMAGE) -f Dockerfile.test .

test-run: test-build
	docker run --rm $(TEST_IMAGE)
