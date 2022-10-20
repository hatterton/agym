
.PHONY: run
run:
	cd src && poetry run python -m agym

.PHONY: tests-unit
tests-unit:
	cd src && poetry run python -m pytest -xs tests/unit

.PHONY: tests-integration
tests-integration:
	cd src && poetry run python -m pytest -xs tests/integration
	# cd src && poetry run python -m pytest -xs tests/integration/breakout_collisions/test_ball_block.py::test_ball_corner_block_collision_type

.PHONY: tests-gui
tests-gui:
	cd src && poetry run python -m pytest -xs tests/gui

.PHONY: tests-gui
tests: | tests-unit tests-integration
# tests:
#     cd src && poetry run python -m pytest -xs tests/unit/test_kdtree.py

.PHONY: env
env:
	cd src && poetry shell

.PHONY: clean
clean:
	find src -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
