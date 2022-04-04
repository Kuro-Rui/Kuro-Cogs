PYTHON ?= python3.8

# Python Code Style
reformat:
	$(PYTHON) -m black --line-length 99 .
stylecheck:
	$(PYTHON) -m black --line-length 99 --check .
stylediff:
	$(PYTHON) -m black --line-length 99 --check --diff .