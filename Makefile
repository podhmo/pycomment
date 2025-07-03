# To install all development dependencies, run:
# pip install -e ".[dev,testing,examples]"

test:
	pytest

ci: test lint examples
	# Check if there are any uncommitted changes after running tests/linting
	git diff --exit-code

format:
	black pycomment

lint:
	flake8 pycomment --ignore W503,E203,E501

# typing:
#	mypy --strict --strict-equality --ignore-missing-imports pycomment

examples:
	# This assumes that the 'examples' directory contains its own Makefile
	$(MAKE) -C examples

build:
	# Clean previous builds and build sdist and wheel
	rm -rf dist/
	python -m build

upload: build
	twine check dist/*
	twine upload dist/*

.PHONY: test ci format lint typing examples build upload