# Makefile for project shortcuts using Hatch.
# To set up the development environment, run `hatch shell`.

.PHONY: test format lint ci

# Run tests using the 'test' script defined in pyproject.toml
test:
	@echo "--> Running tests..."
	@hatch test

# Format code using the 'format' script
format:
	@echo "--> Formatting code..."
	@hatch run format

# Lint code using the 'lint' script
lint:
	@echo "--> Linting code..."
	@hatch run lint

# Run all CI checks
ci:
	@echo "--> Running all CI checks..."
	@hatch run ci