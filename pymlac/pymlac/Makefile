#
# Simple make file just to clean this directory.
# And run a simple test.
#

clean:
	rm -Rf *.pyc *~ *.out

testall:	test0 test1

test0:	test0.ptp
	./pymlac -b ptr -c -t 0100 test0.ptp -r 0100
	diff pymlac.trace good_test0.trace | head -40

test1:	test1.ptp
	./pymlac -b ptr -c -t 0100 test1.ptp -r 0100
	diff pymlac.trace good_test1.trace | head -40

test0.ptp:	test0.asm
	./iasm test0.asm

test1.ptp:	test1.asm
	./iasm test1.asm

hello:
	./pymlac -b ptr -c -t 0100 40tp_simpleDisplay.ptp -r 0100
