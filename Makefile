include common.mk

MODULES=terra_pandas tests
tests:=$(wildcard tests/test_*.py)

test: lint mypy tests

lint:
	flake8 $(MODULES) *.py

mypy:
	mypy --ignore-missing-imports $(MODULES)

test: $(tests)
	coverage combine
	rm -f .coverage.*

# A pattern rule that runs a single test script
$(tests): %.py : mypy lint
	coverage run -p --source=terra-pandas $*.py --verbose

version: terra_pandas/version.py

terra_pandas/version.py: setup.py
	echo "__version__ = '$$(python setup.py --version)'" > $@

clean:
	git clean -dfx

build: version clean
	python setup.py bdist_wheel

sdist: clean
	python setup.py sdist

install: build
	pip install --upgrade dist/*.whl

.PHONY: test lint mypy tests clean build install
