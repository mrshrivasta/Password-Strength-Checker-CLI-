.PHONY: all install uninstall clean test bench

PYTHON ?= python3
SCRIPT = pwcheck.py
BASH_SCRIPT = pwcheck.sh

all: install

install:
	@chmod +x $(BASH_SCRIPT)
	@chmod +x $(SCRIPT)
	@echo "Installed! Use 'pwcheck.sh' or '$(PYTHON) $(SCRIPT)'"
	@echo "Try: ./pwcheck.sh -i"

uninstall:
	@echo "Uninstall not implemented (just delete the files)"

test:
	@echo "Testing common passwords..."
	@./pwcheck.sh -b passwords.txt | grep -c "Very Weak\|Weak"

bench:
	@echo "Benchmarking 1000 passwords..."
	@time ./pwcheck.sh -b passwords.txt > /dev/null

clean:
	@rm -f *.pyc __pycache__/*

install-system:
	sudo cp $(BASH_SCRIPT) /usr/local/bin/pwcheck
	sudo chmod +x /usr/local/bin/pwcheck
	@echo "System-wide install complete! Use 'pwcheck' anywhere"