"""Independent polyhedral-ray and exact PSD replay for the four-seed star bound."""
from itertools import combinations
from pathlib import Path
from math import gcd
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SRC = ROOT / "work/agents/c5_quantum_dimension_obstruction/cycle10_spin11_probe"
BLOCKS = json.loads((SRC / "spin11_fullstar_blocks.json").read_text())
SEEDS = [sp.Matrix(v) for v in [
    (1, 5, 5, 10, 10), (0, 2, 7, 8, 14),
    (1, 1, 1, 14, 14), (0, 0, 5, 10, 16),
]]
TRACE = sp.Matrix([11, 55, 165, 330, 462])


def primitive(vector):
    den = sp.ilcm(*(entry.q for entry in vector))
    ints = [int(entry*den) for entry in vector]
    common = 0
    for entry in ints:
        common = gcd(common, abs(entry))
    return tuple(entry//common for entry in ints)


def ray_set(vertex):
    # Inequalities describe the normal cone where this seed maximizes: alpha>=0
    # and (seed_vertex-seed_j)·alpha>=0. Enumerate independent rank-four faces.
    normals = [sp.eye(5).row(i) for i in range(5)]
    normals.extend((SEEDS[vertex]-SEEDS[j]).T
                   for j in range(len(SEEDS)) if j != vertex)
    rays = set()
    for active in combinations(normals, 4):
        matrix = sp.Matrix.vstack(*active)
        if matrix.rank() != 4:
            continue
        null = matrix.nullspace()
        if len(null) != 1:
            continue
        direction = null[0]
        signs = [(normal*direction)[0] for normal in normals]
        if all(x >= 0 for x in signs):
            pass
        elif all(x <= 0 for x in signs):
            direction = -direction
            if not all((normal*direction)[0] >= 0 for normal in normals):
                continue
        else:
            continue
        rays.add(primitive(direction))
    return rays


def ratmat(raw):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in raw])


def principal_minors_nonnegative(matrix):
    values = []
    for size in range(1, matrix.rows+1):
        for indices in combinations(range(matrix.rows), size):
            determinant = sp.factor(matrix.extract(indices, indices).det())
            values.append(determinant)
            if determinant.is_nonnegative is not True:
                return False, values
    return True, values


def main():
    cones = [ray_set(i) for i in range(len(SEEDS))]
    rays = sorted(set().union(*cones))
    ray_records = []
    minor_count = 0
    block_count = 0
    for ray in rays:
        alpha = sp.Matrix(ray)
        score = max((seed.T*alpha)[0] for seed in SEEDS)
        cap = (TRACE.T*alpha)[0] + score
        per_block = []
        for key, data in BLOCKS["blocks"].items():
            gram = ratmat(data["gram"])
            hs = [ratmat(b) for b in data["bilinear_H"]]
            star = sum((alpha[k]*hs[k] for k in range(5)), sp.zeros(gram.rows))
            gap = sp.simplify(cap*gram-star)
            psd, minors = principal_minors_nonnegative(gap)
            minor_count += len(minors)
            block_count += 1
            if not psd:
                raise AssertionError((ray, key, gap, minors))
            per_block.append({"block": key, "order": gap.rows,
                              "principal_minor_count": len(minors), "psd": psd})
        ray_records.append({"ray": ray, "support": str(score), "cap": str(cap),
                            "blocks": per_block})

    iso_block_results = []
    alpha = sp.ones(5, 1)
    for key, data in BLOCKS["blocks"].items():
        gram = ratmat(data["gram"])
        hs = [ratmat(b) for b in data["bilinear_H"]]
        star = sum(hs, sp.zeros(gram.rows))
        gap = 1054*gram-star
        psd, _ = principal_minors_nonnegative(gap)
        det = sp.factor(gap.det())
        iso_block_results.append({"block": key, "order": gap.rows,
                                  "gap_psd": psd, "det_gap": str(det)})
        if not psd:
            raise AssertionError(("isotropic gap", key, gap))
    has_top = any(record["det_gap"] == "0" for record in iso_block_results)
    if not has_top:
        raise AssertionError("1054 cap has no singular block; exact top not certified")

    result = {
        "status": "PASS",
        "scope": "four-seed support-cone ray coverage and exact PSD of reported reduced star gaps",
        "ray_counts_per_seed_cone": [len(cone) for cone in cones],
        "distinct_rays": len(rays),
        "block_ray_checks": block_count,
        "principal_minor_checks": minor_count,
        "isotropic_1054": {"all_gaps_psd": True, "at_least_one_singular": has_top,
                           "blocks": iso_block_results},
        "rays": ray_records,
        "limits": "This reuses the candidate's exact reduced block matrices; independent ray enumeration and PSD/minor replay do not independently reconstruct the 32768-dimensional representation or star blocks."
    }
    (HERE / "independent_support_replay.json").write_text(json.dumps(result, indent=2)+"\n")
    print(f"PASS: cone sizes {[len(c) for c in cones]}, {len(rays)} distinct rays, "
          f"{block_count} block-ray checks, {minor_count} principal minors; isotropic top 1054.")


if __name__ == "__main__":
    main()
