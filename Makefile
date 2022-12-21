
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
	make black
	make isort


.PHONY: format
format:
	cd src && poetry run black .
	cd src && poetry run isort .


.PHONY: tests
tests: | tests-unit tests-integration


.PHONY: tests-custom
tests-custom:
	cd src && poetry run python -m pytest -m "kdtree and tree" -xsv tests


.PHONY: clean
clean:
	find src -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete



.PHONY: tests-unit
tests-unit:
	cd src && poetry run python -m pytest -xs tests/unit


.PHONY: tests-integration
tests-integration:
	cd src && poetry run python -m pytest -xs tests/integration


.PHONY: tests-gui
tests-gui:
	cd src && poetry run python -m pytest -xs tests/gui


.PHONY: mypy
mypy:
	cd src && poetry run mypy .


.PHONY: black
black:
	cd src && poetry run black --check --diff --color .


.PHONY: isort
isort:
	cd src && poetry run isort --check-only .
