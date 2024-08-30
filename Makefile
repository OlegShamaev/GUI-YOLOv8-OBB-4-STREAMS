#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = Vtormet-CV
PYTHON_VERSION = 3.10.11
PYTHON_INTERPRETER := $(shell command -v python3 || command -v python)

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Set up python interpreter environment
.PHONY: create_venv
create_venv:
	$(PYTHON_INTERPRETER) -m venv .venv
	@echo ">>> New virtualenv created. Activate with: \nsource .venv/bin/activate"

## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 vtormet_cv
	isort --check --diff --profile black vtormet_cv
	black --check --config pyproject.toml vtormet_cv

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml vtormet_cv



#################################################################################
# Run                                                                          #
#################################################################################

## Run the main application
.PHONY: run
run:
	$(PYTHON_INTERPRETER) main.py

#################################################################################
# Data Base                                                                      #
#################################################################################
SCRIPT_DB = src.utils.db_config
SCRIPT_ENV = src.utils.create_env


## Create .env file for Data Base
.PHONY: db_env
db_env:
	@echo "Создание базы данных и директорий..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_ENV) import create_env_file; create_env_file()"

## Create Data Base PostgreSQL
.PHONY: db_create
db_create:
	@echo "Создание базы данных и директорий..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_DB) import create_database_and_folders; create_database_and_folders()"

## Create folders image and labels
.PHONY: folders_create
folders_create:
	@echo "Создание директорий..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_DB) import create_folders; create_folders()"

## Clear Data Base and image folders
.PHONY: clear_db
clear_db:
	@echo "Очистка таблиц и изображений..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_DB) import clear_tables; clear_tables()"
	
## Clear folders image and labels
.PHONY: clear_folders
clear_folders:
	@echo "Очистка директорий..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_DB) import clear_folder_images_and_labels; clear_folder_images_and_labels()"

## Create DUMP Files image and labels
.PHONY: dump_files
dump_files:
	@echo "Создание DUMP папок для изображений и меток..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_DB) import dump_files; dump_files()"

## Create DUMP Data Base and clean
.PHONY: dump_db
dump_db:
	@echo "Создание DUMP Databese и изображений в архив..."
	$(PYTHON_INTERPRETER) -c "from $(SCRIPT_DB) import create_dump_database_with_clear; create_dump_database_with_clear()"



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Install MkDocs
.PHONY: install_docs
install_docs:
	pip install mkdocs mkdocs-material

## Create site MkDocs
.PHONY: build_docs
build_docs:
	mkdocs build -f ./docs/mkdocs.yml

## Start site MkDocs
.PHONY: serve_docs
serve_docs:
	mkdocs serve -f ./docs/mkdocs.yml



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) vtormet_cv/data/make_dataset.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
