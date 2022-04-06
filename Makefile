PYTHON ?= python3.8

# Black
black_reformat:
	$(PYTHON) -m black --line-length 99 .
black_stylecheck:
	$(PYTHON) -m black --line-length 99 --check .
black_stylediff:
	$(PYTHON) -m black --line-length 99 --check --diff .

# Isort
isort_reformat:
	$(PYTHON) -m isort --line-length 99 .
isort_stylecheck:
	$(PYTHON) -m isort --line-length 99 --check .
isort_stylediff:
	$(PYTHON) -m isort --line-length 99 --check --diff .