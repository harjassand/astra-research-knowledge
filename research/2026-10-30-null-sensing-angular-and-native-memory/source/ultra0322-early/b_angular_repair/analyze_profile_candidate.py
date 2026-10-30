"""Exact polynomial matrix of the one pointwise proposal, plus diagnostics.

The rational rounding is a proposal. Neither grid eigenvalues nor exact
minor acquisition alone proves positivity on the full disk.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,json,time
import sympy as S
from sympy.polys.matrices import DomainMatrix
import numpy as np


def main():
    start=time.perf_counter();here=Path(__file__).parent
    raw=json.loads((here/'ANGULAR_REDUCTION.json').read_text());proposal=json.loads((here/'POINTWISE_PROFILE_PROPOSAL.json').read_text())
    A=S.symbols('a b c d',real=True);v=[S.Symbol(n,real=True)for n in raw['effective_parameters']]
    loc={str(x):x for x in (*A,*v)};rational=[Fraction(float(x)).limit_denominator(1000)for x in proposal['parameters']]
    sub={p:S.Rational(q.numerator,q.denominator)for p,q in zip(v,rational)}
    C=S.Matrix([[S.sympify(x,locals=loc)for x in row]for row in raw['cleared_completion']])
    C=S.simplify(C.subs(sub).subs({A[0]:1,A[2]:0}));b,d=A[1],A[3]
    function=S.lambdify((b,d),C,'numpy',cse=True)
    lowest=(1e100,None)
    for radius in np.linspace(0,1,25):
        for angle in np.linspace(0,2*np.pi,97)[:-1]:
            bb,dd=radius*np.cos(angle),radius*np.sin(angle)
            if abs(bb)<1e-12 and abs(abs(dd)-1)<1e-12:continue
            val=float(np.linalg.eigvalsh(function(bb,dd))[0])/(1+bb*bb+dd*dd)**3
            if val<lowest[0]:lowest=(val,[float(bb),float(dd)])
    near=[]
    for sign in (-1,1):
        for t in (1e-2,1e-3,1e-4):
            for angle in np.linspace(0,2*np.pi,33)[:-1]:
                bb=t*np.cos(angle);dd=sign+t*np.sin(angle)
                val=float(np.linalg.eigvalsh(function(bb,dd))[0])
                if val< -1e-10:near.append([float(bb),float(dd),val])
    mapping=time.perf_counter()-start;minors=[]
    for k in range(1,7):
        tick=time.perf_counter()
        det=DomainMatrix.from_Matrix(C[:k,:k]).det().as_expr()
        factor=S.factor_list(det)
        minors.append({'k':k,'degree':S.Poly(det,b,d).total_degree(),'terms':len(S.Poly(det,b,d).terms()),
                       'constant':str(factor[0]),'factors':[[str(p),int(m)]for p,m in factor[1]],
                       'seconds':time.perf_counter()-tick})
        print('minor',k,'degree',minors[-1]['degree'],'terms',minors[-1]['terms'],'sec',minors[-1]['seconds'],flush=True)
    out={'scope':'same one pointwise-profile proposal rounded rationally; exact minors not a positivity proof',
         'parameters':{str(p):str(q)for p,q in zip(v,rational)},
         'cleared_matrix':[[str(v)for v in row]for row in C.tolist()],
         'numeric_disk_min':lowest,'numeric_near_pole_failures':near,
         'leading_minors':minors,'mapping_seconds':mapping,'total_seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':hashlib.sha256((here/'ANGULAR_REDUCTION.json').read_bytes()).hexdigest()}
    (here/'PROFILE_CANDIDATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('parameters','numeric_disk_min','mapping_seconds','total_seconds_after_imports')},indent=2))
    print('near_pole_failures',len(near))


if __name__=='__main__':main()
