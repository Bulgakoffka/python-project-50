lint:
	uv run ruff check
install:
	pip install uv
rmcache:
	find . -name "__pycache__" -type d -exec rm -rf {} \;
run:
	uv run python3 gendiff/diff_core/diff_builder.py