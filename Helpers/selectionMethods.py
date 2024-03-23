from Helpers.decimalBinaryMath import binary_to_decimal

def best_selection(f, parents):
    worst_index = 0
    for i in range(1,len(parents)):
        if f(binary_to_decimal(parents[i])) > f(binary_to_decimal(parents[worst_index])):
            worst_index = i
    return parents[:worst_index] + parents[worst_index+1:]