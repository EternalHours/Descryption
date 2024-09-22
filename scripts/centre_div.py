def centre_div(span, div, offset=0):
    '''Centres an item of size div inside a span of a given size. Can use tuples for extra dimensions.'''
    if isinstance(span, tuple):
        pos = []
        if offset == 0: offset = [0] * len(span)
        for i in range(len(span)): pos.append(centre_div(span[i], div[i], offset[i]))
        return tuple(pos)
    return (span - div) // 2 + offset