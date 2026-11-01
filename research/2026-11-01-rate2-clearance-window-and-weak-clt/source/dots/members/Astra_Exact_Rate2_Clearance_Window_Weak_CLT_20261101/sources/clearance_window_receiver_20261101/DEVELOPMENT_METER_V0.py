#!/usr/bin/env python3
"""Replay accepted scalar certificates with conservative rational-bit charges.
No source is edited. The independent checker's Fraction global is replaced by
an arithmetic-equivalent subclass solely to charge every rational operation.
"""
from fractions import Fraction
from pathlib import Path
from collections import Counter
import importlib.util
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent.parent
COUNTS = Counter()
MAX_BITS = 0
WORK = 0


def charge(name, *values):
    global MAX_BITS, WORK
    bits = 1
    for v in values:
        if isinstance(v, (int, Fraction)):
            v = Fraction(v)
            bits = max(bits, abs(v.numerator).bit_length(), v.denominator.bit_length())
    # Every elementary Fraction operation below has at most four products of
    # two operands and gcd/division on <=2b+2-bit integers. This deliberately
    # cubic schoolbook bound includes Euclidean normalization and bookkeeping.
    temp = 2 * bits + 4
    if temp > 65536:
        raise RuntimeError('acquisition bit ceiling exceeded')
    MAX_BITS = max(MAX_BITS, temp)
    COUNTS[name] += 1
    WORK += 256 * (temp + 1) ** 3
    if sum(COUNTS.values()) > 100000000 or WORK > 10**30:
        raise RuntimeError('acquisition work ceiling exceeded')


class Metered(Fraction):
    def __new__(cls, numerator=0, denominator=None, **kwargs):
        out = super().__new__(cls, numerator, denominator, **kwargs)
        charge('construct', out)
        return out


def operation(name):
    original = getattr(Fraction, name)
    def wrapped(self, other=None):
        values = (self,) if other is None else (self, other)
        charge(name, *values)
        result = original(self) if other is None else original(self, other)
        if result is NotImplemented:
            return result
        if isinstance(result, Fraction):
            return Metered(result.numerator, result.denominator)
        return result
    return wrapped


for _name in ('__add__','__radd__','__sub__','__rsub__','__mul__','__rmul__',
              '__truediv__','__rtruediv__','__neg__','__pos__','__abs__',
              '__pow__','__eq__','__lt__','__le__','__gt__','__ge__'):
    setattr(Metered, _name, operation(_name))
Metered.__hash__ = Fraction.__hash__


def main():
    start = time.monotonic_ns()
    path = ROOT/'audit_inverse_clock_certificate_20261101/independent_check.py'
    spec = importlib.util.spec_from_file_location('scalar_independent_metered', path)
    ic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ic)
    ic.R = Metered
    snap = ROOT/'audit_inverse_clock_certificate_20261101/frozen_scalar'
    results = []
    for name in ('CERTIFICATE.json','CERTIFICATE_FINE.json'):
        before = WORK
        result = ic.check(snap/name, snap/'validated_clock.py')
        result['rational_schoolbook_bit_charge'] = str(WORK-before)
        results.append(result)
    result = {
        'status':'PASS_EXACT_METERED_INDEPENDENT_SCALAR_REPLAY',
        'replays':results, 'arithmetic_operation_counts':dict(COUNTS),
        'charged_rational_operations':sum(COUNTS.values()),
        'max_rational_temporary_bit_upper':MAX_BITS,
        'rational_schoolbook_bit_charge':str(WORK),
        'additional_integer_and_control_charge':'1000000000000000000000000000',
        'total_acquisition_charge':'1000000000000000000000000000',
        'charge_note':'The total is a deliberately larger fixed reserve, not wall-clock instructions; includes both replays, exact startup, self-tests, parsing, hash reads, non-Fraction integer expressions and bookkeeping. No refinements were rejected in this acquisition run. Prior mathematical research is not advertised as an algorithmic complexity bound.',
        'rejected_refinements':0,
        'elapsed_ns_nonproof':time.monotonic_ns()-start,
        'meter_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'independent_code_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    assert WORK < 10**27
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
