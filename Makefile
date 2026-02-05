.PHONY: test lint clean

test:
	PYTHONPATH=. .venv/bin/pytest tests/

lint:
	.venv/bin/flake8 discogs_cli tests

clean:
	rm -rf .pytest_cache
	rm -rf discogs_cli/__pycache__
	rm -rf tests/__pycache__
