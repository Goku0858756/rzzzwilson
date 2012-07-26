#
# Simple make file just to clean this directory.
# And run a simple test.
#

TESTS=test_law test_lwc test_jmp test_dac test_xam test_isz test_jms test_and

test:	$(TESTS)

test_law:	test_law.ptp
	./pymlac -b ptr -t 0100 test_law.ptp -r 0100
	diff pymlac.trace good_test_law.trace | head -40

test_lwc:	test_lwc.ptp
	./pymlac -b ptr -t 0100 test_lwc.ptp -r 0100
	diff pymlac.trace good_test_lwc.trace | head -40

test_jmp:	test_jmp.ptp
	./pymlac -b ptr -t 0100 test_jmp.ptp -r 0100
	diff pymlac.trace good_test_jmp.trace | head -40

test_dac:	test_dac.ptp
	./pymlac -b ptr -t 0100 test_dac.ptp -r 0100
	diff pymlac.trace good_test_dac.trace | head -40

test_xam:	test_xam.ptp
	./pymlac -b ptr -t 0100 test_xam.ptp -r 0100
	diff pymlac.trace good_test_xam.trace | head -40

test_isz:	test_isz.ptp
	./pymlac -b ptr -t 0100 test_isz.ptp -r 0100
	diff pymlac.trace good_test_isz.trace | head -40

test_jms:	test_jms.ptp
	./pymlac -b ptr -t 0100 test_jms.ptp -r 0100
	diff pymlac.trace good_test_jms.trace | head -40

test_and:	test_and.ptp
	./pymlac -b ptr -t 0100 test_and.ptp -r 0100
	diff pymlac.trace good_test_and.trace | head -40

test_law.ptp:	test_law.asm
	./iasm -l test_law.lst test_law.asm

test_lwc.ptp:	test_lwc.asm
	./iasm -l test_lwc.lst test_lwc.asm

test_jmp.ptp:	test_jmp.asm
	./iasm -l test_jmp.lst test_jmp.asm

test_dac.ptp:	test_dac.asm
	./iasm -l test_dac.lst test_dac.asm

test_xam.ptp:	test_xam.asm
	./iasm -l test_xam.lst test_xam.asm

test_isz.ptp:	test_isz.asm
	./iasm -l test_isz.lst test_isz.asm

test_jms.ptp:	test_jms.asm
	./iasm -l test_jms.lst test_jms.asm

test_and.ptp:	test_and.asm
	./iasm -l test_and.lst test_and.asm

hello:
	./pymlac -b ptr -c -t 0100 40tp_simpleDisplay.ptp -r 0100
clean:
	rm -Rf *.pyc *~ *.out

