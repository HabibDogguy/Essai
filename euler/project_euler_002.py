def fibonacci(a,b):
    if (a<4000000):
        yield a
        for x in fibonacci(b,a+b):
            yield x

print(sum([i for i in fibonacci(1,1) if i%2==0]))
