"""Exact one-sided execution for a restricted native quadratic-guard DAG.

This is a research reproduction, NOT a general hybrid-system or Puiseux solver.
Only Python's standard library is used. Input guard coefficients are native
rational coefficients in local time; no event roots are supplied to compile().
"""
from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction as F
from functools import cmp_to_key
import json


def frac(x):
    return x if isinstance(x, F) else F(str(x))


@dataclass(frozen=True)
class GP:
    """A finite generalized polynomial, exact for all epsilon > 0."""
    terms: tuple[tuple[F, F], ...] = ()

    @staticmethod
    def make(terms):
        d = {}
        for e, c in terms:
            e, c = frac(e), frac(c)
            d[e] = d.get(e, F(0)) + c
        return GP(tuple(sorted((e, c) for e, c in d.items() if c)))

    @staticmethod
    def const(c):
        return GP.make([(0, c)])

    @staticmethod
    def monomial(e, c=1):
        return GP.make([(e, c)])

    def __add__(self, other):
        if not isinstance(other, GP):
            other = GP.const(other)
        return GP.make(self.terms + other.terms)

    def __neg__(self):
        return GP(tuple((e, -c) for e, c in self.terms))

    def __sub__(self, other):
        if not isinstance(other, GP):
            other = GP.const(other)
        return self + (-other)

    def sign(self):
        return 0 if not self.terms else (1 if self.terms[0][1] > 0 else -1)

    def sign_certificate(self):
        """For 0 < eps <= 2**(-L), first coefficient fixes the sign.

        The bound is intentionally conservative and computed with integer/rational
        arithmetic, including when L is exponentially large as a number.
        """
        if not self.terms:
            return {"sign": 0, "identically_zero": True, "L": 0}
        e0, c0 = self.terms[0]
        if len(self.terms) == 1:
            L = 0
        else:
            delta = self.terms[1][0] - e0
            C = sum(abs(c) for _, c in self.terms[1:])
            ratio = 2 * C / abs(c0)
            m = 0
            if ratio > 1:
                # Find the exact smallest m with 2**m >= ratio.
                m = max(0, ratio.numerator.bit_length() - ratio.denominator.bit_length())
                if F(1 << m) < ratio:
                    m += 1
            x = F(m) / delta
            L = (x.numerator + x.denominator - 1) // x.denominator
        return {"sign": self.sign(), "identically_zero": False,
                "leading_exponent": str(e0), "leading_coefficient": str(c0), "L": L}

    def at_power_of_two(self, L):
        """Exact evaluation at eps=2**(-L), provided all L*e are integers.

        This verifier is deliberately separate from germ comparison and should
        be used only for small instances: numeric bit sizes can be enormous.
        """
        value = F(0)
        for e, c in self.terms:
            p = e * L
            if p.denominator != 1:
                raise ValueError("Evaluation is irrational at the requested epsilon")
            k = p.numerator
            value += c * (F(1, 1 << k) if k >= 0 else F(1 << (-k)))
        return value

    def serial(self):
        return [[str(e), str(c)] for e, c in self.terms]


@dataclass
class Node:
    name: str
    guard_coeff: tuple[F, F, F]  # c0 + c1*s + c2*s*s - source(eps, gaps)
    activation: tuple[str, ...] = ()
    eps_power: int = 1
    gap_powers: dict[str, int] = field(default_factory=dict)
    source_sign: int = 1
    affine_reset: tuple[F, F] = (F(1), F(0))
    priority: int = 0

    def center(self):
        c0, c1, c2 = map(frac, self.guard_coeff)
        if c2 != 1:
            raise ValueError("Only monic quadratic guards are admitted")
        c = -c1 / 2
        if c <= 0 or c0 != c*c:
            raise ValueError("Guard must be (c-s)^2 - source with c > 0")
        return c

    def serial(self):
        return {"name": self.name, "guard_coeff": [str(x) for x in self.guard_coeff],
                "activation": list(self.activation), "eps_power": self.eps_power,
                "gap_powers": self.gap_powers, "source_sign": self.source_sign,
                "affine_reset": [str(x) for x in self.affine_reset],
                "priority": self.priority}


def node(name, center=1, **kwargs):
    c = frac(center)
    return Node(name, (c*c, -2*c, F(1)), **kwargs)


