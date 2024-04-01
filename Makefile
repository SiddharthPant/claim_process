# See `make help` for a list of all available commands.
.ONESHELL:
.DEFAULT_GOAL := help
SHELL=/bin/bash -eu -o pipefail


README.md: Makefile ## Update dynamic blocks in README.md
	poetry run cog -r README.md

.PHONY: install
install:  ## Setup environment
	poetry install

.PHONY: fmt
fmt:  ## Format Python code
	poetry run ruff format .

.PHONY: lint
lint:  ## Lint Python code
	poetry run ruff check .

.PHONY: fix
fix:  ## Fix linting errors
	poetry run ruff check --fix .

.PHONY: up
run:  ## Stand up the environment
	docker compose up --build

.PHONY: test
test:  ## Run tests
	curl localhost:8004/ping

.PHONY: help
help:
	@echo -e "Available make commands:"
	@echo -e ""
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sort | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\1:\2/' | awk -F: '{ printf "%-25s %s\n", $$1, $$2 }')"

