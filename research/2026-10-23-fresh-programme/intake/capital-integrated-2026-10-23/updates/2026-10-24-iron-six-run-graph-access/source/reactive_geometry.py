#!/usr/bin/env python3
"""Small, dependency-light voxel-network comparator for reactive access.

Input is a 3-D NumPy .npy bool array: True=pore, False=solid. Crop faces are
mathematical reservoirs only when explicitly selected; crop-cut faces are
never counted as reactive solid surface. This is a graph calculation, not a
claim that the XCT crop has those physical boundaries or reaction labels.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from pathlib import Path

import numpy as np

SUBSET_FRACTION = 0.25
RANDOM_SEED = 20261024
K_FACE = 1.0


@dataclass
class Network:
    shape: tuple[int, int, int]
    active: np.ndarray                 # pore voxels in components touching a port
    ids: np.ndarray                    # flat-grid index -> local node, else -1
    ei: np.ndarray                     # each internal undirected edge once
    ej: np.ndarray
    port_diag: np.ndarray              # all reservoir half-cell conductances
    port_source: np.ndarray            # selected unit-affinity inlet conductance
    port_sink: np.ndarray              # opposite zero-potential conductance
    n: int

    def lap(self, x: np.ndarray) -> np.ndarray:
        """Dirichlet graph Laplacian, with port edges to zero potential."""
        y = self.port_diag * x
        if self.ei.size:
            d = x[self.ei] - x[self.ej]
            y += np.bincount(self.ei, weights=d, minlength=self.n)
            y += np.bincount(self.ej, weights=-d, minlength=self.n)
        return y

    def diagonal(self) -> np.ndarray:
        d = self.port_diag.copy()
        if self.ei.size:
            d += np.bincount(self.ei, minlength=self.n)
            d += np.bincount(self.ej, minlength=self.n)
        return d


def _shift(a: np.ndarray, axis: int, offset: int) -> np.ndarray:
    out = np.roll(a, offset, axis=axis)
    sl = [slice(None)] * a.ndim
    sl[axis] = 0 if offset > 0 else -1
    out[tuple(sl)] = 0
    return out


def _face_mask(shape: tuple[int, ...], axis: int, side: int) -> np.ndarray:
    m = np.zeros(shape, dtype=bool)
    sl = [slice(None)] * len(shape)
    sl[axis] = 0 if side == 0 else -1
    m[tuple(sl)] = True
    return m


def _component(pore: np.ndarray, seed: np.ndarray) -> np.ndarray:
    """Six-neighbour connected pore components touching any seed voxel."""
    seen = pore & seed
    frontier = seen.copy()
    while frontier.any():
        nxt = np.zeros_like(pore)
        for axis in range(3):
            nxt |= _shift(frontier, axis, -1)
            nxt |= _shift(frontier, axis, +1)
        nxt &= pore & ~seen
        if not nxt.any():
            break
        seen |= nxt
        frontier = nxt
    return seen


def _distance_from_seed(active: np.ndarray, seed: np.ndarray) -> np.ndarray:
    dist = np.full(active.shape, -1, dtype=np.int32)
    frontier = active & seed
    dist[frontier] = 0
    step = 0
    while frontier.any():
        nxt = np.zeros_like(active)
        for axis in range(3):
            nxt |= _shift(frontier, axis, -1)
            nxt |= _shift(frontier, axis, +1)
        nxt &= active & (dist < 0)
        if not nxt.any():
            break
        step += 1
        dist[nxt] = step
        frontier = nxt
    return dist


def build_network(
    pore: np.ndarray,
    axis: int = 0,
    source_side: int = 0,
    opposite_port: bool = False,
) -> Network:
    """Build a unit-edge network, retaining only port-connected components.

    Every pore-pore face has conductance 1. A selected crop-face reservoir is
    a half-voxel away and therefore has conductance 2 per open voxel face.
    """
    if pore.ndim != 3 or pore.dtype != np.bool_:
        raise ValueError("input must be a 3-D NumPy bool array (True=pore)")
    shape = tuple(int(n) for n in pore.shape)
    source = pore & _face_mask(shape, axis, source_side)
    if opposite_port:
        other = pore & _face_mask(shape, axis, 1 - source_side)
        active = _component(pore, source | other)
    else:
        other = np.zeros_like(pore)
        active = _component(pore, source)

    n = int(active.sum())
    ids = np.full(shape, -1, dtype=np.int32)
    ids[active] = np.arange(n, dtype=np.int32)
    ei_parts: list[np.ndarray] = []
    ej_parts: list[np.ndarray] = []
    for ax in range(3):
        lo = [slice(None)] * 3
        hi = [slice(None)] * 3
        lo[ax] = slice(0, -1)
        hi[ax] = slice(1, None)
        a = ids[tuple(lo)]
        b = ids[tuple(hi)]
        keep = (a >= 0) & (b >= 0)
        ei_parts.append(a[keep].astype(np.int32, copy=False))
        ej_parts.append(b[keep].astype(np.int32, copy=False))
    ei = np.concatenate(ei_parts) if ei_parts else np.empty(0, np.int32)
    ej = np.concatenate(ej_parts) if ej_parts else np.empty(0, np.int32)

    port_diag = np.zeros(n, dtype=float)
    port_source = np.zeros(n, dtype=float)
    port_sink = np.zeros(n, dtype=float)
    src_nodes = ids[source]
    src_nodes = src_nodes[src_nodes >= 0]
    if src_nodes.size:
        np.add.at(port_diag, src_nodes, 2.0)
        np.add.at(port_source, src_nodes, 2.0)
    if opposite_port:
        dst_nodes = ids[other]
        dst_nodes = dst_nodes[dst_nodes >= 0]
        if dst_nodes.size:
            np.add.at(port_diag, dst_nodes, 2.0)
            np.add.at(port_sink, dst_nodes, 2.0)
    return Network(shape, active, ids, ei, ej, port_diag, port_source, port_sink, n)


def _pcg(
    matvec,
    rhs: np.ndarray,
    diagonal: np.ndarray,
    tol: float = 1e-11,
    max_iter: int | None = None,
) -> np.ndarray:
    """Jacobi-preconditioned CG for the positive-definite finite graph."""
    n = rhs.size
    if n == 0:
        return np.empty(0, dtype=float)
    max_iter = max_iter or max(100, min(8 * n, 20000))
    x = np.zeros(n, dtype=float)
    r = rhs.copy()
    bnorm = float(np.linalg.norm(rhs))
    if bnorm == 0.0:
        return x
    if np.any(diagonal <= 0):
        raise ValueError("nonpositive diagonal: check for unanchored graph nodes")
    z = r / diagonal
    p = z.copy()
    rz = float(np.dot(r, z))
    for _ in range(max_iter):
        ap = matvec(p)
        pap = float(np.dot(p, ap))
        if pap <= 0.0:
            raise ArithmeticError("operator is not positive definite")
        step = rz / pap
        x += step * p
        r -= step * ap
        if float(np.linalg.norm(r)) <= tol * max(1.0, bnorm):
            return x
        z = r / diagonal
        rz_new = float(np.dot(r, z))
        p = z + (rz_new / rz) * p
        rz = rz_new
    raise RuntimeError(f"PCG did not converge in {max_iter} iterations")


def through_permeability(network: Network, axis: int = 0) -> dict[str, float]:
    """Return conductance, geometry-normalized permeability, and diagnostics."""
    if network.n == 0:
        return {
            "total_conductance": 0.0, "D_eff_over_D": 0.0,
            "source_flux": 0.0, "sink_flux": 0.0, "flux_mismatch": 0.0,
            "residual_norm": 0.0, "relative_residual": 0.0,
            "potential_min": 0.0, "potential_max": 0.0,
        }
    diag = network.diagonal()
    x = _pcg(network.lap, network.port_source, diag)
    source_flux = float(np.dot(network.port_source, 1.0 - x))
    sink_flux = float(np.dot(network.port_sink, x))
    g = 0.5 * (source_flux + sink_flux)
    residual = network.lap(x) - network.port_source
    residual_norm = float(np.linalg.norm(residual))
    rhs_norm = float(np.linalg.norm(network.port_source))
    area = math.prod(network.shape[d] for d in range(3) if d != axis)
    ratio = g * network.shape[axis] / area
    return {
        "total_conductance": g,
        "D_eff_over_D": ratio,
        "source_flux": source_flux,
        "sink_flux": sink_flux,
        "flux_mismatch": source_flux - sink_flux,
        "residual_norm": residual_norm,
        "relative_residual": residual_norm / rhs_norm if rhs_norm else residual_norm,
        "potential_min": float(x.min()),
        "potential_max": float(x.max()),
    }


def reaction_access(
    network: Network,
    k: np.ndarray,
    rho: float = 1.0,
    depth: np.ndarray | None = None,
) -> dict[str, float]:
    """One-port two-species response using exact proportional-mobility reduction.

    Normalize water mobility on each pore-pore face to 1; hydrogen mobility is
    rho times that. Thus alpha=rho/(1+rho) multiplies the affinity Laplacian.
    The one fixed finite-rate case used here sets k per active solid face to 1
    in these same normalized units. It is not a measured chemical rate.
    """
    if k.shape != (network.n,) or rho <= 0 or np.any(k < 0):
        raise ValueError("k must match network size and rho must be positive")
    if network.n == 0:
        return {
            "finite_rate": 0.0, "infinite_rate": 0.0, "effectiveness": 0.0,
            "source_flux": 0.0, "balance_abs": 0.0,
            "residual_norm": 0.0, "relative_residual": 0.0,
            "affinity_min": 0.0, "affinity_max": 0.0,
            "infinite_residual_norm": 0.0, "infinite_relative_residual": 0.0,
            "infinite_affinity_min": 0.0, "infinite_affinity_max": 0.0,
        }
    alpha = rho / (1.0 + rho)
    lap_diag = network.diagonal()
    diag = alpha * lap_diag + k
    rhs = alpha * network.port_source
    finite_op = lambda x: alpha * network.lap(x) + k * x
    a = _pcg(finite_op, rhs, diag)
    finite = float(np.dot(k, a))
    source_flux = float(alpha * np.dot(network.port_source, 1.0 - a))
    residual = finite_op(a) - rhs
    residual_norm = float(np.linalg.norm(residual))
    rhs_norm = float(np.linalg.norm(rhs))

    # Perfect-kinetics limit: active reaction voxels are exact zero-affinity
    # nodes. Solve only on the remaining nodes; no artificial large-k value.
    sink = k > 0
    free = ~sink
    ainfty = np.zeros(network.n, dtype=float)
    if free.any():
        def free_lap(z: np.ndarray) -> np.ndarray:
            full = np.zeros(network.n, dtype=float)
            full[free] = z
            return alpha * network.lap(full)[free]

        diag_free = (alpha * lap_diag)[free]
        rhs_free = rhs[free]
        ainfty[free] = _pcg(free_lap, rhs_free, diag_free)
        inf_residual = free_lap(ainfty[free]) - rhs_free
        inf_residual_norm = float(np.linalg.norm(inf_residual))
        inf_rhs_norm = float(np.linalg.norm(rhs_free))
    else:
        inf_residual_norm = 0.0
        inf_rhs_norm = 0.0
    infinite = float(alpha * np.dot(network.port_source, 1.0 - ainfty))
    return {
        "finite_rate": finite,
        "infinite_rate": infinite,
        "effectiveness": finite / infinite if infinite > 0 else 0.0,
        "source_flux": source_flux,
        "balance_abs": abs(finite - source_flux),
        "residual_norm": residual_norm,
        "relative_residual": residual_norm / rhs_norm if rhs_norm else residual_norm,
        "affinity_min": float(a.min()),
        "affinity_max": float(a.max()),
        "infinite_residual_norm": inf_residual_norm,
        "infinite_relative_residual": inf_residual_norm / inf_rhs_norm if inf_rhs_norm else inf_residual_norm,
        "infinite_affinity_min": float(ainfty.min()),
        "infinite_affinity_max": float(ainfty.max()),
        **_depth_profile(k * a, depth),
    }


def _depth_profile(contribution: np.ndarray, depth: np.ndarray | None) -> dict[str, float]:
    """Contribution by pore-graph distance; geometry diagnostic, not oxide depth."""
    if depth is None or contribution.size == 0:
        return {}
    if depth.shape != contribution.shape or np.any(depth < 0):
        raise ValueError("depth must be a nonnegative distance for every active node")
    total = float(contribution.sum())
    result: dict[str, float] = {}
    if total <= 0:
        return result
    for cutoff in (1, 3, 10):
        result[f"fraction_C_within_{cutoff}_steps"] = float(contribution[depth <= cutoff].sum() / total)
    order = np.argsort(depth, kind="stable")
    cumulative = np.cumsum(contribution[order])
    median_idx = int(np.searchsorted(cumulative, 0.5 * total, side="left"))
    result["contribution_weighted_median_depth_steps"] = float(depth[order[min(median_idx, order.size - 1)]])
    return result


def interface_faces(network: Network, pore: np.ndarray) -> np.ndarray:
    """Local node index for every internal pore/solid voxel face.

    Interfaces across the artificial crop boundary are deliberately omitted.
    """
    ids = network.ids
    faces: list[np.ndarray] = []
    for axis in range(3):
        lo = [slice(None)] * 3
        hi = [slice(None)] * 3
        lo[axis] = slice(0, -1)
        hi[axis] = slice(1, None)
        id_lo = ids[tuple(lo)]
        id_hi = ids[tuple(hi)]
        pore_lo = pore[tuple(lo)]
        pore_hi = pore[tuple(hi)]
        left_wall = (id_lo >= 0) & ~pore_hi
        right_wall = (id_hi >= 0) & ~pore_lo
        faces.append(id_lo[left_wall].astype(np.int32, copy=False))
        faces.append(id_hi[right_wall].astype(np.int32, copy=False))
    return np.concatenate(faces) if faces else np.empty(0, np.int32)


def reaction_scenarios(
    network: Network,
    pore: np.ndarray,
    source_axis: int = 0,
    source_side: int = 0,
) -> dict[str, dict[str, float]]:
    """All internal wall, and equal-area random/remote 25% wall assignments.

    The remote subset is only a geometry proxy for a deeper reactive phase;
    it is not a measured or phase-labelled interface. The subset size is
    frozen at ceil(25% of internal wall faces), with no parameter sweep.
    """
    f = interface_faces(network, pore)
    result: dict[str, dict[str, float]] = {}
    seed_mask = network.active & _face_mask(network.shape, source_axis, source_side)
    distance = _distance_from_seed(network.active, seed_mask)
    depth = distance[network.active]
    if f.size == 0:
        z = np.zeros(network.n, dtype=float)
        for name in ("all_internal_wall", "random_equal_area_25pct", "remote_equal_area_25pct"):
            result[name] = reaction_access(network, z, depth=depth)
        return result

    k_all = K_FACE * np.bincount(f, minlength=network.n)
    result["all_internal_wall"] = reaction_access(network, k_all, depth=depth)
    m = min(f.size, max(1, int(math.ceil(SUBSET_FRACTION * f.size))))
    rng = np.random.default_rng(RANDOM_SEED)
    random_idx = rng.choice(f.size, size=m, replace=False)
    k_random = K_FACE * np.bincount(f[random_idx], minlength=network.n)
    result["random_equal_area_25pct"] = reaction_access(network, k_random, depth=depth)

    # Local node indices are assigned in row-major active-voxel order.
    face_dist = distance[network.active]
    deep_idx = np.argsort(-face_dist[f], kind="stable")[:m]
    k_deep = K_FACE * np.bincount(f[deep_idx], minlength=network.n)
    result["remote_equal_area_25pct"] = reaction_access(network, k_deep, depth=depth)
    return result


def _dense_block_crosscheck(net: Network, k: np.ndarray, rho: float = 1.0) -> None:
    """Tiny dense solve of full H/W equations checks affinity reduction."""
    n = net.n
    L = np.zeros((n, n), dtype=float)
    np.fill_diagonal(L, net.port_diag)
    for i, j in zip(net.ei, net.ej):
        L[i, i] += 1.0
        L[j, j] += 1.0
        L[i, j] -= 1.0
        L[j, i] -= 1.0
    # Same spatial boundary, H=1 and W=0. Source edge mobility is rho:1.
    b_h = rho * net.port_source
    b_w = np.zeros(n)
    K = np.diag(k)
    block = np.block([[rho * L + K, -K], [-K, L + K]])
    uv = np.linalg.solve(block, np.concatenate([b_h, b_w]))
    full_affinity = uv[:n] - uv[n:]
    flux_full = float(np.dot(k, full_affinity))
    reduced = reaction_access(net, k, rho)["finite_rate"]
    if not np.isclose(flux_full, reduced, rtol=1e-9, atol=1e-11):
        raise AssertionError((flux_full, reduced))


def self_test() -> None:
    # A fully open rectangular voxel slab has D_eff/D=1 exactly under the
    # half-cell boundary convention; this checks edge and boundary scaling.
    slab = np.ones((6, 3, 4), dtype=bool)
    nslab = build_network(slab, axis=0, source_side=0, opposite_port=True)
    slab_result = through_permeability(nslab, axis=0)
    ratio = slab_result["D_eff_over_D"]
    if not np.isclose(ratio, 1.0, atol=1e-10):
        raise AssertionError(f"open slab D_eff/D={ratio}, expected 1")

    # One voxel-wide straight pore through solid: fixed through conductance.
    # Equal-area patches at near/far positions change one-port reaction access
    # while leaving that same-geometry opposed-face permeability untouched.
    pore = np.zeros((3, 3, 8), dtype=bool)
    pore[1, 1, :] = True
    net = build_network(pore, axis=2, source_side=0, opposite_port=True)
    through = through_permeability(net, axis=2)
    g = through["total_conductance"]
    deff = through["D_eff_over_D"]
    expected = 1.0 / 9.0  # one open voxel column / 3x3 gross cross-section
    if not np.isclose(deff, expected, atol=1e-10):
        raise AssertionError(f"line-channel D_eff/D={deff}, expected {expected}")

    one = build_network(pore, axis=2, source_side=0, opposite_port=False)
    near = np.zeros(one.n)
    far = np.zeros(one.n)
    # One of four internal solid-wall faces at each selected voxel; equal area.
    near[one.ids[1, 1, 1]] = 1.0
    far[one.ids[1, 1, 6]] = 1.0
    c_near = reaction_access(one, near)["finite_rate"]
    c_far = reaction_access(one, far)["finite_rate"]
    if not (c_near > c_far > 0.0):
        raise AssertionError((c_near, c_far))
    _dense_block_crosscheck(one, near)
    print("self-test: PASS")
    print("  open slab D_eff/D = 1.000000")
    print(f"  line-pore D_eff/D = {deff:.6f} (expected 0.111111), G={g:.6g}")
    print(f"  same pore, equal wall area: C_near={c_near:.6g} > C_remote={c_far:.6g}")
    print("  two-species block solve agrees with proportional-mobility reduction")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mask", nargs="?", type=Path, help="3-D .npy bool pore mask")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--axis", type=int, default=0, choices=(0, 1, 2))
    parser.add_argument("--source-side", type=int, default=0, choices=(0, 1))
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if args.mask is None:
        parser.error("provide a .npy mask or use --self-test")
    pore = np.load(args.mask, allow_pickle=False)
    net_through = build_network(pore, args.axis, args.source_side, opposite_port=True)
    through = through_permeability(net_through, args.axis)
    net_reaction = build_network(pore, args.axis, args.source_side, opposite_port=False)
    scenarios = reaction_scenarios(net_reaction, pore, args.axis, args.source_side)
    print(f"shape={pore.shape}; pore_fraction={float(pore.mean()):.8g}")
    print("boundary note: selected crop faces are mathematical reservoirs, not verified physical exterior")
    print(f"source-connected pore voxels={net_reaction.n}")
    print(f"opposed-face total conductance G={through['total_conductance']:.10g}; "
          f"geometric D_eff/D={through['D_eff_over_D']:.10g}")
    print(f"through solve: residual={through['residual_norm']:.3g} "
          f"(relative {through['relative_residual']:.3g}); "
          f"influx={through['source_flux']:.10g}; outflux={through['sink_flux']:.10g}; "
          f"mismatch={through['flux_mismatch']:.3g}; "
          f"potential range=[{through['potential_min']:.8g},{through['potential_max']:.8g}]")
    print(f"internal pore-solid faces in source-connected component={interface_faces(net_reaction, pore).size}")
    for name, values in scenarios.items():
        print(f"{name}: C(Da_face=1,rho=1)={values['finite_rate']:.10g}; "
              f"C(perfect-kinetics)={values['infinite_rate']:.10g}; "
              f"effectiveness={values['effectiveness']:.8g}; "
              f"source-flux-check={values['source_flux']:.10g}; "
              f"balance={values['balance_abs']:.3g}; "
              f"residual={values['residual_norm']:.3g} "
              f"(relative {values['relative_residual']:.3g}); "
              f"affinity-range=[{values['affinity_min']:.8g},{values['affinity_max']:.8g}]; "
              f"capacity-residual={values['infinite_residual_norm']:.3g} "
              f"(relative {values['infinite_relative_residual']:.3g}); "
              f"capacity-affinity-range=[{values['infinite_affinity_min']:.8g},{values['infinite_affinity_max']:.8g}]")
        for cutoff in (1, 3, 10):
            key = f"fraction_C_within_{cutoff}_steps"
            if key in values:
                print(f"  contribution fraction within {cutoff} pore steps={values[key]:.8g}")
        if "contribution_weighted_median_depth_steps" in values:
            print(f"  contribution-weighted median pore depth="
                  f"{values['contribution_weighted_median_depth_steps']:.8g} steps")
        if not np.isclose(values["finite_rate"], values["source_flux"], rtol=1e-8, atol=1e-10):
            raise AssertionError(f"mass balance failed in {name}")
    print("reaction labels/rates: synthetic scenarios only; no phase map or kinetic coefficient inferred")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