def compile(nodes):
    """Return exact event germs, ordering, and a shared valid dyadic radius.

    Native input includes a topological listing of a finite DAG. Every node is
    one-shot; source monomials may depend only on completed activation parents.
    Source coefficients are +1 or -1. No arbitrary algebraic-sign oracle occurs.
    """
    if len({n.name for n in nodes}) != len(nodes):
        raise ValueError("Duplicate node name")
    if len({n.priority for n in nodes}) != len(nodes):
        raise ValueError("Explicit priorities must be distinct")
    states = {}
    certificates = []
    L = 0

    def compare(a, b, reason):
        nonlocal L
        diff = a-b
        cert = diff.sign_certificate()
        L = max(L, cert["L"])
        certificates.append({"reason": reason, "difference": diff.serial(), **cert})
        return cert["sign"]

    for n in nodes:
        c = n.center()
        if n.source_sign not in (-1, 1) or not isinstance(n.eps_power, int) or n.eps_power < 0:
            raise ValueError("Invalid source sign/exponent")
        if any(not isinstance(w, int) or w < 0 for w in n.gap_powers.values()):
            raise ValueError("Source powers must be nonnegative integers")
        if any(p not in states for p in n.activation):
            raise ValueError("Native input must be topologically ordered")
        if any(p not in n.activation for p in n.gap_powers):
            raise ValueError("Gap source must already have completed at activation")
        if any(states[p]["status"] != "fires" for p in n.activation):
            states[n.name] = {"status": "blocked_by_absent_parent"}
            continue
        a = F(n.eps_power)
        for p, w in n.gap_powers.items():
            a += w * states[p]["exponent"]
        if a <= 0:
            raise ValueError("Source must vanish with positive exponent at epsilon=0")
        if n.source_sign < 0:
            states[n.name] = {"status": "no_real_guard_root", "source_exponent": a}
            continue
        exponent = a/2
        A = GP.const(0)
        chosen_parent = None
        for p in n.activation:
            tp = states[p]["time"]
            if compare(tp, A, f"activate {n.name}: {p} versus current maximum") > 0:
                A, chosen_parent = tp, p
        duration = GP.const(c)-GP.monomial(exponent)
        assert compare(duration, GP.const(0), f"positive duration {n.name}") > 0
        states[n.name] = {"status": "fires", "exponent": exponent,
                          "activation_time": A, "chosen_parent": chosen_parent,
                          "duration": duration, "time": A+duration}

    alive = [n for n in nodes if states[n.name]["status"] == "fires"]

    def cmp(a, b):
        result = compare(states[a.name]["time"], states[b.name]["time"],
                         f"queue: {a.name} versus {b.name}")
        return result if result else (a.priority > b.priority)-(a.priority < b.priority)

    ordered = sorted(alive, key=cmp_to_key(cmp))
    y = F(0)
    for n in ordered:
        scale, shift = map(frac, n.affine_reset)
        y = scale*y + shift
    return {"states": states, "order": [n.name for n in ordered], "output": y,
            "L": L, "comparisons": certificates}


def nominal(nodes):
    """The epsilon=0 model accepts the first touching root at local s=c."""
    times = {}
    for n in nodes:
        times[n.name] = max((times[p] for p in n.activation), default=F(0))+n.center()
    ordered = sorted(nodes, key=lambda n: (times[n.name], n.priority))
    y = F(0)
    for n in ordered:
        u, v = map(frac, n.affine_reset)
        y = u*y+v
    return {"times": times, "order": [n.name for n in ordered], "output": y}


def verify_at_dyadic(nodes, result, L):
    """Independent finite-epsilon rational check of every native guard and reset."""
    if L < result["L"]:
        raise ValueError("Outside the compiled common radius")
    values = {}
    for n in nodes:
        state = result["states"][n.name]
        if state["status"] == "blocked_by_absent_parent":
            assert any(p not in values for p in n.activation)
            continue
        A = max((values[p]["time"] for p in n.activation), default=F(0))
        source = F(1, 1 << (L*n.eps_power))
        for p, w in n.gap_powers.items():
            source *= values[p]["gap"]**w
        source *= n.source_sign
        if state["status"] == "no_real_guard_root":
            assert source < 0
            continue
        t = state["time"].at_power_of_two(L)
        duration = t-A
        c0, c1, c2 = n.guard_coeff
        assert c0+c1*duration+c2*duration*duration-source == 0
        assert 0 < duration < n.center()
        gap = n.center()-duration
        assert gap == GP.monomial(state["exponent"]).at_power_of_two(L)
        values[n.name] = {"time": t, "gap": gap}
    alive = [n for n in nodes if n.name in values]
    ordered = sorted(alive, key=lambda n: (values[n.name]["time"], n.priority))
    assert [n.name for n in ordered] == result["order"]
    y = F(0)
    for n in ordered:
        u, v = n.affine_reset
        y = u*y+v
    assert y == result["output"]
    for cert in result["comparisons"]:
        d = GP.make(cert["difference"]).at_power_of_two(L)
        assert ((d>0)-(d<0)) == cert["sign"]
    return {"events": len(alive), "comparisons": len(result["comparisons"]), "L": L}


def serialize_result(r):
    def enc(x):
        if isinstance(x, F): return str(x)
        if isinstance(x, GP): return x.serial()
        raise TypeError(type(x).__name__)
    return json.dumps(r, default=enc, indent=2)


def load_native_file(path):
    """Load the documented native rational-guard JSON, without solved roots."""
    with open(path) as f:
        data = json.load(f)
    return [Node(name=n["name"], guard_coeff=tuple(map(frac,n["guard_coeff"])),
                 activation=tuple(n.get("activation", [])),
                 eps_power=n.get("eps_power",1), gap_powers=n.get("gap_powers",{}),
                 source_sign=n.get("source_sign",1),
                 affine_reset=tuple(map(frac,n.get("affine_reset",[1,0]))),
                 priority=n["priority"]) for n in data]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python event_germs.py native_input.json")
    print(serialize_result(compile(load_native_file(sys.argv[1]))))
