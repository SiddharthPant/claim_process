# See `make help` for a list of all available commands.
.ONESHELL:
.DEFAULT_GOAL := help
SHELL=/bin/bash -eu -o pipefail
VENV_BIN=.venv/bin

requirements.txt: pyproject.toml  ## Generate requirements.txt from pyproject.toml
	 $(VENV_BIN)/pip-compile -v \
	  --resolver=backtracking \
	  --strip-extras \
	  --output-file=requirements.txt \
	  pyproject.toml

.PHONY: venv
venv: pyproject.toml ## Install dev requirements in virtual env from pyproject.toml
	$(VENV_BIN)/pip install -e .[dev] -c requirements.txt

README.md: Makefile ## Update dynamic blocks in README.md
	$(VENV_BIN)/cog -r README.md

.PHONY: fmt
fmt:  ## Format Python code
	$(VENV_BIN)/ruff format .

.PHONY: lint
lint:  ## Lint Python code
	$(VENV_BIN)/ruff check .

.PHONY: fix
fix:  ## Fix linting errors
	$(VENV_BIN)/ruff check --fix .

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

