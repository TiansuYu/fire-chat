
.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## install core dependencies
	uv sync

install-all: ## install all dependencies
	uv sync --all-extra -dev

build: ## build the project
	uv build

publish: ## publish the project
	uv publish

build-and-publish: build publish ## build and publish the project
