.PHONY: all
all:
	cp .env-sample .env
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
