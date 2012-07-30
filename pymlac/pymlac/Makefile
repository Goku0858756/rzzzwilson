#
# Simple make file just to clean this directory.
# And run the test files.
#

TESTS = $(shell ls test_*.asm|sed -e "s/\.asm//")

test:	$(TESTS)

#hello:
#	./pymlac -b ptr -c -t 0100 40tp_simpleDisplay.ptp -r 0100

%:	%.ptp
	./pymlac -b ptr -ptr $< -r 040 -t 0100 -r 0100
	diff pymlac.trace good_$*.trace | head -10

%.ptp:	%.asm
	./iasm -l $*.lst $<

clean:
	rm -Rf *.pyc *~ *.out test_*.ptp

