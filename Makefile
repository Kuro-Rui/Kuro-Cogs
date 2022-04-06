PYTHON ?= python3.8

# Black
black_reformat:
	$(PYTHON) -m black .
black_stylecheck:
	$(PYTHON) -m black --check .
black_stylediff:
	$(PYTHON) -m black --check --diff .

# Isort
isort_reformat:
	$(PYTHON) -m isort .
isort_stylecheck:
	$(PYTHON) -m isort --check .
isort_stylediff:
	$(PYTHON) -m isort --check --diff .