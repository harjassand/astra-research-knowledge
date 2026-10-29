"""Pay the additional native premise for projective/nonintegral scaling.

This does not rerun the whole tangent calculation or introduce a case.
It acquires only linear independence of the47 represented term tensors.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np


def main():
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    native = here.parents[1] / "sol23_capability_principles_20261029/b_replacement_operation/factorizations_f2.npz"
    f = np.load(native, allow_pickle=False)["4,4,4"].astype(np.int64)
    columns = []
    for r in range(47):
        array = np.einsum("i,j,k->ijk", *f[:, :, r])
        columns.append(int.from_bytes(np.packbits(array.astype(np.uint8).ravel(), bitorder="little").tobytes(), "little"))
    basis = {}
    for col in columns:
        value = col
        while value:
            p = value.bit_length()-1
            if p not in basis:
                basis[p] = value
                break
            value ^= basis[p]
        assert value, "term tensor dependence found"
    assert len(basis) == 47
    result = {"status":"PASS_47_TERM_TENSORS_LINEALLY_INDEPENDENT_OVER_F2",
              "term_count":47,"term_span_rank":len(basis),
              "native_sha256":hashlib.sha256(native.read_bytes()).hexdigest(),
              "term_tensor_columns_hex":[hex(x) for x in columns],
              "pivot_rows":sorted(basis),
              "scope":"new projective-scaling premise only; no Jacobian/model/search rerun",
              "seconds":time.perf_counter()-start}
    (here / "PROJECTIVE_PROBE.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if not k.endswith("hex") and k!="pivot_rows"},indent=2))


if __name__ == "__main__":
    main()
