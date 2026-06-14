.PHONY: install ingest run test lint format

install:
	poetry install

ingest:
	poetry run python src/ingest.py --config config.yaml

run:
	poetry run streamlit run src/app.py

test:
	poetry run pytest tests/ -v

lint:
	poetry run ruff check src/

format:
	poetry run black src/
