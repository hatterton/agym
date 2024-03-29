
.PHONY: init-env
init-env:
	cd src && poetry install

.PHONY: shell
shell:
	cd src && poetry shell


.PHONY: run
run:
	cd src && poetry run python -m agym


.PHONY: run-profiling
run-profiling:
	cd src && poetry run py-spy record -o agym.svg -- python -m agym


.PHONY: lint
lint:
	make mypy
	make flake8
	make black
	make isort


.PHONY: format
format:
	cd src && poetry run autoflake -r -i .
	cd src && poetry run black .
	cd src && poetry run isort .


.PHONY: tests
tests: | tests-unit tests-integration


.PHONY: tests-unit
tests-unit:
	cd src && poetry run python -m pytest -xs tests/unit


.PHONY: tests-integration
tests-integration:
	cd src && poetry run python -m pytest -xs tests/integration


.PHONY: tests-gui
tests-gui:
	cd src && poetry run python -m pytest -xs tests/gui


.PHONY: tests-custom
tests-custom:
	cd src && poetry run python -m pytest -m "kdtree and tree" -xsv tests


.PHONY: mypy
mypy:
	cd src && poetry run mypy .


.PHONY: flake8
flake8:
	cd src && poetry run flake8 .


.PHONY: black
black:
	cd src && poetry run black --check --diff --color .


.PHONY: isort
isort:
	cd src && poetry run isort --check-only .


.PHONY: clean
clean:
	find src -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
