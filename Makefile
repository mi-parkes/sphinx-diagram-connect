.ONESHELL:
SHELL=/bin/bash

help:
	echo "$(MAKE) install         # Rebuild and reinstall sphinx-ref-in-plantuml-hyperlinks"
	echo "$(MAKE) installx        # Reinstall sphinx-ref-in-plantuml-hyperlinks in active virtual environment"
	echo "$(MAKE) html            # Build sphinx-ref-in-plantuml-hyperlinks documentation"
	echo "$(MAKE) webserver       # Run webserver hosting sphinx-ref-in-plantuml-hyperlinks documentation in docker container"
	echo "$(MAKE) show            # View the documentation for sphinx-ref-in-plantuml-hyperlinks, which is hosted on a server running nginx, in a web browser"

helpx:
	echo "$(MAKE) prep-release    # Prepare release data"
	echo "$(MAKE) upload-package  # Uplaod package to PYPI"

$(VERBOSE).SILENT:
	echo

doc/.venv:
	python3 -m venv doc/.venv
	source doc/.venv/bin/activate
	pip install -r doc/requirements.txt

install: doc/.venv
	source doc/.venv/bin/activate
	rm -rf build dist doc/build
	python -m build  --sdist --wheel
	pip uninstall sphinx-ref-in-plantuml-hyperlinks -y
	pip install dist/sphinx_ref_in_plantuml_hyperlinks*.whl

prep-release: doc/.venv
	source doc/.venv/bin/activate
	python -m pip install --upgrade twine
	rm -rf build dist doc/build
	python -m build  --sdist
	tar -tf dist/*

upload-package:
	source doc/.venv/bin/activate
	python -m twine upload  dist/* --verbose

installx:
	pip uninstall sphinx-ref-in-plantuml-hyperlinks -y
	pip install dist/sphinx_ref_in_plantuml_hyperlinks*.whl

html:
	source doc/.venv/bin/activate
	$(MAKE) -C doc clean html

WEBSERVERPORT=8080

webserver:
	docker ps | awk '$$NF=="sphinx-ref-in-plantuml-hyperlinks"{print "docker stop "$$1}' | bash
	sleep 1
	docker run -it --rm -d -p $(WEBSERVERPORT):80 --name sphinx-ref-in-plantuml-hyperlinks -v $$PWD/doc/build/html:/usr/share/nginx/html nginx

show:
	open http://localhost:$(WEBSERVERPORT)

