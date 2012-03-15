.PHONY: all install dist clean backup deinstall check
.SUFFIXES: .ps .pdf .py

#beginskip
PROG = foo
ALL = genpad.1 genpad.1.pdf enpad.1 enpad.1.pdf depad.1 depad.1.pdf setup.py
SRCS = genpad.in.py enpad.in.py depad.in.py setup.in.py

all: ${ALL} .git/hooks/post-commit tools/replace.sed
#endskip
BASE=/usr/local
MANDIR=$(BASE)/man
BINDIR=$(BASE)/bin
PYSITE!=python -c 'import site; print site.getsitepackages()[0]'

install: genpad.1 enpad.1 depad.1 setup.py genpad.py enpad.py depad.py
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to install the program!"; \
		exit 1; \
	fi
# Let Python do most of the install work.
	python setup.py install
# Lose the extension; this is UNIX. :-)
	mv $(BINDIR)/genpad.py $(BINDIR)/genpad
	mv $(BINDIR)/enpad.py $(BINDIR)/enpad
	mv $(BINDIR)/depad.py $(BINDIR)/depad
	rm -rf build
#Install the manual pages.
	gzip -c genpad.1 >genpad.1.gz
	install -m 644 genpad.1.gz $(MANDIR)/man1
	rm -f genpad.1.gz
	gzip -c enpad.1 >enpad.1.gz
	install -m 644 enpad.1.gz $(MANDIR)/man1
	rm -f enpad.1.gz
	gzip -c depad.1 >depad.1.gz
	install -m 644 depad.1.gz $(MANDIR)/man1
	rm -f depad.1.gz

deinstall::
	@if [ `id -u` != 0 ]; then \
		echo "You must be root to deinstall the program!"; \
		exit 1; \
	fi
	rm -f ${PYSITE}/onepad.py
	rm -f $(BINDIR)/genpad
	rm -f $(BINDIR)/enpad
	rm -f $(BINDIR)/depad
	rm -f $(MANDIR)/man1/genpad.1.gz
	rm -f $(MANDIR)/man1/enpad.1.gz
	rm -f $(MANDIR)/man1/depad.1.gz

#beginskip
dist: ${ALL}
# Make simplified makefile.
	mv Makefile Makefile.org
	awk -f tools/makemakefile.awk Makefile.org >Makefile
# Create distribution file. Use zip format to make deployment easier on windoze.
	python setup.py sdist --format=zip
	mv Makefile.org Makefile
	rm -f MANIFEST
#	sed -f tools/replace.sed port/Makefile.in >port/Makefile
#	cd dist ; sha256 py-stl-* >../port/distinfo
#	cd dist ; ls -l py-stl-* | awk '{printf "SIZE (%s) = %d\n", $$9, $$5};' >>../port/distinfo

clean::
	rm -rf dist build backup-*.tar.gz *.pyc ${ALL} MANIFEST
#	rm -f port/Makefile port/distinfo

backup: ${ALL}
# Generate a full backup.
	sh tools/genbackup

check: .IGNORE
	pylint --rcfile=tools/pylintrc ${SRCS}

.git/hooks/post-commit: tools/post-commit
	install -m 755 $> $@

tools/replace.sed: .git/index
	tools/post-commit

setup.py: setup.in.py tools/replace.sed
	sed -f tools/replace.sed setup.in.py >$@

genpad.py: genpad.in.py tools/replace.sed
	sed -f tools/replace.sed genpad.in.py >$@
	chmod 755 genpad.py

enpad.py: enpad.in.py tools/replace.sed
	sed -f tools/replace.sed enpad.in.py >$@
	chmod 755 enpad.py

depad.py: depad.in.py tools/replace.sed
	sed -f tools/replace.sed depad.in.py >$@
	chmod 755 depad.py

genpad.1: genpad.1.in tools/replace.sed
	sed -f tools/replace.sed genpad.1.in >$@

genpad.1.pdf: genpad.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

enpad.1: enpad.1.in tools/replace.sed
	sed -f tools/replace.sed enpad.1.in >$@

enpad.1.pdf: enpad.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps

depad.1: depad.1.in tools/replace.sed
	sed -f tools/replace.sed depad.1.in >$@

depad.1.pdf: depad.1
	mandoc -Tps $> >$*.ps
	epspdf $*.ps
	rm -f $*.ps



#endskip
