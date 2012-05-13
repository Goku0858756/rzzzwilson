#
# Run the program
#

all:
	python base.py small.in

profile:
	kernprof.py base.py small.in
	echo -e "sort time\nstats" | python -m pstats base.py.prof

test:
	python base.py A-small-practice.in > A-small-practice.out
	python base.py A-large-practice.in > A-large-practice.out

clean:
	rm -f *.pyc *.log *.prof

