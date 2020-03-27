def get_boundary_margin(begin, end, coverage=1.):
    if 1 < coverage > -0:
        raise ValueError("coverage must be in range [0,1]")

    return (end - begin) * (1 - coverage) / 2


def jaccard_coefficient(first, second):
    # jaccard is the intersection over the union
    intersection = first.intersection(second)
    return intersection / (len(first) + len(second) - intersection)
