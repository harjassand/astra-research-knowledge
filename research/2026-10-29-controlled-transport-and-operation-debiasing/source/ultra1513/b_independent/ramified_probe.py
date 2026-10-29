"""Exact deformation probe of the acquired AlphaTensor binary rank47 seed.

No search pool or source refresh. Rebuild the whole Jacobian, all kernel
directions and the tangent action of EXACT integer-defined isotropies and
per-term rescalings. The result decides whether a ramified quadratic
repair can have a nongauge infinitesimal direction at this reduction.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parents[1] / "sol23_capability_principles_20261029/b_replacement_operation/factorizations_f2.npz"


def bits(a):
    return int.from_bytes(np.packbits(np.asarray(a, dtype=np.uint8).ravel(),
                                     bitorder="little").tobytes(), "little")


class Basis:
    def __init__(self):
        self.rows = {}

    def add(self, value, label=0):
        while value:
            k = value.bit_length()-1
            if k not in self.rows:
                self.rows[k] = value, label
                return True, label
            row, code = self.rows[k]
            value ^= row
            label ^= code
        return False, label

    def reduce(self, value):
        while value:
            k = value.bit_length()-1
            if k not in self.rows:
                return value
            value ^= self.rows[k][0]
        return 0


def tensor(shape):
    n, m, p = shape
    out = np.zeros((n*m, m*p, p*n), dtype=np.int64)
    for i in range(n):
        for j in range(m):
            for k in range(p):
                out[i*m+j, j*p+k, k*n+i] = 1
    return out


def term_columns(a, b, c):
    size = len(a)
    out = []
    for mode in range(3):
        for pos in range(size):
            v = np.zeros(size, dtype=np.int64)
            v[pos] = 1
            arrays = [a, b, c]
            arrays[mode] = v
            out.append(bits(np.einsum("i,j,k->ijk", *arrays)))
    return out


def parameter_bits(factors):
    # The Jacobian's parameter convention is term, then mode, then entry.
    return bits(np.transpose(factors, (2, 0, 1)))


def gauge_generators(factors, n):
    rank = factors.shape[2]
    matrices = factors.reshape(3, n, n, rank)
    generators = []
    for leg in range(3):
        for row in range(n):
            for col in range(n):
                e = np.zeros((n, n), dtype=np.int64)
                e[row, col] = 1
                v = np.zeros_like(matrices)
                # Exact cyclic action: a->P a Q^-1, b->Q b R^-1,
                # c->R c P^-1. Minus equals plus in characteristic2.
                v[leg] = np.einsum("ij,jkr->ikr", e, matrices[leg])
                previous = (leg-1) % 3
                v[previous] ^= np.einsum("ijr,jk->ikr", matrices[previous], e)
                generators.append((f"GL{leg}[{row},{col}]", parameter_bits(v.reshape(factors.shape))))
    for r in range(rank):
        for mode in (0, 1):
            v = np.zeros_like(factors)
            # (a,b,c)->(s a,t b,(s t)^-1 c).
            v[mode, :, r] = factors[mode, :, r]
            v[2, :, r] = factors[2, :, r]
            generators.append((f"scale[{r},{mode}]", parameter_bits(v)))
    return generators


def apply_jacobian(columns, value):
    image = 0
    while value:
        bit = value & -value
        image ^= columns[bit.bit_length()-1]
        value ^= bit
    return image


def main():
    begin = time.perf_counter()
    native = np.load(NATIVE, allow_pickle=False)
    f = np.asarray(native["4,4,4"], dtype=np.int64)
    assert f.shape == (3, 16, 47)
    assert np.all((f == 0) | (f == 1))
    target = tensor((4, 4, 4))
    represented = np.einsum("ir,jr,kr->ijk", *f)
    assert np.array_equal(represented % 2, target)
    columns = [x for r in range(47) for x in term_columns(*f[:, :, r])]
    image, kernel = Basis(), []
    for j, col in enumerate(columns):
        independent, dependency = image.add(col, 1 << j)
        if not independent:
            assert apply_jacobian(columns, dependency) == 0
            kernel.append(dependency)
    all_directions_seconds = time.perf_counter()-begin
    gauge = Basis()
    generators = gauge_generators(f, 4)
    for name, direction in generators:
        assert apply_jacobian(columns, direction) == 0, name
        gauge.add(direction)
    nongauge = [v for v in kernel if gauge.reduce(v)]
    defect_int = target-represented
    assert np.all(defect_int % 2 == 0)
    defect = bits((defect_int//2) % 2)
    obstruction = image.reduce(defect)
    assert obstruction != 0
    # An explicit dual functional is a small, directly consumable proof of
    # nonmembership, rather than merely trusting an echelon status/hash.
    missing = obstruction.bit_length()-1
    assert missing not in image.rows
    dual = 1 << missing
    for pivot, (row, _) in sorted(image.rows.items()):
        if (row & dual).bit_count() % 2:
            dual ^= 1 << pivot
    assert all((col & dual).bit_count() % 2 == 0 for col in columns)
    assert (defect & dual).bit_count() % 2 == 1
    result = {
        "status": "ALL_TANGENTS_GAUGE" if not nongauge else "NONGAUGE_DIRECTIONS_FOUND",
        "native_sha256": hashlib.sha256(NATIVE.read_bytes()).hexdigest(),
        "native_relative_path": str(NATIVE.relative_to(HERE.parents[2])),
        "shape": list(f.shape),
        "tensor_coefficients": 4096,
        "parameter_count": len(columns),
        "jacobian_rank": len(image.rows),
        "kernel_dimension": len(kernel),
        "gauge_generator_count": len(generators),
        "gauge_rank": len(gauge.rows),
        "nongauge_kernel_basis_directions": len(nongauge),
        "mod4_obstruction_nonzero": bool(obstruction),
        "obstruction_quotient_weight": obstruction.bit_count(),
        "dual_obstruction_weight": dual.bit_count(),
        "kernel_basis_sha256": hashlib.sha256(b"".join(x.to_bytes(282, "little") for x in kernel)).hexdigest(),
        "gauge_basis_sha256": hashlib.sha256(b"".join(x[0].to_bytes(282, "little") for _, x in sorted(gauge.rows.items()))).hexdigest(),
        "all_directions_seconds": all_directions_seconds,
        "total_seconds": time.perf_counter()-begin,
        "no_field_extension_or_characteristic_zero_algorithm_constructed": True,
    }
    (HERE / "RAMIFICATION_PROBE.json").write_text(json.dumps(result, indent=2)+"\n")
    # These are actual mathematical witness data, not hashes replacing proof.
    witness = {"parameter_order": "term,mode,entry", "kernel_basis_hex": [hex(x) for x in kernel],
               "gauge_generators": [{"name": name, "direction_hex": hex(v)} for name, v in generators],
               "defect_hex": hex(defect), "reduced_obstruction_hex": hex(obstruction),
               "dual_obstruction_hex": hex(dual)}
    (HERE / "RAMIFICATION_WITNESSES.json").write_text(json.dumps(witness, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
