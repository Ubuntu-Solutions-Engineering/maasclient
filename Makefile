#
# Makefile for maasclient
#
NAME        = maasclient
TOPDIR      := $(shell basename `pwd`)
GIT_REV     := $(shell git log --oneline -n1| cut -d" " -f1)
VERSION     := $(shell python3 setup.py version)

$(NAME)_$(VERSION).orig.tar.gz: clean
	cd .. && tar czf $(NAME)_$(VERSION).orig.tar.gz $(TOPDIR) --exclude-vcs --exclude=debian

tarball: $(NAME)_$(VERSION).orig.tar.gz

.PHONY: install-dependencies
install-dependencies:
	sudo apt-get install devscripts equivs
	sudo mk-build-deps -i debian/control

.PHONY: uninstall-dependencies
uninstall-dependencies:
	sudo apt-get remove python3-maasclient-build-deps

clean:
	@debian/rules clean
	@rm -rf debian/maasclient
	@rm -rf docs/_build/*
	@rm -rf ../maasclient_*.deb ../maasclient_*.tar.gz ../maasclient_*.dsc ../maasclient_*.changes \
		../maasclient_*.build ../python3-maasclient_*.deb

deb-src: clean update_version tarball
	@debuild -S -us -uc

deb: clean update_version tarball
	@debuild -us -uc -i

sbuild: clean update_version tarball
	@sbuild -d trusty-amd64 -j4

current_version:
	@echo $(VERSION)

git_rev:
	@echo $(GIT_REV)

update_version:
	wrap-and-sort


.PHONY: ci-test pyflakes pep8 test
ci-test: pyflakes pep8 test

pyflakes:
	python3 `which pyflakes` maasclient

pep8:
	pep8 cloudinstall

test:
	nosetests -v --with-cover --cover-package=maasclient --cover-html test


all: deb
