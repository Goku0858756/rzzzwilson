#
# Simple make file just to clean this directory.
# And run a simple test.
#

clean:
	rm -Rf *.pyc *~

test0:
	./pymlac -b ptr -c -t 0100 test0.ptp -r 0100

test1:
	./pymlac -b ptr -c -t 0100 test1.ptp -r 0100
	diff pymlac.trace good_test1.trace | head -40

hello:
	./pymlac -b ptr -c -t 0100 40tp_simpleDisplay.ptp -r 0100
