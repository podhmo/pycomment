test:
	python setup.py test
ci:
	$(MAKE) test lint

format:
#	pip install -e .[dev]
	black pycomment setup.py

lint:
#	pip install -e .[dev]
	flake8 pycomment --ignore W503,E203,E501

# typing:
# #	pip install -e .[dev]
# 	mypy --strict --strict-equality --ignore-missing-imports pycomment

examples:
	$(MAKE) -C examples

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/pycomment-$(shell cat VERSION)*
	twine upload dist/pycomment-$(shell cat VERSION)*

.PHONY: test format lint build upload examples typing
