def binatodeci(binary):
    return sum(val * (2 ** idx) for idx, val in enumerate(reversed(binary)))
def binary_to_decimal(binarry_chain, start=-10, end=10):
    chain_len = len(binarry_chain)
    return start + binatodeci(binarry_chain) * (end - start) / (2 ** chain_len - 1)