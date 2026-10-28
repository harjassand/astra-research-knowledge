"""Replay the exact rational acquisition from the saved numerical suggestion.

Each upper Gram entry contributes to exactly one monomial row. Fix the six
selector rationals, round the Gram, and distribute each integer row defect
over that row's disjoint Gram variables. This is coefficient projection,
not a positivity proof. Default is read-only comparison with the acquired
suggestion; exact_support.py separately proves the resulting identity/PSD.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import time
import numpy as np

ROOT=Path(__file__).resolve().parent


def main():
    started=time.monotonic()
    maps=np.load(ROOT/'NONLINEAR_LITERAL_MAPS.npz')
    numeric=np.load(ROOT/'BOUNDED_NONLINEAR_NUMERIC.npz')
    denominator=80000000000
    selector=np.rint(numeric['selector']*10000000000).astype(np.int64)*8
    gram=np.array([round(float(v)*denominator) for v in numeric['q']],dtype=object)
    p=list(map(Q,json.loads((ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_text())['coefficients']))
    rhs=[sum((Q(int(v))*c*denominator for v,c in zip(row,p)),Q(0)) for row in maps['E']]
    assert all(v.denominator==1 for v in rhs)
    rhs=np.array([v.numerator for v in rhs],dtype=object)-maps['C'].astype(np.int64).astype(object)@selector.astype(object)
    groups=[[] for _ in range(3185)]
    columns=[]
    for row,col,value in zip(maps['gram_rows'],maps['gram_cols'],maps['gram_values']):
        groups[int(row)].append((int(col),int(value)))
        columns.append(int(col))
    assert len(columns)==len(set(columns))==16290
    for row,group in enumerate(groups):
        residual=int(rhs[row])-sum(value*int(gram[col]) for col,value in group)
        step=residual//sum(value for col,value in group)
        for col,value in group:
            gram[col]+=step
            residual-=step*value
        if residual:
            col,value=next(((c,v) for c,v in group if v==1),group[0])
            assert residual%value==0
            gram[col]+=residual//value
        assert sum(value*int(gram[col]) for col,value in group)==rhs[row]
    acquired=np.load(ROOT/'EXACT_AFFINE_SUGGESTION.npz')
    assert int(acquired['denominator'])==denominator
    assert np.array_equal(gram,acquired['q'])
    assert np.array_equal(selector,acquired['selector'])
    out={'status':'READ_ONLY_EXACT_AFFINE_ACQUISITION_REPLAY_PASS',
         'exact_rows':3185,'disjoint_Gram_variables':16290,
         'selector_coefficients':6,'common_denominator':denominator,
         'seconds':time.monotonic()-started,
         'scope':'Exact coefficient projection reproduced; positivity is a separate dyadic residual certificate.'}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
