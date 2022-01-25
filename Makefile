
.PHONY: run
run:
	cd src && poetry run python -m agym

.PHONY: tests
tests:
	cd src && poetry run pytest tests

.PHONY: env
env:
	cd src && poetry shell

.PHONY: clean
clean:
	find src -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
