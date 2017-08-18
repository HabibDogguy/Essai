def is_palindrome(n):
    return str(n)[::-1] == str(n)

print(max([i*j for i in range(1000) for j in range(1000)if is_palindrome(i*j)]))
