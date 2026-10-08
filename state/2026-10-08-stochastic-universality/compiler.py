#!/usr/bin/env python3
"""Exact stochastic-fiber embedding; research implementation, not formal proof.
Read RESULT_AND_RESTART.md. Rates use falling-factorial mass action.
Run: python compiler.py input.json output.json --mode full_rank
Only the Python standard library is required.
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

@dataclass(frozen=True)
class Reaction:
    source: tuple[int, ...]
    target: tuple[int, ...]
    rate: Fraction = Fraction(1)

    def __post_init__(self) -> None:
        if not self.source or len(self.source) != len(self.target):
            raise ValueError('Source and target must have the same positive dimension.')
        if any(type(x) is not int or x < 0 for x in self.source + self.target):
            raise ValueError('Stoichiometries must be nonnegative integers.')
        if self.source == self.target:
            raise ValueError('Zero-change reactions are excluded; remove them first.')
        if self.rate <= 0:
            raise ValueError('Rates must be strictly positive rationals.')

    @property
    def change(self) -> tuple[int, ...]:
        return tuple(b-a for a, b in zip(self.source, self.target))

    def as_dict(self) -> dict[str, Any]:
        return {'source': list(self.source), 'target': list(self.target), 'rate': str(self.rate)}

def falling(n: int, k: int) -> int:
    if n < 0 or k < 0:
        raise ValueError('Falling factorial arguments must be nonnegative.')
    if n < k:
        return 0
    out = 1
    for j in range(k):
        out *= n-j
    return out

def propensity(r: Reaction, x: Sequence[int]) -> Fraction:
    if len(x) != len(r.source):
        raise ValueError('Wrong state dimension.')
    value = r.rate
    for n, k in zip(x, r.source):
        if type(n) is not int or n < 0:
            raise ValueError('State entries must be nonnegative integers.')
        value *= falling(n, k)
    return value

def compile_network(original: Sequence[Reaction], *, mode: str = 'full_rank',
                    brake_rate: Fraction = Fraction(1)) -> tuple[list[Reaction], dict[str, Any]]:
    if not original:
        raise ValueError('Supply at least one nontrivial reaction.')
    if mode not in ('full_rank', 'conserved'):
        raise ValueError('mode must be full_rank or conserved.')
    d = len(original[0].source)
    if any(len(r.source) != d for r in original):
        raise ValueError('All reactions must have the same dimension.')
    if brake_rate <= 0:
        raise ValueError('brake_rate must be positive.')
    R = max(sum(r.source) for r in original)
    M = R + 1
    out = [Reaction(r.source+(1,1), r.target+(1,1), r.rate) for r in original]
    zero = (0,)*d
    if mode == 'full_rank':
        main_vertices = [zero]
        for i in range(d):
            v = [0]*d
            v[i] = M
            main_vertices.append(tuple(v))
        vertices = [v+z for v in main_vertices for z in ((2,0),(0,2))]
        vertices.append(zero+(3,0))
        out += [Reaction(vertices[i], vertices[(i+1) % len(vertices)], brake_rate)
                for i in range(len(vertices))]
        expected_rank, bound, extra = d+2, R+3, 2*d+3
    else:
        for z in ((2,0), (0,2)):
            for i in range(d):
                ei = [0]*d
                ei[i] = 1
                mei = [0]*d
                mei[i] = M
                out.append(Reaction(zero+z, tuple(ei)+z, brake_rate))
                out.append(Reaction(tuple(mei)+z, zero+z, brake_rate))
        expected_rank, bound, extra = d, R+3, 4*d
    metadata = {
        'mode': mode, 'input_species': d, 'output_species': d+2,
        'input_reactions': len(original), 'output_reactions': len(out),
        'added_reactions': extra, 'input_source_order': R, 'M': M,
        'output_source_order': max(sum(r.source) for r in out),
        'output_source_order_bound': bound,
        'maximum_output_complex_size': max(sum(r.target) for r in out),
        'expected_stoichiometric_rank': expected_rank,
        'exact_invariant_fiber': 'C=1, D=1',
        'rate_convention': 'falling factorial; not monomial on integer states',
        'proof_status': 'human-readable derivation; external review and priority unresolved',
    }
    return out, metadata

def verify_structure(original: Sequence[Reaction], compiled: Sequence[Reaction],
                     mode: str, brake_rate: Fraction = Fraction(1)) -> bool:
    expected, _ = compile_network(original, mode=mode, brake_rate=brake_rate)
    return list(compiled) == expected

def load(path: Path) -> list[Reaction]:
    data = json.loads(path.read_text())
    items = data['reactions'] if isinstance(data, dict) else data
    out = []
    for item in items:
        rate = item.get('rate', 1)
        if isinstance(rate, float) or isinstance(rate, bool):
            raise ValueError('Use integer or string rational rates, not floating point.')
        out.append(Reaction(tuple(item['source']), tuple(item['target']), Fraction(rate)))
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mode', choices=('full_rank', 'conserved'), default='full_rank')
    parser.add_argument('--brake-rate', default='1', help='Positive integer or rational string.')
    args = parser.parse_args()
    original = load(args.input)
    compiled, metadata = compile_network(original, mode=args.mode, brake_rate=Fraction(args.brake_rate))
    args.output.write_text(json.dumps({'metadata': metadata, 'reactions': [r.as_dict() for r in compiled]}, indent=2)+'\n')
    print(json.dumps(metadata, indent=2))

if __name__ == '__main__':
    main()
