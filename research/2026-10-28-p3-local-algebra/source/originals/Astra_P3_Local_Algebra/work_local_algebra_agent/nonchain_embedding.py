#!/usr/bin/env python3
"""Exact tensor embedding in a local Frobenius algebra: a class boundary."""
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path
import json
import random
from local_algebra_acquisition import (centroid, acquire_chain_algebra, span,
                                      polynomial_value)


class TensorAlgebra:
    def __init__(self, k, coefficients):
        self.k, self.m = k, 2*k+2
        self.umask = (1 << k)-1
        self.top = 1 << (2*k+1)
        self.slices = [[0]*k for _ in range(k)]
        for indices, coefficient in coefficients.items():
            if coefficient:
                for i, j, ell in set(permutations(indices)):
                    self.slices[i][j] ^= 1 << ell

    def contraction(self, u, v):
        out = 0
        for i in range(self.k):
            if u >> i & 1:
                for j in range(self.k):
                    if v >> j & 1:
                        out ^= self.slices[i][j]
        return out

    def mul(self, a, b):
        a0, b0 = a & 1, b & 1
        out = (b if a0 else 0) ^ (a if b0 else 0) ^ (a0 & b0)
        u, v = (a >> 1) & self.umask, (b >> 1) & self.umask
        phi, psi = (a >> (self.k+1)) & self.umask, (b >> (self.k+1)) & self.umask
        out ^= self.contraction(u, v) << (self.k+1)
        if ((u & psi).bit_count() ^ (v & phi).bit_count()) & 1:
            out ^= self.top
        return out

    def functional(self, a):
        return int(bool(a & self.top))

    def volume_anf(self):
        out = set()
        for i in range(self.m):
            for j in range(self.m):
                ij = self.mul(1 << i, 1 << j)
                for ell in range(self.m):
                    if self.functional(self.mul(ij, 1 << ell)):
                        out.add((1 << i) | (1 << (self.m+j)) | (1 << (2*self.m+ell)))
        return out


def main():
    rng = random.Random(77102)
    cases = []
    for k in range(1, 5):
        coefficients = {(i, i, i): 1 for i in range(k)}
        coefficients.update({indices: rng.randrange(2)
                             for indices in combinations_with_replacement(range(k), 3)
                             if len(set(indices)) > 1})
        if k >= 3:
            coefficients[0, 1, 2] = 1
        algebra = TensorAlgebra(k, coefficients)
        m, n = algebra.m, 3*algebra.m
        for i in range(m):
            for j in range(m):
                assert algebra.mul(1 << i, 1 << j) == algebra.mul(1 << j, 1 << i)
                for ell in range(m):
                    assert algebra.mul(algebra.mul(1 << i, 1 << j), 1 << ell) == algebra.mul(1 << i, algebra.mul(1 << j, 1 << ell))
        gram = [sum(algebra.functional(algebra.mul(1 << i, 1 << j)) << i
                    for i in range(m)) for j in range(m)]
        assert len(span(gram)) == m
        tensor_signed = (1 << k)*sum(algebra.contraction(u, v) == 0
                                    for u in range(1 << k) for v in range(1 << k))
        ring_signed = (1 << m)*sum(algebra.mul(x, y) == 0
                                  for x in range(1 << m) for y in range(1 << m))
        reconstructed = (1 << (3*k+3))*tensor_signed + 3*(1 << (4*k+3))
        assert reconstructed == ring_signed
        raw = algebra.volume_anf()
        acquired_centroid, _, _ = centroid(raw, n)
        assert len(acquired_centroid) == m
        classification = "accepted chain"
        try:
            recognized = acquire_chain_algebra(acquired_centroid, n)
        except ValueError as exc:
            classification = str(exc)
            assert k > 1 and "not a chain" in classification
        else:
            assert k == 1 and recognized["e"] == 4
        points = list(range(1 << n)) if k == 1 else [rng.getrandbits(n) for _ in range(512)]
        mask = (1 << m)-1
        for point in points:
            x, y, z = [(point >> (m*i)) & mask for i in range(3)]
            assert polynomial_value(raw, point) == algebra.functional(algebra.mul(algebra.mul(x, y), z))
        cases.append(dict(k=k, algebra_dimension=m, input_bits=n, centroid_dimension=len(acquired_centroid),
                          tensor_signed_sum=tensor_signed, ring_signed_sum=ring_signed,
                          reconstruction_exact=True, ring_product_pairs=(1 << (2*m)),
                          raw_pointwise_checks=len(points), classification=classification,
                          tensor_coefficients=[dict(indices=list(key), value=value)
                                               for key, value in sorted(coefficients.items())]))
        print(json.dumps(cases[-1]), flush=True)
    Path(__file__).with_name("nonchain_embedding_results.json").write_text(json.dumps(dict(
        cases=cases, scope="A representation obstruction; no #P-hardness assertion."), indent=2)+"\n")


if __name__ == "__main__":
    main()
