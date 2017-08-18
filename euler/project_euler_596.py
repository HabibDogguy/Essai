from math import sqrt, floor
r=10*10*10;
sum =0
for x in range(1,r):
    for y in range(1,int(sqrt(r*r-x*x))+1):
        for z in range(1,int(sqrt(r*r -x*x-y*y))+1):
            sum += 2*int(sqrt(r*r -x*x-y*y-z*z))
            sum %= 1000000007



print(sum)
