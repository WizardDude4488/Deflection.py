numbers = {1: 1, 2: 24, 3: 40, 4: 10}

#a list of tuples can be created sorted by the value of the index 1 element of the tuple
#the values in the tuples can be accessed by going to numbers_l[i][n] for the nth value of ith tuple
numbers_l = list(sorted(numbers.items(), key = lambda item: item[1]))

print(numbers_l[0][1])
