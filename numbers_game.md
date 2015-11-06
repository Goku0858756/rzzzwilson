# Introduction #

The program here is designed to solve the numbers game from the SBS
television show
[Letters and Numbers](http://en.wikipedia.org/wiki/Letters_and_Numbers)

# Details #

The game consists of selecting a set of 6 number tiles and combining them
in an arithmetic equation using the addition, subtraction, division and
multiplication operations to equal a randomly generated 3 digit target.

For example, the six numbers might be:
```
    9 8 7 3 6 100
```
and the target number:
```
    591
```

Obviously:
```
    (100 * 6) - 9 = 591
```

The aim of the program is to take 7 parameters:
```
    numbers.py n1 n2 n3 n4 n5 n6 target
```
and the program should output one way to combine the numbers and operators
to equal the target number, if possible.

There may be another way, but I chose to generate all permutations of the
six numbers and all permutations of the 4 operators in groups of 5 and operate
on the numbers using RPN.  That is, if we have one number permutation:
```
    9 100 6 3 7 8
```
and operators:
```
    + + / * *
```
then the final evaluation is:
```
    7 + 8 = 15
    15 + 3 = 18
    18 / 6 = 3
    3 * 100 = 300
    300 * 9 = 2700
```
so the closest legal number to the target is 300.  Trying all permutations of
operators and numbers exhaustively will find the closest number to the target.

Note, the program stops at the first match, but may not find the simplest result.