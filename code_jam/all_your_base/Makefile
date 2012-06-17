#
# Run the program
#

all:
	python base.py small.in

profile:
	@echo "MUST USE @profile"
	kernprof.py -l -v base.py small.in
	#kernprof.py -l base.py small.in
	#python -m line_profiler base.py.lprof

test:
	python base.py A-small-practice.in > A-small-practice.out
	python base.py A-large-practice.in > A-large-practice.out

clean:
	rm -f *.pyc *.log *.prof

