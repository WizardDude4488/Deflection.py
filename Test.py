numbers = [10, 50, 80, 150, -100, -20]

def function(n):
    return abs(n)

numbers.sort(key = function)

for i in numbers:
    print(i)
