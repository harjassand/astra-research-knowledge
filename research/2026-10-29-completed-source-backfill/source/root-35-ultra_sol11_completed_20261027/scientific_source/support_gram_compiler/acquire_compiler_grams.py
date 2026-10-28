"""Construct exact useful support and leading Grams from literal old F.

Small26x26 SDP proposes an upper bound C; exact integer coefficient matching
and Bareiss Sylvester checks prove the delivered certificate. The35x35 P8
Gram is extracted directly from acceptedR180 under X=-A, with no new SDP.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cwr
from pathlib import Path
from collections import Counter
import json
import math
import time

START=time.monotonic()
import numpy as np
import sympy as sp
import cvxpy as cp

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
SOURCE=ROOT/'work/sol8_opportunity_selection_20261027/rational_selector/EXACT_RATIONAL_SUPPORT.json'


def expof(ai,xi=()):
    ex=[0]*8
    for j in ai:ex[j]+=1
    for j in xi:ex[4+j]+=1
    return tuple(ex)


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def gram_coeff(gram,features):
    ans={}
    for i in range(len(features)):
        for j in range(i,len(features)):
            v=gram[i][j]*(1 if i==j else 2)
            if v:
                e=add(features[i],features[j])
                ans[e]=ans.get(e,0)+v
    return {e:v for e,v in ans.items() if v}


def integer_pd(mat):
    """All leading principal minors by fraction-free Bareiss elimination."""
    bb=[list(map(int,row)) for row in mat]
    n=len(bb)
    previous=1
    leading=[]
    for k in range(n):
        pivot=bb[k][k]
        assert pivot>0, (k,pivot)
        leading.append(pivot)
        if k==n-1:break
        for i in range(k+1,n):
            for j in range(i,n):
                numerator=pivot*bb[i][j]-bb[i][k]*bb[k][j]
                quotient,remainder=divmod(numerator,previous)
                assert remainder==0
                bb[i][j]=bb[j][i]=quotient
        previous=pivot
    return leading


A=sp.symbols('a0:4')
X=sp.symbols('x0:4')
aa,b,c,d=A
u,v,w,q=aa*aa+c*c,b*b+d*d,aa*b+c*d,aa*d-b*c
T=u+v
x,y,z=u-v,2*w,2*q
F=(sp.Rational(55220381,10**10)*(u*u+v*v)
   +sp.Rational(114430029,625000000)*u*v
   -sp.Rational(801761987,5000000000)*w*w
   +sp.Rational(118849817,4000000000)*q*(u-v))
p6=(sp.Rational(6222019,200000000)*x**3
    +sp.Rational(1686519911,10**10)*x*x*z
    +sp.Rational(81172813,2000000000)*x*z*z
    +sp.Rational(1726116771,10**10)*z**3
    +sp.Rational(128626163,5000000000)*x*y*y
    +sp.Rational(373321239,2000000000)*y*y*z)
shift=F.xreplace(dict(zip(A,[a+xx for a,xx in zip(A,X)])))
BF=sp.expand(shift-F-sum(sp.diff(F,a)*xx for a,xx in zip(A,X)))
normX=sum(xx*xx for xx in X)


def acquire_support():
    start=time.monotonic()
    features=[expof((i,),(j,)) for i in range(4) for j in range(4)]
    features += [expof((),ii) for ii in cwr(range(4),2)]
    assert len(features)==26
    groups={}
    for i in range(26):
        for j in range(i,26):
            groups.setdefault(add(features[i],features[j]),[]).append((i,j))
    target=sp.Poly(BF,*A,*X,domain=sp.QQ)
    norm=sp.Poly(T*normX,*A,*X,domain=sp.QQ)
    bc={e:Q(int(v.p),int(v.q)) for e,v in target.terms()}
    nc={e:Q(int(v.p),int(v.q)) for e,v in norm.terms()}
    assert set(bc)|set(nc)<=set(groups)
    variable=cp.Variable((26,26),symmetric=True)
    constant=cp.Variable(nonneg=True)
    # A small strict margin is deliberately included for safe exact recovery.
    propose_margin=1e-7
    constraints=[variable-propose_margin*np.eye(26)>>0]
    for e,pairs in groups.items():
        constraints.append(sum((1 if i==j else 2)*variable[i,j] for i,j in pairs)
                           ==float(bc.get(e,Q(0)))+constant*float(nc.get(e,Q(0))))
    problem=cp.Problem(cp.Minimize(constant),constraints)
    setup_seconds=time.monotonic()-start
    solve_start=time.monotonic()
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-11,tol_gap_rel=1e-11,
                  tol_feas=1e-11,max_iter=200,verbose=False)
    solve_seconds=time.monotonic()-solve_start
    assert variable.value is not None and constant.value is not None
    suggested=float(constant.value)
    # Fixed rational C slightly above the proposal, with no optimality claim.
    rationalC=Q(math.ceil(suggested*10000),10000)
    prop=np.asarray(variable.value,dtype=float)
    for i in range(16):prop[i,i]+=float(rationalC)-suggested
    D0=80000000000
    denominator=2*D0
    gg=[[2*round(float(prop[i,j])*D0) for j in range(26)] for i in range(26)]
    gg=[[gg[i][j] if i<=j else gg[j][i] for j in range(26)] for i in range(26)]
    actual=gram_coeff(gg,features)
    max_correction=0
    for e,pairs in groups.items():
        want=(bc.get(e,Q(0))+rationalC*nc.get(e,Q(0)))*denominator
        assert want.denominator==1
        residual=int(want)-actual.get(e,0)
        # Prefer a diagonal, otherwise any off-diagonal representation.
        i,j=min(pairs,key=lambda ij:ij[0]!=ij[1])
        if i==j:
            gg[i][i]+=residual
            max_correction=max(max_correction,abs(residual))
        else:
            assert residual%2==0
            gg[i][j]+=residual//2
            gg[j][i]+=residual//2
            max_correction=max(max_correction,abs(residual)//2)
    literal={e:int((bc.get(e,Q(0))+rationalC*nc.get(e,Q(0)))*denominator)
             for e in groups if bc.get(e,Q(0))+rationalC*nc.get(e,Q(0))}
    assert gram_coeff(gg,features)==literal
    # Certify a useful strict interior margin, with exact positivity only.
    certified_margin=Q(1,25000)
    shifted=[[gg[i][j]-(int(certified_margin*denominator) if i==j else 0)
              for j in range(26)] for i in range(26)]
    proof_start=time.monotonic()
    leading=integer_pd(shifted)
    exact_seconds=time.monotonic()-proof_start
    out={'status':'EXACT26_SUPPORT_COMPILER_GRAM','C':str(rationalC),
         'identity':'BF(A,X)+C*|A|^2*|X|^2=Z26^T*G26*Z26',
         'features':features,'gram_denominator':denominator,'gram_numerators':gg,
         'proved_Gram_margin':str(certified_margin),
         'PD_proof':'Integer Bareiss computes strictly positive leading principal minors of G26-margin I.',
         'leading_minor_signs':['positive']*len(leading),
         'max_leading_minor_bits':max(t.bit_length() for t in leading),
         'solver_C_suggestion_diagnostic':suggested,'solver_status_diagnostic':problem.status,
         'solver_iterations':problem.solver_stats.num_iters,
         'numeric_Gram_eigen_range_diagnostic':list(map(float,[np.linalg.eigvalsh(prop)[0],np.linalg.eigvalsh(prop)[-1]])),
         'largest_affine_correction_numerator':max_correction,
         'setup_seconds':setup_seconds,'solve_seconds':solve_seconds,
         'exact_Bareiss_seconds':exact_seconds,'total_seconds':time.monotonic()-start,
         'scope':'Global SOS for literal oldF, with useful explicit C; optimality of C not claimed.'}
    (OUT/'EXACT26_SUPPORT_GRAM.json').write_text(json.dumps(out,indent=2)+'\n')
    return {k:v for k,v in out.items() if k not in ['features','gram_numerators']}


def extract_leading():
    start=time.monotonic()
    source=json.loads(SOURCE.read_text())
    denominator=source['gram_denominator']
    gram=source['gram_integer_matrix']
    features=[expof(ai,(j,)) for ai in cwr(range(4),3) for j in range(4)]
    features += [expof(ai,xi) for ai in cwr(range(4),2) for xi in cwr(range(4),2)]
    quartic=[expof(ii)[:4] for ii in cwr(range(4),4)]
    index={e:i for i,e in enumerate(quartic)}
    mapped=[]
    for e in features:
        degree=tuple(a+x for a,x in zip(e[:4],e[4:]))
        sign=(-1)**sum(e[4:])
        mapped.append((index[degree],sign))
    assert len(features)==180 and len(quartic)==35
    counts=Counter(i for i,_ in mapped)
    assert set(counts.values())=={2,4,5,7,10}
    gg=[[0]*35 for _ in range(35)]
    for i,(ki,si) in enumerate(mapped):
        for j,(kj,sj) in enumerate(mapped):
            gg[ki][kj]+=si*sj*gram[i][j]
    literal=sp.Poly(3*T*T*F-p6*q,*A,domain=sp.QQ)
    target={e:Q(int(v.p),int(v.q)) for e,v in literal.terms()}
    rebuilt=gram_coeff(gg,quartic)
    assert {e:Q(v,denominator) for e,v in rebuilt.items()}==target
    # R>=I/400000 and M^T M=diag(counts)>=2I prove this margin.
    margin=Q(1,200000)
    shifted=[[gg[i][j]-(int(margin*denominator) if i==j else 0)
              for j in range(35)] for i in range(35)]
    proof_start=time.monotonic()
    leading=integer_pd(shifted)
    exact_seconds=time.monotonic()-proof_start
    out={'status':'EXACT35_LEADING_COMPILER_GRAM','identity':'3*T(A)^2*F(A)-p6(A)*det(A)=Z4(A)^T*G35*Z4(A)',
         'features':quartic,'gram_denominator':denominator,'gram_numerators':gg,
         'proved_Gram_margin':str(margin),'map_rows':mapped,
         'feature_multiplicities':[counts[i] for i in range(35)],
         'margin_argument':'Accepted R180>=I/400000; G35=M^T R180 M; M^T M diagonal with min2.',
         'independent_PD_proof':'Integer Bareiss also proves G35-margin I strictly positive definite.',
         'max_leading_minor_bits':max(t.bit_length() for t in leading),
         'exact_Bareiss_seconds':exact_seconds,'total_seconds':time.monotonic()-start,
         'scope':'Exact positive definite Gram, no new SDP. AcceptedR180 acquisition remains a charged prior input.'}
    (OUT/'EXACT35_LEADING_GRAM.json').write_text(json.dumps(out,indent=2)+'\n')
    return {k:v for k,v in out.items() if k not in ['features','gram_numerators','map_rows']}


def main():
    support=acquire_support()
    print(json.dumps(support,indent=2),flush=True)
    leading=extract_leading()
    print(json.dumps(leading,indent=2),flush=True)
    (OUT/'ACQUISITION.json').write_text(json.dumps({'support':support,'leading':leading,
        'module_seconds':time.monotonic()-START,
        'timing_scope':'Includes scientific imports from START, symbolic literal setup, smallSDP, both exact proofs. '
                       'Interpreter startup and stdlib imports before START excluded; oldR180 acquisition is charged prior.'},indent=2)+'\n')


if __name__=='__main__':main()
