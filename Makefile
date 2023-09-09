PYTHON=$(shell which python3 )
VERSION=`cat lru/VERSION`

ifeq (, $(PYTHON))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.10
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'from sys import version_info as v; v_min=int("".join("$(PYTHON_VERSION_MIN)".split("."))); print(0) if int(str(v.major)+str(v.minor)) >= v_min else print(1)')
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )

PIP=$(PYTHON) -m pip

ifeq ($(PYTHON_VERSION_OK),1)
  $(error "Requires Python >= $(PYTHON_VERSION_MIN) - Installed: $(PYTHON_VERSION)")
endif

help: ## Print help for each target
	$(info Things3 low-level Python API.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

.PHONY: install
install: ## Installs dependencies.
	$(PIP) install -r requirements.txt

.PHONY: clean
clean: ## remove the python binary files.
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf build dist *.egg-info .pytest_cache cov_html .coverage

.PHONY: test
test: ## Lint the code
	pytest .
