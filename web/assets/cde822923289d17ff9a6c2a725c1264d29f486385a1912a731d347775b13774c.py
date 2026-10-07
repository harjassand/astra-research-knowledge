"""Materialize dense full responses for one exact prefix-query replay."""
import itertools
import json
import time
from pathlib import Path

import numpy as np

from verify_shift_detector import coefficient, learn, certify_equal, hankel_rank, build_u, word_images, structured_oracle


class SparseMatrix:
    def __init__(self, dimension, rows=None):
        self.dimension = dimension
        self.rows = rows if rows is not None else [{} for _ in range(dimension)]

    @classmethod
    def eye(cls, dimension):
        return cls(dimension, [{i:1} for i in range(dimension)])

    def product(self, other, p):
        result = SparseMatrix(self.dimension)
        for i, row in enumerate(self.rows):
            out = result.rows[i]
            for mid, left in row.items():
                for j, right in other.rows[mid].items():
                    value = (out.get(j,0) + left*right) % p
                    if value:
                        out[j] = value
                    elif j in out:
                        del out[j]
        return result

    def add_scaled(self, other, coefficient_value, p):
        for i, row in enumerate(other.rows):
            out = self.rows[i]
            for j, value in row.items():
                new = (out.get(j,0) + coefficient_value*value) % p
                if new:
                    out[j] = new
                elif j in out:
                    del out[j]

    def dense(self):
        out = np.zeros((self.dimension,self.dimension),dtype=np.int64)
        for i, row in enumerate(self.rows):
            for j, value in row.items():
                out[i,j] = value
        return out

    @property
    def nnz(self):
        return sum(map(len,self.rows))


def expand_tuple(u, m, p):
    n_z, _, e_t = u[0].shape
    d0 = n_z * e_t
    d = m * d0
    matrices = []
    for matrix in u:
        result = SparseMatrix(d)
        for marker in range(m - 1):
            for r in range(n_z):
                for q in range(r):
                    coeff = matrix[r, q]
                    for b in range(e_t):
                        for a in range(b, e_t):
                            value = int(coeff[a-b])
                            if value:
                                row = (marker+1)*d0+r*e_t+a
                                col = marker*d0+q*e_t+b
                                result.rows[row][col] = value
        matrices.append(result)
    assert all(a.product(b,p).nnz == 0 for a in matrices for b in matrices) if m == 2 else True
    return matrices, d


def main():
    start = time.perf_counter()
    p, n, m = 2, 2, 2
    rng = np.random.default_rng(8)
    alpha = rng.integers(0, p, size=m, dtype=np.int64)
    beta = rng.integers(0, p, size=m, dtype=np.int64)
    transitions = [rng.integers(0, p, size=(m,m), dtype=np.int64) for _ in range(n)]
    u, n_z, e_t = build_u(p, n, m)
    target, d = expand_tuple(u, m, p)
    images = word_images(u, m, p)
    expected, _ = structured_oracle(alpha, transitions, beta, images, m, p)
    records = []

    def query(prefix):
        length = len(prefix)
        dimension = d * (length + 1)
        tuple_values = []
        for letter in range(n):
            matrix = SparseMatrix(dimension)
            for i, row in enumerate(target[letter].rows):
                matrix.rows[length*d+i] = {length*d+j:value for j,value in row.items()}
            for at, symbol in enumerate(prefix):
                if letter == symbol:
                    for j in range(d):
                        matrix.rows[at*d+j][(at+1)*d+j] = 1
            tuple_values.append(matrix)
        output = SparseMatrix(dimension)
        identity = SparseMatrix.eye(dimension)
        products = {(): identity}
        for k in range(m + length):
            for word in itertools.product(range(n), repeat=k):
                if word:
                    products[word] = products[word[:-1]].product(tuple_values[word[-1]],p)
                c = coefficient(alpha, transitions, beta, word, p)
                if c:
                    output.add_scaled(products[word],c,p)
        for word in itertools.product(range(n), repeat=m+length):
            final = products[word[:-1]].product(tuple_values[word[-1]],p)
            assert final.nnz == 0
        dense_output = output.dense()
        assert dense_output.shape == (dimension,dimension)
        residual = dense_output[:d, length*d:(length+1)*d]
        compressed = np.zeros((m,n_z,n_z,e_t), dtype=np.int64)
        for marker in range(m):
            for r in range(n_z):
                for q in range(n_z):
                    compressed[marker,r,q] = residual[(marker*n_z+r)*e_t:(marker*n_z+r+1)*e_t,q*e_t]
        feature = compressed.reshape(-1)
        empty = int(residual[0,0])
        expected_feature, expected_empty = expected(prefix)
        assert np.array_equal(feature, expected_feature)
        assert empty == expected_empty
        records.append({'prefix':list(prefix),'dimension':dimension,'input_field_entries':n*dimension*dimension,'output_field_entries':dimension*dimension,'response_nonzero_entries':int(np.count_nonzero(dense_output))})
        return feature, empty

    learned = learn(query, n, p)
    reachable = certify_equal((alpha,transitions,beta), learned, p)
    assert learned[-1] == hankel_rank((alpha,transitions,beta), p)
    result = {'status':'passed','scope':'exact internal full-matrix oracle simulation; all dense responses materialized; prefix extraction checked against separate coefficient model; not an external acquired oracle','p':p,'n':n,'m':m,'N':n_z,'E':e_t,'detector_dimension':d,'minimal_rank':learned[-1],'difference_reachable_dimension':reachable,'wall_seconds':time.perf_counter()-start,'total_response_entries':sum(x['output_field_entries'] for x in records),'records':records}
    Path(__file__).with_name('dense_prefix_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
