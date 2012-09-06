#
# Run the program
#

all:
	python cofm.py small.in

profile:
	kernprof.py cofm.py small.in
	echo -e "sort time\nstats" | python -m pstats cofm.py.prof

test:
	python cofm.py B-small-practice.in > B-small-practice.out
	python cofm.py B-large-practice.in > B-large-practice.out

clean:
	rm -f *.pyc *.log *.prof

