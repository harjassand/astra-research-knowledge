"""Discover block structure from black-box actions and compare trace functionals.

The learner sees only operator actions, Gaussian probes, and ambient dimension.
Hidden block labels are used exclusively by the independent scorer.
This floating-point experiment is not an exact rank/closure certificate.
"""

from dataclasses import dataclass
import json
from pathlib import Path
import time

import numpy as np


@dataclass
class Target:
    matrices: list
    multiplicities_by_rank: dict


def make_target(rng):
    ranks = [1, 2, 3, 4]
    multiplicities = [2, 3, 80, 70]
    n = sum(r * m for r, m in zip(ranks, multiplicities))
    hidden, _ = np.linalg.qr(rng.normal(size=(n, n)))
    arrays = [np.zeros((n, n)), np.zeros((n, n))]
    offset = 0
    for block_index, (r, m) in enumerate(zip(ranks, multiplicities)):
        c1 = np.diag(0.10 + 0.25 * block_index + 0.05 * np.arange(r))
        noise = rng.normal(size=(r, r))
        c2 = 0.50 * np.eye(r) + 0.04 * (noise + noise.T) / r
        width = r * m
        for a, c in zip(arrays, [c1, c2]):
            a[offset:offset + width, offset:offset + width] = np.kron(np.eye(m), c)
        offset += width
    return Target(
        matrices=[hidden @ a @ hidden.T for a in arrays],
        multiplicities_by_rank=dict(zip(ranks, multiplicities)),
    )


def add_vector(vector, basis, tol):
    residual = vector.copy()
    for _ in range(2):
        if basis:
            q = np.column_stack(basis)
            residual -= q @ (q.T @ residual)
    size = np.linalg.norm(residual)
    if size > tol:
        basis.append(residual / size)
        return True
    return False


def close_probes(apply_ops, probes, tol=1e-9):
    # Batch each frontier's residuals before normalization. The naive incremental
    # variant can normalize tiny leakage and spuriously fill the ambient space.
    q, _ = np.linalg.qr(probes, mode="reduced")
    images = [[] for _ in apply_ops]
    processed = 0
    while processed < q.shape[1]:
        old_size = q.shape[1]
        frontier = q[:, processed:old_size]
        candidates = []
        for op_index, apply in enumerate(apply_ops):
            block = np.column_stack([apply(v) for v in frontier.T])
            images[op_index].extend(block.T)
            candidates.append(block)
        residual = np.column_stack(candidates)
        for _ in range(2):
            residual -= q @ (q.T @ residual)
        left, singular, _ = np.linalg.svd(residual, full_matrices=False)
        extra = left[:, singular > tol]
        if extra.shape[1]:
            extra -= q @ (q.T @ extra)
            extra, _ = np.linalg.qr(extra, mode="reduced")
            q = np.column_stack([q, extra])
        processed = old_size
    compressed = []
    closure_error = 0.0
    for op_images in images:
        action = np.column_stack(op_images)
        b = q.T @ action
        closure_error = max(closure_error, np.linalg.norm(action - q @ b, 2))
        compressed.append((b + b.T) / 2)
    return compressed, q.T @ probes, closure_error, sum(map(len, images))


def algebra_basis(generators, tol=1e-8):
    size = generators[0].shape[0]
    basis = [np.eye(size).reshape(-1) / np.sqrt(size)]
    column = 0
    while column < len(basis):
        current = basis[column].reshape(size, size)
        for generator in generators:
            add_vector((generator @ current).reshape(-1), basis, tol)
        column += 1
    return [v.reshape(size, size) for v in basis]


def nullspace(a, tol=1e-8):
    _, singular, vt = np.linalg.svd(a, full_matrices=False)
    return vt[singular < tol].T, singular


