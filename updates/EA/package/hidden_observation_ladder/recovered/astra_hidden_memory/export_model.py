"""Export a rational member of the hidden-observation-ladder family.

Usage: python export_model.py 4 --output model_r4.json
The output is an explicit dense row-generator numerator and common denominator.
It is polynomial in r/output size, not polynomial in log(r).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from test_lift import dense, state_permutation


def export(r: int, path: Path) -> None:
    if r < 1:
        raise ValueError('r must be positive')
    num, den, _, observable = dense(r)
    result = {
        'r': r,
        'states': len(observable),
        'generator_convention': 'row',
        'generator_numerator': num.tolist(),
        'generator_denominator': den,
        'observable': observable.tolist(),
        'stationary_distribution': {'numerator_per_state': 1, 'denominator': len(observable)},
        'auxiliary_label_preserving_reversal_permutation': state_permutation(r).tolist(),
        'epsilon': {'numerator': 1, 'denominator': 16*r},
        'physical_reversal': 'Every microscopic state is even; auxiliary permutation is not physical reversal.',
        'control': 'q_ij(h)=q_ij(0)*exp(h*(f_j-f_i)/2) for i!=j; reset diagonals.',
        'status': 'Research construction; not independently reviewed or formally verified.'
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('r', type=int)
    parser.add_argument('--output', type=Path, default=Path('hidden_ladder_model.json'))
    args = parser.parse_args()
    export(args.r, args.output)
