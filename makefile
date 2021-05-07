make:
	python3.9 src/main.py

lint:
	autopep8 --in-place --recursive --aggressive .
	
push:
ifdef M
	@make lint && git add . && git commit -m "$(M)" && git push
else
	@echo Missing commit msg
endif

uml:
	pyreverse -mn -p Ants ./src/__main__.py