.DEFAULT_GOAL := help
POETRY_RUN = poetry run
TEST = pytest $(arg)
CODE = src tests examples

COVERAGE_REPORT = htmlcov/status.json
COBERTURA_REPORT = cobertura.xml
COVERAGE_REPORT_FOLDER = $(shell dirname $(COVERAGE_REPORT))

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Runs pytest
	$(POETRY_RUN) $(TEST)

.PHONY: ruff-lint
ruff-lint: ## Lint code with ruff
	$(POETRY_RUN) ruff check $(CODE)

.PHONY: pylint
pylint: ## Lint code with pylint
	$(POETRY_RUN) pylint --jobs 1 --rcfile=pyproject.toml $(CODE)

.PHONY: mypy
mypy: ## Lint code with mypy
	$(POETRY_RUN) mypy $(CODE)

.PHONY: lint
lint: ruff-lint pylint mypy ## Lint code
	$(POETRY_RUN) pytest --dead-fixtures --dup-fixtures

.PHONY: format
format: ## Formats all files
	$(POETRY_RUN) ruff check --fix $(CODE)

.PHONY: check
check: format lint test ## Format and lint code then run tests

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: lock
lock: ## Lock dependencies
	poetry lock

.PHONY: build
build: ## Build wheels
	poetry build

.PHONY: publish
publish: ## Publish to PyPi
	poetry publish --username=$(PYPI_USERNAME) --password=$(PYPI_PASSWORD)
