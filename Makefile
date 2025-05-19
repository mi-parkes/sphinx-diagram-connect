.ONESHELL:

ALPINE := $(shell if [ -f /etc/alpine-release ]; then echo yes; else echo no; fi)

.PHONY: doc doc-clean

help:
ifeq ($(ALPINE), yes)
	echo "Running on Alpine Linux using task extension may fail"
	echo -e "\n\tpoetry install --without dev"
	echo
endif
	echo "$(MAKE) install         # Rebuild and reinstall sphinx-ref-in-plantuml-hyperlinks"
	echo "$(MAKE) installx        # Reinstall sphinx-ref-in-plantuml-hyperlinks in active virtual environment"
	echo "$(MAKE) html            # Build sphinx-ref-in-plantuml-hyperlinks documentation"
	echo "$(MAKE) webserver       # Run webserver hosting sphinx-ref-in-plantuml-hyperlinks documentation in docker container"
	echo "$(MAKE) show            # View the documentation for sphinx-ref-in-plantuml-hyperlinks, which is hosted on a server running nginx, in a web browser"

helpx:
	echo "$(MAKE) prep-release    # Prepare release data"
	echo "$(MAKE) upload-package  # Upload package to PYPI"
	echo "$(MAKE) test-building-package # Fetched from github"
	echo "$(MAKE) test-using-package # Using local build or PYPI"

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
	poetry run $(SHELL) -c "cd doc && sphinx-build -M html source build"

htmlx:html
	cp -r doc/build/html/* docs

doc-clean:
	rm -rf doc/build

WEBSERVERPORT=8080

webserver:
	docker ps | awk '$$NF=="sphinx-ref-in-plantuml-hyperlinks"{print "docker stop "$$1}' | $(SHELL)
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
	$(MAKE) html

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
	poetry run $(SHELL) -c "cd doc && sphinx-build -M html source build"

clean-dc:
	docker images | awk '$$1=="<none>"{print "docker rmi "$$3}' | $(SHELL)

