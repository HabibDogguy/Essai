print (sum([i for i in range(1000) if (i % 3 == 0) or (i % 5 == 0)]))

print (reduce(filter(range(1000), lambda i: (i % 3 == 0) or (i % 5 == 0)])), (lambda a, b: a+b)))
