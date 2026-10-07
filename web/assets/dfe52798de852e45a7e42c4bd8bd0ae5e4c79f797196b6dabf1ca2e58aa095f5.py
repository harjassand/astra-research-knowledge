#!/usr/bin/env python3
"""Exact small checks for the charge-detector route discussed in REVISION_01."""

from fractions import Fraction as Q
import json


def apply_mode_permutation(mask, perm):
    """Apply c_i^dagger -> c_perm[i]^dagger to a canonical Fock basis vector."""
    old = [i for i in range(len(perm)) if (mask >> i) & 1]
    moved = [perm[i] for i in old]
    inversions = sum(moved[i] > moved[j]
                     for i in range(len(moved))
                     for j in range(i + 1, len(moved)))
    newmask = sum(1 << i for i in moved)
    return newmask, (-1) ** inversions


def arm_charges(mask):
    # Mode order is a_up, a_down, b_up, b_down.
    return ((mask & 0b0011).bit_count(), (mask & 0b1100).bit_count())


def terminal_hard_projector(mask):
    return arm_charges(mask) == (1, 1)


def compose_pbs_charge_pbs(mask, pbs):
    middle, s1 = apply_mode_permutation(mask, pbs)
    if not terminal_hard_projector(middle):
        return {}
    out, s2 = apply_mode_permutation(middle, pbs)
    return {out: s1 * s2}


def pair_rotation_check():
    """Rotate one site of a two-site singlet using an exact rational SU(2)."""
    c, s = Q(3, 5), Q(4, 5)
    # Canonical order: u1,u2,d1,d2. The singlet is u1*d2 + u2*d1
    # in this order (the physical site-order expression has the usual wedge sign).
    initial = {(0, 3): Q(1), (1, 2): Q(1)}
    # On site 1: u1 -> c*u1 + s*d1; d1 -> -s*u1 + c*d1.
    images = {
        0: [(0, c), (2, s)],
        2: [(0, -s), (2, c)],
        1: [(1, Q(1))],
        3: [(3, Q(1))],
    }
    result = {}
    for monomial, coeff in initial.items():
        for m0, a0 in images[monomial[0]]:
            for m1, a1 in images[monomial[1]]:
                if m0 == m1:
                    continue
                if m0 < m1:
                    key, sign = (m0, m1), 1
                else:
                    key, sign = (m1, m0), -1
                result[key] = result.get(key, Q(0)) + coeff * a0 * a1 * sign
    result = {f"{a}{b}": str(v) for (a, b), v in sorted(result.items()) if v}
    # Modes 0,1 are up-up; modes 2,3 are down-down. Both appear with coefficient 4/5.
    assert result == {"01": "4/5", "03": "3/5", "12": "3/5", "23": "4/5"}
    return result


class Qsqrt2:
    """Exact a + b*sqrt(2), with rational a,b."""
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    def __mul__(self, other):
        other = other if isinstance(other, Qsqrt2) else Qsqrt2(other)
        return Qsqrt2(self.a * other.a + 2 * self.b * other.b,
                      self.a * other.b + self.b * other.a)

    def __eq__(self, other):
        other = other if isinstance(other, Qsqrt2) else Qsqrt2(other)
        return self.a == other.a and self.b == other.b

    def __repr__(self):
        return f"({self.a})+({self.b})sqrt2"


def cnot_branch_from_appendix():
    """Check the fixed p1=p2=1,z=0 branch stated in Beenakker Appendix A."""
    first_outcome_amp = Qsqrt2(0, Q(1, 2))  # 1/sqrt(2) from input |+>.
    second_outcome_amp = Qsqrt2(Q(1, 2), 0)  # normalized H-P1-H branch.
    branch_amp = first_outcome_amp * second_outcome_amp
    assert branch_amp == Qsqrt2(0, Q(1, 4))  # sqrt(2)/4 = 1/(2 sqrt(2)).
    table = {}
    for x in range(2):
        for y in range(2):
            p1 = p2 = 1
            z = 0
            # Eq. (17): ancilla a=x+p1+1; Eq. (18): output target x+y+z+p1+1.
            a = (x + p1 + 1) % 2
            phase = (-1) ** (((p2 + 1) * (x + z + p1 + 1)) % 2)
            target = (a + y + z) % 2
            if z == 0:
                assert target == (x + y) % 2
            assert phase == 1
            table[f"{x}{y}"] = f"{x}{target}"
    assert table == {"00": "00", "01": "01", "10": "11", "11": "10"}
    # (sqrt(2)/4)^2 = 1/8, input-independent on every basis state.
    success_probability = Q(1, 8)
    return table, repr(branch_amp), str(success_probability)


def main():
    pbs = [0, 3, 2, 1]  # polarizing splitter: swap the two down-spin arms.
    logical_basis = {
        "00": (1 << 0) | (1 << 2),
        "01": (1 << 0) | (1 << 3),
        "10": (1 << 1) | (1 << 2),
        "11": (1 << 1) | (1 << 3),
    }
    interleaved = {}
    final_only = {}
    for label, mask in logical_basis.items():
        interleaved[label] = compose_pbs_charge_pbs(mask, pbs)
        final_only[label] = {mask: 1} if terminal_hard_projector(mask) else {}
    expected = {
        "00": {logical_basis["00"]: 1},
        "01": {},
        "10": {},
        "11": {logical_basis["11"]: 1},
    }
    assert interleaved == expected
    assert final_only != interleaved
    cnot_table, cnot_branch_amplitude, cnot_branch_probability = cnot_branch_from_appendix()

    result = {
        "status": "PASS_EXACT_FINITE_DIAGNOSTICS",
        "source_route": "Beenakker et al., arXiv:quant-ph/0401066v1, Fig. 2 and Appendix A",
        "mode_order": ["a_up", "a_down", "b_up", "b_down"],
        "interleaved_p1_branch_on_one_per_arm_basis": {
            label: {format(mask, "04b"): amp for mask, amp in outputs.items()}
            for label, outputs in interleaved.items()
        },
        "terminal_only_p1_on_same_arms": {
            label: {format(mask, "04b"): amp for mask, amp in outputs.items()}
            for label, outputs in final_only.items()
        },
        "interleaved_branch_is_even_spin_parity_projector": True,
        "terminal_only_projector_is_identity_on_input_logical_subspace": True,
        "appendix_selected_cnot_branch": {
            "p1": 1,
            "p2": 1,
            "ancilla_z": 0,
            "basis_map": cnot_table,
            "amplitude_per_basis_state": cnot_branch_amplitude,
            "success_probability": cnot_branch_probability,
        },
        "opposite_spin_pair_interface_local_rotation": {
            "rational_rotation": [["3/5", "-4/5"], ["4/5", "3/5"]],
            "two_site_singlet_after_site1_rotation_coefficients": pair_rotation_check(),
            "same_spin_terms": {"up_up": "4/5", "down_down": "4/5"},
            "conclusion": "a site-local spin rotation leaves the opposite-spin-only pair family",
        },
        "scope": "Finite exact checks; no impossibility theorem for ancillary or teleportation embeddings.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
