#!/usr/bin/env python3
"""Finite q=4 Potts sensor-tree capacity and budgeted design certificate.

This computes the max-ray weighted-flow certificate, not the exact Bayes
sensor-design optimum. A sensor P_rho at a tree vertex is represented by an
extra edge of parameter rho to a perfectly observed terminal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
import json
from itertools import product
from math import inf, isfinite, isqrt, sqrt
from typing import Iterable


@dataclass
class Sensor:
    name: str
    rho: float
    cost: int = 1


@dataclass
class Node:
    name: str
    children: list[tuple[float, "Node"]] = field(default_factory=list)
    sensors: list[Sensor] = field(default_factory=list)

    def add_child(self, lam: float, child: "Node") -> None:
        if not (0.0 <= lam <= 1.0):
            raise ValueError("edge parameter must lie in [0,1]")
        self.children.append((lam, child))


def phi(lam: float, strength: float) -> float:
    """Series transform Phi_lam(S)=lam^2 S/sqrt(1+(1-lam^4)S^2)."""
    if lam == 0.0 or strength == 0.0:
        return 0.0
    if strength == inf:
        if lam == 1.0:
            return inf
        return lam * lam / sqrt(1.0 - lam**4)
    if lam == 1.0:
        return strength
    return lam * lam * strength / sqrt(1.0 + (1.0 - lam**4) * strength**2)


def sensor_strength(rho: float) -> float:
    """Contribution of a sensor channel attached to an observed leaf."""
    if not (0.0 <= rho <= 1.0):
        raise ValueError("sensor parameter must lie in [0,1]")
    if rho == 0.0:
        return 0.0
    if rho == 1.0:
        return inf
    return rho * rho / sqrt(1.0 - rho**4)


def _as_fraction(x: float | Fraction) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(str(x))


def phi_lower_units(lam: float | Fraction, child_units: int | None, Q: int) -> int | None:
    """Exact integer lower bound for Q*Phi_lam(child_units/Q).

    `None` represents +infinity. All square roots are eliminated with
    integer arithmetic, so the returned finite integer is downward-rounded.
    """
    f = _as_fraction(lam)
    if Q <= 0 or not 0 <= f <= 1:
        raise ValueError("need Q>0 and edge parameter in [0,1]")
    if f == 0 or child_units == 0:
        return 0
    if child_units is None:
        if f == 1:
            return None
        a, b = f.numerator, f.denominator
        d = b**4 - a**4
        return isqrt((Q * a * a) ** 2 // d)
    if f == 1:
        return child_units
    a, b = f.numerator, f.denominator
    D = b**4 * Q**2 + (b**4 - a**4) * child_units**2
    N = Q * a**2 * child_units
    return isqrt(N**2 // D)


def sensor_strength_lower_units(rho: float | Fraction, Q: int) -> int | None:
    """Exact integer lower bound for Q*rho^2/sqrt(1-rho^4)."""
    f = _as_fraction(rho)
    if Q <= 0 or not 0 <= f <= 1:
        raise ValueError("need Q>0 and sensor parameter in [0,1]")
    if f == 0:
        return 0
    if f == 1:
        return None
    a, b = f.numerator, f.denominator
    return isqrt((Q * a * a) ** 2 // (b**4 - a**4))


def capacity_lower_units(root: Node, Q: int, selected: set[str] | None = None) -> dict[str, int | None]:
    """Certified downward-rounded S_v values; None means +infinity."""
    values: dict[str, int | None] = {}

    def add_units(a: int | None, b: int | None) -> int | None:
        return None if a is None or b is None else a + b

    def visit(v: Node) -> int | None:
        terms = [phi_lower_units(lam, visit(w), Q) for lam, w in v.children]
        terms.extend(
            sensor_strength_lower_units(s.rho, Q)
            for s in v.sensors
            if selected is None or s.name in selected
        )
        total: int | None = 0
        for term in terms:
            total = add_units(total, term)
        values[v.name] = total
        return total

    visit(root)
    return values


def capacity_strength(root: Node, selected: set[str] | None = None) -> dict[str, float]:
    """Return S_v for all nodes under the chosen sensors.

    `selected=None` selects every sensor. Otherwise sensor names are selected.
    """
    values: dict[str, float] = {}

    def visit(v: Node) -> float:
        terms = [phi(lam, visit(w)) for lam, w in v.children]
        terms.extend(
            sensor_strength(s.rho)
            for s in v.sensors
            if selected is None or s.name in selected
        )
        s_v = sum(terms, 0.0)
        values[v.name] = s_v
        return s_v

    visit(root)
    return values


def capacity_optimal_flow(root: Node, selected: set[str] | None = None):
    """Build the capacity-maximizing flow on the augmented finite tree.

    The returned flow maps ordinary tree-edge names ("v->w") and sensor-edge
    names ("v=>sensor") to masses. With root mass S_root its largest weighted
    path energy is one, except S_root=inf (a zero-resistance perfect route).
    """
    strengths = capacity_strength(root, selected)
    root_mass = strengths[root.name]
    masses: dict[str, float] = {}

    def distribute(v: Node, incoming: float) -> None:
        if incoming == 0.0:
            return
        S = strengths[v.name]
        if S == 0.0:
            raise ValueError("positive incoming flow reached a zero-capacity subtree")
        contributions: list[tuple[str, float, Node | None]] = []
        for lam, w in v.children:
            q = phi(lam, strengths[w.name])
            contributions.append((f"{v.name}->{w.name}", q, w))
        for sensor in v.sensors:
            if selected is None or sensor.name in selected:
                contributions.append((f"{v.name}=>{sensor.name}", sensor_strength(sensor.rho), None))
        infinite = [entry for entry in contributions if entry[1] == inf]
        if infinite:
            # Any finite mass can be sent along zero-energy perfect routes;
            # finite-capacity branches receive zero in this limiting case.
            contributions = [
                (label, 1.0 / len(infinite), child) if q == inf
                else (label, 0.0, child)
                for label, q, child in contributions
            ]
            S_for_split = 1.0
        else:
            S_for_split = S
        for label, q, child in contributions:
            if q == 0.0:
                continue
            edge_mass = incoming * q / S_for_split
            masses[label] = edge_mass
            if child is not None:
                distribute(child, edge_mass)

    if root_mass not in (0.0, inf):
        # Use a tiny explicit safety factor because this witness is assembled
        # with binary floating arithmetic. The capacity value itself is
        # unaffected; the integer DP below is the rigorous lower certificate.
        distribute(root, root_mass * (1.0 - 1e-10))
    elif root_mass == inf:
        # Finite ordinary flow certificates can be obtained by scaling every
        # ideal split by any chosen finite M; the maximizing split has a
        # zero-energy perfect route and is represented only by the limit.
        distribute(root, 1.0)
    return root_mass, strengths, masses


def path_energies(root: Node, masses: dict[str, float]) -> list[float]:
    """Evaluate weighted path energy for every root-to-sensor route."""
    paths: list[float] = []

    def walk(v: Node, Rv: float, energy: float) -> None:
        found = False
        for lam, w in v.children:
            key = f"{v.name}->{w.name}"
            theta = masses.get(key, 0.0)
            if theta == 0.0 or lam == 0.0:
                continue
            found = True
            Rw = Rv * lam**2
            increment = (1.0 - lam**4) * (theta / Rw) ** 2
            walk(w, Rw, energy + increment)
        for sensor in v.sensors:
            key = f"{v.name}=>{sensor.name}"
            theta = masses.get(key, 0.0)
            if theta == 0.0:
                continue
            found = True
            rho = sensor.rho
            if rho == 0.0:
                continue
            Rw = Rv * rho**2
            increment = (1.0 - rho**4) * (theta / Rw) ** 2
            paths.append(energy + increment)
        if not found:
            return

    walk(root, 1.0, 0.0)
    return paths


def budgeted_design(root: Node, budget: int) -> tuple[dict[str, list[float]], dict[str, set[str]]]:
    """Maximize certificate strength with integer sensor costs and budget.

    The DP maximizes the certificate, not true Bayes success. Child budgets
    are convolved; runtime is O(|E| B^2 + local-menu work) for a tree with a
    bounded number of sensor options at each node.
    """
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    dp: dict[str, list[float]] = {}
    chosen: dict[str, list[set[str]]] = {}

    def visit(v: Node) -> None:
        for _, child in v.children:
            visit(child)

        # Exact-cost states; -inf denotes infeasible. Carry-forward later
        # converts them to at-most-cost states.
        local = [0.0] + [-inf] * budget
        local_sets: list[set[str]] = [set() for _ in range(budget + 1)]
        for sensor in v.sensors:
            if sensor.cost <= 0:
                raise ValueError("sensor costs must be positive integers")
            new = local[:]
            new_sets = [s.copy() for s in local_sets]
            for spent in range(budget - sensor.cost + 1):
                if local[spent] == -inf:
                    continue
                target = spent + sensor.cost
                val = local[spent] + sensor_strength(sensor.rho)
                if val > new[target]:
                    new[target] = val
                    new_sets[target] = local_sets[spent] | {sensor.name}
            local, local_sets = new, new_sets

        states = local[:]
        state_sets = [s.copy() for s in local_sets]
        for lam, child in v.children:
            new = [-inf] * (budget + 1)
            new_sets = [set() for _ in range(budget + 1)]
            child_states = dp[child.name]
            child_sets = chosen[child.name]
            for used_parent in range(budget + 1):
                if states[used_parent] == -inf:
                    continue
                for used_child in range(budget - used_parent + 1):
                    if child_states[used_child] == -inf:
                        continue
                    total = used_parent + used_child
                    val = states[used_parent] + phi(lam, child_states[used_child])
                    if val > new[total]:
                        new[total] = val
                        new_sets[total] = state_sets[used_parent] | child_sets[used_child]
            states, state_sets = new, new_sets

        # Convert exact cost to at-most budget and retain the maximizing menu.
        for k in range(1, budget + 1):
            if states[k - 1] > states[k]:
                states[k] = states[k - 1]
                state_sets[k] = state_sets[k - 1].copy()
        dp[v.name] = states
        chosen[v.name] = state_sets

    visit(root)
    return dp, chosen


def budgeted_design_lower_units(root: Node, budget: int, Q: int):
    """Budget DP with exact downward-rounded integer certificate values.

    Finite capacities are stored as floor(Q*S); `None` is +infinity and -1
    marks an infeasible exact-cost state. Sensor costs are integer units.
    """
    if budget < 0 or Q <= 0:
        raise ValueError("need budget>=0 and Q>0")
    dp: dict[str, list[int | None]] = {}
    chosen: dict[str, list[set[str]]] = {}

    def combine(a: int | None, b: int | None) -> int | None:
        return None if a is None or b is None else a + b

    def better(a: int | None, b: int | None) -> bool:
        """Whether feasible candidate a is strictly better than b."""
        if a is None:
            return b is not None
        if b is None:
            return False
        return a > b

    def visit(v: Node) -> None:
        for _, child in v.children:
            visit(child)

        local: list[int | None] = [0] + [-1] * budget  # -1=infeasible
        local_sets = [set() for _ in range(budget + 1)]
        for sensor in v.sensors:
            if sensor.cost <= 0:
                raise ValueError("sensor costs must be positive integers")
            contribution = sensor_strength_lower_units(sensor.rho, Q)
            new, new_sets = local[:], [s.copy() for s in local_sets]
            for spent in range(budget - sensor.cost + 1):
                if local[spent] == -1:
                    continue
                value = combine(local[spent], contribution)
                target = spent + sensor.cost
                if new[target] == -1 or better(value, new[target]):
                    new[target] = value
                    new_sets[target] = local_sets[spent] | {sensor.name}
            local, local_sets = new, new_sets

        states, state_sets = local, local_sets
        for lam, child in v.children:
            new: list[int | None] = [-1] * (budget + 1)
            new_sets = [set() for _ in range(budget + 1)]
            for spent_v in range(budget + 1):
                if states[spent_v] == -1:
                    continue
                for spent_w in range(budget - spent_v + 1):
                    child_cap = dp[child.name][spent_w]
                    if child_cap == -1:
                        continue
                    branch = phi_lower_units(lam, child_cap, Q)
                    value = combine(states[spent_v], branch)
                    total = spent_v + spent_w
                    if new[total] == -1 or better(value, new[total]):
                        new[total] = value
                        new_sets[total] = state_sets[spent_v] | chosen[child.name][spent_w]
            states, state_sets = new, new_sets

        for k in range(1, budget + 1):
            if states[k - 1] != -1 and (states[k] == -1 or better(states[k - 1], states[k])):
                states[k] = states[k - 1]
                state_sets[k] = state_sets[k - 1].copy()
        dp[v.name], chosen[v.name] = states, state_sets

    visit(root)
    return dp, chosen


def regular_perfect_leaf_strength(d: int, lam: float, depth: int) -> list[float]:
    """Return S by level, root first, with perfect observations at depth n."""
    if d < 1 or depth < 0:
        raise ValueError("d must be positive and depth nonnegative")
    levels = [0.0] * (depth + 1)
    levels[depth] = inf
    for j in range(depth - 1, -1, -1):
        levels[j] = d * phi(lam, levels[j + 1])
    return levels


def finite_tv_lower_from_capacity(b: float) -> float:
    """Candidate finite-depth lower bound using C=460 and t=0.01.

    It follows the weighted-capacity proof's explicit loss inequality. The
    `t=eta*sqrt(b^2+2)` substitution gives relative loss <= .462 < 1/2.
    This is a lower bound on E TV(root posterior, uniform), not exact Bayes
    performance.
    """
    if b <= 0.0:
        return 0.0
    if b == inf:
        return 1.0 / 1600.0
    return b / (1600.0 * sqrt(b * b + 2.0))


def bayes_map_advantage_lower_from_capacity(b: float) -> float:
    """Return lower bound on Bayes MAP success above 1/4: E TV / 3."""
    return finite_tv_lower_from_capacity(b) / 3.0


def exact_root_map_success(sensor_rhos: Iterable[Fraction]) -> Fraction:
    """Exact q=4 MAP success for independent Potts sensors at the root."""
    sensors = tuple(Fraction(x) for x in sensor_rhos)
    total = Fraction(0)
    for outputs in product(range(4), repeat=len(sensors)):
        likelihoods = []
        for truth in range(4):
            likelihood = Fraction(1)
            for rho, y in zip(sensors, outputs):
                likelihood *= rho + (1 - rho) / 4 if y == truth else (1 - rho) / 4
            likelihoods.append(likelihood)
        total += max(likelihoods)
    return total / 4


def _self_check() -> None:
    # Two-level asymmetric sensor tree with sensors both internally and at
    # leaves. Includes a deterministic edge and a channel-erasing edge.
    root = Node("r", sensors=[Sensor("root-low", 0.4, 1)])
    a, b = Node("a", sensors=[Sensor("a-mid", 0.7, 2)]), Node("b")
    c, d = Node("c", sensors=[Sensor("c-perfect", 1.0, 3)]), Node("d", sensors=[Sensor("d-noisy", 0.6, 1)])
    root.add_child(0.8, a)
    root.add_child(0.5, b)
    a.add_child(1.0, c)
    b.add_child(0.0, d)
    all_s = capacity_strength(root)
    assert all_s["a"] == inf  # perfect sensor behind deterministic edge

    # Remove perfect sensor: finite max-flow capacity has energy-one witness.
    selected = {"root-low", "a-mid", "d-noisy"}
    S, _, masses = capacity_optimal_flow(root, selected)
    assert isfinite(S) and S > 0.0
    energies = path_energies(root, masses)
    assert energies and max(energies) <= 1.0, (S, energies, masses)
    Q = 10**8
    lower = capacity_lower_units(root, Q, selected)["r"]
    assert lower is not None and lower / Q <= S
    assert sensor_strength_lower_units(Fraction(1, 1), Q) is None
    assert phi_lower_units(Fraction(1, 1), None, Q) is None
    assert phi_lower_units(Fraction(0, 1), None, Q) == 0

    # Independent grid minimization of the two root branches gives the same
    # max-ray unit-flow value as the recursion (up to grid resolution).
    c_root = (1.0 - 0.4**4) / (0.4**4)
    R_sensor = 0.8**2 * 0.7**2
    c_a = (1.0 - 0.8**4) / (0.8**4) + (1.0 - 0.7**4) / (R_sensor**2)
    grid_min = min(max(c_root * (j / 100000) ** 2,
                       c_a * (1.0 - j / 100000) ** 2)
                   for j in range(100001))
    grid_capacity = 1.0 / sqrt(grid_min)
    assert abs(grid_capacity - S) < 1e-4, (grid_capacity, S)

    # DP: a single unit budget chooses the best one of three options.
    dp, menu = budgeted_design(root, 1)
    assert dp["r"][1] >= dp["r"][0]
    assert menu["r"][1]

    # Regular tree: above KS grows from a positive fixed point; critical case
    # decays as depth increases (boundary starts at infinity).
    above = regular_perfect_leaf_strength(2, 0.8, 12)[0]
    critical = regular_perfect_leaf_strength(2, 1.0 / sqrt(2.0), 12)[0]
    assert above > 1.0 and 0.0 < critical < 0.34
    assert finite_tv_lower_from_capacity(S) > 0.0

    # Explicit design counterexample: certificate maximization selects two
    # rho=.6 sensors (cost 2), while Bayes MAP selects one rho=.7 sensor.
    # Thus the DP is optimal for the certificate, not for actual Bayes risk.
    one_strong = sensor_strength(0.7)
    two_moderate = 2.0 * sensor_strength(0.6)
    success_strong = exact_root_map_success([Fraction(7, 10)])
    success_moderate = exact_root_map_success([Fraction(3, 5), Fraction(3, 5)])
    assert two_moderate > one_strong
    assert success_strong == Fraction(31, 40)
    assert success_moderate == Fraction(7, 10)
    assert success_strong > success_moderate
    design_root = Node("design", sensors=[
        Sensor("one-strong", Fraction(7, 10), 2),
        Sensor("two-moderate-a", Fraction(3, 5), 1),
        Sensor("two-moderate-b", Fraction(3, 5), 1)])
    fdp, fmenu = budgeted_design(design_root, 2)
    idp, imenu = budgeted_design_lower_units(design_root, 2, Q)
    assert fmenu["design"][2] == {"two-moderate-a", "two-moderate-b"}
    assert imenu["design"][2] == {"two-moderate-a", "two-moderate-b"}
    assert idp["design"][2] / Q <= fdp["design"][2]
    root_flow_mass = sum(masses.get(f"r->{child.name}", 0.0) for _, child in root.children)
    root_flow_mass += sum(masses.get(f"r=>{sensor.name}", 0.0) for sensor in root.sensors)
    print(json.dumps({"capacity": S, "flow_mass": root_flow_mass,
           "max_path_energy": max(energies),
           "selected_flow": masses, "regular_above_ks": above,
           "regular_critical_ks": critical,
           "tv_lower": finite_tv_lower_from_capacity(S),
           "map_advantage_lower": bayes_map_advantage_lower_from_capacity(S),
           "integer_capacity_lower": lower / Q,
           "independent_grid_capacity": grid_capacity,
           "integer_dp_capacity_lower": idp["design"][2] / Q,
           "design_counterexample": {
               "capacity_one_rho_0.7": one_strong,
               "capacity_two_rho_0.6": two_moderate,
               "map_success_one_rho_0.7": str(success_strong),
               "map_success_two_rho_0.6": str(success_moderate)}},
              indent=2, sort_keys=True))


if __name__ == "__main__":
    _self_check()
