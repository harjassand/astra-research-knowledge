#!/usr/bin/env python3
"""Freeze a source-independent symmetry average of a previously frozen dual."""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "outputs/predictive_flow"))
from flow_grid import geometry


def main():
    source = ROOT / "outputs/predictive_flow/generic_triple_certificate.json"
    data = json.loads(source.read_text())
    s, L, k = data['alphabet_size'], data['depth'], data['mesh']
    assert s == 2
    leaves, nodes, desc, words = geometry(s, L, k)
    index = {x:i for i,x in enumerate(nodes)}
    dindex = {x:i for i,x in enumerate(desc)}
    windex = {x:i for i,x in enumerate(words)}
    y = list(map(Q, data['row_duals']))
    dc = list(map(Q, data['data_duals']))
    ynew = [Q(0)]*len(y)
    dcnew = [Q(0)]*len(dc)
    for flip in (False, True):
        for swap in (False, True):
            for i, (a, plus, minus) in enumerate(nodes):
                if swap:
                    plus, minus = minus, plus
                if flip:
                    a, plus, minus = 1-a, plus[::-1], minus[::-1]
                j = index[a, plus, minus]
                for r, (side, b, w, sign) in enumerate(desc):
                    if swap:
                        side = 1-side
                    if flip:
                        b, w = 1-b, tuple(1-v for v in w)
                    rr = dindex[side, b, w, sign]
                    ynew[i*len(desc)+r] += y[j*len(desc)+rr]/4
            for wi, word in enumerate(words):
                w = word[::-1] if swap else word
                if flip:
                    w = tuple(1-a for a in w)
                wj = windex[w]
                for side in (0, 1):
                    dcnew[2*wi+side] += dc[2*wj+side]/4
    data['row_duals'] = list(map(str, ynew))
    data['data_duals'] = list(map(str, dcnew))
    z = Q(data['normalization_dual'])
    data['word_statistic'] = [str(-z-dcnew[2*i]+dcnew[2*i+1]) for i in range(len(words))]
    data['symmetry_construction'] = {
        'input': str(source),
        'operation': 'average binary label complement and exchange predictive groups',
        'source_parameters_used': False,
        'test_record_used': False,
        'validity': 'exact every-column check required after averaging',
    }
    target = ROOT / 'outputs/reversible_currents/symmetric_dual.json'
    target.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({'target': str(target), 'word_statistic': data['word_statistic']}))


if __name__ == '__main__':
    main()
