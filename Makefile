
.PHONY: run
run:
	cd src && poetry run python -m agym

.PHONY: tests-unit
tests-unit:
	cd src && poetry run python -m pytest -xs tests/unit

.PHONY: tests-integration
tests-integration:
	cd src && poetry run python -m pytest -xs tests/integration

.PHONY: tests-gui
tests-gui:
	cd src && poetry run python -m pytest -xs tests/gui

.PHONY: tests
tests: | tests-unit tests-integration

.PHONY: tests-custom
tests-custom:
	cd src && poetry run python -m pytest -m "intersections" tests

.PHONY: env
env:
	cd src && poetry shell

.PHONY: clean
clean:
	find src -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
