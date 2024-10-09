project_dir := src

# Lint code
.PHONY: lint
lint:
	black --check --diff $(project_dir)
	ruff $(project_dir)

# Reformat code
.PHONY: reformat
reformat:
	black $(project_dir)
	ruff $(project_dir) --fix

.PHONY: run
run:
	python -m src || true
