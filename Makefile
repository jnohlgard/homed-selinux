TARGET?=systemd-homed
MODULES?=${TARGET:=.pp.bz2}
SHAREDIR?=/usr/share

all: ${TARGET:=.pp.bz2}

.PHONY: all clean install install-policy rpm

%.pp.bz2: %.pp
	@echo Compressing $^ -\> $@
	bzip2 -f -9 $^

%.pp: %.te
	$(MAKE) -f ${SHAREDIR}/selinux/devel/Makefile $@

clean:
	$(RM) *~  *.tc *.pp *.pp.bz2
	$(RM) -r tmp .build *.tar.gz

install-policy: all
	semodule -i ${TARGET}.pp.bz2

install: all
	install -D -m 644 ${TARGET}.pp.bz2 ${DESTDIR}${SHAREDIR}/selinux/packages/${TARGET}.pp.bz2
	install -D -m 644 ${TARGET}.if ${DESTDIR}${SHAREDIR}/selinux/devel/include/contrib/${TARGET}.if

rpm:
	rpmbuild \
		--define "_sourcedir $(CURDIR)" \
		--define "_specdir $(CURDIR)" \
		--define "_builddir $(CURDIR)" \
		--define "_srcrpmdir $(CURDIR)" \
		--define "_rpmdir $(CURDIR)" \
		--define "_buildrootdir $(CURDIR)/.build" \
		-ba ${TARGET}-selinux.spec
