"""Exact simplex-grid semantics; no numerical solver dependency."""
from fractions import Fraction as Q
from itertools import product
from math import comb


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, length - 1):
                yield (first,) + rest


def geometry(alphabet, depth, mesh, max_states=None):
    assert alphabet >= 2 and depth >= 1 and mesh >= 1
    leaf_count = alphabet ** depth
    count = alphabet * comb(mesh + leaf_count - 1, leaf_count - 1) ** 2
    if max_states is not None and count > max_states:
        raise ValueError(f'This stated simplex grid has {count} predictive states; the execution cap is {max_states}. No inference was made.')
    leaves = list(product(range(alphabet), repeat=depth))
    simplex = list(compositions(mesh, leaf_count))
    nodes = list(product(range(alphabet), simplex, simplex))
    assert len(nodes) == count
    prefixes = [w for length in range(depth) for w in product(range(alphabet), repeat=length)]
    descriptors = list(product((0, 1), range(alphabet), prefixes, (1, -1)))
    words = list(product(range(alphabet), repeat=2 * depth + 1))
    return leaves, nodes, descriptors, words


def prefix(node, side, word, leaves, mesh):
    return sum((Q(n, mesh) for leaf, n in zip(leaves, node[side + 1]) if leaf[:len(word)] == word), Q(0))


def word_feature(node, word, leaves, depth, mesh):
    if node[0] != word[depth]:
        return Q(0)
    return prefix(node, 1, word[:depth][::-1], leaves, mesh) * prefix(node, 0, word[depth + 1:], leaves, mesh)


def endpoint_coefficient(current, other, descriptor, leaves, mesh):
    side, label, word, sign = descriptor
    return sign * ((prefix(other, side, word, leaves, mesh) if other[0] == label else 0) - prefix(current, side, (label,) + word, leaves, mesh)) - Q(1, mesh)
