make:
	python3.9 src/main.py

lint:
	autopep8 --in-place --recursive --aggressive .