def central_blocks(generators, basis, rng, tol=1e-7):
    commutator_columns = []
    for w in basis:
        commutator_columns.append(np.concatenate([(a @ w - w @ a).reshape(-1) for a in generators]))
    coefficients, singular = nullspace(np.column_stack(commutator_columns))
    centers = [sum(coefficients[j, k] * basis[j] for j in range(len(basis)))
               for k in range(coefficients.shape[1])]
    central = sum(c * w for c, w in zip(rng.normal(size=len(centers)), centers))
    central = (central + central.T) / 2
    values, eigenvectors = np.linalg.eigh(central)
    boundaries = [0] + list(np.flatnonzero(np.diff(values) > tol) + 1) + [len(values)]
    blocks = []
    for lo, hi in zip(boundaries[:-1], boundaries[1:]):
        p = eigenvectors[:, lo:hi]
        restricted = np.column_stack([(p.T @ w @ p).reshape(-1) for w in basis])
        dimension = int(np.sum(np.linalg.svd(restricted, compute_uv=False) > tol))
        rank = int(round(np.sqrt(dimension)))
        if rank * rank != dimension or (hi - lo) % rank:
            raise RuntimeError("Numerically inconsistent inferred simple block")
        blocks.append({"irrep_dimension": rank, "compressed_multiplicity": int((hi - lo) // rank),
                       "basis": p, "algebra_dimension": dimension})
    return sorted(blocks, key=lambda block: block["irrep_dimension"]), len(centers), singular


def learn_trace_compiler(apply_ops, probes, rng):
    started = time.perf_counter()
    generators, z, closure_error, calls = close_probes(apply_ops, probes)
    basis = algebra_basis(generators)
    blocks, center_dimension, commutator_singular = central_blocks(generators, basis, rng)
    q_count = probes.shape[1]
    density = z @ z.T / q_count
    raw_algebra_density = sum(np.sum(w * density) * w for w in basis)
    raw_algebra_density = (raw_algebra_density + raw_algebra_density.T) / 2
    for block in blocks:
        p = block["basis"]
        r = block["irrep_dimension"]
        copies = block["compressed_multiplicity"]
        weight = float(np.linalg.norm(p.T @ z, "fro") ** 2)
        exact = copies < q_count * r
        estimate = float(copies if exact else weight / (q_count * r))
        block.update({"exact_multiplicity": exact, "estimated_original_multiplicity": estimate,
                      "probe_weight": weight,
                      "raw_density_eigenvalues": np.linalg.eigvalsh(p.T @ raw_algebra_density @ p)})
    return {"generators": generators, "probe_coordinates": z, "blocks": blocks,
            "compressed_dimension": generators[0].shape[0], "algebra_dimension": len(basis),
            "center_dimension": center_dimension, "matvec_calls": calls,
            "closure_error": closure_error, "elapsed_seconds": time.perf_counter() - started}


def score(compiler, truth_by_rank):
    """Truth is unavailable to learn_trace_compiler and used only here."""
    block_scores = []
    for block in compiler["blocks"]:
        r = block["irrep_dimension"]
        m = truth_by_rank[r]
        copies = block["compressed_multiplicity"]
        # True trace in this compressed block is (m/copies) times matrix trace.
        raw_error = float(np.max(np.abs(block["raw_density_eigenvalues"] * copies / m - 1)))
        hybrid_error = abs(block["estimated_original_multiplicity"] / m - 1)
        block_scores.append({"irrep_dimension": r, "true_multiplicity": m,
                             "inferred_compressed_multiplicity": copies,
                             "inferred_exact": block["exact_multiplicity"],
                             "estimated_original_multiplicity": block["estimated_original_multiplicity"],
                             "raw_uniform_relative_error": raw_error,
                             "hybrid_uniform_relative_error": hybrid_error})
    return {"raw_uniform_relative_error": max(b["raw_uniform_relative_error"] for b in block_scores),
            "hybrid_uniform_relative_error": max(b["hybrid_uniform_relative_error"] for b in block_scores),
            "blocks": block_scores}


def summarize(values):
    return {"mean": float(np.mean(values)), "median": float(np.median(values)),
            "max": float(np.max(values)), "p90": float(np.quantile(values, .9))}


def main():
    target = make_target(np.random.default_rng(9907))
    n = target.matrices[0].shape[0]
    apply_ops = [lambda v, a=a: a @ v for a in target.matrices]
    records = []
    trials = 24
    for trial in range(trials):
        probes = np.random.default_rng(120000 + trial).normal(size=(n, 16))
        for q_count in [1, 2, 4, 8, 16]:
            learned = learn_trace_compiler(apply_ops, probes[:, :q_count], np.random.default_rng(57000 + trial))
            evaluated = score(learned, target.multiplicities_by_rank)
            records.append({"trial": trial, "q": q_count,
                            **{key: learned[key] for key in ["compressed_dimension", "algebra_dimension", "center_dimension", "matvec_calls", "closure_error", "elapsed_seconds"]},
                            **evaluated})
    summary = []
    for q_count in [1, 2, 4, 8, 16]:
        group = [record for record in records if record["q"] == q_count]
        summary.append({"q": q_count, "compressed_dimension": sorted(set(x["compressed_dimension"] for x in group)),
                        "matvec_calls": sorted(set(x["matvec_calls"] for x in group)),
                        "inferred_algebra_dimension": sorted(set(x["algebra_dimension"] for x in group)),
                        "inferred_center_dimension": sorted(set(x["center_dimension"] for x in group)),
                        "max_closure_error": max(x["closure_error"] for x in group),
                        "raw": summarize([x["raw_uniform_relative_error"] for x in group]),
                        "hybrid": summarize([x["hybrid_uniform_relative_error"] for x in group]),
                        "raw_failures_at_10_percent": sum(x["raw_uniform_relative_error"] > .10 for x in group),
                        "hybrid_failures_at_10_percent": sum(x["hybrid_uniform_relative_error"] > .10 for x in group),
                        "mean_setup_seconds": float(np.mean([x["elapsed_seconds"] for x in group]))})
    result = {"ambient_dimension": n, "generator_count": len(target.matrices), "trials": trials,
              "ground_truth_for_scoring_only": target.multiplicities_by_rank, "summary": summary, "records": records,
              "caveat": "Floating-point rank decisions; no theorem of numerical robustness, no wall-time speedup claim."}
    destination = Path(__file__).with_name("hybrid_trace_four_blocks_results.json")
    destination.write_text(json.dumps(result, indent=2))
    print(json.dumps({key: result[key] for key in ["ambient_dimension", "generator_count", "trials", "summary"]}, indent=2))
    print(f"Full results: {destination}")


if __name__ == "__main__":
    main()
