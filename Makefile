PYTHON ?= python3.8

# Black
black-reformat:
	$(PYTHON) -m black .
black-stylecheck:
	$(PYTHON) -m black --check .
black-stylediff:
	$(PYTHON) -m black --check --diff .

# Isort
isort-reformat:
	$(PYTHON) -m isort .
isort-stylecheck:
	$(PYTHON) -m isort --check .
isort-stylediff:
	$(PYTHON) -m isort --check --diff .