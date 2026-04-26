.PHONY: install dev test run-api run-ui ingest evaluate export-finetune

install:
	pip install -e .[dev]

dev:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

run-api:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000

run-ui:
	streamlit run frontend/app.py

ingest:
	python scripts/ingest.py

evaluate:
	python scripts/evaluate.py

export-finetune:
	python backend/finetuning/train.py
