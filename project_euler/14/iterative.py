CollatzN = {1: 1}
max_N = 0
max_length = 0
for N in range(1, 1000000):
    start_N = N
    count = 0
    while N >= 1:
        if N % 2:
            N = 3*N + 1
        else:
            N = N / 2
        count += 1
        if N in CollatzN:
            length = count + CollatzN[N]
            CollatzN[start_N] = length
            if length > max_length:
                max_length = length
                max_N = start_N
            break
print('Maximum length is %d for N=%d' % (max_length, max_N))
