.ONESHELL:
SHELL           =/bin/bash
MAKEFLAGS       += $(if $(VERBOSE),,--no-print-directory)
MINMAKEVERSION  =3.82

$(if $(findstring $(MINMAKEVERSION),$(firstword $(sort $(MINMAKEVERSION) $(MAKE_VERSION)))),,$(error The Makefile requires minimal GNU make version:$(MINMAKEVERSION) and you are using:$(MAKE_VERSION)))

ALPINE := $(shell if [ -f /etc/alpine-release ]; then echo yes; else echo no; fi)

.PHONY: doc doc-clean

help:
ifeq ($(ALPINE), yes)
	echo "Running on Alpine Linux using task extension may fail"
	echo -e "\n\tpoetry install --without dev"
	echo
endif
	echo "$(MAKE) install         # Rebuild and reinstall sphinx-diagram-connect"
	echo "$(MAKE) installx        # Reinstall sphinx-diagram-connect in active virtual environment"
	echo "$(MAKE) html            # Build sphinx-diagram-connect documentation"
	echo "$(MAKE) webserver       # Run webserver hosting sphinx-diagram-connect documentation in docker container"
	echo "$(MAKE) show            # View the documentation for sphinx-diagram-connect, which is hosted on a server running nginx, in a web browser"
	echo "$(MAKE) html-api"
	echo "$(MAKE) html-api-dd"

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
	pip uninstall sphinx-diagram-connect -y
	pip install dist/sphinx_diagram_connect*.whl

html:
	poetry run $(SHELL) -c "cd doc && sphinx-build -M html source build"

html-api:
	poetry run $(SHELL) -c "cd doc && sphinx-build -M html source build -t APIDOC"

html-api-dd:
	$(eval OFILE=/tmp/$@.txt)
	poetry run $(SHELL) -c \
		"cd doc && sphinx-build -M html source build -t APIDOC_DD $(if $(VERBOSE),-vvv,)" | tee $(OFILE)

htmlx:html
	cp -r doc/build/html/* docs

doc-clean:
	rm -rf doc/build
	rm -rfv doc/source/reference

WEBSERVERPORT=8080

webserver:
	docker ps | awk '$$NF=="sphinx-diagram-connect"{print "docker stop "$$1}' | $(SHELL)
	sleep 1
	$(MAKE) show -n
	echo or
	echo $(MAKE) show
	docker run -it --rm -d -p $(WEBSERVERPORT):80 --name sphinx-diagram-connect -v $$PWD/doc/build/html:/usr/share/nginx/html nginx

show:
	open http://localhost:$(WEBSERVERPORT)

test-building-package:
	$(eval WDIR=/tmp/test)
	$(eval BRANCH=main)
	mkdir -p $(WDIR)
	rm -rf $(WDIR)/*
	cd $(WDIR)
	git clone -b $(BRANCH) --single-branch \
			https://github.com/mi-parkes/sphinx-diagram-connect.git
	cd sphinx-diagram-connect
#	poetry install --only test,docs
	poetry install
	poetry build
	$(MAKE) html

test-using-package:
	$(eval ODIR=/tmp/$@)
	rm -rf $(ODIR)/
	mkdir -p $(ODIR)
	cd $(ODIR)
	cp -v $(CURDIR)/README.md $(ODIR)
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
		$(if $(LOCAL_MODE),$(CURDIR)/dist/sphinx_diagram_connect-*-py3-none-any.whl,sphinx-diagram-connect="*") \
		sphinx-book-theme="*" \
		sphinxcontrib-plantuml="0.30" \
		sphinxcontrib-drawio="^0.0.17" \
		pillow="*" \
		myst-parser="*"

	rsync -av --exclude 'build/' "$(CURDIR)/doc" .
	$(if $(VERBOSE),poetry show,)
	poetry run $(SHELL) -c "cd doc && sphinx-build -M html source build"

clean-dc:
	docker images | awk '$$1=="<none>"{print "docker rmi "$$3}' | $(SHELL)
