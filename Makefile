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
	echo "$(MAKE) upload-package  # Upload package to PYPI"
	echo "$(MAKE) test-building-package # Fetched from github
	echo "$(MAKE) test-using-package # Using local build or PYPI

$(VERBOSE).SILENT:
	echo

doc/.venv:
	poetry install

install: doc/.venv
	rm -rf build dist doc/build
	poetry install

prep-release: doc/.venv
	rm -rf build dist doc/build
	poetry install
	poetry build
	tar -tf dist/*.tar.gz

upload-package:
	poetry publish

installx:
	pip uninstall sphinx-ref-in-plantuml-hyperlinks -y
	pip install dist/sphinx_ref_in_plantuml_hyperlinks*.whl

html:
	poetry run task doc

htmlx:
	poetry run task doc
	cp -r doc/build/html/* docs

WEBSERVERPORT=8080

webserver:
	docker ps | awk '$$NF=="sphinx-ref-in-plantuml-hyperlinks"{print "docker stop "$$1}' | bash
	sleep 1
	docker run -it --rm -d -p $(WEBSERVERPORT):80 --name sphinx-ref-in-plantuml-hyperlinks -v $$PWD/doc/build/html:/usr/share/nginx/html nginx

show:
	open http://localhost:$(WEBSERVERPORT)

test-building-package:
	$(eval WDIR=/tmp/test)
	$(eval BRANCH=main)
	mkdir -p $(WDIR)
	rm -rf $(WDIR)/*
	cd $(WDIR)
	git clone -b $(BRANCH) --single-branch \
			https://github.com/mi-parkes/sphinx-ref-in-plantuml-hyperlinks.git
	cd sphinx-ref-in-plantuml-hyperlinks
#	poetry install --only test,docs
	poetry install
	poetry build
	poetry run task doc

test-using-package:
	$(eval ODIR=/tmp/$@)
	rm -rf $(ODIR)/
	mkdir -p $(ODIR)
	cd $(ODIR)
	poetry init \
			-n \
			--name $@ \
			--description "$@" \
			--author john.doe \
			--python "^3.10" \
			-l MIT

	$(if $(VERBOSE),ls -l.)
	$(if $(VERBOSE),cat pyproject.toml,)

	poetry add \
		$(if $(LOCAL_MODE),$(CURDIR)/dist/sphinx_ref_in_plantuml_hyperlinks-*-py3-none-any.whl,sphinx-ref-in-plantuml-hyperlinks="*") \
		sphinx-book-theme="*" \
		sphinxcontrib-plantuml="0.30"

	cp -r $(CURDIR)/doc .
	$(if $(VERBOSE),poetry show,)
	poetry run  bash -c "cd doc && sphinx-build -M html source build"
