all:

vimlac:	cpu.o ptr.o memory.o Makefile
	gcc -o vimlac cpu.o ptr.o memory.o

test_ptr:	test_ptr.c ptr.c ptr.h Makefile
	gcc -o test_ptr ptr.c test_ptr.c

test_memory:	test_memory.c memory.c memory.h Makefile
	gcc -o test_memory memory.c test_memory.c

clean:
	rm -f *.pyc *.o vimlac test_ptr test_memory 
