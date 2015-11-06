## Introduction ##

The directories here contain code that tests the comparative speed and memory usage of various Python constructs.

The results here should be considered general.  You should always test for your specific circumstances and Python version.

### string\_concat ###

If you read the Python programming blogs or google for "python string
concatenation" you find statements that the naive 'a += b' method
of concatenating strings is horribly slow and uses too much memory.

Well, it's not that simple with newer Pythons.  The [code](http://code.google.com/p/rzzzwilson/source/browse/#hg%2Fspeed_tests%2Fstring_concat) here tests various methods of concatenating strings:

| naive | the old 'a += b' method |
|:------|:------------------------|
| array | using the array module .join() method |
| join  | using the list object .join() method |
| stringio | concatenating with a StringIO object |
| comprehension | creating a string with comprehension |

An additional method using mutable strings was tried, but it was so slow it isn't tested.

The general method used in _test.py_ is a tight loop over a large range appending a numeric string.  The printed results shows that the naive method is the preferred method: it uses less memory and runs more quickly.  This is contrary to the general sentiment on the web which probably came about because older Pythons **were** slow doing 'a += b'.

Using Python 2.7.3 and 50000000 concatenations the times were:

| naive | 13.02s |
|:------|:-------|
| array | 31.39s |
| join  | 15.99s |
| stringio | 19.17s |
| comprehension | 12.20s |

New Pythons, possibly 2.5 and later, apparently have an optimization for string objects concatenated in a tight loop.  _test.py_ tests code of this form.  _test2.py_ is a copy of _test.py_ with the actual concatenation done in a small function in an attempt to defeat the above optimization.  The naive method does show the expected pathological behaviour.

A [memory profile](http://rzzzwilson.googlecode.com/hg/speed_tests/string_concat/results.png) of _test.py_ is eye-opening!  The array, join and comprehension methods use a **lot** of memory, much more than expected.

#### Conclusions ####

Generally, if you concatenate a large string in a tight loop use the naive 'a += b' method.

If you need to concatenate string data outside a tight loop, use the .join() method if you can spare the memory.  If you can't, use the stringio method.

If you aren't in a tight loop and you can use the slightly less general comprehension method then do that if memory is not a concern, else use stringio.

### if vs ifelse ###

This tests the relative speed of
```
    value = 1
    if flag:
        value = 2
```
against
```
    value = 2 if flag else 1
```
The three line version is quicker, though not by much:
```
if     took 10.43s
ifelse took 11.25s
```

I feel that the three line version is clearer.

### defaultdict versus dict ###

A common usage of dictionaries is to collect occurrence counts of objects by incrementing an integer value in a dictionary corresponding to the object.  A slight difficulty occurs when an object is found for the first time: how do we handle creating the initial '1' entry?

There are a few ways of doing this:
| setdefault | use the dict.setdefault(key, 0) method to set a default |
|:-----------|:--------------------------------------------------------|
| get        | use the dict.get(key, 0) method to set the default      |
| defaultdict | use a defaultdict(int) and rely on the default being 0  |
| try/except | use try/except to catch the missing key case            |

The common opinion is that **defaultdict** is the way to go.  The test code shows this to be correct, with an approximate speedup factor of 2:
| setdefault | 8.78s |
|:-----------|:------|
| get        | 7.49s |
| defaultdict | 4.04s |
| try/except | 4.78s |

The basic [testing code](http://code.google.com/p/rzzzwilson/source/browse/#hg%2Fspeed_tests%2Fdefaultdict) was, for **setdefault**:
```
accum = {}
for key in data:
    accum.setdefault(key, 0)
    accum[key] += 1
```
**get**:
```
accum = {}
for key in data:
    accum[key] = accum_get.get(key, 0) + 1
```
**defaultdict**:
```
accum = collections.defaultdict(int)
for key in data:
    accum[key] += 1
```
**try/except**:
```
accum = {}
for key in data:
    try:
        accum[key] += 1
    except KeyError:
        accum[key] = 1
```

#### Conclusions ####

In the past I've always used the **get** approach, through inertia I guess.  It is simple and short.  But I'm moving to **defaultdict** from now on.

The **try/except** method is almost as quick as **defaultdict**, but much more wordy.