def Collatz(N):
    if N in CollatzN:
        result = CollatzN[N]
    else:
        if N % 2:
            result = Collatz(3*N+1) + 1
        else:
            result = Collatz(N/2) + 1
        CollatzN[N] = result
    return result

CollatzN = {1: 1}
max_N = 0
max_length = 0
for N in range(1, 1000000):
    length = Collatz(N)
    if length > max_length:
        max_length = length
        max_N = N
print('Maximum length is %d for N=%d' % (max_length, max_N))
