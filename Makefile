venv:
	python3 -m venv venv
install:
	pip3 install -r requirements.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 10112