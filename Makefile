ifeq ($(PREFIX),)
    PREFIX := /etc
endif

install: 
	install -d $(DESTDIR)$(PREFIX)/rasiel/
	install -m 755 keyboard-daemon.py $(DESTDIR)$(PREFIX)/rasiel/
	install -m 755 chroma.py $(DESTDIR)$(PREFIX)/rasiel/
	install -m 644 chroma-rasiel.service /etc/systemd/user
	install -m 644 keyboard-rasiel.service /etc/systemd/system
