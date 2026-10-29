"""Exact SAME-arity-boundary control, CREDITED to Eriksson v2 Theorem3.1.

It is a prior counterexample, not a new activation theorem.
"""
import json
from pathlib import Path
from time import perf_counter
import sympy as s
from compile_order import compile_channel

HERE=Path(__file__).resolve().parent

def metric(S,X):
    d=S.rows
    # Column vectorization: vec(SL+LS)=(I tensor S+S^T tensor I)vecL.
    J=(s.kronecker_product(s.eye(d),S)+s.kronecker_product(S.T,s.eye(d)))/2
    rhs=s.Matrix([X[i,j] for j in range(d) for i in range(d)])
    v=J.inv()*rhs
    L=s.Matrix(d,d,lambda i,j:v[j*d+i])
    assert (S*L+L*S)/2==X
    return s.simplify(s.trace(X*L))

def main():
    begin=perf_counter();n=3;xi=s.Rational(1,10);eta=s.Rational(3,4)
    u=s.ones(3,1);vs=[s.eye(3)[:,i]-u/3 for i in range(3)]
    S=[(1-xi)*v*v.T/2+xi*s.eye(3)/9 for v in vs]
    X=[u*v.T+v*u.T for v in vs]
    assert sum(X,s.zeros(3))==s.zeros(3) and sum(s.trace(a) for a in S)==1
    ch={'n':3,'P':[{str(i):str(eta)} for i in range(3)]+[{str(i):str(1-eta) for i in range(3)}],
        'Q':[{str(i):'1/2' for i in range(3) if i!=y} for y in range(3)]}
    def result(name):
        g=s.Rational(0)
        for row in ch[name]:
            A=sum((s.Rational(a)*S[int(i)] for i,a in row.items()),s.zeros(3))
            H=sum((s.Rational(a)*X[int(i)] for i,a in row.items()),s.zeros(3))
            assert all(p>0 for p in A.cholesky(hermitian=False).diagonal())
            g+=metric(A,H)
        return s.cancel(g)
    gi=sum(metric(a,x) for a,x in zip(S,X));gp,gq=result('P'),result('Q')
    assert gi==s.Rational(2160,29) and gq/gi==s.Rational(29,35)>eta
    assert gp-gq==s.Rational(-1188,203)
    unsupported=compile_channel(ch)
    assert unsupported['complete_order'] is None and not unsupported['eligible']
    out={'primary':'Lluis Eriksson, Support and quantum-reference activation of classical channels, v2, Theorem3.1 and Section4',
         'url':'https://airr.science/papers/ARR-2026-564FZ70CSN83KACD/versions/v2/',
         'credit':'literal rational specialization of an acquired primary construction; not new activation',
         'P_global_erasure_row':'1/4','Q_exclusion_nonzero_rows_support':2,
         'ordinary_Q_contraction':'1/2 (primary Eq8, n3 lambda=-1/2)',
         'ordinary_P_dominates_Q':True,'reference_dimension':3,'faithful_xi':str(xi),
         'g_identity':str(gi),'g_P':str(gp),'g_Q':str(gq),'gap':str(gp-gq),
         'SLD_ratio_Q_over_identity':str(gq/gi),'compiler_status':unsupported['status'],
         'seconds':perf_counter()-begin,
         'scope':'one unmatched ternary output row invalidates scalar-order lifting; no arity3 undecidability claim'}
    (HERE/'ARITY_BOUNDARY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
