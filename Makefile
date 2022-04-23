PYTHON ?= python3.8

install-reqs:
    $(PYTHON) -m pip install -U black isort

# Black
black-reformat:
	$(PYTHON) -m black .
black-stylediff:
	$(PYTHON) -m black --check --color --diff .

# Isort
isort-reformat:
	$(PYTHON) -m isort .
isort-stylediff:
	$(PYTHON) -m isort --check --color --diff .