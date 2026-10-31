#!/usr/bin/env python3
"""Independent small exact exhaustive checks of the grid-enumeration backend."""
from pathlib import Path
import hashlib,itertools,json,sys
import sympy as s
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import exhaustive_openloop as e
R=s.Rational


def run():
    model=json.loads((ROOT.parent/'history_sensitive_4096_result.json').read_text())
    mats=[s.Matrix(x['numerators'])/x['denominator'] for x in model['compiled']['operators']]
    b=s.Matrix([model['task_b'][p[0]] for p in model['partition']])
    ell=s.Matrix([R(sum(model['task_ell_numer'][i] for i in p),model['task_ell_denominator']) for p in model['partition']])
    checks=0
    for L in range(9):
        out=e.run(length=L,grid_bits=10,prefix_depth=min(4,L));values=[]
        for word in itertools.product(range(2),repeat=L):
            v=b
            for a in word:v=mats[a]*v
            values.append((ell.T*v)[0]);checks+=1
        lo,hi=map(R,out['coarse_optimal_interval']);assert lo<=max(values)<=hi;checks+=1
        assert hi-lo==R(L,1<<10);checks+=1
        assert out['explicit_words_checked']==len(values);checks+=1
        assert out['true_feedback_minus_best_openloop_lower'] is None;checks+=1
        assert out['true_gap_lower_float'] is None;checks+=1
    try:e.run(length=1,grid_bits=37,prefix_depth=0)
    except AssertionError:checks+=1
    else:raise AssertionError('uint64 overflow interface accepted')
    return {'status':'PASS_EXACT_BACKEND_CHECKS','checks':checks,
      'scope':'Every word through length8 checked against exact rational multiplication; grid error intervals and uint64 admission checked. No new source observations or randomness validation.',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'enumerator_sha256':hashlib.sha256((ROOT/'exhaustive_openloop.py').read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'exhaustive_backend_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
