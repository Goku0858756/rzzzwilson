all:

vimlac:	cpu.c cpu.h ptr.c ptr.h memory.c memory.h Makefile
	gcc -o vimlac cpu.c ptr.c memory.c

test_ptr:	test_ptr.c ptr.c ptr.h Makefile
	gcc -o test_ptr ptr.c test_ptr.c

test_memory:	test_memory.c memory.c memory.h Makefile
	gcc -o test_memory memory.c test_memory.c

clean:
	rm -f *.pyc *.o test_ptr test_memory
