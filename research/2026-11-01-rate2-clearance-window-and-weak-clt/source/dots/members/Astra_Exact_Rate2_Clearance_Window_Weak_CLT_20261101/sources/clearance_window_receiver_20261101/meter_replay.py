#!/usr/bin/env python3
"""Replay accepted scalar certificates with conservative rational-bit charges.
No source is edited. The independent checker's Fraction global is replaced by
an arithmetic-equivalent subclass solely to charge every rational operation.
"""
from fractions import Fraction
from pathlib import Path
from collections import Counter
import types
import hashlib
import json
import time
import sys

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


def load_verified_module(path, expected):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError('independent replay source hash mismatch')
    module = types.ModuleType('scalar_independent_metered')
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module


class FrozenText:
    def __init__(self, path, expected):
        self.path = path
        self.data = path.read_bytes()
        if hashlib.sha256(self.data).hexdigest() != expected:
            raise RuntimeError('scalar input hash mismatch')
    def read_bytes(self): return self.data
    def read_text(self): return self.data.decode('utf-8')
    def __str__(self): return str(self.path)


def main():
    start = time.monotonic_ns()
    path = ROOT/'audit_inverse_clock_certificate_20261101/independent_check.py'
    if sys.flags.optimize:
        raise RuntimeError('optimized Python disables independent assertions')
    ic = load_verified_module(path, '8b6489d4657b9646d0983ae17afd9d8d5e20045f8908038c9164b18a9bbeac44')
    ic.R = Metered
    snap = ROOT/'audit_inverse_clock_certificate_20261101/frozen_scalar'
    results = []
    for name in ('CERTIFICATE.json','CERTIFICATE_FINE.json'):
        expected = {'CERTIFICATE.json':'f65c7c6b3ec164bbbe2ac978dcc24ed6738f0b277e37adb294d244188038a016','CERTIFICATE_FINE.json':'ad0e3e581ed0a6d516c1cd56498fea073ff15f6d5411bd7ca009e9769c98fe21'}[name]
        certificate = FrozenText(snap/name, expected)
        source = FrozenText(snap/'validated_clock.py', 'f7b3a0a64440042d1ce951d6acb072fca15c771ef8078bfec672e92ed65c5732')
        before = WORK
        result = ic.check(certificate, source)
        result['rational_schoolbook_bit_charge'] = str(WORK-before)
        results.append(result)
    result = {
        'status':'PASS_EXACT_METERED_INDEPENDENT_SCALAR_REPLAY',
        'replays':results, 'arithmetic_operation_counts':dict(COUNTS),
        'charged_rational_operations':sum(COUNTS.values()),
        'max_rational_temporary_bit_upper':MAX_BITS,
        'rational_schoolbook_bit_charge':str(WORK),
        'additional_integer_and_control_charge':str(10**27-WORK),
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
